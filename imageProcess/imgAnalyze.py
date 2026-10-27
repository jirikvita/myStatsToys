#!/usr/bin/env python3


"""Analyze images chosen via a File Open dialog (starts in photos/): histograms, grayscale, edge detection, Gaussian blur.

One Tk window per image with a thumbnail, buttons to show each histogram,
a button showing all histograms on a grid, and buttons to view edges / blur.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from scipy import ndimage

PHOTO_DIR = Path(__file__).parent / "photos"
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"}
ENTROPY_WINDOW = 5  # sliding window size in pixels
ENTROPY_THRESHOLD = 2.0  # bits, default cut for the colour mask
ENTROPY_BINS = 32  # grey levels used when estimating local entropy
HOUGH_THRESHOLD = 0.5  # fraction of max edge strength counted as an edge pixel
HOUGH_LINES = 10  # number of strongest lines drawn
FFT_CUTOFF = 0.2  # radial frequency cut, fraction of Nyquist
BLUR_WIDTH = 10  # gaussian sigma in pixels
THUMB_SIZE = (300, 300)
CHANNELS = [("Red", "red"), ("Green", "green"), ("Blue", "blue")]

SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
SOBEL_Y = SOBEL_X.T


def to_gray(rgb):
    return rgb @ np.array([0.299, 0.587, 0.114])


def edges(gray):
    gx = ndimage.convolve(gray, SOBEL_X, mode="reflect")
    gy = ndimage.convolve(gray, SOBEL_Y, mode="reflect")
    mag = np.hypot(gx, gy)
    return mag / mag.max() * 255 if mag.max() > 0 else mag


def entropy_map(gray, window=ENTROPY_WINDOW, bins=ENTROPY_BINS):
    """Shannon entropy (bits) of quantized grey levels in a sliding window."""
    q = np.clip(gray * bins / 256, 0, bins - 1).astype(np.int32)
    ent = np.zeros(gray.shape, dtype=np.float32)
    for b in range(bins):
        p = ndimage.uniform_filter((q == b).astype(np.float32), size=window, mode="reflect")
        mask = p > 1e-6
        ent[mask] -= p[mask] * np.log2(p[mask])
    return ent


def hough_lines(edge_img, thr_frac, n_lines, max_dim=800, n_theta=180):
    """Standard Hough line transform (rho = x cos t + y sin t) on thresholded edges.

    Returns (accumulator, thetas, rho_axis, lines, scale); lines are (rho, theta, votes)
    in the coordinates of the full-size image.
    """
    step = max(1, int(np.ceil(max(edge_img.shape) / max_dim)))
    small = edge_img[::step, ::step]
    ys, xs = np.nonzero(small > thr_frac * small.max())
    thetas = np.deg2rad(np.arange(-90, 90, 180 / n_theta))
    diag = int(np.ceil(np.hypot(*small.shape)))
    acc = np.zeros((2 * diag + 1, len(thetas)), dtype=np.int32)
    for j, t in enumerate(thetas):
        rho = np.rint(xs * np.cos(t) + ys * np.sin(t)).astype(np.int64) + diag
        acc[:, j] = np.bincount(rho, minlength=acc.shape[0])
    # Peaks: local maxima in the accumulator, strongest first
    peaks = (acc == ndimage.maximum_filter(acc, size=15)) & (acc > 0)
    pi, pj = np.nonzero(peaks)
    order = np.argsort(acc[pi, pj])[::-1][:n_lines]
    lines = [((pi[k] - diag) * step, thetas[pj[k]], acc[pi[k], pj[k]]) for k in order]
    return acc, thetas, np.arange(-diag, diag + 1) * step, lines, len(xs)


def fft_cut(gray, radius_frac, invert):
    """Radial frequency cut. radius_frac is a fraction of Nyquist (0..1).

    Keeps frequencies inside the radius (low-pass); invert keeps those outside (high-pass).
    Returns (shifted spectrum, mask, reconstructed image).
    """
    spec = np.fft.fftshift(np.fft.fft2(gray))
    h, w = gray.shape
    fy = np.fft.fftshift(np.fft.fftfreq(h))[:, None]  # cycles/pixel, Nyquist = 0.5
    fx = np.fft.fftshift(np.fft.fftfreq(w))[None, :]
    r = np.hypot(fx, fy) / 0.5
    mask = r > radius_frac if invert else r <= radius_frac
    rec = np.fft.ifft2(np.fft.ifftshift(spec * mask)).real
    return spec, mask, rec


def analyze(path):
    img = Image.open(path)
    is_gray = img.mode in ("L", "1", "I", "I;16", "LA")
    rgb = np.asarray(img.convert("RGB"), dtype=float)
    gray = to_gray(rgb) if not is_gray else np.asarray(img.convert("L"), dtype=float)

    # 1D flattened histograms of intensity (256 bins)
    hists = {}
    if not is_gray:
        for i, (name, _) in enumerate(CHANNELS):
            hists[name] = np.histogram(rgb[..., i].ravel(), bins=256, range=(0, 256))[0]
    hists["Gray"] = np.histogram(gray.ravel(), bins=256, range=(0, 256))[0]

    return {
        "path": path,
        "img": img.convert("RGB"),
        "is_gray": is_gray,
        "hists": hists,
        "gray": gray,
        "entropy": None,  # computed on demand
        "rgb": rgb,
        "blur": None,  # computed on demand
    }


class ImageWindow:
    def __init__(self, master, data):
        self.data = data
        self.win = tk.Toplevel(master)
        self.v_blur = tk.DoubleVar(self.win, BLUR_WIDTH)
        self.v_win = tk.IntVar(self.win, ENTROPY_WINDOW)
        self.v_bins = tk.IntVar(self.win, ENTROPY_BINS)
        self.v_thr = tk.DoubleVar(self.win, ENTROPY_THRESHOLD)
        self.v_below = tk.BooleanVar(self.win, False)
        self.ent_key = None
        self.edge_key = "unset"
        self.edges_img = None
        self.v_hthr = tk.DoubleVar(self.win, HOUGH_THRESHOLD)
        self.v_hlines = tk.IntVar(self.win, HOUGH_LINES)
        self.v_fcut = tk.DoubleVar(self.win, FFT_CUTOFF)
        self.v_finv = tk.BooleanVar(self.win, False)
        self._last_thr_view = self.show_binary
        self.blur_key = None
        self.win.title(data["path"].name)

        left = tk.Frame(self.win)
        left.pack(side="left", fill="y", padx=5, pady=5)

        thumb = data["img"].copy()
        thumb.thumbnail(THUMB_SIZE)
        self.thumb = ImageTk.PhotoImage(thumb)  # keep reference
        tk.Label(left, image=self.thumb).pack()
        tk.Label(left, text=f"{data['path'].name}\n{data['img'].size[0]}x{data['img'].size[1]}"
                            f"{' (grayscale)' if data['is_gray'] else ''}").pack(pady=4)

        row = tk.Frame(left)
        row.pack(fill="x")
        hist_style = {"Red": ("R", "#ff8080"), "Green": ("G", "#80e080"),
                      "Blue": ("B", "#8cb4ff"), "Gray": ("Gray", "#d0d0d0")}
        for name in data["hists"]:
            text, bg = hist_style[name]
            tk.Button(row, text=text, bg=bg, activebackground=bg,
                      command=lambda n=name: self.show_hist(n)).pack(side="left", fill="x", expand=True)
        tk.Button(left, text="Original image", command=self.show_original_image).pack(fill="x", pady=(8, 0))
        tk.Button(left, text="Original histogram (overlay)", command=self.show_original).pack(fill="x")
        tk.Button(left, text="All histograms (grid)", command=self.show_all).pack(fill="x", pady=(8, 0))
        tk.Button(left, text="Greyscale image", command=self.show_gray).pack(fill="x", pady=(8, 0))
        tk.Button(left, text="Edges", command=self.show_edges).pack(fill="x")

        self._row(left, "Gaussian blur", self.show_blur,
                  [("width px", self.v_blur, 0.5, 200, 0.5)], pady=(8, 0))
        self._row(left, "Entropy map", self.show_entropy,
                  [("win px", self.v_win, 2, 101, 1), ("bins", self.v_bins, 2, 256, 1)])
        self._row(left, "Binary mask: entropy cut", self.show_binary,
                  [("bits", self.v_thr, 0, 8, 0.1)])
        tk.Checkbutton(left, text="Invert cut (show entropy below)", variable=self.v_below,
                       command=lambda: self._last_thr_view()).pack(anchor="w")
        tk.Button(left, text="Colour where entropy passes cut",
                  command=self.show_threshold).pack(fill="x")

        self._row(left, "Hough transform", self.show_hough,
                  [("thr", self.v_hthr, 0.05, 1, 0.05), ("lines", self.v_hlines, 1, 200, 1)],
                  pady=(8, 0))

        tk.Button(left, text="Fourier spectrum", command=self.show_fft).pack(fill="x", pady=(8, 0))
        self._row(left, "Cut + inverse Fourier", self.show_fft_cut,
                  [("r/Nyq", self.v_fcut, 0, 1, 0.01)])
        tk.Checkbutton(left, text="Invert cut (keep frequencies above)", variable=self.v_finv,
                       command=self.show_fft_cut).pack(anchor="w")

        tk.Button(left, text="Reset (original image, default params)",
                  command=self.reset).pack(fill="x", pady=(12, 0))

        self.fig = Figure(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.win)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        self.show_all()

    def _plot_hist(self, ax, name):
        ax.bar(np.arange(256), self.data["hists"][name], width=1.0,
               color=dict(CHANNELS).get(name, "gray"))
        ax.set_title(name)
        ax.set_xlim(0, 255)
        ax.set_xlabel("Intensity")
        ax.set_ylabel("Pixels")

    def show_hist(self, name):
        self.fig.clear()
        self._plot_hist(self.fig.add_subplot(111), name)
        self.fig.tight_layout()
        self.canvas.draw()

    def _row(self, parent, text, command, spins, pady=0):
        """A button with its small labelled spinboxes to the right, on one row."""
        row = tk.Frame(parent)
        row.pack(fill="x", pady=pady)
        tk.Button(row, text=text, command=command).pack(side="left", fill="x", expand=True)
        for label, var, lo, hi, step in spins:
            tk.Label(row, text=label, font=("TkDefaultFont", 8)).pack(side="left", padx=(6, 1))
            tk.Spinbox(row, textvariable=var, from_=lo, to=hi, increment=step,
                       width=5).pack(side="left")

    def _get(self, var, lo, hi):
        """Read a spinbox value, clamped; fall back to the last valid value on bad input."""
        try:
            v = var.get()
        except tk.TclError:
            v = getattr(var, "_last", lo)
        v = min(max(v, lo), hi)
        var.set(v)
        var._last = v
        return v

    def show_original(self):
        """Histogram of the original image: R, G, B overlaid (or grey if monochrome)."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        names = [n for n in self.data["hists"] if n != "Gray"] or ["Gray"]
        for name in names:
            ax.plot(np.arange(256), self.data["hists"][name],
                    color=dict(CHANNELS).get(name, "gray"), label=name, linewidth=1)
        ax.set_title("Original image histogram")
        ax.set_xlim(0, 255)
        ax.set_xlabel("Intensity")
        ax.set_ylabel("Pixels")
        ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def show_all(self):
        self.fig.clear()
        names = list(self.data["hists"])
        cols = 2
        rows = (len(names) + cols - 1) // cols
        for i, name in enumerate(names):
            self._plot_hist(self.fig.add_subplot(rows, cols, i + 1), name)
        self.fig.tight_layout()
        self.canvas.draw()

    def show_original_image(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(self.data["img"])
        ax.set_title("Original image")
        ax.axis("off")
        self.canvas.draw()

    def show_gray(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        im = ax.imshow(self.data["gray"], cmap="gray", vmin=0, vmax=255)
        self.fig.colorbar(im, ax=ax, label="Intensity")
        ax.set_title("Greyscale")
        ax.axis("off")
        self.canvas.draw()

    def _compute_entropy(self):
        win = int(self._get(self.v_win, 2, 101))
        bins = int(self._get(self.v_bins, 2, 256))
        # Use the blurred image only once it has been generated via the blur button
        use_blur = self.data["blur"] is not None
        key = (win, bins, self.blur_key if use_blur else None)
        if self.ent_key != key:
            self.win.config(cursor="watch")
            self.win.update_idletasks()
            src = to_gray(self.data["blur"]) if use_blur else self.data["gray"]
            self.data["entropy"] = entropy_map(src, win, bins)
            self.ent_key = key
            self.win.config(cursor="")
        return win, bins

    def _threshold_mask(self):
        win, bins = self._compute_entropy()
        thr = self._get(self.v_thr, 0, 8)
        below = self.v_below.get()
        ent = self.data["entropy"]
        mask = ent < thr if below else ent > thr
        return mask, win, bins, thr, below

    def show_binary(self):
        mask, win, bins, thr, below = self._threshold_mask()
        self._last_thr_view = self.show_binary
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(mask.astype(np.uint8) * 255, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"Binary mask: 255 where entropy {'<' if below else '>'} {thr:g} bits "
                     f"({mask.mean():.1%}; {win}px, {bins} bins)")
        ax.axis("off")
        self.canvas.draw()

    def show_threshold(self):
        mask, win, bins, thr, below = self._threshold_mask()
        self._last_thr_view = self.show_threshold
        grey = np.repeat(self.data["gray"][..., None], 3, axis=2)
        out = np.where(mask[..., None], np.asarray(self.data["img"], dtype=float), grey)
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(out.astype(np.uint8))
        ax.set_title(f"Colour where entropy {'<' if below else '>'} {thr:g} bits "
                     f"({mask.mean():.1%} of pixels; {win}px, {bins} bins)")
        ax.axis("off")
        self.canvas.draw()

    def show_entropy(self):
        win, bins = self._compute_entropy()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        im = ax.imshow(self.data["entropy"], cmap="inferno")
        self.fig.colorbar(im, ax=ax, label="bits")
        src = "blurred" if self.data["blur"] is not None else "original"
        ax.set_title(f"Local entropy of {src} image ({win}x{win} window, {bins} bins)")
        ax.axis("off")
        self.canvas.draw()

    def _edges(self):
        """Edge image from the original, or from the latest blur once generated."""
        blurred = self.data["blur"] is not None
        key = self.blur_key if blurred else None
        if self.edge_key != key:
            src = to_gray(self.data["blur"]) if blurred else self.data["gray"]
            self.edges_img = edges(src)
            self.edge_key = key
        return blurred

    def show_hough(self):
        blurred = self._edges()
        self.win.config(cursor="watch")
        self.win.update_idletasks()
        thr = self._get(self.v_hthr, 0.05, 1)
        n = int(self._get(self.v_hlines, 1, 200))
        acc, thetas, rhos, lines, npts = hough_lines(self.edges_img, thr, n)
        self.win.config(cursor="")
        self.fig.clear()
        ax1, ax2 = self.fig.subplots(1, 2)
        h, w = self.edges_img.shape
        ax1.imshow(self.data["gray"], cmap="gray", vmin=0, vmax=255)
        xs = np.array([0, w - 1])
        for rho, t, _ in lines:
            if abs(np.sin(t)) > 1e-6:
                ax1.plot(xs, (rho - xs * np.cos(t)) / np.sin(t), "r-", lw=1)
            else:
                ax1.axvline(rho / np.cos(t), color="r", lw=1)
        ax1.set_xlim(0, w - 1)
        ax1.set_ylim(h - 1, 0)
        ax1.set_title(f"Top {len(lines)} Hough lines")
        ax1.axis("off")
        im = ax2.imshow(acc, cmap="inferno", aspect="auto",
                        extent=[-90, 90, rhos[-1], rhos[0]])
        self.fig.colorbar(im, ax=ax2, label="Votes")
        ax2.set_xlabel("theta (deg)")
        ax2.set_ylabel("rho (px)")
        ax2.set_title(f"Hough accumulator ({npts} edge px, "
                      f"{'blurred' if blurred else 'original'} edges)")
        self.fig.tight_layout()
        self.canvas.draw()

    def show_fft(self):
        spec = self._spectrum()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        im = ax.imshow(np.log1p(np.abs(spec)), cmap="magma")
        self.fig.colorbar(im, ax=ax, label="log(1 + |F|)")
        ax.set_title("Fourier spectrum (centred, grey image)")
        ax.axis("off")
        self.canvas.draw()

    def _spectrum(self):
        if self.data.get("spec") is None:
            self.data["spec"] = np.fft.fftshift(np.fft.fft2(self.data["gray"]))
        return self.data["spec"]

    def show_fft_cut(self):
        radius = self._get(self.v_fcut, 0, 1)
        inv = self.v_finv.get()
        self.win.config(cursor="watch")
        self.win.update_idletasks()
        spec, mask, rec = fft_cut(self.data["gray"], radius, inv)
        self.win.config(cursor="")
        self.fig.clear()
        axes = self.fig.subplots(1, 2)
        im0 = axes[0].imshow(np.log1p(np.abs(spec * mask)), cmap="magma")
        self.fig.colorbar(im0, ax=axes[0], label="log(1 + |F|)")
        axes[0].set_title(f"Kept spectrum ({'high' if inv else 'low'}-pass, "
                          f"r {'>' if inv else '<='} {radius:g} Nyquist; {mask.mean():.1%} kept)")
        im1 = axes[1].imshow(rec, cmap="gray")
        self.fig.colorbar(im1, ax=axes[1], label="Intensity")
        axes[1].set_title("Inverse Fourier transform")
        for ax in axes:
            ax.axis("off")
        self.fig.tight_layout()
        self.canvas.draw()

    def show_edges(self):
        blurred = self._edges()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(self.edges_img, cmap="gray")
        ax.set_title(f"Edges (Sobel convolution) of {'blurred' if blurred else 'original'} image")
        ax.axis("off")
        self.canvas.draw()

    def _blurred(self):
        """Ensure the blurred image matches the current width; return the width."""
        sigma = self._get(self.v_blur, 0.5, 200)
        if self.blur_key != sigma:
            self.data["blur"] = ndimage.gaussian_filter(
                self.data["rgb"], sigma=(sigma, sigma, 0))
            self.blur_key = sigma
        return sigma

    def reset(self):
        """Restore default parameters, drop cached results, show the original image."""
        self.v_blur.set(BLUR_WIDTH)
        self.v_win.set(ENTROPY_WINDOW)
        self.v_bins.set(ENTROPY_BINS)
        self.v_thr.set(ENTROPY_THRESHOLD)
        self.v_below.set(False)
        self.ent_key = self.blur_key = None
        self.edge_key = "unset"
        self.v_hthr.set(HOUGH_THRESHOLD)
        self.v_hlines.set(HOUGH_LINES)
        self.v_fcut.set(FFT_CUTOFF)
        self.v_finv.set(False)
        self.data["entropy"] = self.data["blur"] = None
        self._last_thr_view = self.show_binary
        self.show_original_image()

    def show_blur(self):
        sigma = self._blurred()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(self.data["blur"].clip(0, 255).astype(np.uint8))
        ax.set_title(f"Gaussian blur (sigma={sigma:g}px)")
        ax.axis("off")
        self.canvas.draw()


def open_image(root, path=None):
    """Ask for an image file (unless a path is given) and open an analysis window."""
    if path is None:
        patterns = " ".join(f"*{e}" for e in sorted(EXTS))
        path = filedialog.askopenfilename(
            parent=root, title="Open image",
            initialdir=PHOTO_DIR if PHOTO_DIR.is_dir() else Path(__file__).parent,
            filetypes=[("Images", patterns), ("All files", "*.*")])
        if not path:
            return
    try:
        data = analyze(Path(path))
    except Exception as exc:  # unreadable / unsupported file
        messagebox.showerror("Cannot open image", f"{path}\n\n{exc}", parent=root)
        return
    ImageWindow(root, data)


def main():
    root = tk.Tk()
    root.title("Image analyzer")
    tk.Label(root, text="Open an image to analyze it.\nEach image opens in its own window.",
             padx=20, pady=10).pack()
    tk.Button(root, text="Open image...  (Ctrl+O)",
              command=lambda: open_image(root)).pack(padx=20, pady=(0, 8))
    tk.Button(root, text="Exit", bg="#ff9999", activebackground="#ff7777",
              command=root.destroy).pack(padx=20, pady=(0, 15), fill="x")
    root.bind("<Control-o>", lambda e: open_image(root))
    menu = tk.Menu(root)
    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=lambda: open_image(root))
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.destroy)
    menu.add_cascade(label="File", menu=filemenu)
    root.config(menu=menu)
    root.mainloop()


if __name__ == "__main__":
    main()
