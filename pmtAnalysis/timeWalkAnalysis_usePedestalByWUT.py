#!/usr/bin/env python3
"""Per-channel pedestal-corrected time-walk and TTS analysis of a `pmt_events` ROOT file.

Per-channel pedestals are read from `json_results_to_db/channel_??.json`
(key `adc_pedestal`) instead of being fitted. The pedestal-corrected ADC is cut
by the ADC threshold, and ToT, time-walk and TTS are computed on the selected pulses.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
ADC_RANGE = (180, 480)
ADC_HIST_BINS = (ADC_RANGE[1] - ADC_RANGE[0]) // 2  # 2 ADC counts per bin
ADC_PLOT_LOGY = True

# ADC axis limits for pedestal-corrected ADC plots.
ADC_CORRECTED_RANGE = (-10, 310)
ADC_CORRECTED_HIST_BINS = (ADC_CORRECTED_RANGE[1] - ADC_CORRECTED_RANGE[0]) // 2

# Time definitions for pulse-time plots.
TDC_LSB_NS = 0.25
PMT_TIME_TICK_NS = 4.0
PMT_PULSE_MODULO_TICKS = 25_000

# Custom Y ranges (ns) for pulse-time 2D plots.
# Set to None to auto-infer from data.
PULSE_TIME_2D_Y_RANGE_OPTION1_NS: tuple[float, float] | None = (2.0, 2030.0)
PULSE_TIME_2D_Y_RANGE_OPTION2_NS: tuple[float, float] | None = (140.0, 160.0)

# Optional per-channel Y-range overrides (display channel indexing: 1, 2, ...).
# Any channel absent from these maps falls back to the global ranges above.
PULSE_TIME_2D_Y_RANGE_OPTION1_BY_CHANNEL_NS: dict[int, tuple[float, float]] = {
    1: (210.0, 235.0),
}
PULSE_TIME_2D_Y_RANGE_OPTION2_BY_CHANNEL_NS: dict[int, tuple[float, float]] = {
    #1: (110.0, 120.0),
    #4: (140.0, 165.0),
    #18: (140.0, 165.0),
    #6: (110.0, 120.0),
}

# Base bin width (ns) for 1D pulse-time histograms.
# Final 1D width is this value multiplied by --rebin-time.
PULSE_TIME_1D_BIN_WIDTH_NS = 0.25

# Global minimum ADC threshold used for timing-related plots.
ADC_THRESHOLD_DEFAULT = 10.0

# Global controls for pulse-time-vs-ADC profile extraction/fitting.
PULSE_ADC_MIN_CUT_DEFAULT = 20.0
PULSE_PROFILE_ADC_SUBRANGE_DEFAULT = (20.0, ADC_CORRECTED_RANGE[1])

# Custom Y range (ns) for ToT 2D plots. Set to None to auto-infer from data.
TOT_2D_Y_RANGE_NS: tuple[float, float] | None = (0.0, 75.0)

PEDESTAL_JSON_SUBDIR = "json_results_to_db"


def load_pedestals_from_json(pedestal_dir: str, raw_channels: list[int]) -> dict[int, float]:
    """Read 'adc_pedestal' from channel_<display channel>.json (display = raw + 1)."""
    pedestals: dict[int, float] = {}
    for raw_ch in raw_channels:
        display_ch = raw_ch + 1
        path = os.path.join(pedestal_dir, f"channel_{display_ch:02d}.json")
        if not os.path.isfile(path):
            print(f"Channel {display_ch:02d}: pedestal file {path} not found.")
            continue
        with open(path) as f:
            value = json.load(f).get("adc_pedestal")
        if isinstance(value, (int, float)) and np.isfinite(value):
            pedestals[display_ch] = float(value)
        else:
            print(f"Channel {display_ch:02d}: no valid 'adc_pedestal' in {path}.")
    return pedestals


def timewalk_model(adc: np.ndarray, c0: float, a0: float, b0: float) -> np.ndarray:
    """Time-walk model: C + A * exp(-adc / B)."""
    return c0 + a0 * np.exp(-adc / b0)


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
        # option2: (pmt_time % 25000) * 4 ns + tdc_start * 0.25 ns
        modulo_i64 = np.int64(pmt_pulse_modulo_ticks)
        pulse_time_ticks = np.mod(pmt_time_i64, modulo_i64)
        pulse_time_ns = (
            pulse_time_ticks.astype(np.float64) * PMT_TIME_TICK_NS
            + tdc_start_i64.astype(np.float64) * TDC_LSB_NS
        )
        label = (
            "Pulse time [ns] = (pmt_time % "
            f"{pmt_pulse_modulo_ticks}) * {PMT_TIME_TICK_NS:.0f}"
            f" + tdc_start * {TDC_LSB_NS:.2f}"
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
    pedestal_adc: float | None,
    adc_ch: np.ndarray,
    pmt_time_ch: np.ndarray,
    tdc_start_ch: np.ndarray,
    tdc_coarse_ch: np.ndarray,
    tdc_stop_ch: np.ndarray,
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
) -> dict | None:
    """Collect per-channel arrays and the externally supplied pedestal."""
    display_ch = raw_channel + 1

    if pedestal_adc is None or not np.isfinite(pedestal_adc):
        print(f"Channel {display_ch:02d}: no adc_pedestal in JSON, skipping.")
        return None

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
    print(f"Channel {display_ch:02d}: entries={n_entries:,}, ADC RMS={adc_rms:.2f}, pedestal={pedestal_adc:.2f}")

    return {
        "channel": display_ch,
        "adc": adc_ch,
        "pulse_time_ns": pulse_time_ns,
        "pulse_time_label": pulse_time_label,
        "cycle_index": cycle_index,
        "is_first_pulse_in_cycle": is_first_pulse_in_cycle,
        "tot_ns": tot_ns,
        "pedestal_adc": pedestal_adc,
        "entries": n_entries,
        "adc_rms": adc_rms,
    }


def _grid_shape(n_items: int) -> tuple[int, int]:
    """Pick a roughly-square (rows, cols) grid layout for n_items subplots."""
    ncols = math.ceil(math.sqrt(n_items))
    nrows = math.ceil(n_items / ncols)
    return nrows, ncols


def extract_threshold_tag_from_path(path: str) -> str | None:
    """Extract threshold tag from a file path, e.g. Thr15mV or thr30mV.

    Returns a canonical tag like "Thr15mV" when a match is found,
    otherwise returns None.
    """
    match = re.search(r"thr\s*[_-]?\s*(\d+)\s*mv", path, flags=re.IGNORECASE)
    if match is None:
        return None
    return f"Thr{match.group(1)}mV"


def save_figure_dual_format(fig: plt.Figure, output_dir: str, base_name: str) -> None:
    """Save figure as both PNG and PDF under png/ and pdf/ subdirectories."""
    png_dir = os.path.join(output_dir, "png")
    pdf_dir = os.path.join(output_dir, "pdf")
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    fig.savefig(os.path.join(png_dir, f"{base_name}.png"), dpi=150)
    fig.savefig(os.path.join(pdf_dir, f"{base_name}.pdf"))


def plot_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc",
    adc_range: tuple[float, float] = ADC_RANGE,
    adc_bins: int = ADC_HIST_BINS,
    title: str = "ADC by channel",
    output_suffix: str = "adc_grid",
    dataset_tag: str | None = None,
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

        if adc_key == "adc" and data.get("pedestal_adc") is not None:
            ax.axvline(
                data["pedestal_adc"],
                color="royalblue",
                linewidth=1.5,
                label=f"pedestal={data['pedestal_adc']:.1f}",
            )

        ax.set_xlim(*adc_range)
        if ADC_PLOT_LOGY:
            ax.set_yscale("log")
            ax.set_ylim(bottom=0.5)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)
        if dataset_tag is not None:
            ax.plot([], [], " ", label=dataset_tag)
        ax.legend(fontsize=7, loc="upper right")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_{output_suffix}")
    return fig


def plot_pulse_time_vs_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    pulse_time_source: str,
    adc_key: str = "adc_pedestal_corrected",
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    adc_min_cut: float = ADC_THRESHOLD_DEFAULT,
    output_suffix: str = "pulse_time_vs_pedestal_corrected_adc_grid",
    title: str = "Pulse time vs pedestal-corrected ADC by channel",
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot pulse time (ns) vs ADC as a 2D histogram for each channel.

    Overlays a red Y-profile (mean pulse time per ADC bin) with statistical
    uncertainties (standard error of the mean).
    """
    adc_bins_2d = max(1, int(round(adc_range[1] - adc_range[0])))
    profile_min_counts = 20
    profile_x_bins = int(adc_bins_2d / 10)

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
        default_y_min, default_y_max = custom_range
    elif all_t:
        merged = np.concatenate(all_t)
        default_y_min = float(np.min(merged))
        default_y_max = float(np.max(merged))
        if default_y_max <= default_y_min:
            default_y_max = default_y_min + 1.0
        pad = max((default_y_max - default_y_min) * 0.05, TDC_LSB_NS)
        default_y_min -= pad
        default_y_max += pad
    else:
        default_y_min, default_y_max = 0.0, 1.0

    channel_range_overrides = (
        PULSE_TIME_2D_Y_RANGE_OPTION1_BY_CHANNEL_NS
        if pulse_time_source == "option1"
        else PULSE_TIME_2D_Y_RANGE_OPTION2_BY_CHANNEL_NS
    )

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        y_min, y_max = channel_range_overrides.get(data["channel"], (default_y_min, default_y_max))
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

        # Apply global ADC threshold before filling the 2D histogram.
        adc_cut_mask = adc_vals > adc_min_cut
        adc_vals = adc_vals[adc_cut_mask]
        pulse_time_ns = pulse_time_ns[adc_cut_mask]

        image = None
        if adc_vals.size > 0 and pulse_time_ns.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                pulse_time_ns,
                bins=[int(adc_bins_2d/10), 75],
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

        # Y-profile vs X: mean pulse time in each ADC bin with SEM uncertainty.
        # Use only points inside the displayed 2D histogram Y-range.
        profile_y_mask = (pulse_time_ns >= y_min) & (pulse_time_ns <= y_max)
        adc_vals_profile = adc_vals[profile_y_mask]
        pulse_time_profile = pulse_time_ns[profile_y_mask]

        x_edges = np.linspace(adc_range[0], adc_range[1], profile_x_bins + 1)
        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
        x_bin_idx = np.digitize(adc_vals_profile, x_edges) - 1
        in_x_range = (x_bin_idx >= 0) & (x_bin_idx < profile_x_bins)

        x_bin_idx = x_bin_idx[in_x_range]
        y_in_range = pulse_time_profile[in_x_range]

        counts = np.bincount(x_bin_idx, minlength=profile_x_bins)
        sum_y = np.bincount(x_bin_idx, weights=y_in_range, minlength=profile_x_bins)
        sum_y2 = np.bincount(x_bin_idx, weights=y_in_range * y_in_range, minlength=profile_x_bins)

        mean_y = np.divide(sum_y, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        mean_y2 = np.divide(sum_y2, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        var_y = np.clip(mean_y2 - mean_y * mean_y, a_min=0.0, a_max=None)
        sem_y = np.sqrt(var_y / counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)

        profile_mask = (counts >= profile_min_counts) & np.isfinite(mean_y) & np.isfinite(sem_y)
        if np.any(profile_mask):
            ax.errorbar(
                x_centers[profile_mask],
                mean_y[profile_mask],
                yerr=sem_y[profile_mask],
                fmt="o",
                markersize=2.8,
                color="red",
                ecolor="red",
                elinewidth=0.8,
                capsize=2,
                alpha=0.95,
                label=f"Y profile (mean ± SEM, n>={profile_min_counts})",
            )

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel(data.get("pulse_time_label", "Pulse time [ns]"))
        if np.any(profile_mask):
            if dataset_tag is not None:
                ax.plot([], [], " ", label=dataset_tag)
            ax.legend(loc="upper right", fontsize=7)
        elif dataset_tag is not None:
            ax.plot([], [], " ", label=dataset_tag)
            ax.legend(loc="upper right", fontsize=7)
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_{output_suffix}")
    return fig


def plot_tot_vs_adc_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    adc_key: str = "adc_pedestal_corrected",
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    adc_min_cut: float = ADC_THRESHOLD_DEFAULT,
    output_suffix: str = "tot_vs_pedestal_corrected_adc_grid",
    title: str = "ToT vs pedestal-corrected ADC by channel",
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot ToT (ns) vs ADC as a 2D histogram for each channel.

    Overlays a red Y-profile (mean ToT per ADC bin) with statistical
    uncertainties (standard error of the mean).
    """
    adc_bins_2d = max(1, int(round(adc_range[1] - adc_range[0])))
    profile_min_counts = 20
    profile_x_bins = adc_bins_2d
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

        adc_cut_mask = adc_vals >= adc_min_cut
        adc_vals = adc_vals[adc_cut_mask]
        tot_ns = tot_ns[adc_cut_mask]

        image = None
        if adc_vals.size > 0 and tot_ns.size > 0:
            _, _, _, image = ax.hist2d(
                adc_vals,
                tot_ns,
                bins=[adc_bins_2d, 150],
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

        # Y-profile vs X: mean ToT in each ADC bin with SEM uncertainty.
        # Use only points inside the displayed 2D histogram Y-range.
        profile_y_mask = (tot_ns >= y_min) & (tot_ns <= y_max)
        adc_vals_profile = adc_vals[profile_y_mask]
        tot_profile = tot_ns[profile_y_mask]

        x_edges = np.linspace(adc_range[0], adc_range[1], profile_x_bins + 1)
        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
        x_bin_idx = np.digitize(adc_vals_profile, x_edges) - 1
        in_x_range = (x_bin_idx >= 0) & (x_bin_idx < profile_x_bins)

        x_bin_idx = x_bin_idx[in_x_range]
        y_in_range = tot_profile[in_x_range]

        counts = np.bincount(x_bin_idx, minlength=profile_x_bins)
        sum_y = np.bincount(x_bin_idx, weights=y_in_range, minlength=profile_x_bins)
        sum_y2 = np.bincount(x_bin_idx, weights=y_in_range * y_in_range, minlength=profile_x_bins)

        mean_y = np.divide(sum_y, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        mean_y2 = np.divide(sum_y2, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        var_y = np.clip(mean_y2 - mean_y * mean_y, a_min=0.0, a_max=None)
        sem_y = np.sqrt(var_y / counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)

        profile_mask = (counts >= profile_min_counts) & np.isfinite(mean_y) & np.isfinite(sem_y)
        if np.any(profile_mask):
            ax.errorbar(
                x_centers[profile_mask],
                mean_y[profile_mask],
                yerr=sem_y[profile_mask],
                fmt="o",
                markersize=2.8,
                color="red",
                ecolor="red",
                elinewidth=0.8,
                capsize=2,
                alpha=0.95,
                label=f"Y profile (mean ± SEM, n>={profile_min_counts})",
            )

        ax.set_xlim(*adc_range)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel("ADC")
        ax.set_ylabel("ToT [ns]")
        if np.any(profile_mask):
            if dataset_tag is not None:
                ax.plot([], [], " ", label=dataset_tag)
            ax.legend(loc="upper right", fontsize=7)
        elif dataset_tag is not None:
            ax.plot([], [], " ", label=dataset_tag)
            ax.legend(loc="upper right", fontsize=7)
        if image is not None:
            fig.colorbar(image, ax=ax, label="Counts")

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_{output_suffix}")
    return fig


def histogram_fwhm(bin_counts: np.ndarray, bin_edges: np.ndarray) -> float | None:
    """Estimate FWHM from a histogram as width of bins above half-maximum."""
    if bin_counts.size == 0 or bin_edges.size != bin_counts.size + 1:
        return None

    max_count = float(np.max(bin_counts))
    if not np.isfinite(max_count) or max_count <= 0.0:
        return None

    half_max = 0.5 * max_count
    above = np.flatnonzero(bin_counts >= half_max)
    if above.size == 0:
        return None

    lo_idx = int(above[0])
    hi_idx = int(above[-1])
    fwhm = float(bin_edges[hi_idx + 1] - bin_edges[lo_idx])
    if not np.isfinite(fwhm) or fwhm < 0.0:
        return None
    return fwhm


def plot_pulse_time_hist_grid(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    pulse_time_source: str,
    adc_key: str = "adc",
    adc_min_cut: float = ADC_THRESHOLD_DEFAULT,
    rebin_time: int = 1,
    time_bin_width_ns: float = 0.25,
    output_suffix: str = "pulse_time_hist_grid",
    title: str = "Pulse time distribution by channel",
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot 1D pulse-time histograms for each channel as a grid.

    Applies a global ADC threshold cut before filling each histogram.
    """
    nrows, ncols = _grid_shape(len(channel_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    all_t = []
    for data in channel_data:
        t = np.asarray(data.get("pulse_time_ns", []), dtype=np.float64)
        adc_vals = np.asarray(data.get(adc_key, []), dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pulse_in_cycle", np.ones_like(t, dtype=bool)),
            dtype=bool,
        )
        if first_cycle_mask.shape[0] == t.shape[0]:
            t = t[first_cycle_mask]
        if first_cycle_mask.shape[0] == adc_vals.shape[0]:
            adc_vals = adc_vals[first_cycle_mask]

        finite_mask = np.isfinite(t) & np.isfinite(adc_vals)
        t = t[finite_mask]
        adc_vals = adc_vals[finite_mask]

        adc_cut_mask = adc_vals >= adc_min_cut
        t = t[adc_cut_mask]
        if t.size > 0:
            all_t.append(t)

    custom_range = (
        PULSE_TIME_2D_Y_RANGE_OPTION1_NS
        if pulse_time_source == "option1"
        else PULSE_TIME_2D_Y_RANGE_OPTION2_NS
    )

    if custom_range is not None:
        default_t_min, default_t_max = custom_range
    elif all_t:
        merged = np.concatenate(all_t)
        default_t_min = float(np.min(merged))
        default_t_max = float(np.max(merged))
        if default_t_max <= default_t_min:
            default_t_max = default_t_min + 1.0
        pad = max((default_t_max - default_t_min) * 0.05, TDC_LSB_NS)
        default_t_min -= pad
        default_t_max += pad
    else:
        default_t_min, default_t_max = 0.0, 1.0

    channel_range_overrides = (
        PULSE_TIME_2D_Y_RANGE_OPTION1_BY_CHANNEL_NS
        if pulse_time_source == "option1"
        else PULSE_TIME_2D_Y_RANGE_OPTION2_BY_CHANNEL_NS
    )

    for idx, data in enumerate(channel_data):
        ax = axes[idx // ncols][idx % ncols]
        t_min, t_max = channel_range_overrides.get(data["channel"], (default_t_min, default_t_max))
        t = np.asarray(data.get("pulse_time_ns", []), dtype=np.float64)
        adc_vals = np.asarray(data.get(adc_key, []), dtype=np.float64)
        first_cycle_mask = np.asarray(
            data.get("is_first_pulse_in_cycle", np.ones_like(t, dtype=bool)),
            dtype=bool,
        )
        if first_cycle_mask.shape[0] == t.shape[0]:
            t = t[first_cycle_mask]
        if first_cycle_mask.shape[0] == adc_vals.shape[0]:
            adc_vals = adc_vals[first_cycle_mask]

        finite_mask = np.isfinite(t) & np.isfinite(adc_vals)
        t = t[finite_mask]
        adc_vals = adc_vals[finite_mask]

        adc_cut_mask = adc_vals >= adc_min_cut
        t = t[adc_cut_mask]
        data["pulse_time_fwhm_ns"] = np.nan

        if t.size > 0:
            # Build 1D bins from a target bin width (ns), optionally rebinned.
            effective_bin_width_ns = time_bin_width_ns * float(rebin_time)
            t_span = max(t_max - t_min, effective_bin_width_ns)
            n_bins = max(1, int(np.ceil(t_span / effective_bin_width_ns)))
            counts, edges, _ = ax.hist(
                t,
                bins=n_bins,
                range=(t_min, t_max),
                histtype="stepfilled",
                color="steelblue",
                alpha=0.65,
                edgecolor="black",
                linewidth=0.3,
            )
            mean_t = float(np.mean(t))
            fwhm = histogram_fwhm(counts.astype(np.float64), edges.astype(np.float64))
            if fwhm is not None:
                data["pulse_time_fwhm_ns"] = fwhm
                legend_label = f"mean={mean_t:.2f} ns\nFWHM={fwhm:.2f} ns"
            else:
                legend_label = f"mean={mean_t:.2f} ns\nFWHM=N/A"
            if dataset_tag is not None:
                legend_label += f"\n{dataset_tag}"
            ax.axvline(
                mean_t,
                color="darkred",
                linestyle="--",
                linewidth=1.2,
                label=legend_label,
            )
            ax.legend(fontsize=7, loc="upper right")
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
            if dataset_tag is not None:
                ax.plot([], [], " ", label=dataset_tag)
                ax.legend(fontsize=7, loc="upper right")

        ax.set_xlim(t_min, t_max)
        ax.set_title(f"Ch {data['channel']:02d}")
        ax.set_xlabel(data.get("pulse_time_label", "Pulse time [ns]"))
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(channel_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(f"{title} ({pulse_time_source}, first pulse/cycle)")
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_{output_suffix}")
    return fig


def plot_pulse_time_fwhm_vs_channel(
    channel_data: list[dict],
    output_dir: str,
    stem: str,
    pulse_time_source: str,
    tts_data: list[dict] | None = None,
    dataset_tag: str | None = None,
) -> plt.Figure | None:
    """Plot pulse-time FWHM vs channel, optionally overlaid with TTS FWHM."""
    channels = []
    fwhm_values = []

    for data in channel_data:
        fwhm = data.get("pulse_time_fwhm_ns", np.nan)
        if fwhm is None or not np.isfinite(fwhm):
            continue
        channels.append(data["channel"])
        fwhm_values.append(float(fwhm))

    if not channels:
        print("No valid pulse-time FWHM values available for channel plot.")
        return None

    channels_arr = np.asarray(channels, dtype=np.float64)
    fwhm_arr = np.asarray(fwhm_values, dtype=np.float64)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.plot(
        channels_arr,
        fwhm_arr,
        "o-",
        color="firebrick",
        markersize=5,
        linewidth=1.5,
        label="Pulse-time FWHM",
    )

    if tts_data:
        tts_channels: list[float] = []
        tts_fwhm_values: list[float] = []
        tts_bin_width_ns = 0.15
        for row in tts_data:
            values = np.asarray(row.get("tts", []), dtype=np.float64)
            values = values[np.isfinite(values)]
            if values.size == 0:
                continue
            vmin = float(np.min(values))
            vmax = float(np.max(values))
            if not np.isfinite(vmin) or not np.isfinite(vmax):
                continue
            if vmax <= vmin:
                vmax = vmin + tts_bin_width_ns
            pad = max(0.05 * (vmax - vmin), tts_bin_width_ns)
            x_range = (vmin - pad, vmax + pad)
            n_bins = max(1, int(np.ceil((x_range[1] - x_range[0]) / tts_bin_width_ns)))
            counts, edges = np.histogram(values, bins=n_bins, range=x_range)
            tts_fwhm = histogram_fwhm(counts.astype(np.float64), edges.astype(np.float64))
            if tts_fwhm is None or not np.isfinite(tts_fwhm):
                continue
            tts_channels.append(float(row["channel"]))
            tts_fwhm_values.append(float(tts_fwhm))

        if tts_channels:
            tts_channels_arr = np.asarray(tts_channels, dtype=np.float64)
            tts_fwhm_arr = np.asarray(tts_fwhm_values, dtype=np.float64)
            ax.plot(
                tts_channels_arr,
                tts_fwhm_arr,
                "s-",
                color="navy",
                markersize=5,
                linewidth=1.5,
                label="TTS-corrected FWHM",
            )

    ax.set_xlabel("Channel")
    ax.set_ylabel("Pulse-time FWHM [ns]")
    title = f"Pulse-time FWHM vs channel ({pulse_time_source})"
    if dataset_tag is not None:
        title += f" ({dataset_tag})"
    ax.set_title(title)
    ax.set_ylim(bottom=0.0)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xticks(channels_arr)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_pulse_time_fwhm_vs_channel")
    return fig


def get_pulse_time_display_range_by_channel(
    channel_data: list[dict], pulse_time_source: str
) -> tuple[tuple[float, float], dict[int, tuple[float, float]]]:
    """Return default and per-channel pulse-time ranges used for profile extraction."""
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
        default_y_min, default_y_max = custom_range
    elif all_t:
        merged = np.concatenate(all_t)
        default_y_min = float(np.min(merged))
        default_y_max = float(np.max(merged))
        if default_y_max <= default_y_min:
            default_y_max = default_y_min + 1.0
        pad = max((default_y_max - default_y_min) * 0.05, TDC_LSB_NS)
        default_y_min -= pad
        default_y_max += pad
    else:
        default_y_min, default_y_max = 0.0, 1.0

    channel_range_overrides = (
        PULSE_TIME_2D_Y_RANGE_OPTION1_BY_CHANNEL_NS
        if pulse_time_source == "option1"
        else PULSE_TIME_2D_Y_RANGE_OPTION2_BY_CHANNEL_NS
    )
    return (default_y_min, default_y_max), channel_range_overrides


def fit_timewalk_profile_per_channel(
    channel_data: list[dict],
    pulse_time_source: str,
    adc_key: str = "adc_pedestal_corrected",
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    adc_min_cut: float = ADC_THRESHOLD_DEFAULT,
    profile_x_bins: int = 40,
    profile_min_counts: int = 20,
) -> list[dict]:
    """Fit pulse-time profile vs ADC for each channel with C + A*exp(-adc/B).

    Uses the same restricted pulse-time Y-ranges as the extracted profile plots.
    """
    fit_results: list[dict] = []
    (default_y_min, default_y_max), channel_range_overrides = get_pulse_time_display_range_by_channel(
        channel_data, pulse_time_source
    )

    for data in channel_data:
        adc_vals = np.asarray(data.get(adc_key, []), dtype=np.float64)
        pulse_time_ns = np.asarray(data.get("pulse_time_ns", []), dtype=np.float64)
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

        cut_mask = (
            (adc_vals > adc_min_cut)
            & (adc_vals >= adc_range[0])
            & (adc_vals <= adc_range[1])
        )
        adc_vals = adc_vals[cut_mask]
        pulse_time_ns = pulse_time_ns[cut_mask]

        y_min, y_max = channel_range_overrides.get(data["channel"], (default_y_min, default_y_max))
        y_mask = (pulse_time_ns >= y_min) & (pulse_time_ns <= y_max)
        adc_vals = adc_vals[y_mask]
        pulse_time_ns = pulse_time_ns[y_mask]

        x_edges = np.linspace(adc_range[0], adc_range[1], profile_x_bins + 1)
        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])

        x_bin_idx = np.digitize(adc_vals, x_edges) - 1
        in_x_range = (x_bin_idx >= 0) & (x_bin_idx < profile_x_bins)
        x_bin_idx = x_bin_idx[in_x_range]
        y_in_range = pulse_time_ns[in_x_range]

        counts = np.bincount(x_bin_idx, minlength=profile_x_bins)
        sum_y = np.bincount(x_bin_idx, weights=y_in_range, minlength=profile_x_bins)
        sum_y2 = np.bincount(x_bin_idx, weights=y_in_range * y_in_range, minlength=profile_x_bins)

        mean_y = np.divide(sum_y, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        mean_y2 = np.divide(sum_y2, counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)
        var_y = np.clip(mean_y2 - mean_y * mean_y, a_min=0.0, a_max=None)
        sem_y = np.sqrt(var_y / counts, out=np.full(profile_x_bins, np.nan), where=counts > 0)

        profile_mask = (counts >= profile_min_counts) & np.isfinite(mean_y) & np.isfinite(sem_y)
        x_fit = x_centers[profile_mask]
        y_fit = mean_y[profile_mask]
        y_err = sem_y[profile_mask]

        result = {
            "channel": data["channel"],
            "fit_success": False,
            "x_profile": x_fit,
            "y_profile": y_fit,
            "yerr_profile": y_err,
            "n_profile_points": int(x_fit.size),
        }

        if x_fit.size < 4:
            fit_results.append(result)
            continue

        c_guess = float(np.median(y_fit[max(0, y_fit.size // 2) :]))
        a_guess = float(y_fit[0] - c_guess)
        b_guess = max(5.0, 0.2 * (adc_range[1] - adc_range[0]))

        try:
            popt, pcov = curve_fit(
                timewalk_model,
                x_fit,
                y_fit,
                p0=[c_guess, a_guess, b_guess],
                sigma=y_err,
                absolute_sigma=True,
                bounds=([-np.inf, -np.inf, 1e-6], [np.inf, np.inf, np.inf]),
                maxfev=20_000,
            )
            perr = np.sqrt(np.diag(pcov))
            y_pred = timewalk_model(x_fit, *popt)
            chi2 = float(np.sum(((y_fit - y_pred) / y_err) ** 2))
            ndf = int(x_fit.size - 3)
            chi2_ndf = chi2 / ndf if ndf > 0 else np.nan

            result.update(
                {
                    "fit_success": True,
                    "C": float(popt[0]),
                    "A": float(popt[1]),
                    "B": float(popt[2]),
                    "C_err": float(perr[0]),
                    "A_err": float(perr[1]),
                    "B_err": float(perr[2]),
                    "chi2": chi2,
                    "ndf": ndf,
                    "chi2_ndf": chi2_ndf,
                }
            )
        except (RuntimeError, ValueError, OverflowError, FloatingPointError):
            pass

        fit_results.append(result)

    return fit_results


def plot_timewalk_fit_grid(
    fit_results: list[dict],
    output_dir: str,
    stem: str,
    adc_range: tuple[float, float] = ADC_CORRECTED_RANGE,
    dataset_tag: str | None = None,
) -> plt.Figure:
    """Plot per-channel pulse-time profile points and exponential fit curves."""
    nrows, ncols = _grid_shape(len(fit_results))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, fit in enumerate(fit_results):
        ax = axes[idx // ncols][idx % ncols]
        x = np.asarray(fit.get("x_profile", []), dtype=np.float64)
        y = np.asarray(fit.get("y_profile", []), dtype=np.float64)
        yerr = np.asarray(fit.get("yerr_profile", []), dtype=np.float64)

        if x.size > 0:
            ax.errorbar(
                x,
                y,
                yerr=yerr,
                fmt="o",
                markersize=3,
                color="black",
                ecolor="gray",
                elinewidth=0.8,
                capsize=2,
                alpha=0.9,
                label="Profile mean ± SEM",
            )

        if fit.get("fit_success", False):
            xx = np.linspace(adc_range[0], adc_range[1], 300)
            yy = timewalk_model(xx, fit["C"], fit["A"], fit["B"])
            label = (
                f"C={fit['C']:.3g}, A={fit['A']:.3g}, B={fit['B']:.3g}\n"
                f"chi2/ndf={fit['chi2_ndf']:.2f}"
            )
            ax.plot(xx, yy, color="crimson", linewidth=1.8, label=label)

        ax.set_xlim(*adc_range)
        ax.set_title(f"Ch {fit['channel']:02d}")
        ax.set_xlabel("Pedestal-corrected ADC")
        ax.set_ylabel("Pulse time [ns]")
        ax.grid(True, linestyle="--", alpha=0.4)
        if dataset_tag is not None:
            ax.plot([], [], " ", label=dataset_tag)
        if x.size > 0 or fit.get("fit_success", False) or dataset_tag is not None:
            ax.legend(fontsize=7, loc="upper right")

    for idx in range(len(fit_results), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle("Pulse-time profile fits by channel: C + A*exp(-ADC/B)")
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_timewalk_profile_fit_grid")
    return fig


def plot_timewalk_chi2ndf_vs_channel(
    fit_results: list[dict], output_dir: str, stem: str, dataset_tag: str | None = None
) -> plt.Figure | None:
    """Plot chi2/ndf of time-walk fits vs channel."""
    channels = []
    chi2ndf = []
    for fit in fit_results:
        if not fit.get("fit_success", False):
            continue
        value = fit.get("chi2_ndf", np.nan)
        if value is None or not np.isfinite(value):
            continue
        channels.append(fit["channel"])
        chi2ndf.append(float(value))

    if not channels:
        print("No successful time-walk fits available for chi2/ndf plot.")
        return None

    x = np.asarray(channels, dtype=np.float64)
    y = np.asarray(chi2ndf, dtype=np.float64)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.plot(x, y, "o-", color="darkgreen", linewidth=1.5, markersize=5)
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Channel")
    ax.set_ylabel("chi2/ndf")
    title = "Time-walk fit quality vs channel"
    if dataset_tag is not None:
        title += f" ({dataset_tag})"
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xticks(x)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_timewalk_fit_chi2ndf_vs_channel")
    return fig


def plot_timewalk_parameter_histograms(
    fit_results: list[dict], output_dir: str, stem: str, dataset_tag: str | None = None
) -> plt.Figure | None:
    """Plot channel-wise distributions of fitted C, A, B parameters."""
    params = {"C": [], "A": [], "B": []}
    for fit in fit_results:
        if not fit.get("fit_success", False):
            continue
        for key in params:
            value = fit.get(key, np.nan)
            if value is not None and np.isfinite(value):
                params[key].append(float(value))

    if not params["C"] or not params["A"] or not params["B"]:
        print("No complete C/A/B fit-parameter set available for histogram plot.")
        return None

    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.2))
    colors = {"C": "royalblue", "A": "darkorange", "B": "seagreen"}
    for ax, key in zip(axes, ("C", "A", "B")):
        values = np.asarray(params[key], dtype=np.float64)
        bins = max(10, int(np.sqrt(values.size)))
        ax.hist(values, bins=bins, histtype="stepfilled", alpha=0.65, color=colors[key], edgecolor="black")
        ax.set_xlabel(key)
        ax.set_ylabel("Channels")
        ax.set_title(f"{key} over channels")
        ax.grid(True, linestyle="--", alpha=0.4)

    title = "Time-walk fit parameter distributions"
    if dataset_tag is not None:
        title += f" ({dataset_tag})"
    fig.suptitle(title)
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_timewalk_fit_param_histograms")
    return fig


def build_tts_from_second_tree_pass(
    arrays: dict,
    fit_results: list[dict],
    pedestal_by_channel: dict[int, float],
    pulse_time_source: str,
    pmt_pulse_modulo_ticks: int,
    adc_min_cut: float,
    adc_range: tuple[float, float],
    default_pulse_time_range: tuple[float, float],
    pulse_time_range_by_channel: dict[int, tuple[float, float]],
) -> list[dict]:
    """Second pass over tree arrays to build event-wise corrected TTS.

    Correction requested by user:
        TTS_corr = pulse_time - fit(ADC) + C
    where fit(ADC) = C + A * exp(-ADC/B) from per-channel profile fits.
    Selection for TTS filling uses the same restricted pulse-time window and
    ADC cuts/range used to build profile points and fits.
    """
    fit_by_channel: dict[int, tuple[float, float, float]] = {}
    for fit in fit_results:
        if not fit.get("fit_success", False):
            continue
        fit_by_channel[int(fit["channel"])] = (fit["C"], fit["A"], fit["B"])

    channel = arrays["channel"].astype(np.int64)
    adc = arrays["adc"].astype(np.float64)
    pmt_time = arrays["pmt_time"].astype(np.int64)
    tdc_start = arrays["tdc_start"].astype(np.int64)

    tts_data: list[dict] = []
    for raw_ch in sorted(np.unique(channel).tolist()):
        display_ch = int(raw_ch) + 1
        if display_ch not in fit_by_channel:
            continue
        pedestal = pedestal_by_channel.get(display_ch)
        if pedestal is None or not np.isfinite(pedestal):
            continue

        mask = channel == raw_ch
        adc_ch = adc[mask]
        pmt_time_ch = pmt_time[mask]
        tdc_start_ch = tdc_start[mask]

        pulse_time_ns, pulse_time_label = compute_pulse_time_ns(
            pmt_time_ch,
            tdc_start_ch,
            pulse_time_source=pulse_time_source,
            pmt_pulse_modulo_ticks=pmt_pulse_modulo_ticks,
        )
        cycle_index = np.floor_divide(pmt_time_ch.astype(np.int64), np.int64(pmt_pulse_modulo_ticks))
        first_cycle_mask = first_pulse_in_cycle_mask(pulse_time_ns, cycle_index)
        y_min, y_max = pulse_time_range_by_channel.get(display_ch, default_pulse_time_range)

        adc_corr = adc_ch - pedestal
        finite_mask = np.isfinite(adc_corr) & np.isfinite(pulse_time_ns)
        keep = (
            finite_mask
            & first_cycle_mask
            & (adc_corr >= adc_min_cut)
            & (adc_corr <= adc_range[1])
            & (pulse_time_ns >= y_min)
            & (pulse_time_ns <= y_max)
        )

        adc_corr = adc_corr[keep]
        pulse_time_ns = pulse_time_ns[keep]
        if adc_corr.size == 0:
            continue

        c0, a0, b0 = fit_by_channel[display_ch]
        fit_time = timewalk_model(adc_corr, c0, a0, b0)
        valid = np.isfinite(fit_time) & (fit_time > 0.0)
        if not np.any(valid):
            continue

        tts = pulse_time_ns[valid] - fit_time[valid] + c0
        tts = tts[np.isfinite(tts)]
        if tts.size == 0:
            continue

        tts_data.append(
            {
                "channel": display_ch,
                "tts": tts,
                "pulse_time_label": pulse_time_label,
                "entries": int(tts.size),
            }
        )

    return tts_data


def plot_tts_hist_grid(
    tts_data: list[dict],
    output_dir: str,
    stem: str,
    dataset_tag: str | None = None,
) -> plt.Figure | None:
    """Plot event-by-event TTS histograms per channel."""
    if not tts_data:
        print("No TTS data available to plot.")
        return None

    all_tts = np.concatenate([np.asarray(row["tts"], dtype=np.float64) for row in tts_data])
    all_tts = all_tts[np.isfinite(all_tts)]
    if all_tts.size == 0:
        print("No finite TTS values available to plot.")
        return None

    bin_width_ns = 0.15

    nrows, ncols = _grid_shape(len(tts_data))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)

    for idx, row in enumerate(tts_data):
        ax = axes[idx // ncols][idx % ncols]
        values = np.asarray(row["tts"], dtype=np.float64)
        values = values[np.isfinite(values)]

        if values.size > 0:
            vmin = float(np.min(values))
            vmax = float(np.max(values))
            if not np.isfinite(vmin) or not np.isfinite(vmax):
                vmin, vmax = -1.0, 1.0
            if vmax <= vmin:
                vmax = vmin + bin_width_ns
            pad = max(0.05 * (vmax - vmin), bin_width_ns)
            x_range = (vmin - pad, vmax + pad)
            n_bins = max(1, int(np.ceil((x_range[1] - x_range[0]) / bin_width_ns)))
            counts, edges, _ = ax.hist(
                values,
                bins=n_bins,
                range=x_range,
                histtype="stepfilled",
                color="mediumpurple",
                alpha=0.65,
                edgecolor="black",
                linewidth=0.3,
            )
            mean_v = float(np.mean(values))
            fwhm = histogram_fwhm(counts.astype(np.float64), edges.astype(np.float64))
            if fwhm is not None:
                label = f"mean={mean_v:.4f}\nFWHM={fwhm:.4f}"
            else:
                label = f"mean={mean_v:.4f}\nFWHM=N/A"
            if dataset_tag is not None:
                label += f"\n{dataset_tag}"
            ax.axvline(mean_v, color="darkred", linestyle="--", linewidth=1.2, label=label)
            ax.legend(fontsize=7, loc="upper right")
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

        if values.size > 0:
            ax.set_xlim(*x_range)
        ax.set_title(f"Ch {row['channel']:02d}")
        ax.set_xlabel("TTS_corr = pulse_time - fit(ADC) + C [ns]")
        ax.set_ylabel("Counts")
        ax.grid(True, linestyle="--", alpha=0.4)

    for idx in range(len(tts_data), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle("Event-by-event corrected TTS by channel")
    fig.tight_layout()
    save_figure_dual_format(fig, output_dir, f"{stem}_tts_hist_grid")
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
                f"Channel {data['channel']:02d}: missing pedestal; "
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
        description=(
            "Per-channel pedestal-corrected time-walk/TTS analysis of a pmt_events ROOT file."
        )
    )
    parser.add_argument("input", nargs="?", default=DEFAULT_INPUT, help="Path to input ROOT file.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Base directory for outputs (default: alongside the input file). "
            "Plots are saved as PNG and PDF under png/ and pdf/ subdirectories."
        ),
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
        default="option2",
        help=(
            "Pulse-time definition for the 2D pulse-time-vs-ADC plot: "
            "option1=((pmt_time<<4)+tdc_start)*0.25 ns, "
            "option2=(pmt_time%%25000)*4 ns + tdc_start*0.25 ns."
        ),
    )
    parser.add_argument(
        "--pmt-pulse-modulo-ticks",
        type=int,
        default=PMT_PULSE_MODULO_TICKS,
        help="Modulo period for option2 pulse time (default: %(default)s).",
    )
    parser.add_argument(
        "--adc-threshold",
        "--adc-2d-min-cut",
        dest="adc_threshold",
        type=float,
        default=ADC_THRESHOLD_DEFAULT,
        help=(
            "Global ADC threshold for TTS, ToT, and time-walk plots: "
            "keep only ADC >= value (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--pulse-adc-min-cut",
        type=float,
        default=PULSE_ADC_MIN_CUT_DEFAULT,
        help=(
            "Global ADC lower cut for pulse-time-vs-ADC profile extraction/fits: "
            "keep only ADC > value (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--pulse-adc-subrange-min",
        type=float,
        default=PULSE_PROFILE_ADC_SUBRANGE_DEFAULT[0],
        help="Lower bound of ADC subrange used for pulse-time profiles/fits.",
    )
    parser.add_argument(
        "--pulse-adc-subrange-max",
        type=float,
        default=PULSE_PROFILE_ADC_SUBRANGE_DEFAULT[1],
        help="Upper bound of ADC subrange used for pulse-time profiles/fits.",
    )
    parser.add_argument(
        "--rebin-time",
        type=int,
        default=1,
        help=(
            "Rebin factor for 1D pulse-time histograms (default: %(default)s). "
            "Effective 1D time-bin width is --time-bin-width * rebin-time."
        ),
    )
    parser.add_argument(
        "--time-bin-width",
        type=float,
        default=PULSE_TIME_1D_BIN_WIDTH_NS,
        help=(
            "Base 1D pulse-time histogram bin width in ns (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--pedestal-dir",
        default=None,
        help=(
            "Directory with channel_??.json files holding the 'adc_pedestal' key "
            f"(default: <input dir>/{PEDESTAL_JSON_SUBDIR})."
        ),
    )
    args = parser.parse_args()

    if not np.isfinite(args.second_pass_adc_min):
        raise ValueError("--second-pass-adc-min must be finite")
    if args.pmt_pulse_modulo_ticks <= 0:
        raise ValueError("--pmt-pulse-modulo-ticks must be > 0")
    if not np.isfinite(args.adc_threshold):
        raise ValueError("--adc-threshold must be finite")
    if not np.isfinite(args.pulse_adc_min_cut):
        raise ValueError("--pulse-adc-min-cut must be finite")
    if not np.isfinite(args.pulse_adc_subrange_min) or not np.isfinite(args.pulse_adc_subrange_max):
        raise ValueError("--pulse-adc-subrange-min/max must be finite")
    if args.pulse_adc_subrange_max <= args.pulse_adc_subrange_min:
        raise ValueError("--pulse-adc-subrange-max must be greater than --pulse-adc-subrange-min")
    if args.rebin_time <= 0:
        raise ValueError("--rebin-time must be > 0")
    if not np.isfinite(args.time_bin_width) or args.time_bin_width <= 0:
        raise ValueError("--time-bin-width must be finite and > 0")

    pulse_profile_adc_range = (args.pulse_adc_subrange_min, args.pulse_adc_subrange_max)

    input_file = args.input
    dataset_tag = extract_threshold_tag_from_path(input_file)
    output_dir = args.output_dir or os.path.dirname(os.path.abspath(input_file))
    os.makedirs(output_dir, exist_ok=True)
    png_output_dir = os.path.join(output_dir, "png")
    pdf_output_dir = os.path.join(output_dir, "pdf")
    os.makedirs(png_output_dir, exist_ok=True)
    os.makedirs(pdf_output_dir, exist_ok=True)
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

    pedestal_dir = args.pedestal_dir or os.path.join(
        os.path.dirname(os.path.abspath(input_file)), PEDESTAL_JSON_SUBDIR
    )
    pedestal_by_channel = load_pedestals_from_json(pedestal_dir, channels)

    channel_data = []
    for raw_ch in channels:
        mask = channel == raw_ch
        result = analyze_channel(
            raw_ch,
            pedestal_by_channel.get(raw_ch + 1),
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
        f.write("channel entries pedestal_adc\n")
        for row in channel_data:
            f.write(f"{row['channel']:02d} {row['entries']} {row['pedestal_adc']:.6f}\n")
    print(f"Saved ADC summary to {summary_path}")
    print(f"Saving PNG plots to {png_output_dir}")
    print(f"Saving PDF plots to {pdf_output_dir}")

    if not channel_data:
        print("No channel data available to plot.")
        return

    plot_adc_grid(channel_data, output_dir, stem, dataset_tag=dataset_tag)
    corrected_channel_data = build_pedestal_corrected_channel_data(
        channel_data, second_pass_adc_min=args.second_pass_adc_min
    )
    if not corrected_channel_data:
        print(
            "No channels with a valid pedestal; skipping pedestal-corrected timing and ADC plots."
        )
    else:
        plot_pulse_time_hist_grid(
            corrected_channel_data,
            output_dir,
            stem,
            pulse_time_source=args.pulse_time_source,
            adc_key="adc_pedestal_corrected",
            adc_min_cut=args.adc_threshold,
            rebin_time=args.rebin_time,
            time_bin_width_ns=args.time_bin_width,
            output_suffix=f"pulse_time_{args.pulse_time_source}_hist_grid",
            title=(
                "Pulse time distribution by channel "
                f"(pedestal-corrected ADC>={args.adc_threshold:g})"
            ),
            dataset_tag=dataset_tag,
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
            dataset_tag=dataset_tag,
        )
        plot_tot_vs_adc_grid(
            corrected_channel_data,
            output_dir,
            stem,
            adc_key="adc_pedestal_corrected",
            adc_range=ADC_CORRECTED_RANGE,
            adc_min_cut=args.adc_threshold,
            output_suffix="tot_vs_pedestal_corrected_adc_grid",
            title=f"ToT vs pedestal-corrected ADC by channel (ADC>={args.adc_threshold:g})",
            dataset_tag=dataset_tag,
        )
        plot_pulse_time_vs_adc_grid(
                    corrected_channel_data,
                    output_dir,
                    stem,
                    pulse_time_source=args.pulse_time_source,
                    adc_key="adc_pedestal_corrected",
                    adc_range=pulse_profile_adc_range,
                    adc_min_cut=args.pulse_adc_min_cut,
                    output_suffix=f"pulse_time_{args.pulse_time_source}_vs_pedestal_corrected_adc_grid",
                    title=(
                        "Pulse time vs pedestal-corrected ADC by channel ("
                        + args.pulse_time_source
                        + f", ADC>{args.pulse_adc_min_cut:g}, ADC in [{pulse_profile_adc_range[0]:g}, {pulse_profile_adc_range[1]:g}])"
                    ),
                    dataset_tag=dataset_tag,
                )

        # Fit pulse-time profile vs ADC with C + A*exp(-ADC/B) for each channel.
        timewalk_fit_results = fit_timewalk_profile_per_channel(
            corrected_channel_data,
            pulse_time_source=args.pulse_time_source,
            adc_key="adc_pedestal_corrected",
            adc_range=pulse_profile_adc_range,
            adc_min_cut=args.pulse_adc_min_cut,
            profile_x_bins=40,
            profile_min_counts=20,
        )

        fit_summary_path = os.path.join(output_dir, f"{stem}_timewalk_fit_summary.txt")
        with open(fit_summary_path, "w") as f:
            f.write("channel fit_success n_profile_points C C_err A A_err B B_err chi2 ndf chi2_ndf\n")
            for fit in timewalk_fit_results:
                if fit.get("fit_success", False):
                    f.write(
                        f"{fit['channel']:02d} 1 {fit['n_profile_points']} "
                        f"{fit['C']:.8g} {fit['C_err']:.8g} "
                        f"{fit['A']:.8g} {fit['A_err']:.8g} "
                        f"{fit['B']:.8g} {fit['B_err']:.8g} "
                        f"{fit['chi2']:.8g} {fit['ndf']} {fit['chi2_ndf']:.8g}\n"
                    )
                else:
                    f.write(
                        f"{fit['channel']:02d} 0 {fit['n_profile_points']} "
                        "nan nan nan nan nan nan nan -1 nan\n"
                    )
        print(f"Saved time-walk fit summary to {fit_summary_path}")

        plot_timewalk_fit_grid(
            timewalk_fit_results,
            output_dir,
            stem,
            adc_range=pulse_profile_adc_range,
            dataset_tag=dataset_tag,
        )
        plot_timewalk_chi2ndf_vs_channel(
            timewalk_fit_results,
            output_dir,
            stem,
            dataset_tag=dataset_tag,
        )
        plot_timewalk_parameter_histograms(
            timewalk_fit_results,
            output_dir,
            stem,
            dataset_tag=dataset_tag,
        )

        # Second tree pass: build event-by-event corrected TTS = pulse_time - fit(ADC) + C.
        print("Re-reading tree for second-pass event-by-event TTS filling...")
        arrays_second_pass = load_events(input_file)
        default_pulse_time_range, pulse_time_range_by_channel = get_pulse_time_display_range_by_channel(
            corrected_channel_data, args.pulse_time_source
        )
        tts_data = build_tts_from_second_tree_pass(
            arrays_second_pass,
            timewalk_fit_results,
            pedestal_by_channel,
            pulse_time_source=args.pulse_time_source,
            pmt_pulse_modulo_ticks=args.pmt_pulse_modulo_ticks,
            adc_min_cut=args.adc_threshold,
            adc_range=pulse_profile_adc_range,
            default_pulse_time_range=default_pulse_time_range,
            pulse_time_range_by_channel=pulse_time_range_by_channel,
        )

        tts_summary_path = os.path.join(output_dir, f"{stem}_tts_summary.txt")
        with open(tts_summary_path, "w") as f:
            f.write("channel entries tts_mean tts_std\n")
            for row in tts_data:
                tts = np.asarray(row["tts"], dtype=np.float64)
                mean_v = float(np.mean(tts)) if tts.size > 0 else np.nan
                std_v = float(np.std(tts)) if tts.size > 0 else np.nan
                f.write(f"{row['channel']:02d} {row['entries']} {mean_v:.8g} {std_v:.8g}\n")
        print(f"Saved TTS summary to {tts_summary_path}")

        plot_tts_hist_grid(
            tts_data,
            output_dir,
            stem,
            dataset_tag=dataset_tag,
        )
        plot_pulse_time_fwhm_vs_channel(
            corrected_channel_data,
            output_dir,
            stem,
            pulse_time_source=args.pulse_time_source,
            tts_data=tts_data,
            dataset_tag=dataset_tag,
        )

    report_path = os.path.join(os.path.dirname(os.path.abspath(input_file)), "tts_report.pdf")
    with PdfPages(report_path) as pdf:
        for fig_num in plt.get_fignums():
            pdf.savefig(plt.figure(fig_num))
    print(f"Saved PDF report to {report_path}")

    if tk is None:
        plt.show()
    else:
        plt.show(block=False)
        run_exit_gui()


if __name__ == "__main__":
    main()
