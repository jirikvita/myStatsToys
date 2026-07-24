#!/usr/bin/env python3
"""Per-channel ADC peak/valley analysis for a `pmt_events` ROOT file.

This script keeps only ADC-related processing from analyzePeakValley.py:
- raw ADC histogram per channel,
- pedestal (1st peak) and 1 p.e. (2nd peak) Gaussian fits,
- valley fit between the two peaks,
- pedestal-corrected ADC histogram per channel,
- shifted 2nd-peak mean vs channel.
"""

from __future__ import annotations

import argparse
import math
import os

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.optimize import curve_fit
import uproot

try:
    import tkinter as tk
except ImportError:
    tk = None

DEFAULT_INPUT = "1pe_measurement/28cm/test_run_thr30_att825_20260629_141522.root"
TREE_NAME = "pmt_events"

# ADC axis limits used for both the 1D and 2D histograms.
ADC_RANGE = (0, 800)
ADC_HIST_BINS = (ADC_RANGE[1] - ADC_RANGE[0]) // 2  # 2 ADC counts per bin

# ADC axis limits for pedestal-corrected ADC plots.
ADC_CORRECTED_RANGE = (-100, 500)
ADC_CORRECTED_HIST_BINS = (ADC_CORRECTED_RANGE[1] - ADC_CORRECTED_RANGE[0]) // 2

# Time definitions for pulse-time plots.
TDC_LSB_NS = 0.25
PMT_TIME_TICK_NS = 4.0
PMT_PULSE_MODULO_TICKS = 25_000

# Custom Y ranges (ns) for pulse-time 2D plots.
# Set to None to auto-infer from data.
PULSE_TIME_2D_Y_RANGE_OPTION1_NS: tuple[float, float] | None = (2150.0, 2300.0)
PULSE_TIME_2D_Y_RANGE_OPTION2_NS: tuple[float, float] | None = (130.0, 180.0)

# Default ADC cut applied before filling 2D pulse-time plots.
ADC_2D_MIN_CUT = 25.0

# Custom Y range (ns) for ToT 2D plots. Set to None to auto-infer from data.
TOT_2D_Y_RANGE_NS: tuple[float, float] | None = (0.0, 75.0)

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

# Half-width (in ADC counts) of the fit window used for the valley fit.
VALLEY_FIT_HALF_WINDOW = 5
VALLEY_REFIT_HALF_WINDOW = 5
WIDE_RMS_THRESHOLD = 70
WIDE_RMS_VALLEY_REFIT_HALF_WINDOW = 6
VALLEY_FALLBACK_HALF_WINDOW = 15


def gaussian(x: np.ndarray, amplitude: float, mean: float, sigma: float) -> np.ndarray:
    return amplitude * np.exp(-0.5 * ((x - mean) / sigma) ** 2)


def _adc_histogram(adc_ch: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Histogram ADC values with the standard ADC_HIST_BINS/ADC_RANGE binning."""
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
    """Find the tallest bin in `search_range` and fit a Gaussian around it."""
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
                pass

    return result


def parabola(x: np.ndarray, curvature: float, vertex: float, offset: float) -> np.ndarray:
    return offset - curvature * (x - vertex) ** 2


def fit_valley(
    adc_ch: np.ndarray,
    search_range: tuple[float, float],
    half_window: float = VALLEY_FIT_HALF_WINDOW,
    refit_half_window: float = VALLEY_REFIT_HALF_WINDOW,
) -> dict | None:
    """Find the shallowest bin in `search_range` and fit a parabola around it."""
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

    def _fit_stage(center: float, window: float) -> dict | None:
        x, y, fit_range = _fit_window(center, window)
        if x.size < 3:
            return None
        p0 = [-50.0, center, 10e3]
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

    result = _fit_stage(valley_center, half_window)
    if result is None:
        result = _fit_stage(valley_center, VALLEY_FALLBACK_HALF_WINDOW)
    if result is None:
        return None

    result2 = _fit_stage(result["mean"], refit_half_window)
    if result2 is not None:
        result = result2

    return result


def load_events(root_file: str, tree_name: str = TREE_NAME) -> dict:
    """Read ADC and pulse-time branches as numpy arrays."""
    with uproot.open(root_file) as f:
        tree = f[tree_name]
        arrays = tree.arrays(
            ["channel", "adc", "pmt_time", "tdc_start", "tdc_coarse", "tdc_stop"],
            library="np",
        )
    return arrays


def compute_tot_ns(
    tdc_coarse: np.ndarray,
    tdc_start: np.ndarray,
    tdc_stop: np.ndarray,
) -> np.ndarray:
    """Compute ToT in ns.

    Definition requested by user:
        ToT = tdc_coarse * 4 + (tdc_stop - tdc_start) * 4/16
    """
    tdc_coarse_f64 = tdc_coarse.astype(np.float64)
    tdc_start_f64 = tdc_start.astype(np.float64)
    tdc_stop_f64 = tdc_stop.astype(np.float64)
    return (tdc_coarse_f64 * 4.0) + ((tdc_stop_f64 - tdc_start_f64) * (4.0 / 16.0))


def compute_pulse_time_ns(
    pmt_time: np.ndarray,
    tdc_start: np.ndarray,
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
) -> tuple[np.ndarray, str]:
    """Compute pulse time in nanoseconds using one of the two definitions.

    Note: multiplying by 1e-9 would convert ns to seconds, so it is not used
    here because this function returns values in ns for plotting.
    """
    pmt_time_i64 = pmt_time.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)

    if pulse_time_source == "option1":
        # option1: ((pmt_time << 4) + tdc_start) * 0.25 ns
        T = (pmt_time_i64 << np.int64(4)) + tdc_start_i64
        pulse_time_ns = T.astype(np.float64) * TDC_LSB_NS * 1e-9
        label = "Pulse time [ns] = ((pmt_time << 4) + tdc_start) * 0.25 * 1e-9"
    elif pulse_time_source == "option2":
        # option2: (pmt_time % 25000) * 4 ns
        modulo_i64 = np.int64(pmt_pulse_modulo_ticks)
        pulse_time_ticks = np.mod(pmt_time_i64, modulo_i64)
        pulse_time_ns = pulse_time_ticks.astype(np.float64) * PMT_TIME_TICK_NS
        label = (
            "Pulse time [ns] = (pmt_time % "
            f"{pmt_pulse_modulo_ticks}) * {PMT_TIME_TICK_NS:.0f}"
        )
    else:
        raise ValueError(f"Unsupported pulse_time_source: {pulse_time_source}")

    return pulse_time_ns, label


def first_pulse_in_cycle_mask(pulse_time_ns: np.ndarray, cycle_index: np.ndarray) -> np.ndarray:
    """Return mask that keeps only the first (earliest) pulse in each cycle."""
    n = cycle_index.size
    if n == 0:
        return np.zeros(0, dtype=bool)

    idx = np.arange(n, dtype=np.int64)
    order = np.lexsort((idx, pulse_time_ns, cycle_index))
    ordered_cycles = cycle_index[order]
    first_in_sorted = np.empty(order.size, dtype=bool)
    first_in_sorted[0] = True
    first_in_sorted[1:] = ordered_cycles[1:] != ordered_cycles[:-1]

    mask = np.zeros(n, dtype=bool)
    mask[order[first_in_sorted]] = True
    return mask


def analyze_channel(
    raw_channel: int,
    adc_ch: np.ndarray,
    pmt_time_ch: np.ndarray,
    tdc_start_ch: np.ndarray,
    tdc_coarse_ch: np.ndarray,
    tdc_stop_ch: np.ndarray,
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
) -> dict | None:
    """Compute ADC-only fit products and summary stats for a single channel."""
    finite_mask = (
        np.isfinite(adc_ch)
        & np.isfinite(pmt_time_ch)
        & np.isfinite(tdc_start_ch)
        & np.isfinite(tdc_coarse_ch)
        & np.isfinite(tdc_stop_ch)
    )
    adc_ch = adc_ch[finite_mask]
    pmt_time_ch = pmt_time_ch[finite_mask]
    tdc_start_ch = tdc_start_ch[finite_mask]
    tdc_coarse_ch = tdc_coarse_ch[finite_mask]
    tdc_stop_ch = tdc_stop_ch[finite_mask]

    display_ch = raw_channel + 1

    if adc_ch.size == 0:
        print(f"Channel {display_ch:02d}: no finite ADC data, skipping.")
        return None

    pulse_time_ns, pulse_time_label = compute_pulse_time_ns(
        pmt_time_ch,
        tdc_start_ch,
        pulse_time_source=pulse_time_source,
        pmt_pulse_modulo_ticks=pmt_pulse_modulo_ticks,
    )
    cycle_index = np.floor_divide(pmt_time_ch.astype(np.int64), np.int64(pmt_pulse_modulo_ticks))
    is_first_pulse_in_cycle = first_pulse_in_cycle_mask(pulse_time_ns, cycle_index)
    tot_ns = compute_tot_ns(tdc_coarse_ch, tdc_start_ch, tdc_stop_ch)

    n_entries = adc_ch.size
    adc_rms = float(np.std(adc_ch))
    print(f"Channel {display_ch:02d}: entries={n_entries:,}, ADC RMS={adc_rms:.2f}")

    if adc_rms < NARROW_RMS_THRESHOLD:
        sigma_scale = 1.0 / NARROW_RMS_SIGMA_SCALE
        peak2_sigma_scale = 1.0 / NARROW_RMS_PEAK2_SIGMA_SCALE
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

    valley_fit = None
    if peak1_fit is not None and peak2_fit is not None:
        refit_half_window = VALLEY_REFIT_HALF_WINDOW
        if adc_rms > WIDE_RMS_THRESHOLD:
            refit_half_window = WIDE_RMS_VALLEY_REFIT_HALF_WINDOW
        valley_fit = fit_valley(
            adc_ch,
            (peak1_fit["mean"], peak2_fit["mean"]),
            VALLEY_FIT_HALF_WINDOW,
            refit_half_window,
        )

    peak_valley_ratio = None
    if peak2_fit is not None and valley_fit is not None and valley_fit["offset"] != 0:
        peak_valley_ratio = peak2_fit["amplitude"] / valley_fit["offset"]

    return {
        "channel": display_ch,
        "adc": adc_ch,
        "pulse_time_ns": pulse_time_ns,
        "pulse_time_label": pulse_time_label,
        "cycle_index": cycle_index,
        "is_first_pulse_in_cycle": is_first_pulse_in_cycle,
        "tot_ns": tot_ns,
        "pedestal_adc": peak1_fit["mean"] if peak1_fit is not None else None,
        "entries": n_entries,
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
    """Plot ADC histogram of every channel as a single grid figure."""
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
                ax.plot(x_fit, y_fit, color="seagreen", linewidth=2, label=label)

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
                threshold_label = f"ADC>{threshold}" if threshold is not None else "shifted peak fit"
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
        if not np.isfinite(fit.get("mean", np.nan)) or not np.isfinite(fit.get("mean_err", np.nan)):
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


def plot_pulse_time_vs_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    pulse_time_source: str,
    adc_key: str = "adc_pedestal_corrected",
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    adc_min_cut: float = ADC_2D_MIN_CUT,
    output_suffix: str = "pulse_time_vs_pedestal_corrected_adc_grid",
    title: str = "Pulse time vs pedestal-corrected ADC by channel",
) -> plt.Figure:
    """Plot pulse time (ns) vs ADC as a 2D histogram for each channel."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    all_t = []
    for data in channel_data:
        t = np.asarray(data.get("pulse_time_ns", []), dtype=np.float64)
        t = t[np.isfinite(t)]
        if t.size > 0:
            all_t.append(t)

    custom_range = (
        PULSE_TIME_2D_Y_RANGE_OPTION1_NS
        if pulse_time_source == "option1"
        else PULSE_TIME_2D_Y_RANGE_OPTION2_NS
    )

    if custom_range is not None:
        y_min, y_max = custom_range
    elif all_t:
        merged = np.concatenate(all_t)
        y_min = float(np.min(merged))
        y_max = float(np.max(merged))
        if y_max <= y_min:
            y_max = y_min + 1.0
        pad = max((y_max - y_min) * 0.05, TDC_LSB_NS)
        y_min -= pad
        y_max += pad
    else:
        y_min, y_max = 0.0, 1.0

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        adc_vals = np.asarray(data[adc_key], dtype=np.float64)
        pulse_time_ns = np.asarray(data["pulse_time_ns"], dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pulse_in_cycle", np.ones_like(pulse_time_ns, dtype=bool)),
            dtype=bool,
        )

        if first_cycle_mask.shape[0] == adc_vals.shape[0]:
            adc_vals = adc_vals[first_cycle_mask]
        if first_cycle_mask.shape[0] == pulse_time_ns.shape[0]:
            pulse_time_ns = pulse_time_ns[first_cycle_mask]

        finite_mask = np.isfinite(adc_vals) & np.isfinite(pulse_time_ns)
        adc_vals = adc_vals[finite_mask]
        pulse_time_ns = pulse_time_ns[finite_mask]

        # Apply ADC threshold before filling the 2D histogram.
        adc_cut_mask = adc_vals > adc_min_cut
        adc_vals = adc_vals[adc_cut_mask]
        pulse_time_ns = pulse_time_ns[adc_cut_mask]

        image = None
        if adc_vals.size > 0 and pulse_time_ns.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                pulse_time_ns,
                bins=[150, 150],
                range=[list(adc_range), [y_min, y_max]],
                cmap="viridis",
                norm=LogNorm(),
                cmin=1,
            )
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

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel(data.get("pulse_time_label", "Pulse time [ns]"))
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_tot_vs_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc_pedestal_corrected",
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    adc_min_cut: float = ADC_2D_MIN_CUT,
    output_suffix: str = "tot_vs_pedestal_corrected_adc_grid",
    title: str = "ToT vs pedestal-corrected ADC by channel",
) -> plt.Figure:
    """Plot ToT (ns) vs ADC as a 2D histogram for each channel."""
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    all_tot = []
    for data in channel_data:
        values = np.asarray(data.get("tot_ns", []), dtype=np.float64)
        values = values[np.isfinite(values)]
        if values.size > 0:
            all_tot.append(values)

    if TOT_2D_Y_RANGE_NS is not None:
        y_min, y_max = TOT_2D_Y_RANGE_NS
    elif all_tot:
        merged = np.concatenate(all_tot)
        y_min = float(np.min(merged))
        y_max = float(np.max(merged))
        if y_max <= y_min:
            y_max = y_min + 1.0
        pad = max((y_max - y_min) * 0.05, TDC_LSB_NS)
        y_min -= pad
        y_max += pad
    else:
        y_min, y_max = 0.0, 1.0

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        adc_vals = np.asarray(data[adc_key], dtype=np.float64)
        tot_ns = np.asarray(data.get("tot_ns", []), dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pulse_in_cycle", np.ones_like(tot_ns, dtype=bool)),
            dtype=bool,
        )

        if first_cycle_mask.shape[0] == adc_vals.shape[0]:
            adc_vals = adc_vals[first_cycle_mask]
        if first_cycle_mask.shape[0] == tot_ns.shape[0]:
            tot_ns = tot_ns[first_cycle_mask]

        finite_mask = np.isfinite(adc_vals) & np.isfinite(tot_ns)
        adc_vals = adc_vals[finite_mask]
        tot_ns = tot_ns[finite_mask]

        adc_cut_mask = adc_vals > adc_min_cut
        adc_vals = adc_vals[adc_cut_mask]
        tot_ns = tot_ns[adc_cut_mask]

        image = None
        if adc_vals.size > 0 and tot_ns.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                tot_ns,
                bins=[150, 150],
                range=[list(adc_range), [y_min, y_max]],
                cmap="viridis",
                norm=LogNorm(),
                cmin=1,
            )
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

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("ToT [ns]")
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def build_pedestal_corrected_channel_data(
    channel_data: list[dict], second_pass_adc_min: float = 25.0
) -> list[dict]:
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

        second_pass_mask = corrected_row["adc_pedestal_corrected"] > second_pass_adc_min
        n_before = corrected_row["adc_pedestal_corrected"].size
        n_after = int(np.count_nonzero(second_pass_mask))
        if n_after == 0:
            print(
                f"Channel {data['channel']:02d}: no entries survive 2nd-pass cut "
                f"ADC>{second_pass_adc_min}; skipping this channel."
            )
            continue

        for key, value in list(corrected_row.items()):
            if isinstance(value, np.ndarray) and value.shape[0] == n_before:
                corrected_row[key] = value[second_pass_mask]

        corrected_adc_rms = float(np.std(corrected_row["adc_pedestal_corrected"]))
        corrected_row["adc_rms"] = corrected_adc_rms
        corrected_row["second_pass_adc_min"] = second_pass_adc_min

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
                    max(second_pass_adc_min, shifted_mean - shifted_sigma),
                    min(ADC_CORRECTED_RANGE[1], shifted_mean + shifted_sigma),
                ),
            }

        corrected_row["shifted_peak_fit_threshold"] = second_pass_adc_min
        corrected_row["shifted_peak2_fit"] = shifted_peak_fit
        corrected_data.append(corrected_row)

    return corrected_data


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
        description="Per-channel ADC peak/valley analysis of a pmt_events ROOT file."
    )
    parser.add_argument("input", nargs="?", default=DEFAULT_INPUT, help="Path to input ROOT file.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for output plots (default: alongside the input file).",
    )
    parser.add_argument(
        "--second-pass-adc-min",
        type=float,
        default=0.0,
        help="Second-pass cut for pedestal-corrected ADC: keep only ADC > value.",
    )
    parser.add_argument(
        "--pulse-time-source",
        choices=("option1", "option2"),
        default="option1",
        help=(
            "Pulse-time definition for the 2D pulse-time-vs-ADC plot: "
            "option1=((pmt_time<<4)+tdc_start)*0.25 ns, "
            "option2=(pmt_time%%25000)*4 ns."
        ),
    )
    parser.add_argument(
        "--pmt-pulse-modulo-ticks",
        type=int,
        default=PMT_PULSE_MODULO_TICKS,
        help="Modulo period for option2 pulse time (default: %(default)s).",
    )
    parser.add_argument(
        "--adc-2d-min-cut",
        type=float,
        default=ADC_2D_MIN_CUT,
        help=(
            "ADC threshold applied before filling pulse-time 2D histograms: "
            "keep only ADC > value (default: %(default)s)."
        ),
    )
    args = parser.parse_args()

    if not np.isfinite(args.second_pass_adc_min):
        raise ValueError("--second-pass-adc-min must be finite")
    if args.pmt_pulse_modulo_ticks <= 0:
        raise ValueError("--pmt-pulse-modulo-ticks must be > 0")
    if not np.isfinite(args.adc_2d_min_cut):
        raise ValueError("--adc-2d-min-cut must be finite")

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
    tdc_coarse = arrays["tdc_coarse"].astype(np.int64)
    tdc_stop = arrays["tdc_stop"].astype(np.int64)

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
            tdc_coarse[mask],
            tdc_stop[mask],
            pulse_time_source=args.pulse_time_source,
            pmt_pulse_modulo_ticks=args.pmt_pulse_modulo_ticks,
        )
        if result:
            channel_data.append(result)

    summary_path = os.path.join(output_dir, f"{stem}_adc_summary.txt")
    with open(summary_path, "w") as f:
        f.write("channel entries pedestal_mean_adc peak2_mean_adc valley_mean_adc peak_valley_ratio\n")
        for row in channel_data:
            pedestal = row["pedestal_adc"]
            peak2 = row["peak2_fit"]["mean"] if row["peak2_fit"] is not None else np.nan
            valley = row["valley_fit"]["mean"] if row["valley_fit"] is not None else np.nan
            ratio = row["peak_valley_ratio"] if row["peak_valley_ratio"] is not None else np.nan
            f.write(
                f"{row['channel']:02d} {row['entries']} {pedestal if pedestal is not None else np.nan:.6f} "
                f"{peak2:.6f} {valley:.6f} {ratio:.6f}\n"
            )
    print(f"Saved ADC summary to {summary_path}")

    if not channel_data:
        print("No channel data available to plot.")
        return

    plot_adc_grid(channel_data, output_dir, stem)

    corrected_channel_data = build_pedestal_corrected_channel_data(
        channel_data, second_pass_adc_min=args.second_pass_adc_min
    )
    if not corrected_channel_data:
        print("No channels with valid pedestal fit; skipping corrected ADC plots.")
    else:
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
        plot_pulse_time_vs_adc_grid(
            corrected_channel_data,
            output_dir,
            stem,
            pulse_time_source=args.pulse_time_source,
            adc_key="adc_pedestal_corrected",
            adc_range=ADC_CORRECTED_RANGE,
            adc_min_cut=args.adc_2d_min_cut,
            output_suffix=f"pulse_time_{args.pulse_time_source}_vs_pedestal_corrected_adc_grid",
            title=(
                "Pulse time vs pedestal-corrected ADC by channel ("
                + args.pulse_time_source
                + f", ADC>{args.adc_2d_min_cut:g})"
            ),
        )
        plot_tot_vs_adc_grid(
            corrected_channel_data,
            output_dir,
            stem,
            adc_key="adc_pedestal_corrected",
            adc_range=ADC_CORRECTED_RANGE,
            adc_min_cut=args.adc_2d_min_cut,
            output_suffix="tot_vs_pedestal_corrected_adc_grid",
            title=f"ToT vs pedestal-corrected ADC by channel (ADC>{args.adc_2d_min_cut:g})",
        )
        plot_shifted_peak_mean_vs_channel(corrected_channel_data, output_dir, stem)

    if tk is None:
        plt.show()
    else:
        plt.show(block=False)
        run_exit_gui()


if __name__ == "__main__":
    main()
