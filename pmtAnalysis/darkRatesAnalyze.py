#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


TARGET_CHANNELS = ["1", "2", "3", "5", "8"]


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
	plt.figure(figsize=(11, 6))

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
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)
	plt.show()


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
		ax.scatter(x_vals, y_vals, s=10, alpha=0.4)
		ax.set_title(f"Ch {ch_x} vs Ch {ch_y}")
		ax.set_xlabel(f"Ch {ch_x} r_mon [Hz]")
		ax.set_ylabel(f"Ch {ch_y} r_mon [Hz]")
		ax.grid(True, linestyle="--", alpha=0.35)

	for idx in range(n_pairs, n_rows * n_cols):
		row = idx // n_cols
		col = idx % n_cols
		axes[row][col].axis("off")

	fig.suptitle("Pairwise Dark Rate Correlations", y=1.02)
	fig.tight_layout()
	fig.savefig(output_file, dpi=150, bbox_inches="tight")
	plt.show()


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Read test results JSON and plot r_mon dark rates for selected channels."
	)
	parser.add_argument(
		"--input",
		type=Path,
		default=Path("test_results_20260619_150727.json"),
		help="Input JSON file path",
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
	args = parser.parse_args()

	with args.input.open("r", encoding="utf-8") as f:
		data = json.load(f)

	series = extract_rmon_series(data, TARGET_CHANNELS)
	plot_rmon(series, args.output)
	plot_pairwise_scatter_grid(series, args.scatter_output)
	print(f"Saved plot to: {args.output}")
	print(f"Saved scatter grid to: {args.scatter_output}")


if __name__ == "__main__":
	main()
