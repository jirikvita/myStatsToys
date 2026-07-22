#!/usr/bin/env python3
"""Per-channel ADC/time analysis of a `pmt_events` ROOT file.

For each channel found in the tree, this script produces:
  - an ADC histogram,
    - a pedestal-corrected ADC histogram,
  - a measurement-time histogram (pulses vs. time within the run),
    - a pedestal-corrected time-vs-ADC 2D histogram.

The per-pulse measurement time is reconstructed from the raw TDC branches:

    T = (pmt_time << 4) + tdc_start
    t_ns = T * 0.25

and the overall run duration is estimated as:

    measurement_time_s = (max(t_ns) - min(t_ns)) * 1e-9
"""

from __future__ import annotations

import argparse
import math
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.optimize import curve_fit
import uproot

try:
    import tkinter as tk
except ImportError:
    tk = None

DEFAULT_INPUT = "1pe_measurement/28cm/test_run_thr30_att825_20260629_141522.root"
TREE_NAME = "pmt_events"

# Nominal pulser frequency; adjust with --pulser-freq-hz if the run used a
# different setting.
PULSER_FREQ_HZ = 10_000

# Time unit used for the timing plots (the measurement-time histogram and the
# time-vs-ADC 2D histogram): "ns" (nanoseconds, raw time resolution) or "s"
# (seconds, i.e. measurement_time_s). Override with --time-unit.
DEFAULT_TIME_UNIT = "s"

# ADC axis limits used for both the 1D and 2D histograms.
ADC_RANGE = (250, 500)
ADC_HIST_BINS = (ADC_RANGE[1] - ADC_RANGE[0]) // 2  # 2 ADC counts per bin

# ADC axis limits for pedestal-corrected ADC plots.
ADC_CORRECTED_RANGE = (-100, 500)
ADC_CORRECTED_HIST_BINS = (ADC_CORRECTED_RANGE[1] - ADC_CORRECTED_RANGE[0]) // 2

# Boundary (in ADC counts) separating the pedestal peak from the 1 p.e. peak,
# and the initial sigma guesses used to seed each Gaussian fit.
PEAK_SPLIT_ADC = 325
PEAK1_INITIAL_SIGMA = 10
PEAK2_INITIAL_SIGMA = 35

# For channels whose overall ADC RMS is narrower than this, the initial fit
# sigmas above are scaled down before seeding the fits: the 1st peak's sigma
# is divided by NARROW_RMS_SIGMA_SCALE, and the 2nd peak's sigma is divided by
# NARROW_RMS_PEAK2_SIGMA_SCALE (a total factor, not on top of the 1st scale).
NARROW_RMS_THRESHOLD = 50
NARROW_RMS_SIGMA_SCALE = 1.5
NARROW_RMS_PEAK2_SIGMA_SCALE = 3.5

# Half-width (in ADC counts) of the fit window used for the 3rd fit: the
# valley (dip) between the two peaks. The window is asymmetric:
# [center - half_window, center + half_window/2]. The 1st-stage fit uses
# VALLEY_FIT_HALF_WINDOW around the histogram minimum; the 2nd-stage refit
# uses VALLEY_REFIT_HALF_WINDOW around the 1st-stage fitted minimum, unless
# the channel's ADC RMS exceeds WIDE_RMS_THRESHOLD, in which case the wider
# WIDE_RMS_VALLEY_REFIT_HALF_WINDOW is used instead. If the stage-1 fit fails,
# it is retried once with VALLEY_FALLBACK_HALF_WINDOW.
VALLEY_FIT_HALF_WINDOW = 5
VALLEY_REFIT_HALF_WINDOW = 5
WIDE_RMS_THRESHOLD = 70
WIDE_RMS_VALLEY_REFIT_HALF_WINDOW = 6
VALLEY_FALLBACK_HALF_WINDOW = 15


def gaussian(x: np.ndarray, amplitude: float, mean: float, sigma: float) -> np.ndarray:
    return amplitude * np.exp(-0.5 * ((x - mean) / sigma) ** 2)


def _adc_histogram(adc_ch: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Histogram ADC values with the standard ADC_HIST_BINS/ADC_RANGE binning.

    numpy's rightmost histogram bin is closed on both ends (unlike all other
    bins, which are half-open [lo, hi)), so entries exactly equal to
    ADC_RANGE[1] get folded into the last bin on top of its normal [lo, hi)
    contents. For channels whose 2nd peak is broad and close to ADC_RANGE[1]
    (e.g. channel 6), this can inflate the last bin enough to be mistaken for
    the true peak. Subtract the duplicate count so the last bin behaves like
    the others.
    """
    counts, edges = np.histogram(adc_ch, bins=ADC_HIST_BINS, range=ADC_RANGE)
    counts[-1] -= np.count_nonzero(adc_ch == ADC_RANGE[1])
    centers = 0.5 * (edges[:-1] + edges[1:])
    return counts, centers


def fit_gaussian_peak(
    adc_ch: np.ndarray,
    search_range: tuple[float, float],
    initial_sigma: float,
    n_sigma_window: float = 2,
    refit: bool = False,
) -> dict | None:
    """Find the tallest bin in `search_range` and fit a Gaussian around it.

    The fit window is restricted to +/- n_sigma_window * initial_sigma around
    the peak found in the search region. If `refit` is True, a second fit is
    performed in a window of +/- n_sigma_window * sigma_fit1 centered on the
    mean found by the first fit.
    """
    counts, centers = _adc_histogram(adc_ch)

    def _fit_window(center: float, sigma: float) -> tuple[np.ndarray, np.ndarray, tuple[float, float]]:
        lo = center - n_sigma_window * sigma
        hi = center + n_sigma_window * sigma
        mask = (centers >= lo) & (centers <= hi)
        return centers[mask], counts[mask], (lo, hi)

    region_mask = (centers >= search_range[0]) & (centers < search_range[1])
    if not np.any(region_mask):
        return None

    region_counts = counts[region_mask]
    region_centers = centers[region_mask]
    peak_idx = np.argmax(region_counts)
    peak_center = region_centers[peak_idx]
    peak_amplitude = region_counts[peak_idx]

    x, y, fit_range = _fit_window(peak_center, initial_sigma)
    if x.size < 3 or peak_amplitude <= 0:
        return None

    p0 = [peak_amplitude, peak_center, initial_sigma]
    try:
        popt, pcov = curve_fit(gaussian, x, y, p0=p0)
    except (RuntimeError, ValueError):
        return None

    perr = np.sqrt(np.diag(pcov))
    result = {
        "amplitude": popt[0],
        "mean": popt[1],
        "sigma": abs(popt[2]),
        "amplitude_err": perr[0],
        "mean_err": perr[1],
        "sigma_err": perr[2],
        "fit_range": fit_range,
    }

    if refit:
        x2, y2, fit_range2 = _fit_window(result["mean"], result["sigma"])
        if x2.size >= 3:
            p0_2 = [result["amplitude"], result["mean"], result["sigma"]]
            try:
                popt2, pcov2 = curve_fit(gaussian, x2, y2, p0=p0_2)
                perr2 = np.sqrt(np.diag(pcov2))
                result = {
                    "amplitude": popt2[0],
                    "mean": popt2[1],
                    "sigma": abs(popt2[2]),
                    "amplitude_err": perr2[0],
                    "mean_err": perr2[1],
                    "sigma_err": perr2[2],
                    "fit_range": fit_range2,
                }
            except (RuntimeError, ValueError):
                pass  # keep the first-stage fit if the refit doesn't converge

    return result


def parabola(x: np.ndarray, curvature: float, vertex: float, offset: float) -> np.ndarray:
    """Parabola: offset - curvature * (x - vertex)**2.

    `curvature` is constrained to be <= 0 so that the quadratic term is
    negative, which yields a valid valley (minimum at x=vertex, rising away
    from it) since offset - curvature*(x-vertex)**2 = offset + |curvature|*(x-vertex)**2.
    """
    return offset - curvature * (x - vertex) ** 2


def fit_valley(
    adc_ch: np.ndarray,
    search_range: tuple[float, float],
    half_window: float = VALLEY_FIT_HALF_WINDOW,
    refit_half_window: float = VALLEY_REFIT_HALF_WINDOW,
) -> dict | None:
    """Find the shallowest bin in `search_range` and fit a parabola around it.

    A 2-step iterative fit is performed: the first fit uses an asymmetric
    window of [center - half_window, center + half_window/2] around the
    minimum found in the histogram, and the second fit re-fits in the same
    asymmetric shape (using refit_half_window) centered on the 1st-found
    minimum (the vertex of the 1st fit).
    """
    counts, centers = _adc_histogram(adc_ch)

    def _fit_window(center: float, window: float) -> tuple[np.ndarray, np.ndarray, tuple[float, float]]:
        lo = center - window
        hi = center + window / 2
        mask = (centers >= lo) & (centers <= hi)
        return centers[mask], counts[mask], (lo, hi)

    region_mask = (centers >= search_range[0]) & (centers <= search_range[1])
    if not np.any(region_mask):
        return None

    region_counts = counts[region_mask]
    region_centers = centers[region_mask]
    min_idx = np.argmin(region_counts)
    valley_center = region_centers[min_idx]
    valley_count = region_counts[min_idx]

    def _fit_stage(center: float, window: float) -> dict | None:
        x, y, fit_range = _fit_window(center, window)
        if x.size < 3:
            return None
        curvature0 = -50.0
        offset0 = 10e3
        p0 = [curvature0, center, offset0]
        bounds = ([-np.inf, -np.inf, -np.inf], [0, np.inf, np.inf])
        try:
            popt, pcov = curve_fit(parabola, x, y, p0=p0, bounds=bounds)
        except (RuntimeError, ValueError):
            return None
        perr = np.sqrt(np.diag(pcov))
        return {
            "curvature": popt[0],
            "mean": popt[1],
            "offset": popt[2],
            "curvature_err": perr[0],
            "mean_err": perr[1],
            "offset_err": perr[2],
            "fit_range": fit_range,
        }

    # Stage 1: fit around the histogram minimum.
    result = _fit_stage(valley_center, half_window)
    if result is None:
        # Fallback: retry stage 1 with a wider initial half-width.
        result = _fit_stage(valley_center, VALLEY_FALLBACK_HALF_WINDOW)
    if result is None:
        return None

    # Stage 2: refit in a symmetric +/- refit_half_window interval centered
    # on the 1st-found minimum (the vertex of the stage-1 fit).
    result2 = _fit_stage(result["mean"], refit_half_window)
    if result2 is not None:
        result = result2

    return result


def load_events(root_file: str, tree_name: str = TREE_NAME) -> dict:
    """Read the branches needed for this analysis as numpy arrays."""
    with uproot.open(root_file) as f:
        tree = f[tree_name]
        arrays = tree.arrays(
            ["channel", "adc", "pmt_time", "tdc_start"], library="np"
        )
    return arrays


def compute_time_ns(pmt_time: np.ndarray, tdc_start: np.ndarray) -> np.ndarray:
    """Reconstruct the fine-grained pulse time (in ns) from raw TDC data."""
    pmt_time_i64 = pmt_time.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)

    T = (pmt_time_i64 << np.int64(4)) + tdc_start_i64

    t_ns = T.astype(np.float64) * 0.25
    return t_ns


def analyze_channel(
    raw_channel: int,
    adc_ch: np.ndarray,
    pmt_time_ch: np.ndarray,
    tdc_start_ch: np.ndarray,
    t_ns_ch: np.ndarray,
    pulser_freq_hz: float,
) -> dict | None:
    """Compute the ADC/time data and summary stats for a single channel."""
    finite_mask = np.isfinite(t_ns_ch)
    t_ns_ch = t_ns_ch[finite_mask]
    adc_ch = adc_ch[finite_mask]
    pmt_time_ch = pmt_time_ch[finite_mask]
    tdc_start_ch = tdc_start_ch[finite_mask]

    display_ch = raw_channel + 1

    if t_ns_ch.size == 0:
        print(f"Channel {display_ch:02d}: no finite timing data, skipping.")
        return None

    PERIOD_4NS = int((1.0 / pulser_freq_hz) / 4e-9)

    pmt_time_i64 = pmt_time_ch.astype(np.int64)
    tdc_start_i64 = tdc_start_ch.astype(np.int64)
    pmt_time_shift4 = pmt_time_i64 << np.int64(4)
    T = pmt_time_shift4 + tdc_start_i64

    # -----------------------------
    # Measurement time from data
    # -----------------------------
    measurement_time_s = (np.max(t_ns_ch) - np.min(t_ns_ch)) * 1e-9

    t_ns_shifted = t_ns_ch - t_ns_ch.min()  # run starts at t = 0 ns
    t_s = t_ns_shifted * 1e-9

    n_entries = adc_ch.size
    rate_hz = n_entries / measurement_time_s if measurement_time_s > 0 else float("nan")

    print(
        f"Channel {display_ch:02d}: entries={n_entries:,}, "
        f"measurement_time={measurement_time_s:.3f} s, "
        f"rate={rate_hz:.2f} Hz, PERIOD_4NS={PERIOD_4NS} ticks"
    )

    adc_rms = float(np.std(adc_ch))
    if adc_rms < NARROW_RMS_THRESHOLD:
        sigma_scale = 1.0 / NARROW_RMS_SIGMA_SCALE
        peak2_sigma_scale = 1.0 / NARROW_RMS_PEAK2_SIGMA_SCALE
        print(
            f"  Channel {display_ch:02d}: ADC RMS={adc_rms:.2f} < "
            f"{NARROW_RMS_THRESHOLD}, scaling initial fit sigmas by "
            f"{sigma_scale:.3f} (peak1) / {peak2_sigma_scale:.3f} (peak2)"
        )
    else:
        sigma_scale = 1.0
        peak2_sigma_scale = 1.0

    peak1_fit = fit_gaussian_peak(
        adc_ch,
        (ADC_RANGE[0], PEAK_SPLIT_ADC),
        PEAK1_INITIAL_SIGMA * sigma_scale,
        n_sigma_window=2,
    )
    peak2_fit = fit_gaussian_peak(
        adc_ch,
        (PEAK_SPLIT_ADC, ADC_RANGE[1]),
        PEAK2_INITIAL_SIGMA * peak2_sigma_scale,
        n_sigma_window=1,
        refit=True,
    )

    for label, fit in (("peak1 (<325)", peak1_fit), ("peak2 (>=325)", peak2_fit)):
        if fit is None:
            print(f"  Channel {display_ch:02d}: {label} fit failed.")
        else:
            print(
                f"  Channel {display_ch:02d}: {label} fit -> "
                f"mu={fit['mean']:.2f}+/-{fit['mean_err']:.2f}, "
                f"sigma={fit['sigma']:.2f}+/-{fit['sigma_err']:.2f}"
            )

    valley_fit = None
    if peak1_fit is not None and peak2_fit is not None:
        refit_half_window = VALLEY_REFIT_HALF_WINDOW
        if adc_rms > WIDE_RMS_THRESHOLD:
            refit_half_window = WIDE_RMS_VALLEY_REFIT_HALF_WINDOW
            print(
                f"  Channel {display_ch:02d}: ADC RMS={adc_rms:.2f} > "
                f"{WIDE_RMS_THRESHOLD}, using valley refit half-window "
                f"{refit_half_window}"
            )
        valley_fit = fit_valley(
            adc_ch,
            (peak1_fit["mean"], peak2_fit["mean"]),
            VALLEY_FIT_HALF_WINDOW,
            refit_half_window,
        )

    if valley_fit is None:
        print(f"  Channel {display_ch:02d}: valley fit failed.")
    else:
        print(
            f"  Channel {display_ch:02d}: valley fit -> "
            f"mu={valley_fit['mean']:.2f}+/-{valley_fit['mean_err']:.2f}, "
            f"offset={valley_fit['offset']:.2f}+/-{valley_fit['offset_err']:.2f}, "
            f"curvature={valley_fit['curvature']:.4f}+/-{valley_fit['curvature_err']:.4f}"
        )

    # Peak/valley ratio: maximum of the 2nd (peak2) Gaussian fit divided by
    # the minimum of the 3rd (valley) parabola fit. The Gaussian's peak
    # value is its amplitude, and the parabola's minimum value is its offset.
    peak_valley_ratio = None
    if peak2_fit is not None and valley_fit is not None and valley_fit["offset"] != 0:
        peak_valley_ratio = peak2_fit["amplitude"] / valley_fit["offset"]
        print(f"  Channel {display_ch:02d}: peak/valley ratio -> {peak_valley_ratio:.2f}")

    return {
        "channel": display_ch,
        "adc": adc_ch,
        "pedestal_adc": peak1_fit["mean"] if peak1_fit is not None else None,
        "pmt_time": pmt_time_i64,
        "pmt_time_shift4": pmt_time_shift4,
        "tdc_start": tdc_start_i64,
        "T": T,
        "t_s": t_s,
        "t_ns": t_ns_shifted,
        "measurement_time": t_s,
        "entries": n_entries,
        "measurement_time_s": measurement_time_s,
        "rate_hz": rate_hz,
        "period_4ns_ticks": PERIOD_4NS,
        "adc_rms": adc_rms,
        "peak1_fit": peak1_fit,
        "peak2_fit": peak2_fit,
        "valley_fit": valley_fit,
        "peak_valley_ratio": peak_valley_ratio,
    }


def _grid_shape(n_items: int) -> tuple[int, int]:
    """Pick a roughly-square (rows, cols) grid layout for n_items subplots."""
    ncols = math.ceil(math.sqrt(n_items))
    nrows = math.ceil(n_items / ncols)
    return nrows, ncols


def plot_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    adc_bins: int = ADC_HIST_BINS,
    title: str = "ADC by channel",
    output_suffix: str = "adc_grid",
) -> plt.Figure:
    """Plot the ADC histogram of every channel as a single grid figure."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        adc_rms = data["adc_rms"]
        ax.hist(
            data[adc_key],
            bins=adc_bins,
            range=adc_range,
            histtype="stepfilled",
            color="indianred",
            alpha=0.6,
            edgecolor="black",
            linewidth=0.3,
            label=f"RMS={adc_rms:.1f}",
        )

        if adc_key == "adc":
            for fit_key, color in (("peak1_fit", "royalblue"), ("peak2_fit", "darkorange")):
                fit = data.get(fit_key)
                if fit is None:
                    continue
                x_fit = np.linspace(fit["fit_range"][0], fit["fit_range"][1], 200)
                y_fit = gaussian(x_fit, fit["amplitude"], fit["mean"], fit["sigma"])
                ax.plot(
                    x_fit,
                    y_fit,
                    color=color,
                    linewidth=2,
                    label=f"$\\mu$={fit['mean']:.1f}, $\\sigma$={fit['sigma']:.1f}",
                )

            valley_fit = data.get("valley_fit")
            if valley_fit is not None:
                x_fit = np.linspace(valley_fit["fit_range"][0], valley_fit["fit_range"][1], 200)
                y_fit = parabola(
                    x_fit, valley_fit["curvature"], valley_fit["mean"], valley_fit["offset"]
                )
                label = f"valley position={valley_fit['mean']:.1f}"
                peak_valley_ratio = data.get("peak_valley_ratio")
                if peak_valley_ratio is not None:
                    label += f"\npeak/valley={peak_valley_ratio:.2f}"
                ax.plot(
                    x_fit,
                    y_fit,
                    color="seagreen",
                    linewidth=2,
                    label=label,
                )
        elif adc_key == "adc_pedestal_corrected":
            shifted_peak2_fit = data.get("shifted_peak2_fit")
            if shifted_peak2_fit is not None:
                x_fit = np.linspace(
                    shifted_peak2_fit["fit_range"][0], shifted_peak2_fit["fit_range"][1], 200
                )
                y_fit = gaussian(
                    x_fit,
                    shifted_peak2_fit["amplitude"],
                    shifted_peak2_fit["mean"],
                    shifted_peak2_fit["sigma"],
                )
                threshold = data.get("shifted_peak_fit_threshold")
                threshold_label = (
                    f"ADC>{threshold}" if threshold is not None else "shifted peak fit"
                )
                ax.plot(
                    x_fit,
                    y_fit,
                    color="darkorange",
                    linewidth=2,
                    label=f"{threshold_label}, $\\mu$={shifted_peak2_fit['mean']:.1f}",
                )

        ax.set_xlim(*adc_range)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(fontsize=7, loc="upper right")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_time_grid(
    channel_data: list[dict], output_dir: str, stem: str, time_unit: str = DEFAULT_TIME_UNIT
) -> plt.Figure:
    """Plot the measurement-time histogram of every channel as a grid figure."""
    time_key = "t_ns" if time_unit == "ns" else "t_s"
    time_label = "Time [ns]" if time_unit == "ns" else "Time [s]"

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        upper = data["measurement_time_s"] * 1e9 if time_unit == "ns" else data["measurement_time_s"]
        ax.hist(
            data[time_key],
            bins=200,
            range=(0.0, upper),
            histtype="stepfilled",
            color="steelblue",
            alpha=0.6,
            edgecolor="black",
            linewidth=0.3,
        )
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel(time_label)
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle("Measurement time by channel")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_time_grid.png"), dpi=150)
    return fig


def plot_1d_value_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    value_key: str,
    xlabel: str,
    output_suffix: str,
    title: str,
    bins: int = 200,
    value_range: tuple[float, float] | None = None,
) -> plt.Figure:
    """Plot a generic 1D value histogram for every channel as a grid figure."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        values = np.asarray(data[value_key])
        finite_values = values[np.isfinite(values)]

        if finite_values.size == 0:
            ax.set_title(f"Ch {data['channel']:02d}")
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Counts")
            ax.grid(True, linestyle="--", alpha=0.4)
            continue

        hist_range = value_range
        if hist_range is None:
            lo = float(np.min(finite_values))
            hi = float(np.max(finite_values))
            if hi <= lo:
                hi = lo + 1.0
            hist_range = (lo, hi)

        ax.hist(
            finite_values,
            bins=bins,
            range=hist_range,
            histtype="stepfilled",
            color="slateblue",
            alpha=0.6,
            edgecolor="black",
            linewidth=0.3,
        )
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_time_vs_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    time_unit: str = DEFAULT_TIME_UNIT,
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    output_suffix: str = "time_vs_adc_grid",
    title: str = "Time vs ADC by channel",
) -> plt.Figure:
    """Plot the time-vs-ADC 2D histogram of every channel as a grid figure."""
    time_key = "t_ns" if time_unit == "ns" else "t_s"
    time_label = "Time [ns]" if time_unit == "ns" else "Time [s]"

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        t = data[time_key]
        upper = data["measurement_time_s"] * 1e9 if time_unit == "ns" else data["measurement_time_s"]
        _, _, _, image = ax.hist2d(
            data[adc_key],
            t,
            bins=[150, 150],
            range=[list(adc_range), [0.0, upper]],
            cmap="viridis",
            norm=LogNorm(),
        )
        ax.set_xlim(*adc_range)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel(time_label)
        fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_shifted_peak_mean_vs_channel(
    channel_data: list[dict], output_dir: str, stem: str
) -> plt.Figure | None:
    """Plot shifted peak mean vs channel with fit-parameter mean errors."""
    channels = []
    means = []
    mean_errs = []

    for data in channel_data:
        fit = data.get("shifted_peak2_fit")
        if fit is None:
            continue
        if not np.isfinite(fit.get("mean", np.nan)) or not np.isfinite(
            fit.get("mean_err", np.nan)
        ):
            continue
        channels.append(data["channel"])
        means.append(fit["mean"])
        mean_errs.append(fit["mean_err"])

    if not channels:
        print("No valid shifted peak fits available for mean-vs-channel plot.")
        return None

    channels_arr = np.asarray(channels, dtype=np.float64)
    means_arr = np.asarray(means, dtype=np.float64)
    mean_errs_arr = np.asarray(mean_errs, dtype=np.float64)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.errorbar(
        channels_arr,
        means_arr,
        yerr=mean_errs_arr,
        fmt="o-",
        color="darkorange",
        ecolor="black",
        elinewidth=1.0,
        capsize=3,
        markersize=5,
    )
    ax.set_xlabel("Channel")
    ax.set_ylabel("Shifted peak mean [ADC]")
    ax.set_title("Shifted peak mean vs channel")
    ax.set_ylim(bottom=0.0)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xticks(channels_arr)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_shifted_peak_mean_vs_channel.png"), dpi=150)
    return fig


def run_exit_gui() -> None:
    """Open a tiny control GUI; Exit closes plots and ends the program."""
    if tk is None:
        print("Tkinter is not available; skipping GUI.")
        return

    try:
        root = tk.Tk()
    except tk.TclError:
        print("Tkinter GUI could not start (no display?).")
        return

    root.title("PMT Analysis")
    root.geometry("320x140")

    label = tk.Label(root, text="Plots are running. Click Exit to close everything.")
    label.pack(pady=12)

    def _exit_all() -> None:
        plt.close("all")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _exit_all)

    exit_button = tk.Button(root, text="Exit", width=12, command=_exit_all)
    exit_button.pack(pady=8)

    root.mainloop()


def build_pedestal_corrected_channel_data(channel_data: list[dict]) -> list[dict]:
    """Build a second-pass dataset with pedestal-corrected ADC for each channel."""
    corrected_data = []
    for data in channel_data:
        pedestal = data.get("pedestal_adc")
        if pedestal is None or not np.isfinite(pedestal):
            print(
                f"Channel {data['channel']:02d}: missing pedestal from 1st Gaussian fit; "
                "skipping pedestal correction for this channel."
            )
            continue
        corrected_row = dict(data)
        corrected_row["adc_pedestal_corrected"] = data["adc"] - pedestal
        corrected_adc_rms = float(np.std(corrected_row["adc_pedestal_corrected"]))
        corrected_row["adc_rms"] = corrected_adc_rms

        shifted_peak_min = 25 if corrected_adc_rms < 50 else 50

        nonshifted_peak2_fit = data.get("peak2_fit")
        shifted_peak_fit = None
        if nonshifted_peak2_fit is not None:
            shifted_mean = nonshifted_peak2_fit["mean"] - pedestal
            shifted_sigma = nonshifted_peak2_fit["sigma"]
            shifted_peak_fit = {
                "amplitude": nonshifted_peak2_fit["amplitude"],
                "mean": shifted_mean,
                "sigma": shifted_sigma,
                "amplitude_err": nonshifted_peak2_fit["amplitude_err"],
                "mean_err": nonshifted_peak2_fit["mean_err"],
                "sigma_err": nonshifted_peak2_fit["sigma_err"],
                "fit_range": (
                    max(shifted_peak_min, shifted_mean - shifted_sigma),
                    min(ADC_CORRECTED_RANGE[1], shifted_mean + shifted_sigma),
                ),
            }

        corrected_row["shifted_peak_fit_threshold"] = shifted_peak_min
        corrected_row["shifted_peak2_fit"] = shifted_peak_fit

        if shifted_peak_fit is None:
            print(
                f"Channel {data['channel']:02d}: shifted ADC peak2 parameters unavailable "
                f"(missing non-shifted peak2 fit; threshold would be {shifted_peak_min})."
            )
        else:
            print(
                f"Channel {data['channel']:02d}: shifted ADC peak2 (from non-shifted fit, ADC>{shifted_peak_min}) -> "
                f"mu={shifted_peak_fit['mean']:.2f}+/-{shifted_peak_fit['mean_err']:.2f}, "
                f"sigma={shifted_peak_fit['sigma']:.2f}+/-{shifted_peak_fit['sigma_err']:.2f}"
            )
        corrected_data.append(corrected_row)
    return corrected_data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Per-channel ADC/time analysis of a pmt_events ROOT file."
    )
    parser.add_argument(
        "input", nargs="?", default=DEFAULT_INPUT, help="Path to the input ROOT file."
    )
    parser.add_argument(
        "--pulser-freq-hz",
        type=float,
        default=PULSER_FREQ_HZ,
        help="Nominal pulser frequency in Hz (default: %(default)s).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for output plots (default: alongside the input file).",
    )
    parser.add_argument(
        "--time-unit",
        choices=("ns", "s"),
        default=DEFAULT_TIME_UNIT,
        help="Time unit used for the timing plots (default: %(default)s).",
    )
    args = parser.parse_args()

    input_file = args.input
    output_dir = args.output_dir or os.path.dirname(os.path.abspath(input_file))
    os.makedirs(output_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_file))[0]

    print(f"Reading {input_file} ...")
    arrays = load_events(input_file)

    channel = arrays["channel"].astype(np.int64)
    adc = arrays["adc"].astype(np.float64)
    pmt_time = arrays["pmt_time"].astype(np.int64)
    tdc_start = arrays["tdc_start"].astype(np.int64)
    t_ns = compute_time_ns(pmt_time, tdc_start)

    channels = sorted(np.unique(channel).tolist())
    print(f"Found channels (0-indexed): {channels}")

    channel_data = []
    for raw_ch in channels:
        mask = channel == raw_ch
        result = analyze_channel(
            raw_ch,
            adc[mask],
            pmt_time[mask],
            tdc_start[mask],
            t_ns[mask],
            args.pulser_freq_hz,
        )
        if result:
            channel_data.append(result)

    summary_path = os.path.join(output_dir, f"{stem}_timing_summary.txt")
    with open(summary_path, "w") as f:
        f.write("channel entries measurement_time_s rate_hz period_4ns_ticks pedestal_mean_adc\n")
        for row in channel_data:
            pedestal = row["pedestal_adc"]
            pedestal_str = f"{pedestal:.6f}" if pedestal is not None else "nan"
            f.write(
                f"{row['channel']:02d} {row['entries']} "
                f"{row['measurement_time_s']:.6f} {row['rate_hz']:.6f} "
                f"{row['period_4ns_ticks']} {pedestal_str}\n"
            )
    print(f"Saved summary to {summary_path}")

    pedestal_path = os.path.join(output_dir, f"{stem}_pedestals.txt")
    with open(pedestal_path, "w") as f:
        f.write("channel pedestal_mean_adc\n")
        for row in channel_data:
            pedestal = row["pedestal_adc"]
            pedestal_str = f"{pedestal:.6f}" if pedestal is not None else "nan"
            f.write(f"{row['channel']:02d} {pedestal_str}\n")
    print(f"Saved pedestals to {pedestal_path}")

    if not channel_data:
        print("No channel data available to plot.")
        return

    corrected_channel_data = build_pedestal_corrected_channel_data(channel_data)
    if not corrected_channel_data:
        print("No channels with valid pedestal fit; skipping corrected ADC plots.")
        return

    plot_adc_grid(channel_data, output_dir, stem)
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="pmt_time",
        xlabel="pmt_time",
        output_suffix="pmt_time_grid",
        title="pmt_time by channel",
    )
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="pmt_time_shift4",
        xlabel="pmt_time << 4",
        output_suffix="pmt_time_shift4_grid",
        title="pmt_time << 4 by channel",
    )
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="tdc_start",
        xlabel="tdc_start",
        output_suffix="tdc_start_grid",
        title="tdc_start by channel",
    )
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="T",
        xlabel="T = (pmt_time << 4) + tdc_start",
        output_suffix="T_grid",
        title="T by channel",
    )
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="t_ns",
        xlabel="t_ns [ns]",
        output_suffix="t_ns_grid",
        title="t_ns by channel",
    )
    plot_1d_value_grid(
        channel_data,
        output_dir,
        stem,
        value_key="measurement_time",
        xlabel="measurement_time [s]",
        output_suffix="measurement_time_grid",
        title="measurement_time by channel",
    )
    plot_adc_grid(
        corrected_channel_data,
        output_dir,
        stem,
        adc_key="adc_pedestal_corrected",
        adc_range=ADC_CORRECTED_RANGE,
        adc_bins=ADC_CORRECTED_HIST_BINS,
        title="Pedestal-corrected ADC by channel",
        output_suffix="adc_pedestal_corrected_grid",
    )
    plot_time_grid(channel_data, output_dir, stem, time_unit=args.time_unit)
    plot_time_vs_adc_grid(
        corrected_channel_data,
        output_dir,
        stem,
        time_unit=args.time_unit,
        adc_key="adc_pedestal_corrected",
        adc_range=ADC_CORRECTED_RANGE,
        output_suffix="time_vs_adc_pedestal_corrected_grid",
        title="Time vs pedestal-corrected ADC by channel",
    )
    plot_shifted_peak_mean_vs_channel(corrected_channel_data, output_dir, stem)

    if tk is None:
        plt.show()
    else:
        plt.show(block=False)
        run_exit_gui()


if __name__ == "__main__":
    main()
