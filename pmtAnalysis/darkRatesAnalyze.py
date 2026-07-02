#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


#TARGET_CHANNELS = ["1", "2", "3", "5", "8"]
TARGET_CHANNELS = ["1", "2", "3", "4", "5", "6"]


def _iter_timestamp_channel_nodes(obj: Any):
	"""Yield dicts that contain both timestamp and channels keys."""
	if isinstance(obj, dict):
		if "timestamp" in obj and "channels" in obj and isinstance(obj["channels"], dict):
			yield obj
		for value in obj.values():
			yield from _iter_timestamp_channel_nodes(value)
	elif isinstance(obj, list):
		for item in obj:
			yield from _iter_timestamp_channel_nodes(item)


def extract_rmon_series(data: Any, channels: list[str]) -> dict[str, list[tuple[datetime, float]]]:
	series: dict[str, list[tuple[datetime, float]]] = {ch: [] for ch in channels}

	for node in _iter_timestamp_channel_nodes(data):
		timestamp_raw = node.get("timestamp")
		if not isinstance(timestamp_raw, str):
			continue

		try:
			ts = datetime.fromisoformat(timestamp_raw)
		except ValueError:
			continue

		channels_dict = node.get("channels", {})
		for ch in channels:
			ch_data = channels_dict.get(ch)
			if not isinstance(ch_data, dict):
				continue
			r_mon = ch_data.get("r_mon")
			if isinstance(r_mon, (int, float)):
				series[ch].append((ts, float(r_mon)))

	for ch in channels:
		series[ch].sort(key=lambda item: item[0])

	return series


def plot_rmon(series: dict[str, list[tuple[datetime, float]]], output_file: Path) -> None:
	plt.figure(figsize=(11, 5))

	has_points = False
	for ch in TARGET_CHANNELS:
		points = series.get(ch, [])
		if not points:
			continue
		has_points = True
		x = [t for t, _ in points]
		y = [math.log1p(v) for _, v in points]
		plt.plot(x, y, marker="o", markersize=2, linewidth=1.2, alpha=0.4, label=f"Ch {ch}")

	if not has_points:
		raise RuntimeError("No r_mon data found for requested channels.")

	plt.title("Dark Rates log(1 + r_mon) vs Time")
	plt.xlabel("Timestamp")
	plt.ylabel("log(1 + r_mon [Hz])")
	plt.ylim(5, 11)
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def _series_to_timestamp_map(points: list[tuple[datetime, float]]) -> dict[datetime, float]:
	return {timestamp: value for timestamp, value in points}


def plot_pairwise_scatter_grid(series: dict[str, list[tuple[datetime, float]]], output_file: Path) -> None:
	pairs: list[tuple[str, str, list[float], list[float]]] = []

	for i, ch_x in enumerate(TARGET_CHANNELS):
		for ch_y in TARGET_CHANNELS[i + 1 :]:
			map_x = _series_to_timestamp_map(series.get(ch_x, []))
			map_y = _series_to_timestamp_map(series.get(ch_y, []))
			common_ts = sorted(set(map_x.keys()) & set(map_y.keys()))

			x_vals = [map_x[ts] for ts in common_ts]
			y_vals = [map_y[ts] for ts in common_ts]

			if x_vals and y_vals:
				pairs.append((ch_x, ch_y, x_vals, y_vals))

	if not pairs:
		raise RuntimeError("No overlapping timestamp data for pairwise scatter plots.")

	n_pairs = len(pairs)
	n_cols = min(4, n_pairs)
	n_rows = math.ceil(n_pairs / n_cols)

	fig, axes = plt.subplots(n_rows, n_cols, figsize=(4.2 * n_cols, 3.8 * n_rows), squeeze=False)

	for idx, (ch_x, ch_y, x_vals, y_vals) in enumerate(pairs):
		row = idx // n_cols
		col = idx % n_cols
		ax = axes[row][col]
		x_vals_log = [math.log1p(v) for v in x_vals]
		y_vals_log = [math.log1p(v) for v in y_vals]
		ax.scatter(x_vals_log, y_vals_log, s=10, alpha=0.4)
		ax.set_title(f"Ch {ch_x} vs Ch {ch_y}")
		ax.set_xlabel(f"log(1 + Ch {ch_x} r_mon [Hz])")
		ax.set_ylabel(f"log(1 + Ch {ch_y} r_mon [Hz])")
		ax.set_xlim(5, 11)
		ax.set_ylim(5, 11)
		ax.grid(True, linestyle="--", alpha=0.35)

	for idx in range(n_pairs, n_rows * n_cols):
		row = idx // n_cols
		col = idx % n_cols
		axes[row][col].axis("off")

	fig.suptitle("Pairwise Dark Rate Correlations in log(1 + r_mon)", y=1.02)
	fig.tight_layout()
	fig.savefig(output_file, dpi=150, bbox_inches="tight")


def plot_fft_rate_histograms(series: dict[str, list[tuple[datetime, float]]], output_file: Path) -> None:
	plt.figure(figsize=(11, 5))

	has_points = False
	for ch in TARGET_CHANNELS:
		rate_values = [rate for _, rate in series.get(ch, [])]
		if len(rate_values) < 2:
			continue

		hist_counts, _ = np.histogram(rate_values, bins=64)
		centered_counts = hist_counts.astype(float) - np.mean(hist_counts)
		fft_vals = np.fft.rfft(centered_counts)
		freqs = np.fft.rfftfreq(centered_counts.size, d=1.0)
		amplitude = np.abs(fft_vals)

		if freqs.size <= 1:
			continue

		has_points = True
		plt.plot(freqs[1:], amplitude[1:], linewidth=1.2, alpha=0.8, label=f"Ch {ch}")

	if not has_points:
		raise RuntimeError("Insufficient data to compute FFT of 1D rate histograms.")

	plt.title("FFT Magnitude of 1D Rate Histograms")
	plt.xlabel("Frequency (1/bin)")
	plt.ylabel("Magnitude")
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def _spike_centers_from_runs(points: list[tuple[datetime, float]], threshold: float) -> list[datetime]:
	centers: list[datetime] = []
	run_start: datetime | None = None
	run_end: datetime | None = None

	for ts, rate in points:
		if rate > threshold:
			if run_start is None:
				run_start = ts
			run_end = ts
			continue

		if run_start is not None and run_end is not None:
			centers.append(run_start + (run_end - run_start) / 2)
			run_start = None
			run_end = None

	if run_start is not None and run_end is not None:
		centers.append(run_start + (run_end - run_start) / 2)

	return centers


def plot_spike_delta_histograms(series: dict[str, list[tuple[datetime, float]]], output_file: Path) -> None:
	plt.figure(figsize=(11, 5))

	alpha = 1.0 / len(TARGET_CHANNELS)
	has_data = False
	for ch in TARGET_CHANNELS:
		spike_times = _spike_centers_from_runs(series.get(ch, []), threshold=3000.0)
		if len(spike_times) < 2:
			continue

		delta_seconds = [
			(spike_times[idx] - spike_times[idx - 1]).total_seconds()
			for idx in range(1, len(spike_times))
		]
		if not delta_seconds:
			continue

		has_data = True
		plt.hist(delta_seconds, bins=50, alpha=alpha, label=f"Ch {ch}")

	if not has_data:
		# Keep the analysis flow running even when no spike deltas are available.
		plt.title("Histogram of Consecutive Spike-Center Time Differences (r_mon > 3000)")
		plt.xlabel("Time Difference Between Consecutive Spikes [s]")
		plt.ylabel("Count")
		plt.text(
			0.5,
			0.5,
			"No consecutive spikes found for threshold r_mon > 3000.",
			ha="center",
			va="center",
			transform=plt.gca().transAxes,
		)
		plt.grid(True, linestyle="--", alpha=0.35)
		plt.tight_layout()
		plt.savefig(output_file, dpi=150)
		return

	plt.title("Histogram of Consecutive Spike-Center Time Differences (r_mon > 3000)")
	plt.xlabel("Time Difference Between Consecutive Spikes [s]")
	plt.ylabel("Count")
	plt.grid(True, linestyle="--", alpha=0.35)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Read test results JSON and plot r_mon dark rates for selected channels."
	)
	parser.add_argument(
		"input",
		type=Path,
		help="Input JSON file path (first positional argument)",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=Path("dark_rates_r_mon_channels_1_2_3_5_8.png"),
		help="Output plot PNG path",
	)
	parser.add_argument(
		"--scatter-output",
		type=Path,
		default=Path("dark_rates_pairwise_scatter_channels_1_2_3_5_8.png"),
		help="Output pairwise scatter-grid PNG path",
	)
	parser.add_argument(
		"--fft-output",
		type=Path,
		default=Path("dark_rates_fft_hist_channels_1_2_3_5_8.png"),
		help="Output FFT-of-histograms PNG path",
	)
	parser.add_argument(
		"--spike-dt-output",
		type=Path,
		default=Path("dark_rates_spike_dt_hist_channels_1_2_3_5_8.png"),
		help="Output histogram of consecutive spike time differences PNG path",
	)
	args = parser.parse_args()
	output_dir = args.input.parent / args.input.stem
	output_dir.mkdir(parents=True, exist_ok=True)

	def to_output_path(path: Path) -> Path:
		resolved = path if path.is_absolute() else output_dir / path
		resolved.parent.mkdir(parents=True, exist_ok=True)
		return resolved

	output_path = to_output_path(args.output)
	scatter_output_path = to_output_path(args.scatter_output)
	fft_output_path = to_output_path(args.fft_output)
	spike_dt_output_path = to_output_path(args.spike_dt_output)

	with args.input.open("r", encoding="utf-8") as f:
		data = json.load(f)

	series = extract_rmon_series(data, TARGET_CHANNELS)
	plot_rmon(series, output_path)
	plot_pairwise_scatter_grid(series, scatter_output_path)
	plot_fft_rate_histograms(series, fft_output_path)
	plot_spike_delta_histograms(series, spike_dt_output_path)
	plt.show()
	print(f"Saved plot to: {output_path}")
	print(f"Saved scatter grid to: {scatter_output_path}")
	print(f"Saved FFT histogram plot to: {fft_output_path}")
	print(f"Saved spike delta histogram plot to: {spike_dt_output_path}")


if __name__ == "__main__":
	main()
