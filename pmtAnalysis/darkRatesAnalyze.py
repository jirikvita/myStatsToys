#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np


LOG_AXIS_MIN = 5.0
LOG_AXIS_MAX = 12.5
SPIKE_THRESHOLD = 3000.0


# Keep widget objects alive for the lifetime of the UI.
_UI_CONTROLS: list[Any] = []


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


def detect_channels_with_data(data: Any) -> list[str]:
	detected: set[str] = set()
	for node in _iter_timestamp_channel_nodes(data):
		channels_dict = node.get("channels", {})
		if not isinstance(channels_dict, dict):
			continue
		for ch, ch_data in channels_dict.items():
			if not isinstance(ch_data, dict):
				continue
			r_mon = ch_data.get("r_mon")
			if isinstance(r_mon, (int, float)):
				detected.add(str(ch))

	# Sort numerically when possible, then lexicographically as fallback.
	def sort_key(value: str) -> tuple[int, float | str]:
		try:
			return (0, float(value))
		except ValueError:
			return (1, value)

	return sorted(detected, key=sort_key)


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


def plot_rmon(
	series: dict[str, list[tuple[datetime, float]]],
	channels: list[str],
	output_file: Path,
	use_log_scale: bool,
) -> None:
	plt.figure(figsize=(11, 5))

	has_points = False
	for ch in channels:
		points = series.get(ch, [])
		if not points:
			continue
		has_points = True
		x = [t for t, _ in points]
		y = [math.log1p(v) for _, v in points] if use_log_scale else [v for _, v in points]
		plt.plot(x, y, marker="o", markersize=2, linewidth=1.2, alpha=0.4, label=f"Ch {ch}")

	if not has_points:
		raise RuntimeError("No r_mon data found for requested channels.")

	title = "Dark Rates log(1 + r_mon) vs Time" if use_log_scale else "Dark Rates r_mon vs Time"
	plt.title(title)
	plt.xlabel("Timestamp")
	ylabel = "log(1 + r_mon [Hz])" if use_log_scale else "r_mon [Hz]"
	plt.ylabel(ylabel)
	if use_log_scale:
		plt.ylim(LOG_AXIS_MIN, LOG_AXIS_MAX)
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def _series_to_timestamp_map(points: list[tuple[datetime, float]]) -> dict[datetime, float]:
	return {timestamp: value for timestamp, value in points}


def plot_pairwise_scatter_grid(
	series: dict[str, list[tuple[datetime, float]]],
	channels: list[str],
	output_file: Path,
	use_log_scale: bool,
) -> None:
	pairs: list[tuple[str, str, list[float], list[float]]] = []

	for i, ch_x in enumerate(channels):
		for ch_y in channels[i + 1 :]:
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
	palette = plt.cm.get_cmap("tab20", max(1, n_pairs))

	for idx, (ch_x, ch_y, x_vals, y_vals) in enumerate(pairs):
		row = idx // n_cols
		col = idx % n_cols
		ax = axes[row][col]
		x_plot = [math.log1p(v) for v in x_vals] if use_log_scale else x_vals
		y_plot = [math.log1p(v) for v in y_vals] if use_log_scale else y_vals
		ax.scatter(
			x_plot,
			y_plot,
			s=10,
			alpha=0.45,
			color=palette(idx),
		)
		ax.set_title(f"Ch {ch_x} vs Ch {ch_y}")
		if use_log_scale:
			ax.set_xlabel(f"log(1 + Ch {ch_x} r_mon [Hz])")
			ax.set_ylabel(f"log(1 + Ch {ch_y} r_mon [Hz])")
			ax.set_xlim(LOG_AXIS_MIN, LOG_AXIS_MAX)
			ax.set_ylim(LOG_AXIS_MIN, LOG_AXIS_MAX)
		else:
			ax.set_xlabel(f"Ch {ch_x} r_mon [Hz]")
			ax.set_ylabel(f"Ch {ch_y} r_mon [Hz]")
		ax.grid(True, linestyle="--", alpha=0.35)

	for idx in range(n_pairs, n_rows * n_cols):
		row = idx // n_cols
		col = idx % n_cols
		axes[row][col].axis("off")

	title = (
		"Pairwise Dark Rate Correlations in log(1 + r_mon)"
		if use_log_scale
		else "Pairwise Dark Rate Correlations in r_mon"
	)
	fig.suptitle(title, y=1.02)
	fig.tight_layout()
	fig.savefig(output_file, dpi=150, bbox_inches="tight")


def plot_fft_rate_histograms(
	series: dict[str, list[tuple[datetime, float]]],
	channels: list[str],
	output_file: Path,
) -> None:
	plt.figure(figsize=(11, 5))

	has_points = False
	for ch in channels:
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


def count_spike_runs(points: list[tuple[datetime, float]], threshold: float) -> int:
	return len(_spike_centers_from_runs(points, threshold=threshold))


def plot_spike_delta_histograms(
	series: dict[str, list[tuple[datetime, float]]],
	channels: list[str],
	output_file: Path,
) -> None:
	plt.figure(figsize=(11, 5))

	alpha = 1.0 / len(channels)
	has_data = False
	for ch in channels:
		spike_times = _spike_centers_from_runs(series.get(ch, []), threshold=SPIKE_THRESHOLD)
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
		plt.title(f"Histogram of Consecutive Spike-Center Time Differences (r_mon > {int(SPIKE_THRESHOLD)})")
		plt.xlabel("Time Difference Between Consecutive Spikes [s]")
		plt.ylabel("Count")
		plt.text(
			0.5,
			0.5,
			f"No consecutive spikes found for threshold r_mon > {int(SPIKE_THRESHOLD)}.",
			ha="center",
			va="center",
			transform=plt.gca().transAxes,
		)
		plt.grid(True, linestyle="--", alpha=0.35)
		plt.tight_layout()
		plt.savefig(output_file, dpi=150)
		return

	plt.title(f"Histogram of Consecutive Spike-Center Time Differences (r_mon > {int(SPIKE_THRESHOLD)})")
	plt.xlabel("Time Difference Between Consecutive Spikes [s]")
	plt.ylabel("Count")
	plt.grid(True, linestyle="--", alpha=0.35)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def print_spike_counts_linear(
	series: dict[str, list[tuple[datetime, float]]],
	channels: list[str],
	threshold: float,
) -> None:
	print(f"Spike counts in linear scale (r_mon > {int(threshold)}):")
	total = 0
	for ch in channels:
		count = count_spike_runs(series.get(ch, []), threshold=threshold)
		total += count
		print(f"  Ch {ch}: {count}")
	print(f"  Total: {total}")


def add_exit_button() -> None:
	control_fig = plt.figure("Controls", figsize=(2.6, 1.2))
	control_fig.patch.set_facecolor("#ffe6e6")
	button_ax = control_fig.add_axes([0.12, 0.2, 0.76, 0.62])
	exit_button = Button(
		button_ax,
		"Exit",
		color="lightcoral",
		hovercolor="#ff6b6b",
	)
	exit_button.label.set_color("white")
	exit_button.label.set_fontweight("bold")
	_UI_CONTROLS.extend([control_fig, button_ax, exit_button])

	def _close_all(_event):
		plt.close("all")
		sys.exit(0)

	exit_button.on_clicked(_close_all)


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
	parser.add_argument(
		"--linear",
		action="store_true",
		help="Use linear r_mon scale for time and pairwise scatter plots (default is log(1 + r_mon)).",
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

	channels = detect_channels_with_data(data)
	if not channels:
		raise RuntimeError("No channels with numeric r_mon data were found in the input JSON.")
	print(f"Auto-detected channels with data: {', '.join(channels)}")

	series = extract_rmon_series(data, channels)
	use_log_scale = not args.linear
	plot_rmon(series, channels, output_path, use_log_scale=use_log_scale)
	plot_pairwise_scatter_grid(series, channels, scatter_output_path, use_log_scale=use_log_scale)
	plot_fft_rate_histograms(series, channels, fft_output_path)
	plot_spike_delta_histograms(series, channels, spike_dt_output_path)
	print_spike_counts_linear(series, channels, threshold=SPIKE_THRESHOLD)
	add_exit_button()
	plt.show()
	print(f"Saved plot to: {output_path}")
	print(f"Saved scatter grid to: {scatter_output_path}")
	print(f"Saved FFT histogram plot to: {fft_output_path}")
	print(f"Saved spike delta histogram plot to: {spike_dt_output_path}")


if __name__ == "__main__":
	main()
