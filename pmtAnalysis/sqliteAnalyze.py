#!/usr/bin/env python3
"""Analyze and plot PMT monitor data from a SQLite database.

Focuses on plotting `rate_hz` for channels 1..6 over time.
"""

from __future__ import annotations

import argparse
import csv
import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt


@dataclass
class Reading:
	ts: datetime
	channel: int
	rate_hz: float


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Analyze and plot channel rates from monitor SQLite data"
	)
	parser.add_argument(
		"--db",
		type=Path,
		default=Path("Sqlite/20260707/158.194.88.101_monitor.sqlite"),
		help="Path to monitor SQLite DB",
	)
	parser.add_argument(
		"--outdir",
		type=Path,
		default=Path("plots/20260707"),
		help="Directory where figures and summary CSV are written",
	)
	parser.add_argument(
		"--start",
		type=str,
		default=None,
		help="Optional start timestamp filter (ISO format)",
	)
	parser.add_argument(
		"--end",
		type=str,
		default=None,
		help="Optional end timestamp filter (ISO format)",
	)
	parser.add_argument(
		"--peak-threshold",
		type=float,
		default=3000.0,
		help="Rate threshold [Hz] above which points are treated as a peak run",
	)
	parser.add_argument(
		"--peak-dt-bins",
		type=int,
		default=200,
		help="Number of bins for consecutive peak time-distance histogram",
	)
	parser.add_argument(
		"--log-scale",
		action="store_true",
		help="Plot rates as log(1 + rate). Default is linear rate.",
	)
	parser.add_argument(
		"--max-rate",
		type=float,
		default=3_000.0,
		help="Upper y-axis limit in Hz for rate plots (before optional log transform)",
	)
	parser.add_argument(
		"--rates-alpha",
		type=float,
		default=0.35,
		help="Alpha transparency for channel rate plots",
	)
	parser.add_argument(
		"--full-range",
		action="store_true",
		help="Disable default zoom and show full time range in rate plots",
	)
	parser.add_argument(
		"--pairwise-alpha",
		type=float,
		default=0.35,
		help="Alpha transparency for pairwise channel-correlation scatter points",
	)
	return parser.parse_args()


def parse_timestamp(value: str | None) -> datetime | None:
	if value is None:
		return None
	try:
		return datetime.fromisoformat(value)
	except ValueError as exc:
		raise ValueError(f"Invalid ISO timestamp: {value}") from exc


def load_readings(
	db_path: Path,
	channels: tuple[int, ...],
	start: datetime | None,
	end: datetime | None,
) -> list[Reading]:
	placeholders = ", ".join("?" for _ in channels)
	query = f"""
		SELECT ts, channel, rate_hz
		FROM readings
		WHERE channel IN ({placeholders})
		  AND rate_hz IS NOT NULL
	"""
	params: list[object] = list(channels)

	if start is not None:
		query += " AND ts >= ?"
		params.append(start.isoformat(sep=" "))
	if end is not None:
		query += " AND ts <= ?"
		params.append(end.isoformat(sep=" "))

	query += " ORDER BY ts, channel"

	with sqlite3.connect(db_path) as conn:
		rows = conn.execute(query, params).fetchall()

	readings: list[Reading] = []
	for ts_raw, channel, rate_hz in rows:
		try:
			ts = datetime.fromisoformat(str(ts_raw))
		except ValueError:
			# Keep parser robust if timestamps include trailing Z.
			ts = datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
		readings.append(Reading(ts=ts, channel=int(channel), rate_hz=float(rate_hz)))
	return readings


def build_channel_series(readings: list[Reading]) -> dict[int, tuple[list[datetime], list[float]]]:
	series: dict[int, tuple[list[datetime], list[float]]] = {
		ch: ([], []) for ch in range(1, 7)
	}
	for reading in readings:
		xs, ys = series[reading.channel]
		xs.append(reading.ts)
		ys.append(reading.rate_hz)
	return series


def write_summary_csv(out_csv: Path, series: dict[int, tuple[list[datetime], list[float]]]) -> None:
	out_csv.parent.mkdir(parents=True, exist_ok=True)
	with out_csv.open("w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow([
			"channel",
			"samples",
			"min_rate_hz",
			"max_rate_hz",
			"mean_rate_hz",
			"median_rate_hz",
		])
		for ch in range(1, 7):
			_, ys = series[ch]
			if not ys:
				writer.writerow([ch, 0, "", "", "", ""])
				continue
			writer.writerow(
				[
					ch,
					len(ys),
					min(ys),
					max(ys),
					sum(ys) / len(ys),
					median(ys),
				]
			)


def _last_all_positive_interval(
	series: dict[int, tuple[list[datetime], list[float]]],
) -> tuple[datetime, datetime] | None:
	maps: dict[int, dict[datetime, float]] = {}
	for ch in range(1, 7):
		xs, ys = series[ch]
		if not xs:
			return None
		maps[ch] = {ts: rate for ts, rate in zip(xs, ys, strict=True)}

	common_ts: set[datetime] | None = None
	for ch in range(1, 7):
		ch_ts = set(maps[ch].keys())
		common_ts = ch_ts if common_ts is None else common_ts & ch_ts

	if not common_ts:
		return None

	timestamps = sorted(common_ts)
	flags = [all(maps[ch][ts] > 0.0 for ch in range(1, 7)) for ts in timestamps]

	end_idx: int | None = None
	for i in range(len(flags) - 1, -1, -1):
		if flags[i]:
			end_idx = i
			break

	if end_idx is None:
		return None

	start_idx = end_idx
	while start_idx > 0 and flags[start_idx - 1]:
		start_idx -= 1

	return timestamps[start_idx], timestamps[end_idx]


def _filter_series_to_interval(
	series: dict[int, tuple[list[datetime], list[float]]],
	start_ts: datetime,
	end_ts: datetime,
) -> dict[int, tuple[list[datetime], list[float]]]:
	filtered: dict[int, tuple[list[datetime], list[float]]] = {}
	for ch in range(1, 7):
		xs, ys = series[ch]
		xs_out: list[datetime] = []
		ys_out: list[float] = []
		for ts, rate in zip(xs, ys, strict=True):
			if start_ts <= ts <= end_ts:
				xs_out.append(ts)
				ys_out.append(rate)
		filtered[ch] = (xs_out, ys_out)
	return filtered


def _moving_average(values: list[float], window: int) -> list[float]:
	if window <= 1 or len(values) < window:
		return values[:]

	prefix = [0.0]
	for value in values:
		prefix.append(prefix[-1] + value)

	half = window // 2
	out: list[float] = []
	for i in range(len(values)):
		start = max(0, i - half)
		end = min(len(values), start + window)
		start = max(0, end - window)
		total = prefix[end] - prefix[start]
		out.append(total / (end - start))
	return out


def _series_to_timestamp_map(points: list[tuple[datetime, float]]) -> dict[datetime, float]:
	return {timestamp: value for timestamp, value in points}


def plot_pairwise_scatter_grid(
	out_png: Path,
	series: dict[int, tuple[list[datetime], list[float]]],
	log_scale: bool,
	max_rate_hz: float,
	pairwise_alpha: float,
) -> None:
	out_png.parent.mkdir(parents=True, exist_ok=True)

	channels = list(range(1, 7))
	pairs: list[tuple[int, int, list[float], list[float]]] = []

	for i, ch_x in enumerate(channels):
		for ch_y in channels[i + 1 :]:
			map_x = _series_to_timestamp_map(list(zip(series[ch_x][0], series[ch_x][1], strict=True)))
			map_y = _series_to_timestamp_map(list(zip(series[ch_y][0], series[ch_y][1], strict=True)))
			common_ts = sorted(set(map_x.keys()) & set(map_y.keys()))

			x_vals = [map_x[ts] for ts in common_ts]
			y_vals = [map_y[ts] for ts in common_ts]

			if x_vals and y_vals:
				pairs.append((ch_x, ch_y, x_vals, y_vals))

	if not pairs:
		raise RuntimeError("No overlapping timestamp data for pairwise channel-correlation plots.")

	n_pairs = len(pairs)
	n_cols = min(4, n_pairs)
	n_rows = math.ceil(n_pairs / n_cols)

	fig, axes = plt.subplots(n_rows, n_cols, figsize=(4.2 * n_cols, 3.8 * n_rows), squeeze=False)
	palette = plt.cm.get_cmap("tab20", max(1, n_pairs))

	pairwise_alpha = max(0.0, min(1.0, pairwise_alpha))
	xy_max = math.log1p(max_rate_hz) if log_scale else max_rate_hz
	xy_min = 5.0 if log_scale else 0.0
	xlabel_prefix = "log(1 + " if log_scale else ""
	xlabel_suffix = ")" if log_scale else ""

	for idx, (ch_x, ch_y, x_vals, y_vals) in enumerate(pairs):
		row = idx // n_cols
		col = idx % n_cols
		ax = axes[row][col]

		x_vals_plot = [math.log1p(v) for v in x_vals] if log_scale else x_vals
		y_vals_plot = [math.log1p(v) for v in y_vals] if log_scale else y_vals

		ax.scatter(
			x_vals_plot,
			y_vals_plot,
			s=10,
			alpha=pairwise_alpha,
			color=palette(idx),
		)
		ax.set_title(f"CH{ch_x} vs CH{ch_y}")
		ax.set_xlabel(f"{xlabel_prefix}CH{ch_x} rate_hz{xlabel_suffix}")
		ax.set_ylabel(f"{xlabel_prefix}CH{ch_y} rate_hz{xlabel_suffix}")
		ax.set_xlim(xy_min, xy_max)
		ax.set_ylim(xy_min, xy_max)
		ax.grid(True, linestyle="--", alpha=0.35)

	for idx in range(n_pairs, n_rows * n_cols):
		row = idx // n_cols
		col = idx % n_cols
		axes[row][col].axis("off")

	title_prefix = "log(1 + rate_hz)" if log_scale else "rate_hz"
	fig.suptitle(f"Pairwise Channel Correlations ({title_prefix})", y=1.02)
	fig.tight_layout()
	fig.savefig(out_png, dpi=180, bbox_inches="tight")


def plot_rates(
	out_png: Path,
	series: dict[int, tuple[list[datetime], list[float]]],
	log_scale: bool,
	max_rate_hz: float,
	rates_alpha: float,
	full_range: bool,
) -> tuple[datetime, datetime] | None:
	out_png.parent.mkdir(parents=True, exist_ok=True)
	fig, (ax_ts, ax_dist) = plt.subplots(2, 1, figsize=(14, 10), constrained_layout=True)
	y_max = math.log1p(max_rate_hz) if log_scale else max_rate_hz
	y_min = 5.0 if log_scale else 0.0
	ylabel = "log(1 + Rate [Hz])" if log_scale else "Rate [Hz]"
	title_prefix = "log(1 + Rate)" if log_scale else "Rate"
	box_data: list[list[float]] = []
	labels: list[str] = []
	rates_alpha = max(0.0, min(1.0, rates_alpha))
	zoom_interval: tuple[datetime, datetime] | None = None
	plot_series = series

	if not full_range:
		zoom_interval = _last_all_positive_interval(series)
		if zoom_interval is not None:
			start_ts, end_ts = zoom_interval
			plot_series = _filter_series_to_interval(series, start_ts, end_ts)

	for ch in range(1, 7):
		xs, ys = plot_series[ch]
		if xs:
			ys_plot = [math.log1p(v) for v in ys] if log_scale else ys
			ax_ts.plot(
				xs,
				ys_plot,
				marker=".",
				linewidth=1.0,
				markersize=2.0,
				alpha=rates_alpha,
				label=f"CH{ch}",
			)

			box_data.append(ys_plot)
			labels.append(f"CH{ch}")

	ax_ts.set_title(f"{title_prefix} vs Time (Channels 1-6)")
	ax_ts.set_xlabel("Timestamp")
	ax_ts.set_ylabel(ylabel)
	ax_ts.set_ylim(y_min, y_max)
	if zoom_interval is not None:
		ax_ts.set_xlim(zoom_interval[0], zoom_interval[1])
	ax_ts.grid(True, alpha=0.3)
	ax_ts.legend(ncol=3)

	if box_data:
		bp = ax_dist.boxplot(box_data, labels=labels, showfliers=False, patch_artist=True)
		for patch in bp["boxes"]:
			patch.set_alpha(rates_alpha)
	ax_dist.set_title(f"{title_prefix} Distribution by Channel")
	ax_dist.set_xlabel("Channel")
	ax_dist.set_ylabel(ylabel)
	ax_dist.set_ylim(y_min, y_max)
	ax_dist.grid(True, axis="y", alpha=0.3)

	fig.savefig(out_png, dpi=180)
	return zoom_interval


def plot_rates_moving_average(
	out_png: Path,
	series: dict[int, tuple[list[datetime], list[float]]],
	log_scale: bool,
	max_rate_hz: float,
	window: int = 20,
) -> None:
	out_png.parent.mkdir(parents=True, exist_ok=True)
	fig, ax = plt.subplots(1, 1, figsize=(14, 6), constrained_layout=True)

	y_max = math.log1p(max_rate_hz) if log_scale else max_rate_hz
	y_min = 5.0 if log_scale else 0.0
	ylabel = "log(1 + Rate [Hz])" if log_scale else "Rate [Hz]"
	title_prefix = "log(1 + Rate)" if log_scale else "Rate"

	for ch in range(1, 7):
		xs, ys = series[ch]
		if not xs:
			continue
		ys_avg_raw = _moving_average(ys, window=window)
		ys_avg = [math.log1p(v) for v in ys_avg_raw] if log_scale else ys_avg_raw
		ax.plot(xs, ys_avg, linewidth=2.0, label=f"CH{ch} avg{window}")

	ax.set_title(f"{title_prefix} Moving Average (window={window}) vs Time")
	ax.set_xlabel("Timestamp")
	ax.set_ylabel(ylabel)
	ax.set_ylim(y_min, y_max)
	ax.grid(True, alpha=0.3)
	ax.legend(ncol=3)

	fig.savefig(out_png, dpi=180)


def _peak_centers_from_runs(
	points: list[tuple[datetime, float]],
	threshold: float,
) -> list[datetime]:
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


def plot_peak_time_distance_hist(
	out_png: Path,
	series: dict[int, tuple[list[datetime], list[float]]],
	threshold: float,
	bins: int,
) -> None:
	out_png.parent.mkdir(parents=True, exist_ok=True)
	plt.figure(figsize=(14, 6))

	all_peaks: list[tuple[datetime, int]] = []
	for ch in range(1, 7):
		xs, ys = series[ch]
		points = list(zip(xs, ys, strict=True))
		for peak_time in _peak_centers_from_runs(points, threshold=threshold):
			all_peaks.append((peak_time, ch))

	all_peaks.sort(key=lambda item: item[0])

	delta_seconds: list[float] = []
	for i in range(1, len(all_peaks)):
		prev_ts, prev_ch = all_peaks[i - 1]
		curr_ts, curr_ch = all_peaks[i]
		if prev_ch == curr_ch:
			continue
		delta_seconds.append((curr_ts - prev_ts).total_seconds())

	has_data = bool(delta_seconds)
	if has_data:
		plt.hist(delta_seconds, bins=bins, alpha=0.7, color="tab:blue")

	plt.title(f"Inter-Channel Consecutive Peak-Center Time Differences (rate_hz > {threshold:.1f})")
	plt.xlabel("Time Difference Between Consecutive Peaks [s]")
	plt.xlim(-1_000., 19_000.)	
	plt.ylabel("Count")
	plt.grid(True, linestyle="--", alpha=0.15)

	if not has_data:
		plt.text(
			0.5,
			0.5,
			f"No inter-channel consecutive peaks found for threshold rate_hz > {threshold:.1f}.",
			ha="center",
			va="center",
			transform=plt.gca().transAxes,
		)

	plt.tight_layout()
	plt.savefig(out_png, dpi=180)


def print_summary(series: dict[int, tuple[list[datetime], list[float]]]) -> None:
	print("Per-channel rate summary")
	print("channel,samples,min,max,mean,median")
	for ch in range(1, 7):
		_, ys = series[ch]
		if not ys:
			print(f"{ch},0,,,,")
			continue
		print(
			f"{ch},{len(ys)},{min(ys):.4f},{max(ys):.4f},"
			f"{(sum(ys) / len(ys)):.4f},{median(ys):.4f}"
		)


def main() -> None:
	args = parse_args()
	channels = (1, 2, 3, 4, 5, 6)

	start = parse_timestamp(args.start)
	end = parse_timestamp(args.end)

	readings = load_readings(args.db, channels, start, end)
	if not readings:
		raise SystemExit("No readings found for channels 1..6 in the selected range")

	series = build_channel_series(readings)
	analysis_series = series
	zoom_interval: tuple[datetime, datetime] | None = None
	if not args.full_range:
		zoom_interval = _last_all_positive_interval(series)
		if zoom_interval is not None:
			analysis_series = _filter_series_to_interval(series, zoom_interval[0], zoom_interval[1])

	print_summary(analysis_series)

	png_suffix = "_logy" if args.log_scale else ""
	rates_png = args.outdir / f"rate_channels_1_to_6{png_suffix}.png"
	rates_avg_png = args.outdir / f"rate_channels_1_to_6_avg20{png_suffix}.png"
	summary_csv = args.outdir / "rate_channels_1_to_6_summary.csv"
	peak_dt_png = args.outdir / f"rate_channels_1_to_6_peak_dt_hist{png_suffix}.png"
	pairwise_png = args.outdir / f"rate_channels_1_to_6_pairwise_scatter{png_suffix}.png"
	plot_rates(
		rates_png,
		analysis_series,
		log_scale=args.log_scale,
		max_rate_hz=args.max_rate,
		rates_alpha=args.rates_alpha,
		full_range=True,
	)
	plot_rates_moving_average(
		rates_avg_png,
		analysis_series,
		log_scale=args.log_scale,
		max_rate_hz=args.max_rate,
		window=20,
	)
	plot_peak_time_distance_hist(
		peak_dt_png,
		analysis_series,
		threshold=args.peak_threshold,
		bins=args.peak_dt_bins,
	)
	plot_pairwise_scatter_grid(
		pairwise_png,
		analysis_series,
		log_scale=args.log_scale,
		max_rate_hz=args.max_rate,
		pairwise_alpha=args.pairwise_alpha,
	)
	write_summary_csv(summary_csv, analysis_series)

	print(f"Saved plot: {rates_png}")
	print(f"Saved moving-average plot: {rates_avg_png}")
	if zoom_interval is not None:
		print(f"Applied default zoom range: {zoom_interval[0]} -> {zoom_interval[1]}")
	elif not args.full_range:
		print("Default zoom unavailable (no trailing all-positive interval found); using full range.")
	print(f"Saved peak dt histogram: {peak_dt_png}")
	print(f"Saved pairwise scatter grid: {pairwise_png}")
	print(f"Saved summary: {summary_csv}")

	plt.show()


if __name__ == "__main__":
	main()
