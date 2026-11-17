#!/usr/bin/env python3
"""Tkinter launcher for timeCorrsSearch.py."""

from __future__ import annotations

import math
import os
import queue
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from runTTs import (
    BUTTON_IDLE_BG,
    BUTTON_RUNNING_BG,
    EXIT_BUTTON_BG,
    add_bottom_image,
    discover_root_files,
    drain_output,
    launch_with_output,
    load_logo,
)
from timeCorrsSearch import (
    COINCIDENCE_WINDOW_NS_DEFAULT,
    CROSSHIT_THRESHOLD_REF_DEFAULT,
    CROSSHIT_THRESHOLD_TEST_DEFAULT,
)


def run_analysis(
    root_file: str,
    base_dir: str,
    status_var: tk.StringVar,
    ref_var: tk.StringVar,
    test_var: tk.StringVar,
    window_var: tk.StringVar,
    button: tk.Button,
    running_processes: dict[str, subprocess.Popen],
    output_queue: queue.Queue[str],
) -> None:
    script_path = os.path.join(base_dir, "timeCorrsSearch.py")
    if not os.path.isfile(script_path):
        messagebox.showerror("Missing script", f"Cannot find {script_path}")
        return

    if root_file in running_processes and running_processes[root_file].poll() is None:
        status_var.set(f"Already running: {os.path.basename(root_file)}")
        return

    try:
        ref = float(ref_var.get().strip())
        test = float(test_var.get().strip())
        window = float(window_var.get().strip())
    except ValueError:
        messagebox.showerror("Invalid settings", "Thresholds and time window must be numeric.")
        return
    if not all(math.isfinite(value) for value in (ref, test, window)) or window <= 0:
        messagebox.showerror(
            "Invalid settings", "Thresholds must be finite and the time window finite and positive."
        )
        return

    command = [
        sys.executable, script_path, root_file,
        "--crosshit-threshold-ref", str(ref),
        "--crosshit-threshold-test", str(test),
        "--crosshit-window-ns", str(window),
    ]
    try:
        process = launch_with_output(command, base_dir, output_queue, os.path.basename(root_file))
    except OSError as exc:
        messagebox.showerror("Launch failed", f"Could not launch analysis:\n{exc}")
        return

    running_processes[root_file] = process
    button.configure(bg=BUTTON_RUNNING_BG)
    status_var.set(
        f"Running: {os.path.basename(root_file)} "
        f"(ref ADC >= {ref:g}, test ADC >= {test:g}, window {window:g} ns)"
    )


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = discover_root_files(base_dir)

    root = tk.Tk()
    root.title("runCorrs")
    root.geometry("1000x1600")

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=(8, 2))
    left_logo = load_logo(root, os.path.join(base_dir, "share", "logo_combined_small_new_0.png"))
    right_logo = load_logo(root, os.path.join(base_dir, "share", "hk_logo.jpg"))
    tk.Label(top_frame, image=left_logo).pack(side="left", anchor="n")
    tk.Label(top_frame, image=right_logo).pack(side="right", anchor="n")
    center_frame = tk.Frame(top_frame)
    center_frame.pack(side="left", fill="both", expand=True)
    tk.Label(center_frame, text="Joint Laboratory of Optics, Palacký University, Olomouc").pack(expand=True)

    tk.Label(
        root,
        text="Select ROOT file (newest TESTER_0_pmt_test_2026* dates first):",
        anchor="w",
        font=("TkDefaultFont", 11, "bold"),
    ).pack(fill="x", padx=10, pady=(2, 6))
    tk.Label(
        root,
        text="Cross-channel coincidence analysis using timeCorrsSearch.py",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(0, 6))

    controls = tk.Frame(root)
    controls.pack(fill="x", padx=10, pady=(0, 6))
    ref_var = tk.StringVar(value=str(CROSSHIT_THRESHOLD_REF_DEFAULT))
    test_var = tk.StringVar(value=str(CROSSHIT_THRESHOLD_TEST_DEFAULT))
    window_var = tk.StringVar(value=str(COINCIDENCE_WINDOW_NS_DEFAULT))
    for label, variable in (
        ("Ref ADC threshold:", ref_var),
        ("Test ADC threshold:", test_var),
        ("Full window (ns):", window_var),
    ):
        tk.Label(controls, text=label).pack(side="left", padx=(0, 4))
        tk.Entry(controls, textvariable=variable, width=8).pack(side="left", padx=(0, 12))
    tk.Button(controls, text="Exit", bg=EXIT_BUTTON_BG, command=root.destroy).pack(side="right")

    status_var = tk.StringVar(value="Ready.")
    tk.Label(root, textvariable=status_var, anchor="w", fg="navy").pack(
        fill="x", padx=10, pady=(0, 8)
    )

    tk.Label(root, text="2026 (c) Jiří Kvita, Adam Jüttner, Vladimír Urbášek").pack(
        side="bottom", fill="x", padx=10, pady=(0, 5)
    )
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
    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    frame_window = canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(frame_window, width=event.width))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))

    running_processes: dict[str, subprocess.Popen] = {}
    buttons_by_path: dict[str, tk.Button] = {}
    if not files:
        tk.Label(
            frame, text="No matching ROOT files found from September 2026 onwards.",
            fg="darkred", anchor="w",
        ).pack(fill="x", padx=10, pady=10)
    for label, path in files:
        button = tk.Button(
            frame, text=label, anchor="w", bg=BUTTON_IDLE_BG,
            command=lambda p=path: run_analysis(
                p, base_dir, status_var, ref_var, test_var, window_var,
                buttons_by_path[p], running_processes, output_queue,
            ),
        )
        button.pack(fill="x", padx=8, pady=3)
        buttons_by_path[path] = button

    def refresh_running_state() -> None:
        finished = [path for path, process in running_processes.items() if process.poll() is not None]
        for path in finished:
            returncode = running_processes.pop(path).returncode
            buttons_by_path[path].configure(bg=BUTTON_IDLE_BG)
            if returncode == 0:
                status_var.set(f"Finished: {os.path.basename(path)}")
            else:
                status_var.set(f"Failed ({returncode}): {os.path.basename(path)}; see output")
        root.after(1000, refresh_running_state)

    root.after(1000, refresh_running_state)
    root.mainloop()


if __name__ == "__main__":
    main()
