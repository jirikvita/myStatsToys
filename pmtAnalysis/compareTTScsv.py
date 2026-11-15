#!/usr/bin/env python3
"""Compare TTS table CSVs for all ADC thresholds in one TESTER directory."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_csv(path: Path) -> tuple[float, dict[int, tuple[float | None, float | None]]]:
    """Read the threshold and per-channel FWHM values from an exported table."""
    measurements: dict[int, tuple[float | None, float | None]] = {}
    threshold: float | None = None
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"channel", "tts_before_ns", "tts_after_ns", "adc_threshold_cut_ge"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path}: missing required CSV columns: {', '.join(sorted(required))}")
        for line, row in enumerate(reader, start=2):
            try:
                channel = int(row["channel"])
                cut = float(row["adc_threshold_cut_ge"])
                before = float(row["tts_before_ns"]) if row["tts_before_ns"].strip() else None
                after = float(row["tts_after_ns"]) if row["tts_after_ns"].strip() else None
            except (TypeError, ValueError, AttributeError) as exc:
                raise ValueError(f"{path}:{line}: invalid channel, threshold or TTS value") from exc
            if not math.isfinite(cut) or any(
                value is not None and not math.isfinite(value) for value in (before, after)
            ):
                raise ValueError(f"{path}:{line}: threshold and TTS values must be finite")
            if threshold is not None and cut != threshold:
                raise ValueError(f"{path}:{line}: inconsistent ADC thresholds")
            if channel in measurements:
                raise ValueError(f"{path}:{line}: duplicate channel {channel}")
            threshold = cut
            measurements[channel] = (before, after)
    if threshold is None:
        raise ValueError(f"{path}: CSV contains no channel rows")
    return threshold, measurements


def plot_comparisons(directory: Path) -> list[plt.Figure]:
    """Plot before and after correction against channel for each ADC cut."""
    paths = sorted(directory.glob("tts_table_adc_ge_*.csv"))
    if not paths:
        raise ValueError(f"No TTS table CSVs found in {directory}")
    datasets = sorted(((*load_csv(path), path) for path in paths), key=lambda item: item[0])

    figures = []
    for index, title in enumerate(("TTS before time-walk correction", "TTS after time-walk correction")):
        fig, ax = plt.subplots(figsize=(9, 5))
        for threshold, measurements, path in datasets:
            channels = sorted(ch for ch, values in measurements.items() if values[index] is not None)
            if not channels:
                print(f"{path}: no {title.lower()} values; omitted from this plot.")
                continue
            values = [measurements[ch][index] for ch in channels]
            average = float(np.mean(values))
            ax.plot(channels, values, "o-", label=f"ADC ≥ {threshold:g}, mean = {average:.3f} ns")
        ax.set_title(f"{title} — {directory.name}")
        ax.set_xlabel("Channel")
        ax.set_ylabel("TTS FWHM [ns]")
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 3.5)
        ax.grid(True, linestyle="--", alpha=0.4)
        if ax.lines:
            ax.legend(loc="lower right")
        else:
            ax.text(0.5, 0.5, "No available values", transform=ax.transAxes, ha="center")
        fig.tight_layout()
        figures.append(fig)
    return figures


def save_comparisons(directory: Path, figures: list[plt.Figure]) -> None:
    """Save both comparison plots in the selected TESTER directory."""
    for fig, name in zip(figures, ("tts_comparison_before", "tts_comparison_after")):
        for extension in ("png", "pdf"):
            path = directory / f"{name}.{extension}"
            fig.savefig(path, dpi=150)
            print(f"Saved {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="TESTER directory containing TTS table CSVs")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")
    try:
        figures = plot_comparisons(args.directory)
        save_comparisons(args.directory, figures)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"CSV comparison failed: {exc}\n")
    plt.show()


if __name__ == "__main__":
    main()
