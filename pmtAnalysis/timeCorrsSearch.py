#!/usr/bin/env python3
"""Per-channel ADC, pedestal-shifted ADC, raw pulse-time and cross-hit plots of a `pmt_events` ROOT file.

Per-channel pedestals are read from `json_results_to_db/channel_??.json`
(key `adc_pedestal`) instead of being fitted.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import uproot

try:
    import tkinter as tk
except ImportError:
    tk = None

DEFAULT_INPUT = "1pe_measurement/28cm/test_run_thr30_att825_20260629_141522.root"
TREE_NAME = "pmt_events"

# ADC axis limits for raw ADC histograms.
ADC_RANGE = (180, 480)
ADC_HIST_BINS = (ADC_RANGE[1] - ADC_RANGE[0]) // 2  # 2 ADC counts per bin
ADC_PLOT_LOGY = True

# ADC axis limits for pedestal-shifted ADC histograms.
ADC_CORRECTED_RANGE = (-10, 310)
ADC_CORRECTED_HIST_BINS = (ADC_CORRECTED_RANGE[1] - ADC_CORRECTED_RANGE[0]) // 2

# Time definitions for pulse-time plots.
TDC_LSB_NS = 0.25
PMT_TIME_TICK_NS = 4.0
PMT_PULSE_MODULO_TICKS = 25_000

# Time axis ranges (ns) for raw pulse-time histograms.
# Set to None to auto-infer from data.
PULSE_TIME_RANGE_OPTION1_NS: tuple[float, float] | None = (2.0, 2030.0)
PULSE_TIME_RANGE_OPTION2_NS: tuple[float, float] | None = (140.0, 160.0)

# Optional per-channel range overrides (display channel indexing: 1, 2, ...).
PULSE_TIME_RANGE_OPTION1_BY_CHANNEL_NS: dict[int, tuple[float, float]] = {
    1: (210.0, 235.0),
}
PULSE_TIME_RANGE_OPTION2_BY_CHANNEL_NS: dict[int, tuple[float, float]] = {}

# Base bin width (ns) for 1D pulse-time histograms.
# Final 1D width is this value multiplied by --rebin-time.
PULSE_TIME_1D_BIN_WIDTH_NS = 0.25

# Coincidence-analysis globals (can be adjusted here).
COINCIDENCE_WINDOW_NS_DEFAULT = 4.0
CROSSHIT_THRESHOLD_REF_DEFAULT = 50.0
CROSSHIT_THRESHOLD_TEST_DEFAULT = 40.0
CROSSHIT_CHANNEL_MIN = 0
CROSSHIT_CHANNEL_MAX = 20
CROSSHIT_CHANNEL_BINS = CROSSHIT_CHANNEL_MAX - CROSSHIT_CHANNEL_MIN

PEDESTAL_JSON_SUBDIR = "json_results_to_db"


def load_pedestals_from_json(pedestal_dir: str, raw_channels: list[int]) -> dict[int, float]:
    """Read 'adc_pedestal' from channel_<display channel>.json (display = raw + 1)."""
    pedestals: dict[int, float] = {}
    for raw_ch in raw_channels:
        display_ch = raw_ch + 1
        path = os.path.join(pedestal_dir, f"channel_{display_ch:02d}.json")
        if not os.path.isfile(path):
            print(f"Channel {display_ch:02d}: pedestal file {path} not found.")
            continue
        with open(path) as f:
            value = json.load(f).get("adc_pedestal")
        if isinstance(value, (int, float)) and np.isfinite(value):
            pedestals[display_ch] = float(value)
        else:
            print(f"Channel {display_ch:02d}: no valid 'adc_pedestal' in {path}.")
    return pedestals


def load_events(root_file: str, tree_name: str = TREE_NAME) -> dict:
    """Read ADC and pulse-time branches as numpy arrays."""
    with uproot.open(root_file) as f:
        tree = f[tree_name]
        arrays = tree.arrays(["channel", "adc", "pmt_time", "tdc_start"], library="np")
    return arrays


def compute_pulse_time_ns(
    pmt_time: np.ndarray,
    tdc_start: np.ndarray,
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
) -> tuple[np.ndarray, str]:
    """Compute raw pulse time in nanoseconds using one of the two definitions."""
    pmt_time_i64 = pmt_time.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)

    if pulse_time_source == "option1":
        # option1: ((pmt_time << 4) + tdc_start) * 0.25 ns
        T = (pmt_time_i64 << np.int64(4)) + tdc_start_i64
        pulse_time_ns = T.astype(np.float64) * TDC_LSB_NS
        label = "Pulse time [ns] = ((pmt_time << 4) + tdc_start) * 0.25"
    elif pulse_time_source == "option2":
        # option2: (pmt_time % 25000) * 4 ns + tdc_start * 0.25 ns
        modulo_i64 = np.int64(pmt_pulse_modulo_ticks)
        pulse_time_ticks = np.mod(pmt_time_i64, modulo_i64)
        pulse_time_ns = (
            pulse_time_ticks.astype(np.float64) * PMT_TIME_TICK_NS
            + tdc_start_i64.astype(np.float64) * TDC_LSB_NS
        )
        label = (
            "Pulse time [ns] = (pmt_time % "
            f"{pmt_pulse_modulo_ticks}) * {PMT_TIME_TICK_NS:.0f}"
            f" + tdc_start * {TDC_LSB_NS:.2f}"
        )
    else:
        raise ValueError(f"Unsupported pulse_time_source: {pulse_time_source}")

    return pulse_time_ns, label


def analyze_channel(
    raw_channel: int,
    pedestal_adc: float | None,
    adc_ch: np.ndarray,
    pmt_time_ch: np.ndarray,
    tdc_start_ch: np.ndarray,
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
) -> dict | None:
    """Collect per-channel arrays and the externally supplied pedestal."""
    display_ch = raw_channel + 1

    if pedestal_adc is None or not np.isfinite(pedestal_adc):
        print(f"Channel {display_ch:02d}: no adc_pedestal in JSON, skipping.")
        return None

    finite_mask = np.isfinite(adc_ch) & np.isfinite(pmt_time_ch) & np.isfinite(tdc_start_ch)
    adc_ch = adc_ch[finite_mask]
    pmt_time_ch = pmt_time_ch[finite_mask]
    tdc_start_ch = tdc_start_ch[finite_mask]

    if adc_ch.size == 0:
        print(f"Channel {display_ch:02d}: no finite ADC data, skipping.")
        return None

    pulse_time_ns, pulse_time_label = compute_pulse_time_ns(
        pmt_time_ch,
        tdc_start_ch,
        pulse_time_source=pulse_time_source,
        pmt_pulse_modulo_ticks=pmt_pulse_modulo_ticks,
    )

    n_entries = adc_ch.size
    adc_rms = float(np.std(adc_ch))
    print(f"Channel {display_ch:02d}: entries={n_entries:,}, ADC RMS={adc_rms:.2f}, pedestal={pedestal_adc:.2f}")

    return {
        "channel": display_ch,
        "adc": adc_ch,
        "adc_pedestal_shifted": adc_ch - pedestal_adc,
        "pulse_time_ns": pulse_time_ns,
        "pulse_time_label": pulse_time_label,
        "pedestal_adc": pedestal_adc,
        "entries": n_entries,
        "adc_rms": adc_rms,
        "adc_shifted_rms": float(np.std(adc_ch - pedestal_adc)),
    }


def _grid_shape(n_items: int) -> tuple[int, int]:
    """Pick a roughly-square (rows, cols) grid layout for n_items subplots."""
    ncols = math.ceil(math.sqrt(n_items))
    nrows = math.ceil(n_items / ncols)
    return nrows, ncols


def extract_threshold_tag_from_path(path: str) -> str | None:
    """Extract threshold tag from a file path, e.g. Thr15mV or thr30mV.

    Returns a canonical tag like "Thr15mV" when a match is found,
    otherwise returns None.
    """
    match = re.search(r"thr\s*[_-]?\s*(\d+)\s*mv", path, flags=re.IGNORECASE)
    if match is None:
        return None
    return f"Thr{match.group(1)}mV"


def save_figure_dual_format(fig: plt.Figure, output_dir: str, base_name: str) -> None:
    """Save figure as both PNG and PDF under png/ and pdf/ subdirectories."""
    png_dir = os.path.join(output_dir, "png")
    pdf_dir = os.path.join(output_dir, "pdf")
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    fig.savefig(os.path.join(png_dir, f"{base_name}.png"), dpi=150)
    fig.savefig(os.path.join(pdf_dir, f"{base_name}.pdf"))


def plot_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc",
    rms_key: str = "adc_rms",
    adc_range: tuple[float, float] = ADC_RANGE,
    adc_bins: int = ADC_HIST_BINS,
    title: str = "ADC by channel",
    output_suffix: str = "adc_grid",
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot ADC histogram of every channel as a single grid figure."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        ax.hist(
            data[adc_key],
            bins=adc_bins,
            range=adc_range,
            histtype="stepfilled",
            color="indianred",
            alpha=0.6,
            edgecolor="black",
            linewidth=0.3,
            label=f"RMS={data[rms_key]:.1f}",
        )

        if adc_key == "adc":
            ax.axvline(
                data["pedestal_adc"],
                color="royalblue",
                linewidth=1.5,
                label=f"pedestal={data['pedestal_adc']:.1f}",
            )

        ax.set_xlim(*adc_range)
        if ADC_PLOT_LOGY:
            ax.set_yscale("log")
            ax.set_ylim(bottom=0.5)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)
        if dataset_tag is not None:
            ax.plot([], [], " ", label=dataset_tag)
        ax.legend(fontsize=7, loc="upper right")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_{output_suffix}")
    return fig


def plot_pulse_time_hist_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    pulse_time_source: str,
    rebin_time: int = 1,
    time_bin_width_ns: float = PULSE_TIME_1D_BIN_WIDTH_NS,
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot raw (uncut) 1D pulse-time histograms for each channel as a grid."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    if pulse_time_source == "option1":
        default_range = PULSE_TIME_RANGE_OPTION1_NS
        overrides = PULSE_TIME_RANGE_OPTION1_BY_CHANNEL_NS
    else:
        default_range = PULSE_TIME_RANGE_OPTION2_NS
        overrides = PULSE_TIME_RANGE_OPTION2_BY_CHANNEL_NS

    if default_range is None:
        finite_all = [
            data["pulse_time_ns"][np.isfinite(data["pulse_time_ns"])] for data in channel_data
        ]
        merged = np.concatenate(finite_all) if finite_all else np.array([])
        if merged.size > 0:
            t_lo, t_hi = float(np.min(merged)), float(np.max(merged))
            if t_hi <= t_lo:
                t_hi = t_lo + 1.0
            pad = max((t_hi - t_lo) * 0.05, TDC_LSB_NS)
            default_range = (t_lo - pad, t_hi + pad)
        else:
            default_range = (0.0, 1.0)

    bin_width_ns = time_bin_width_ns * float(rebin_time)
    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        t_min, t_max = overrides.get(data["channel"], default_range)
        t = data["pulse_time_ns"]
        t = t[np.isfinite(t)]

        if t.size > 0:
            n_bins = max(1, int(np.ceil(max(t_max - t_min, bin_width_ns) / bin_width_ns)))
            mean_t = float(np.mean(t))
            ax.hist(
                t,
                bins=n_bins,
                range=(t_min, t_max),
                histtype="stepfilled",
                color="steelblue",
                alpha=0.65,
                edgecolor="black",
                linewidth=0.3,
            )
            legend_label = f"mean={mean_t:.2f} ns"
            if dataset_tag is not None:
                legend_label += f"\n{dataset_tag}"
            ax.axvline(mean_t, color="darkred", linestyle="--", linewidth=1.2, label=legend_label)
            ax.legend(fontsize=7, loc="upper right")
        else:
            ax.text(
                0.5,
                0.5,
                "No finite points",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=8,
                color="dimgray",
            )

        ax.set_xlim(t_min, t_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel(data["pulse_time_label"])
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(f"Raw pulse time by channel ({pulse_time_source})")
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_pulse_time_{pulse_time_source}_hist_grid")
    return fig


def build_cross_hit_histograms(
    channel: np.ndarray,
    adc: np.ndarray,
    pmt_time: np.ndarray,
    tdc_start: np.ndarray,
    pedestal_by_channel: dict[int, float],
    threshold_ref: float,
    threshold_test: float,
    coincidence_window_ns: float,
) -> list[dict]:
    """Build per-channel cross-hit counts versus test channel using option1 time in ns."""
    def _print_progress(done: int, total: int) -> None:
        bar_width = 30
        fraction = 1.0 if total <= 0 else done / total
        filled = min(bar_width, max(0, int(round(fraction * bar_width))))
        bar = "#" * filled + "-" * (bar_width - filled)
        print(
            f"\rCross-hit analysis: [{bar}] {done}/{total} ({fraction * 100.0:5.1f}%)",
            end="",
            flush=True,
        )

    times_by_channel: dict[int, np.ndarray] = {}
    shifted_adc_by_channel: dict[int, np.ndarray] = {}
    available_channels: list[int] = []

    raw_channels = np.unique(channel.astype(np.int64))
    for raw_ch in raw_channels:
        display_ch = int(raw_ch) + 1
        if not CROSSHIT_CHANNEL_MIN <= display_ch < CROSSHIT_CHANNEL_MAX:
            raise ValueError(f"Channel {display_ch} is outside the cross-hit histogram range")
        pedestal = pedestal_by_channel.get(display_ch)
        if pedestal is None or not np.isfinite(pedestal):
            continue

        mask = channel == raw_ch
        adc_ch = adc[mask]
        pmt_time_ch = pmt_time[mask]
        tdc_start_ch = tdc_start[mask]
        finite_mask = np.isfinite(adc_ch) & np.isfinite(pmt_time_ch) & np.isfinite(tdc_start_ch)
        if not np.any(finite_mask):
            continue

        adc_ch = adc_ch[finite_mask]
        pmt_time_ch = pmt_time_ch[finite_mask]
        tdc_start_ch = tdc_start_ch[finite_mask]
        pulse_time_ns, _ = compute_pulse_time_ns(
            pmt_time_ch,
            tdc_start_ch,
            pulse_time_source="option1",
            pmt_pulse_modulo_ticks=PMT_PULSE_MODULO_TICKS,
        )

        times_by_channel[display_ch] = pulse_time_ns
        shifted_adc_by_channel[display_ch] = adc_ch - pedestal
        available_channels.append(display_ch)

    available_channels = sorted(set(available_channels))
    if not available_channels:
        return []

    test_times_by_channel: dict[int, np.ndarray] = {}
    for ch in available_channels:
        ch_times = times_by_channel[ch]
        ch_adc_shifted = shifted_adc_by_channel[ch]
        test_mask = ch_adc_shifted >= threshold_test
        test_times = ch_times[test_mask]
        if test_times.size > 0:
            test_times = np.sort(test_times.astype(np.float64))
        else:
            test_times = np.array([], dtype=np.float64)
        test_times_by_channel[ch] = test_times

    half_window_ns = 0.5 * coincidence_window_ns
    results: list[dict] = []
    total_refs = len(available_channels)
    _print_progress(0, total_refs)
    for idx_ref, ref_ch in enumerate(available_channels, start=1):
        ref_times = times_by_channel[ref_ch]
        ref_adc_shifted = shifted_adc_by_channel[ref_ch]
        ref_mask = ref_adc_shifted >= threshold_ref
        ref_selected_times = ref_times[ref_mask].astype(np.float64)
        counts_by_test = np.zeros(CROSSHIT_CHANNEL_BINS, dtype=np.int64)

        for test_ch in available_channels:
            if test_ch == ref_ch:
                continue
            test_times = test_times_by_channel[test_ch]
            if ref_selected_times.size == 0 or test_times.size == 0:
                continue

            match_count = 0
            for t_ref in ref_selected_times:
                left = np.searchsorted(test_times, t_ref - half_window_ns, side="left")
                right = np.searchsorted(test_times, t_ref + half_window_ns, side="right")
                if right > left:
                    match_count += 1
            counts_by_test[test_ch] = match_count

        results.append(
            {
                "channel": ref_ch,
                "counts_by_test_channel": counts_by_test,
                "n_ref_hits": int(ref_selected_times.size),
            }
        )
        _print_progress(idx_ref, total_refs)

    print()

    return results


def plot_cross_hit_grid(
    cross_hit_data: list[dict],
    output_dir: str,
    stem: str,
    threshold_ref: float,
    threshold_test: float,
    coincidence_window_ns: float,
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot per-reference-channel cross-hit histograms for integer channels in [0, 20)."""
    nrows, ncols = _grid_shape(len(cross_hit_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.8 * ncols, 3.8 * nrows), squeeze=False)
    bin_centers = np.arange(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX, dtype=np.float64)

    for idx, data in enumerate(cross_hit_data):
        ax = axes[idx // ncols][idx % ncols]
        counts = np.asarray(data["counts_by_test_channel"], dtype=np.int64)
        ax.hist(
            bin_centers,
            bins=CROSSHIT_CHANNEL_BINS,
            range=(CROSSHIT_CHANNEL_MIN - 0.5, CROSSHIT_CHANNEL_MAX - 0.5),
            weights=counts,
            histtype="stepfilled",
            color="mediumpurple",
            alpha=0.7,
            edgecolor="black",
            linewidth=0.4,
        )
        ax.axvline(float(data["channel"]), color="black", linestyle="--", linewidth=1.0)
        ax.set_xlim(float(CROSSHIT_CHANNEL_MIN), float(CROSSHIT_CHANNEL_MAX))
        ax.set_xticks(np.arange(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX + 1))
        ax.set_title(f"Ref Ch {data['channel']:02d}")
        ax.set_xlabel("Test channel")
        ax.set_ylabel("Cross-hits")
        legend_label = (
            f"Ref hits={data['n_ref_hits']}\n"
            f"Total cross={int(np.sum(counts))}"
        )
        if dataset_tag is not None:
            legend_label += f"\n{dataset_tag}"
        ax.plot([], [], " ", label=legend_label)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(cross_hit_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(
        "Cross-channel coincidence counts "
        f"(option1 time, window={coincidence_window_ns:g} ns, "
        f"ref ADC>={threshold_ref:g}, test ADC>={threshold_test:g})"
    )
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_cross_hit_grid")
    return fig


def plot_cross_hit_2d(
    cross_hit_data: list[dict],
    output_dir: str,
    stem: str,
    threshold_ref: float,
    threshold_test: float,
    coincidence_window_ns: float,
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot a 2D cross-hit map: reference channel vs test channel."""
    matrix = np.zeros((CROSSHIT_CHANNEL_BINS, CROSSHIT_CHANNEL_BINS), dtype=np.float64)
    for row in cross_hit_data:
        ref_ch = int(row["channel"])
        if not (CROSSHIT_CHANNEL_MIN <= ref_ch < CROSSHIT_CHANNEL_MAX):
            continue
        counts = np.asarray(row["counts_by_test_channel"], dtype=np.float64)
        matrix[ref_ch, : counts.size] = counts

    fig, ax = plt.subplots(figsize=(8.5, 7.0))
    image = ax.imshow(
        matrix,
        origin="lower",
        interpolation="nearest",
        aspect="auto",
        extent=(
            CROSSHIT_CHANNEL_MIN - 0.5,
            CROSSHIT_CHANNEL_MAX - 0.5,
            CROSSHIT_CHANNEL_MIN - 0.5,
            CROSSHIT_CHANNEL_MAX - 0.5,
        ),
    )
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("Cross-hit count")

    ax.set_xlabel("Test channel")
    ax.set_ylabel("Reference channel")
    ax.set_xlim(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX)
    ax.set_ylim(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX)
    ax.set_xticks(np.arange(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX + 1))
    ax.set_yticks(np.arange(CROSSHIT_CHANNEL_MIN, CROSSHIT_CHANNEL_MAX + 1))
    ax.grid(True, linestyle="--", alpha=0.2)
    title = (
        "Cross-hit 2D map "
        f"(option1 time, window={coincidence_window_ns:g} ns, "
        f"ref ADC>={threshold_ref:g}, test ADC>={threshold_test:g})"
    )
    if dataset_tag is not None:
        title += f"\n{dataset_tag}"
    ax.set_title(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_cross_hit_2d")
    return fig


def run_exit_gui() -> None:
    """Open a tiny control GUI in the top-right; Exit closes all and quits."""
    if tk is None:
        print("Tkinter is not available; skipping GUI.")
        return

    try:
        root = tk.Tk()
    except tk.TclError:
        print("Tkinter GUI could not start (no display?).")
        return

    root.title("PMT ADC Analysis")
    window_width = 320
    window_height = 140
    margin = 20
    screen_width = root.winfo_screenwidth()
    x_pos = max(0, screen_width - window_width - margin)
    y_pos = margin
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    label = tk.Label(root, text="Plots are running. Click Exit to close everything.")
    label.pack(pady=12)

    def _exit_all() -> None:
        plt.close("all")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _exit_all)

    exit_button = tk.Button(
        root,
        text="Exit",
        width=12,
        command=_exit_all,
        bg="#f28a8a",
        fg="white",
        activebackground="#e06f6f",
        activeforeground="white",
    )
    exit_button.pack(pady=8)

    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Per-channel ADC, pedestal-shifted ADC, raw time and cross-hit "
            "plots of a pmt_events ROOT file."
        )
    )
    parser.add_argument("input", nargs="?", default=DEFAULT_INPUT, help="Path to input ROOT file.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Base directory for outputs (default: alongside the input file). "
            "Plots are saved as PNG and PDF under png/ and pdf/ subdirectories."
        ),
    )
    parser.add_argument(
        "--pulse-time-source",
        choices=("option1", "option2"),
        default="option2",
        help=(
            "Pulse-time definition: "
            "option1=((pmt_time<<4)+tdc_start)*0.25 ns, "
            "option2=(pmt_time%%25000)*4 ns + tdc_start*0.25 ns."
        ),
    )
    parser.add_argument(
        "--pmt-pulse-modulo-ticks",
        type=int,
        default=PMT_PULSE_MODULO_TICKS,
        help="Modulo period for option2 pulse time (default: %(default)s).",
    )
    parser.add_argument(
        "--rebin-time",
        type=int,
        default=1,
        help=(
            "Rebin factor for 1D pulse-time histograms (default: %(default)s). "
            "Effective 1D time-bin width is --time-bin-width * rebin-time."
        ),
    )
    parser.add_argument(
        "--time-bin-width",
        type=float,
        default=PULSE_TIME_1D_BIN_WIDTH_NS,
        help="Base 1D pulse-time histogram bin width in ns (default: %(default)s).",
    )
    parser.add_argument(
        "--crosshit-threshold-ref",
        type=float,
        default=CROSSHIT_THRESHOLD_REF_DEFAULT,
        help=(
            "Pedestal-shifted ADC threshold for the reference channel hit "
            "(default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--crosshit-threshold-test",
        type=float,
        default=CROSSHIT_THRESHOLD_TEST_DEFAULT,
        help=(
            "Pedestal-shifted ADC threshold for the test channel hit "
            "(default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--crosshit-window-ns",
        type=float,
        default=COINCIDENCE_WINDOW_NS_DEFAULT,
        help=(
            "Full coincidence time window in ns for cross-hit matching "
            "(default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--pedestal-dir",
        default=None,
        help=(
            "Directory with channel_??.json files holding the 'adc_pedestal' key "
            f"(default: <input dir>/{PEDESTAL_JSON_SUBDIR})."
        ),
    )
    args = parser.parse_args()

    if args.pmt_pulse_modulo_ticks <= 0:
        raise ValueError("--pmt-pulse-modulo-ticks must be > 0")
    if args.rebin_time <= 0:
        raise ValueError("--rebin-time must be > 0")
    if not np.isfinite(args.time_bin_width) or args.time_bin_width <= 0:
        raise ValueError("--time-bin-width must be finite and > 0")
    if not np.isfinite(args.crosshit_threshold_ref):
        raise ValueError("--crosshit-threshold-ref must be finite")
    if not np.isfinite(args.crosshit_threshold_test):
        raise ValueError("--crosshit-threshold-test must be finite")
    if not np.isfinite(args.crosshit_window_ns) or args.crosshit_window_ns <= 0:
        raise ValueError("--crosshit-window-ns must be finite and > 0")

    input_file = args.input
    dataset_tag = extract_threshold_tag_from_path(input_file)
    output_dir = args.output_dir or os.path.dirname(os.path.abspath(input_file))
    os.makedirs(output_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_file))[0]

    print(f"Reading {input_file} ...")
    arrays = load_events(input_file)

    channel = arrays["channel"].astype(np.int64)
    adc = arrays["adc"].astype(np.float64)
    pmt_time = arrays["pmt_time"].astype(np.int64)
    tdc_start = arrays["tdc_start"].astype(np.int64)

    channels = sorted(np.unique(channel).tolist())
    print(f"Found channels (0-indexed): {channels}")

    pedestal_dir = args.pedestal_dir or os.path.join(
        os.path.dirname(os.path.abspath(input_file)), PEDESTAL_JSON_SUBDIR
    )
    pedestal_by_channel = load_pedestals_from_json(pedestal_dir, channels)

    channel_data = []
    for raw_ch in channels:
        mask = channel == raw_ch
        result = analyze_channel(
            raw_ch,
            pedestal_by_channel.get(raw_ch + 1),
            adc[mask],
            pmt_time[mask],
            tdc_start[mask],
            pulse_time_source=args.pulse_time_source,
            pmt_pulse_modulo_ticks=args.pmt_pulse_modulo_ticks,
        )
        if result:
            channel_data.append(result)

    if not channel_data:
        print("No channel data available to plot.")
        return

    print(f"Saving PNG/PDF plots under {output_dir}/png and {output_dir}/pdf")
    plot_adc_grid(channel_data, output_dir, stem, dataset_tag=dataset_tag)
    plot_adc_grid(
        channel_data,
        output_dir,
        stem,
        adc_key="adc_pedestal_shifted",
        rms_key="adc_shifted_rms",
        adc_range=ADC_CORRECTED_RANGE,
        adc_bins=ADC_CORRECTED_HIST_BINS,
        title="Pedestal-shifted ADC by channel",
        output_suffix="adc_pedestal_shifted_grid",
        dataset_tag=dataset_tag,
    )
    plot_pulse_time_hist_grid(
        channel_data,
        output_dir,
        stem,
        pulse_time_source=args.pulse_time_source,
        rebin_time=args.rebin_time,
        time_bin_width_ns=args.time_bin_width,
        dataset_tag=dataset_tag,
    )
    cross_hit_data = build_cross_hit_histograms(
        channel=channel,
        adc=adc,
        pmt_time=pmt_time,
        tdc_start=tdc_start,
        pedestal_by_channel=pedestal_by_channel,
        threshold_ref=args.crosshit_threshold_ref,
        threshold_test=args.crosshit_threshold_test,
        coincidence_window_ns=args.crosshit_window_ns,
    )
    if cross_hit_data:
        plot_cross_hit_grid(
            cross_hit_data,
            output_dir,
            stem,
            threshold_ref=args.crosshit_threshold_ref,
            threshold_test=args.crosshit_threshold_test,
            coincidence_window_ns=args.crosshit_window_ns,
            dataset_tag=dataset_tag,
        )
        plot_cross_hit_2d(
            cross_hit_data,
            output_dir,
            stem,
            threshold_ref=args.crosshit_threshold_ref,
            threshold_test=args.crosshit_threshold_test,
            coincidence_window_ns=args.crosshit_window_ns,
            dataset_tag=dataset_tag,
        )
    else:
        print("No channels available for cross-hit analysis.")

    if tk is None:
        plt.show()
    else:
        plt.show(block=False)
        run_exit_gui()


if __name__ == "__main__":
    main()
