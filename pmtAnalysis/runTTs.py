#!/usr/bin/env python3
"""Tkinter launcher for timeWalkAnalysis_usePedestalByWUT.py."""

from __future__ import annotations

import glob
import os
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

TESTER_DATE_RE = re.compile(r"TESTER_0_pmt_test_(\d{8})(?:_(\d{6}))?")
MIN_TESTER_DATE = "20260901"
BUTTON_IDLE_BG = "light green"
BUTTON_RUNNING_BG = "light blue"
BUTTON_COMPARE_BG = "magenta"
BUTTON_COMPARE_DISABLED_BG = "light grey"
EXIT_BUTTON_BG = "#ffb3b3"
ADC_THRESHOLD_FALLBACK = 10.0
LOGO_HEIGHT = 64


def load_logo(root: tk.Tk, path: str) -> ImageTk.PhotoImage:
    """Load a logo at the configured height, preserving its aspect ratio."""
    with Image.open(path) as image:
        width = max(1, round(image.width * LOGO_HEIGHT / image.height))
        resized = image.resize((width, LOGO_HEIGHT), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized, master=root)


def add_bottom_image(root: tk.Tk, parent: tk.Frame, path: str) -> None:
    """Display a left-aligned image at one-third of the window width."""
    with Image.open(path) as image:
        original = image.copy()
    label = tk.Label(parent)
    label.pack(side="left", anchor="n", padx=(0, 10))
    photo: ImageTk.PhotoImage | None = None
    displayed_width = 0

    def resize(event: tk.Event) -> None:
        nonlocal photo, displayed_width
        if event.widget is not root:
            return
        width = max(1, event.width // 3)
        if width == displayed_width:
            return
        height = max(1, round(original.height * width / original.width))
        resized = original.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized, master=root)
        label.configure(image=photo)
        displayed_width = width

    root.bind("<Configure>", resize, add="+")


def launch_with_output(
    command: list[str], cwd: str, output_queue: queue.Queue[str], label: str
) -> subprocess.Popen:
    """Run a child unbuffered and read its combined output off the Tk thread."""
    process = subprocess.Popen(
        [command[0], "-u", *command[1:]],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    def read_output() -> None:
        assert process.stdout is not None
        try:
            with process.stdout:
                for line in process.stdout:
                    output_queue.put(f"[{label}] {line}")
        except OSError as exc:
            output_queue.put(f"[{label}] Error reading output: {exc}\n")

    threading.Thread(target=read_output, daemon=True).start()
    return process


def drain_output(output_queue: queue.Queue[str], output_text: tk.Text) -> None:
    """Append queued child output on the Tk thread."""
    lines = []
    for _ in range(500):
        try:
            lines.append(output_queue.get_nowait())
        except queue.Empty:
            break
    if lines:
        output_text.configure(state=tk.NORMAL)
        output_text.insert(tk.END, "".join(lines))
        output_text.see(tk.END)
        output_text.configure(state=tk.DISABLED)


def find_tts_csvs(root_file: str) -> list[str]:
    """Find the CSVs that the comparison script will read."""
    return glob.glob(os.path.join(os.path.dirname(root_file), "tts_table_adc_ge_*.csv"))


def update_compare_buttons(buttons_by_path: dict[str, tk.Button]) -> None:
    """Refresh counts as analysis runs create additional CSVs."""
    for path, button in buttons_by_path.items():
        count = len(find_tts_csvs(path))
        button.configure(
            text=f"Compare CSVs ({count})",
            state=tk.NORMAL if count else tk.DISABLED,
            bg=BUTTON_COMPARE_BG if count else BUTTON_COMPARE_DISABLED_BG,
        )


def discover_root_files(base_dir: str) -> list[tuple[str, str]]:
    """Return (display_label, root_file) sorted by newest TESTER date first."""
    pattern = os.path.join(base_dir, "TESTER_0_pmt_test_2026*", "*data*.root")
    root_files = [
        path
        for path in glob.glob(pattern)
        if (match := TESTER_DATE_RE.match(os.path.basename(os.path.dirname(path))))
        and match.group(1) >= MIN_TESTER_DATE
    ]

    def sort_key(path: str) -> tuple[str, str, float]:
        tester_dir = os.path.basename(os.path.dirname(path))
        match = TESTER_DATE_RE.match(tester_dir)
        if match:
            date_str = match.group(1)
            time_str = match.group(2) or "000000"
        else:
            date_str = "00000000"
            time_str = "000000"
        mtime = os.path.getmtime(path)
        return (date_str, time_str, mtime)

    sorted_files = sorted(root_files, key=sort_key, reverse=True)
    labeled_files: list[tuple[str, str]] = []
    for path in sorted_files:
        tester_dir = os.path.basename(os.path.dirname(path))
        filename = os.path.basename(path)
        match = TESTER_DATE_RE.match(tester_dir)
        date_label = match.group(1) if match else "00000000"
        labeled_files.append((f"{date_label} | {tester_dir}/{filename}", path))
    return labeled_files


def load_default_adc_threshold(base_dir: str) -> float:
    """Read ADC_THRESHOLD_DEFAULT from analysis script."""
    script_path = os.path.join(base_dir, "timeWalkAnalysis_usePedestalByWUT.py")
    if not os.path.isfile(script_path):
        return ADC_THRESHOLD_FALLBACK
    pattern = re.compile(r"^\s*ADC_THRESHOLD_DEFAULT\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*$")
    with open(script_path) as f:
        for line in f:
            match = pattern.match(line)
            if match:
                return float(match.group(1))
    return ADC_THRESHOLD_FALLBACK


def run_analysis(
    root_file: str,
    base_dir: str,
    status_var: tk.StringVar,
    adc_threshold_var: tk.StringVar,
    button: tk.Button,
    running_processes: dict[str, subprocess.Popen],
    output_queue: queue.Queue[str],
) -> None:
    script_path = os.path.join(base_dir, "timeWalkAnalysis_usePedestalByWUT.py")
    if not os.path.isfile(script_path):
        messagebox.showerror("Missing script", f"Cannot find {script_path}")
        return

    if root_file in running_processes and running_processes[root_file].poll() is None:
        status_var.set(f"Already running: {os.path.basename(root_file)}")
        return

    try:
        adc_threshold = float(adc_threshold_var.get().strip())
    except ValueError:
        messagebox.showerror("Invalid ADC threshold", "ADC threshold must be a numeric value.")
        return

    command = [sys.executable, script_path, root_file, "--adc-threshold", f"{adc_threshold:g}"]
    try:
        process = launch_with_output(command, base_dir, output_queue, os.path.basename(root_file))
    except OSError as exc:
        messagebox.showerror("Launch failed", f"Could not launch analysis:\n{exc}")
        return

    running_processes[root_file] = process
    button.configure(bg=BUTTON_RUNNING_BG)
    status_var.set(
        f"Running: {os.path.basename(root_file)} (ADC threshold >= {adc_threshold:g})"
    )


def compare_csvs(
    root_file: str, base_dir: str, status_var: tk.StringVar, root: tk.Tk,
    output_queue: queue.Queue[str],
) -> None:
    """Launch the comparison for CSVs stored alongside this ROOT file."""
    data_dir = os.path.dirname(root_file)
    if not find_tts_csvs(root_file):
        return
    script_path = os.path.join(base_dir, "compareTTScsv.py")
    if not os.path.isfile(script_path):
        messagebox.showerror("Missing script", f"Cannot find {script_path}")
        return
    try:
        process = launch_with_output(
            [sys.executable, script_path, data_dir], base_dir, output_queue,
            f"Compare {os.path.basename(data_dir)}",
        )
    except OSError as exc:
        messagebox.showerror("Launch failed", f"Could not launch CSV comparison:\n{exc}")
        return
    status_var.set(f"Comparing CSVs: {os.path.basename(data_dir)}")

    def check_process() -> None:
        returncode = process.poll()
        if returncode is None:
            root.after(1000, check_process)
        elif returncode != 0:
            status_var.set(f"CSV comparison failed: {os.path.basename(data_dir)}")
            messagebox.showerror(
                "CSV comparison failed",
                f"Comparison exited with code {returncode}. See the output box for details.",
            )
        else:
            status_var.set(f"CSV comparison closed: {os.path.basename(data_dir)}")

    root.after(1000, check_process)


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = discover_root_files(base_dir)
    default_adc_threshold = load_default_adc_threshold(base_dir)

    root = tk.Tk()
    root.title("runTTs")
    root.geometry("1000x1600")

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=(8, 2))
    left_logo = load_logo(root, os.path.join(base_dir, "share", "logo_combined_small_new_0.png"))
    right_logo = load_logo(root, os.path.join(base_dir, "share", "hk_logo.jpg"))
    left_label = tk.Label(top_frame, image=left_logo)
    left_label.pack(side="left", anchor="n")
    right_label = tk.Label(top_frame, image=right_logo)
    right_label.pack(side="right", anchor="n")
    center_frame = tk.Frame(top_frame)
    center_frame.pack(side="left", fill="both", expand=True)
    tk.Label(center_frame, text="Joint Laboratory of Optics, Palacký University, Olomouc").pack(expand=True)

    header = tk.Label(
        root,
        text="Select ROOT file (newest TESTER_0_pmt_test_2026* dates first):",
        anchor="w",
        justify="left",
        font=("TkDefaultFont", 11, "bold"),
    )
    header.pack(fill="x", padx=10, pady=(2, 6))

    tk.Label(
        root,
        text=(
            "TTS analysis of 3'' Hamamatsu PMTs (type R14374) using "
            "timeWalkAnalysis_usePedestalByWUT.py"
        ),
        anchor="w",
    ).pack(fill="x", padx=10, pady=(0, 6))

    controls_frame = tk.Frame(root)
    controls_frame.pack(fill="x", padx=10, pady=(0, 6))
    tk.Label(
        controls_frame,
        text="ADC threshold cut (passed as --adc-threshold):",
        anchor="w",
    ).pack(side="left")
    adc_threshold_var = tk.StringVar(value=f"{default_adc_threshold:g}")
    adc_threshold_entry = tk.Entry(controls_frame, textvariable=adc_threshold_var, width=12)
    adc_threshold_entry.pack(side="left", padx=(8, 0))
    exit_button = tk.Button(controls_frame, text="Exit", bg=EXIT_BUTTON_BG, command=root.destroy)
    exit_button.pack(side="right")

    status_var = tk.StringVar(value="Ready.")
    status_label = tk.Label(root, textvariable=status_var, anchor="w", fg="navy")
    status_label.pack(fill="x", padx=10, pady=(0, 8))

    tk.Label(
        root,
        text="2026 (c) Jiří Kvita, Adam Jüttner, Vladimír Urbášek",
    ).pack(side="bottom", fill="x", padx=10, pady=(0, 5))
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=5)
    add_bottom_image(
        root, bottom_frame, os.path.join(base_dir, "share", "Screenshot_from_2026-11-15_18-20-35.png")
    )
    output_text = ScrolledText(bottom_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
    output_text.pack(side="left", fill="both", expand=True)
    output_queue: queue.Queue[str] = queue.Queue()

    def refresh_output() -> None:
        drain_output(output_queue, output_text)
        root.after(100, refresh_output)

    root.after(100, refresh_output)

    canvas = tk.Canvas(root, borderwidth=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas)
    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    frame_window = canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(frame_window, width=event.width))
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))
    running_processes: dict[str, subprocess.Popen] = {}
    buttons_by_path: dict[str, tk.Button] = {}
    compare_buttons_by_path: dict[str, tk.Button] = {}

    if not files:
        tk.Label(
            frame,
            text="No matching ROOT files found from September 2026 onwards.",
            fg="darkred",
            anchor="w",
        ).pack(fill="x", padx=10, pady=10)
    else:
        for label, path in files:
            row = tk.Frame(frame)
            row.pack(fill="x", padx=8, pady=3)
            compare_button = tk.Button(
                row,
                command=lambda p=path: compare_csvs(p, base_dir, status_var, root, output_queue),
            )
            compare_button.pack(side="right", padx=(6, 0))
            compare_buttons_by_path[path] = compare_button
            update_compare_buttons({path: compare_button})
            button = tk.Button(
                row,
                text=label,
                anchor="w",
                bg=BUTTON_IDLE_BG,
                command=lambda p=path: run_analysis(
                    p,
                    base_dir,
                    status_var,
                    adc_threshold_var,
                    buttons_by_path[p],
                    running_processes,
                    output_queue,
                ),
            )
            button.pack(side="left", fill="x", expand=True)
            buttons_by_path[path] = button

    def refresh_running_state() -> None:
        update_compare_buttons(compare_buttons_by_path)
        finished: list[str] = []
        for path, process in running_processes.items():
            if process.poll() is not None:
                finished.append(path)
        for path in finished:
            returncode = running_processes.pop(path).returncode
            button = buttons_by_path.get(path)
            if button is not None:
                button.configure(bg=BUTTON_IDLE_BG)
            if returncode == 0:
                status_var.set(f"Finished: {os.path.basename(path)}")
            else:
                status_var.set(f"Failed ({returncode}): {os.path.basename(path)}; see output")
        root.after(1000, refresh_running_state)

    root.after(1000, refresh_running_state)

    root.mainloop()


if __name__ == "__main__":
    main()
