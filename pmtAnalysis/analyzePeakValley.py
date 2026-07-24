#!/usr/bin/env python3
"""Per-channel ADC/time analysis of a `pmt_events` ROOT file.

For each channel found in the tree, this script produces:
  - an ADC histogram,
    - a pedestal-corrected ADC histogram,
  - a measurement-time histogram (pulses vs. time within the run),
    - a pedestal-corrected time-vs-ADC 2D histogram,
        - a time-walk 2D histogram (per-pulse TDC arrival time vs ADC),
        - a ToT 2D histogram (time-over-threshold vs ADC).

The per-pulse measurement time (absolute time since the start of the run,
used only to get the overall run duration/rate) is reconstructed from the
raw `pmt_time`/`tdc_start` branches:

    T = (pmt_time << 4) + tdc_start
    t_ns = T * 0.25

and the overall run duration is estimated as:

    measurement_time_s = (max(t_ns) - min(t_ns)) * 1e-9

For per-pulse timing plots, this script supports two pulse-time definitions:

    pulse-time      = (pmt_time % 25000) * 4 ns
    pulse-time-alt  = ((pmt_time << 4) + tdc_start) * 0.25 ns

`pulse-time` is a coarse time-within-cycle variable, while `pulse-time-alt`
adds the fine TDC interpolation from `tdc_start`.
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

# LSB (in ns) of the fine TDC counter. Shared by the low 4 bits of pmt_time
# (used to build the absolute t_ns) and by tdc_coarse/tdc_start (used to
# build the per-pulse tdc_walk_ns for the time-walk plot).
TDC_LSB_NS = 0.25

# PMT cycle period (in coarse pmt_time ticks) used to identify cycle index for
# first-pulse-per-cycle bookkeeping.
PMT_PULSE_MODULO_TICKS = 25_000

# Coarse pmt_time tick size (ns): 1 tick = 4 ns.
PMT_TIME_TICK_NS = 4.0

# Time-axis zoom for 2D timing plots (in ns).
# If range[0] is negative, the range is auto-inferred from finite data.
TIME_2D_Y_RANGE_NS = (-100., 200.0)
TIME_2D_Y_RANGE_PULSE_TIME_NS = (-100.0, 200.0)
TIME_2D_Y_RANGE_PULSE_TIME_ALT_NS = (-100.0, 2000.0)
TIME_2D_Y_RANGE_ToT_NS = (-100.0, 75.0)

# ADC axis limits used for both the 1D and 2D histograms.
ADC_RANGE = (0, 800)
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
            ["channel", "adc", "pmt_time", "tdc_start", "tdc_coarse", "tdc_stop"],
            library="np",
        )
    return arrays


def compute_time_ns(pmt_time: np.ndarray, tdc_start: np.ndarray) -> np.ndarray:
    """Reconstruct the absolute (run-time) pulse time (in ns) from raw TDC data."""
    pmt_time_i64 = pmt_time.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)

    T = (pmt_time_i64 << np.int64(4)) + tdc_start_i64

    t_ns = T.astype(np.float64) * TDC_LSB_NS
    return t_ns


def compute_tdc_walk_ns(
    tdc_coarse: np.ndarray, tdc_start: np.ndarray, tdc_stop: np.ndarray
) -> np.ndarray:
    """Reconstruct the per-pulse TDC arrival time (in ns) for the time-walk plot.

    Unlike `compute_time_ns` (built from `pmt_time`, the absolute run clock),
    `tdc_coarse` resets every event/trigger, so this is the variable that
    actually exhibits amplitude-dependent time walk when plotted against ADC.

    `tdc_coarse`/`tdc_start`/`tdc_stop` follow the classic TDC START/STOP
    interpolation scheme: `tdc_coarse` counts whole clock cycles between the
    START (trigger) and STOP (leading-edge threshold crossing) signals, and
    `tdc_start`/`tdc_stop` are each edge's own fine sub-cycle interpolation.
    The STOP edge's fine offset is therefore added and the START edge's fine
    offset subtracted, not both added.
    """
    tdc_coarse_i64 = tdc_coarse.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)
    tdc_stop_i64 = tdc_stop.astype(np.int64)

    # START/STOP interpolation: coarse cycles plus STOP fine minus START fine.
    tdc_walk_ticks = (tdc_coarse_i64 << np.int64(4)) - tdc_start_i64 + tdc_stop_i64

    return tdc_walk_ticks.astype(np.float64) * TDC_LSB_NS


def compute_pulse_time_alt_ns_and_cycle(
    pmt_time: np.ndarray,
    tdc_start: np.ndarray,
    modulo_ticks: int = PMT_PULSE_MODULO_TICKS,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute pulse-time alternative in ns and its corresponding cycle index.

    Returns:
        - pulse-time alternative in ns, defined exactly as:
              T = (pmt_time << 4) + tdc_start
              t_ns = np.array(T) * 0.25
        - integer cycle index (pmt_time // modulo_ticks), kept for
          first-pulse-per-cycle bookkeeping.
    """
    pmt_time_i64 = pmt_time.astype(np.int64)
    tdc_start_i64 = tdc_start.astype(np.int64)

    # Explicit reconstruction requested for the alternative time variable:
    # Formula by Andrzej:
    #   T = (pmt_time << 4) + tdc_start
    #   t_ns = np.array(T) * 0.25
    T = (pmt_time_i64 << np.int64(4)) + tdc_start_i64
    pulse_time_alt_ns = np.array(T, dtype=np.float64) * 0.25

    modulo_i64 = np.int64(modulo_ticks)
    cycle_index = np.floor_divide(pmt_time_i64, modulo_i64)
    return pulse_time_alt_ns, cycle_index


def compute_pulse_time_ns_and_cycle(
    pmt_time: np.ndarray,
    modulo_ticks: int = PMT_PULSE_MODULO_TICKS,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute coarse pulse time in ns and its cycle index.

    Definition requested by user:
        pulse_time_ns = (pmt_time % modulo_ticks) * 4 ns
    """
    pmt_time_i64 = pmt_time.astype(np.int64)
    modulo_i64 = np.int64(modulo_ticks)
    pulse_time_ticks = np.mod(pmt_time_i64, modulo_i64)
    pulse_time_ns = pulse_time_ticks.astype(np.float64) * PMT_TIME_TICK_NS
    cycle_index = np.floor_divide(pmt_time_i64, modulo_i64)
    return pulse_time_ns, cycle_index


def first_pulse_in_cycle_mask(pulse_time_ns: np.ndarray, cycle_index: np.ndarray) -> np.ndarray:
    """Return a mask that keeps only the first (earliest) pulse in each cycle."""
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


def compute_tot_ns(
    tdc_coarse: np.ndarray, tdc_start: np.ndarray, tdc_stop: np.ndarray
) -> np.ndarray:
    """Compute time-over-threshold (ToT) in ns.

    Definition requested by user:
        ToT = tdc_coarse * 4 + (tdc_stop - tdc_start) * 4/16
    where 4 ns is the coarse period and 4/16 = 0.25 ns is the fine LSB.
    """
    tdc_coarse_f64 = tdc_coarse.astype(np.float64)
    tdc_start_f64 = tdc_start.astype(np.float64)
    tdc_stop_f64 = tdc_stop.astype(np.float64)
    return (tdc_coarse_f64 * 4.0) + ((tdc_stop_f64 - tdc_start_f64) * (4.0 / 16.0))


def analyze_channel(
    raw_channel: int,
    adc_ch: np.ndarray,
    pmt_time_ch: np.ndarray,
    tdc_start_ch: np.ndarray,
    tdc_coarse_ch: np.ndarray,
    tdc_stop_ch: np.ndarray,
    t_ns_ch: np.ndarray,
    pulser_freq_hz: float,
    time_walk_source: str,
    pmt_pulse_modulo_ticks: int,
) -> dict | None:
    """Compute the ADC/time data and summary stats for a single channel."""
    finite_mask = np.isfinite(t_ns_ch)
    t_ns_ch = t_ns_ch[finite_mask]
    adc_ch = adc_ch[finite_mask]
    pmt_time_ch = pmt_time_ch[finite_mask]
    tdc_start_ch = tdc_start_ch[finite_mask]
    tdc_coarse_ch = tdc_coarse_ch[finite_mask]
    tdc_stop_ch = tdc_stop_ch[finite_mask]

    display_ch = raw_channel + 1

    if t_ns_ch.size == 0:
        print(f"Channel {display_ch:02d}: no finite timing data, skipping.")
        return None

    pulse_time_alt_ns, pulse_cycle_index = compute_pulse_time_alt_ns_and_cycle(
        pmt_time_ch,
        tdc_start_ch,
        modulo_ticks=pmt_pulse_modulo_ticks,
    )
    pulse_time_ns, _ = compute_pulse_time_ns_and_cycle(
        pmt_time_ch,
        modulo_ticks=pmt_pulse_modulo_ticks,
    )
    is_first_pmt_pulse_in_cycle = first_pulse_in_cycle_mask(
        pulse_time_alt_ns, pulse_cycle_index
    )

    if time_walk_source in ("pulse-time", "pulse-time-alt"):
        n_before_cycle = pulse_cycle_index.size
        n_after_cycle = int(np.count_nonzero(is_first_pmt_pulse_in_cycle))
        print(
            f"Channel {display_ch:02d}: first pulse per PMT cycle available "
            f"{n_after_cycle}/{n_before_cycle} entries (modulo={pmt_pulse_modulo_ticks}); "
            "first-pass ADC histograms/fits remain uncut."
        )

    PERIOD_4NS = int((1.0 / pulser_freq_hz) / 4e-9)

    pmt_time_i64 = pmt_time_ch.astype(np.int64)
    tdc_start_i64 = tdc_start_ch.astype(np.int64)
    pmt_time_shift4 = pmt_time_i64 << np.int64(4)
    T = pmt_time_shift4 + tdc_start_i64
    tdc_walk_ns = compute_tdc_walk_ns(tdc_coarse_ch, tdc_start_ch, tdc_stop_ch)
    tot_ns = compute_tot_ns(tdc_coarse_ch, tdc_start_ch, tdc_stop_ch)
    if time_walk_source == "pulse-time":
        time_walk_ns = pulse_time_ns
        time_walk_ylabel = (
            "First-pulse time [ns] = (pmt_time % "
            f"{pmt_pulse_modulo_ticks}) * {PMT_TIME_TICK_NS:.0f}"
        )
        time_walk_name = "pulse_time"
    elif time_walk_source == "pulse-time-alt":
        time_walk_ns = pulse_time_alt_ns
        time_walk_ylabel = "First-pulse time (alt.) [ns] = ((pmt_time << 4) + tdc_start) * 0.25"
        time_walk_name = "pulse_time_alt"
    else:
        raise ValueError(f"Unsupported time_walk_source: {time_walk_source}")

    # -----------------------------
    # Measurement time from data
    # -----------------------------
    measurement_time_s = (np.max(t_ns_ch) - np.min(t_ns_ch)) * 1e-9

    t_ns_shifted = t_ns_ch - t_ns_ch.min()  # run starts at t = 0 ns

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
        "tdc_coarse": tdc_coarse_ch,
        "tdc_stop": tdc_stop_ch,
        "T": T,
        "t_ns": t_ns_shifted,
        "measurement_time": t_ns_shifted,
        "tdc_walk_ns": tdc_walk_ns,
        "pulse_time_ns": pulse_time_ns,
        "pulse_time_alt_ns": pulse_time_alt_ns,
        "pulse_cycle_index": pulse_cycle_index,
        "is_first_pmt_pulse_in_cycle": is_first_pmt_pulse_in_cycle,
        "tot_ns": tot_ns,
        "time_walk_ns": time_walk_ns,
        "time_walk_ylabel": time_walk_ylabel,
        "time_walk_name": time_walk_name,
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


def _infer_range_from_values(
    values_list: list[np.ndarray],
    fallback: tuple[float, float],
    pad_fraction: float = 0.05,
) -> tuple[float, float]:
    """Infer a padded [min, max] range from finite values across arrays."""
    finite_chunks = []
    for values in values_list:
        arr = np.asarray(values, dtype=np.float64)
        if arr.size == 0:
            continue
        arr = arr[np.isfinite(arr)]
        if arr.size > 0:
            finite_chunks.append(arr)

    if not finite_chunks:
        return fallback

    merged = np.concatenate(finite_chunks)
    lo = float(np.nanmin(merged))
    hi = float(np.nanmax(merged))
    if not (np.isfinite(lo) and np.isfinite(hi)) or hi <= lo:
        return fallback

    span = hi - lo
    pad = max(span * pad_fraction, TDC_LSB_NS)
    return (lo - pad, hi + pad)


def _resolve_time_y_range(
    configured_range: tuple[float, float],
    values_list: list[np.ndarray],
) -> tuple[float, float]:
    """Use configured range unless its lower bound is negative, then auto-infer."""
    if configured_range[0] < 0:
        return _infer_range_from_values(values_list, fallback=configured_range)
    return configured_range


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


def plot_time_grid(channel_data: list[dict], output_dir: str, stem: str) -> plt.Figure:
    """Plot the measurement-time histogram of every channel as a grid figure."""
    time_label = "Time [ns]"

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        t = np.asarray(data["t_ns"], dtype=np.float64)
        upper = float(np.max(t)) if t.size else 1.0
        ax.hist(
            t,
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
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    output_suffix: str = "time_vs_adc_grid",
    title: str = "Time vs ADC by channel",
) -> plt.Figure:
    """Plot the time-vs-ADC 2D histogram of every channel as a grid figure."""
    time_label = "Time [ns]"

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    y_min, y_max = _resolve_time_y_range(
        TIME_2D_Y_RANGE_NS,
        [np.asarray(data.get("t_ns", []), dtype=np.float64) for data in channel_data],
    )

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        t = np.asarray(data["t_ns"], dtype=np.float64)
        adc_vals = np.asarray(data[adc_key], dtype=np.float64)

        finite_mask = np.isfinite(adc_vals) & np.isfinite(t)
        adc_vals = adc_vals[finite_mask]
        t = t[finite_mask]

        in_zoom_y = (t >= y_min) & (t <= y_max)
        adc_vals = adc_vals[in_zoom_y]
        t = t[in_zoom_y]

        image = None
        if adc_vals.size > 0 and t.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                t,
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
                "No points in window",
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
        ax.set_ylabel(time_label)
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_time_walk_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    y_range_ns: tuple[float, float] = TIME_2D_Y_RANGE_PULSE_TIME_NS,
    output_suffix: str = "time_walk_grid",
    title: str = "Time walk vs ADC by channel",
) -> plt.Figure:
    """Plot the selected per-pulse time variable vs ADC.

    This uses `time_walk_ns`, which is configured from --time-walk-source as
    either pulse-time or pulse-time-alt.
    """
    profile_min_counts = 20
    profile_x_bins = 150

    resolved_y_range_ns = y_range_ns
    if y_range_ns[0] < 0:
        values_list = []
        for data in channel_data:
            values = np.asarray(data.get("time_walk_ns", []), dtype=np.float64)
            first_cycle_mask = np.asarray(
                data.get("is_first_pmt_pulse_in_cycle", np.ones_like(values, dtype=bool)),
                dtype=bool,
            )
            if first_cycle_mask.shape[0] == values.shape[0]:
                values = values[first_cycle_mask]
            values_list.append(values)
        resolved_y_range_ns = _resolve_time_y_range(y_range_ns, values_list)

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        adc_vals = np.asarray(data[adc_key], dtype=np.float64)
        time_walk_ns = np.asarray(data["time_walk_ns"], dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pmt_pulse_in_cycle", np.ones_like(time_walk_ns, dtype=bool)),
            dtype=bool,
        )

        if first_cycle_mask.shape[0] == adc_vals.shape[0]:
            adc_vals = adc_vals[first_cycle_mask]
        if first_cycle_mask.shape[0] == time_walk_ns.shape[0]:
            time_walk_ns = time_walk_ns[first_cycle_mask]

        finite_mask = np.isfinite(adc_vals) & np.isfinite(time_walk_ns)
        adc_vals = adc_vals[finite_mask]
        time_walk_ns = time_walk_ns[finite_mask]

        # Keep only points inside the zoom window so both the 2D map and
        # Y-profile are computed from the same visible time range.
        y_min, y_max = resolved_y_range_ns
        in_zoom_y = (
            (time_walk_ns >= y_min)
            & (time_walk_ns <= y_max)
        )
        adc_vals = adc_vals[in_zoom_y]
        time_walk_ns = time_walk_ns[in_zoom_y]

        image = None
        if adc_vals.size > 0 and time_walk_ns.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                time_walk_ns,
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
                "No points in window",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=8,
                color="dimgray",
            )

        # Y-profile vs X: mean TDC arrival time in each ADC bin.
        x_edges = np.linspace(adc_range[0], adc_range[1], profile_x_bins + 1)
        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
        x_bin_idx = np.digitize(adc_vals, x_edges) - 1
        in_x_range = (x_bin_idx >= 0) & (x_bin_idx < profile_x_bins)

        x_bin_idx = x_bin_idx[in_x_range]
        time_walk_in_range = time_walk_ns[in_x_range]

        counts = np.bincount(x_bin_idx, minlength=profile_x_bins)
        sum_y = np.bincount(x_bin_idx, weights=time_walk_in_range, minlength=profile_x_bins)
        mean_y = np.divide(sum_y, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)

        profile_mask = (counts >= profile_min_counts) & np.isfinite(mean_y)
        if np.any(profile_mask):
            ax.plot(
                x_centers[profile_mask],
                mean_y[profile_mask],
                linestyle="none",
                marker="o",
                markersize=2.8,
                color="red",
                alpha=0.95,
                label=f"Y profile (mean, n>={profile_min_counts})",
            )

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel(data.get("time_walk_ylabel", "Time-walk variable [ns]"))
        if np.any(profile_mask):
            ax.legend(loc="upper right", fontsize=7)
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"{stem}_{output_suffix}.png"), dpi=150)
    return fig


def plot_tot_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    output_suffix: str = "tot_vs_adc_grid",
    title: str = "ToT vs ADC by channel",
) -> plt.Figure:
    """Plot ToT vs ADC with the same profile-style overlay used for time-walk."""
    profile_min_counts = 20
    profile_x_bins = 150

    if TIME_2D_Y_RANGE_ToT_NS[0] < 0:
        values_list = []
        for data in channel_data:
            values = np.asarray(data.get("tot_ns", []), dtype=np.float64)
            first_cycle_mask = np.asarray(
                data.get("is_first_pmt_pulse_in_cycle", np.ones_like(values, dtype=bool)),
                dtype=bool,
            )
            if first_cycle_mask.shape[0] == values.shape[0]:
                values = values[first_cycle_mask]
            values_list.append(values)
        y_min, y_max = _resolve_time_y_range(TIME_2D_Y_RANGE_ToT_NS, values_list)
    else:
        y_min, y_max = TIME_2D_Y_RANGE_ToT_NS

    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        adc_vals = np.asarray(data[adc_key], dtype=np.float64)
        tot_ns = np.asarray(data["tot_ns"], dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pmt_pulse_in_cycle", np.ones_like(tot_ns, dtype=bool)),
            dtype=bool,
        )

        finite_mask = np.isfinite(adc_vals) & np.isfinite(tot_ns) & first_cycle_mask
        adc_vals = adc_vals[finite_mask]
        tot_ns = tot_ns[finite_mask]

        in_zoom_y = (tot_ns >= y_min) & (tot_ns <= y_max)
        adc_vals = adc_vals[in_zoom_y]
        tot_ns = tot_ns[in_zoom_y]

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
                "No points in window",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=8,
                color="dimgray",
            )

        x_edges = np.linspace(adc_range[0], adc_range[1], profile_x_bins + 1)
        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
        x_bin_idx = np.digitize(adc_vals, x_edges) - 1
        in_x_range = (x_bin_idx >= 0) & (x_bin_idx < profile_x_bins)

        x_bin_idx = x_bin_idx[in_x_range]
        tot_in_range = tot_ns[in_x_range]

        counts = np.bincount(x_bin_idx, minlength=profile_x_bins)
        sum_y = np.bincount(x_bin_idx, weights=tot_in_range, minlength=profile_x_bins)
        mean_y = np.divide(sum_y, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)

        profile_mask = (counts >= profile_min_counts) & np.isfinite(mean_y)
        if np.any(profile_mask):
            ax.plot(
                x_centers[profile_mask],
                mean_y[profile_mask],
                linestyle="none",
                marker="o",
                markersize=2.8,
                color="red",
                alpha=0.95,
                label=f"Y profile (mean, n>={profile_min_counts})",
            )

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("ToT [ns]")
        if np.any(profile_mask):
            ax.legend(loc="upper right", fontsize=7)
        if image is not None:
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
        bg="#f62828",
        fg="white",
        activebackground="#fe0000",
        activeforeground="white",
    )
    exit_button.pack(pady=8)

    root.mainloop()


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

        # Keep all per-entry arrays aligned after the second-pass ADC cut.
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

        if shifted_peak_fit is None:
            print(
                f"Channel {data['channel']:02d}: shifted ADC peak2 parameters unavailable "
                f"(missing non-shifted peak2 fit; threshold is {second_pass_adc_min})."
            )
        else:
            print(
                f"Channel {data['channel']:02d}: 2nd-pass cut kept {n_after}/{n_before} entries, "
                f"shifted ADC peak2 (from non-shifted fit, ADC>{second_pass_adc_min}) -> "
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
        "--time-walk-source",
        choices=("pulse-time", "pulse-time-alt"),
        default="pulse-time-alt",
        help=(
            "Variable used on the time-walk Y axis: "
            "'pulse-time' uses (pmt_time%%25000)*4 ns; "
            "'pulse-time-alt' (alternative) uses ((pmt_time<<4)+tdc_start)*0.25 ns."
        ),
    )
    parser.add_argument(
        "--pmt-pulse-modulo-ticks",
        type=int,
        default=PMT_PULSE_MODULO_TICKS,
        help=(
            "Modulo period (in coarse pmt_time ticks) used for pulse-cycle bookkeeping "
            "(first-pulse-per-cycle selection) in pulse-time-alt mode "
            "(default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--second-pass-adc-min",
        type=float,
        default=0.0,
        help="Second-pass cut for pedestal-corrected ADC: keep only ADC > value.",
    )
    args = parser.parse_args()

    if args.pmt_pulse_modulo_ticks <= 0:
        raise ValueError("--pmt-pulse-modulo-ticks must be > 0")
    if not np.isfinite(args.second_pass_adc_min):
        raise ValueError("--second-pass-adc-min must be finite")

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
            tdc_coarse[mask],
            tdc_stop[mask],
            t_ns[mask],
            args.pulser_freq_hz,
            args.time_walk_source,
            args.pmt_pulse_modulo_ticks,
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

    plot_adc_grid(channel_data, output_dir, stem)
    # Time-variable plots disabled per user request.
    # plot_1d_value_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     value_key="pmt_time",
    #     xlabel="pmt_time",
    #     output_suffix="pmt_time_grid",
    #     title="pmt_time by channel",
    # )
    # plot_1d_value_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     value_key="pmt_time_shift4",
    #     xlabel="pmt_time << 4",
    #     output_suffix="pmt_time_shift4_grid",
    #     title="pmt_time << 4 by channel",
    # )
    # plot_1d_value_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     value_key="tdc_start",
    #     xlabel="tdc_start",
    #     output_suffix="tdc_start_grid",
    #     title="tdc_start by channel",
    # )
    # plot_1d_value_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     value_key="T",
    #     xlabel="T = (pmt_time << 4) + tdc_start",
    #     output_suffix="T_grid",
    #     title="T by channel",
    # )
    # plot_1d_value_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     value_key="t_ns",
    #     xlabel="t_ns [ns]",
    #     output_suffix="t_ns_grid",
    #     title="t_ns by channel",
    # )
    # plot_time_vs_adc_grid(
    #     channel_data,
    #     output_dir,
    #     stem,
    #     adc_key="adc",
    #     adc_range=ADC_RANGE,
    #     output_suffix="time_vs_adc_grid",
    #     title="Time vs ADC by channel",
    # )

    corrected_channel_data = build_pedestal_corrected_channel_data(
        channel_data, second_pass_adc_min=args.second_pass_adc_min
    )
    if not corrected_channel_data:
        print("No channels with valid pedestal fit; skipping corrected ADC plots.")
    else:
        # Time-variable plots disabled per user request.
        # time_walk_y_range_ns = (
        #     TIME_2D_Y_RANGE_PULSE_TIME_ALT_NS
        #     if args.time_walk_source == "pulse-time-alt"
        #     else TIME_2D_Y_RANGE_PULSE_TIME_NS
        # )

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
        # plot_time_vs_adc_grid(
        #     corrected_channel_data,
        #     output_dir,
        #     stem,
        #     adc_key="adc_pedestal_corrected",
        #     adc_range=ADC_CORRECTED_RANGE,
        #     output_suffix="time_vs_pedestal_corrected_adc_grid",
        #     title="Time vs pedestal-corrected ADC by channel",
        # )
        # plot_time_walk_grid(
        #     corrected_channel_data,
        #     output_dir,
        #     stem,
        #     adc_key="adc_pedestal_corrected",
        #     adc_range=ADC_CORRECTED_RANGE,
        #     y_range_ns=time_walk_y_range_ns,
        #     output_suffix=f"time_walk_{args.time_walk_source}_pedestal_corrected_grid",
        #     title=(
        #         "Time walk: "
        #         + corrected_channel_data[0].get("time_walk_ylabel", "time-walk variable [ns]")
        #         + " vs pedestal-corrected ADC by channel"
        #     ),
        # )
        # plot_tot_grid(
        #     corrected_channel_data,
        #     output_dir,
        #     stem,
        #     adc_key="adc_pedestal_corrected",
        #     adc_range=ADC_CORRECTED_RANGE,
        #     output_suffix="tot_vs_pedestal_corrected_adc_grid",
        #     title="ToT vs pedestal-corrected ADC by channel",
        # )
        plot_shifted_peak_mean_vs_channel(corrected_channel_data, output_dir, stem)

    if tk is None:
        plt.show()
    else:
        plt.show(block=False)
        run_exit_gui()


if __name__ == "__main__":
    main()
