#!/usr/bin/env python3
"""Plot convolutions of Uniform[-A, A] with Gaussian(0, sigma).

The resulting PDF for Z = U + G, where U ~ Uniform[-A, A]
and G ~ Normal(0, sigma), is:

    f_Z(x) = [Phi((x + A)/sigma) - Phi((x - A)/sigma)] / (2A)

For A -> 0, this approaches the Gaussian PDF.
"""

from __future__ import annotations

import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf


SIGMA = 1.3
A_MULTIPLES = [0.1, 0.3, 0.5, 0.75, 1.0, 1.5, 2.]
N_EVENTS = 100_000
HIST_RANGE = (-5.0, 5.0)
HIST_BINS = 100


def gaussian_pdf(x: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian PDF centered at zero."""
    norm = 1.0 / (np.sqrt(2.0 * np.pi) * sigma)
    return norm * np.exp(-0.5 * (x / sigma) ** 2)


def standard_normal_cdf(x: np.ndarray) -> np.ndarray:
    """Standard normal CDF via erf."""
    return 0.5 * (1.0 + erf(x / np.sqrt(2.0)))


def uniform_gaussian_convolution_pdf(x: np.ndarray, A: float, sigma: float) -> np.ndarray:
    """PDF of Uniform[-A, A] convolved with Normal(0, sigma)."""
    if A <= 0:
        return gaussian_pdf(x, sigma)

    upper = (x + A) / sigma
    lower = (x - A) / sigma
    return (standard_normal_cdf(upper) - standard_normal_cdf(lower)) / (2.0 * A)


def shifted_uniform_gaussian_convolution_pdf(
    x: np.ndarray, mu: float, A: float, sigma: float
) -> np.ndarray:
    """PDF of mu + Uniform[-A, A] + Normal(0, sigma)."""
    return uniform_gaussian_convolution_pdf(x - mu, A, sigma)


def _grid_shape(n_items: int) -> tuple[int, int]:
    """Pick a roughly square grid layout for n_items panels."""
    ncols = math.ceil(math.sqrt(n_items))
    nrows = math.ceil(n_items / ncols)
    return nrows, ncols


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot Uniform[-A,A] convolved with Gaussian(0, sigma=1.3)."
    )
    parser.add_argument(
        "--linear-y",
        action="store_true",
        help="Use linear y-axis (default is log-scale y-axis).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=12345,
        help="Random seed for toy generation (default: %(default)s).",
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    A_values = [mult * SIGMA for mult in A_MULTIPLES]

    # Figure 1: original analytic convolution curves.
    max_A = max(A_values)
    x_conv_min = -(max_A + 5.0 * SIGMA)
    x_conv_max = max_A + 5.0 * SIGMA
    x_conv = np.linspace(x_conv_min, x_conv_max, 2000)

    fig_analytic = plt.figure(figsize=(9, 5.5))
    for mult, A in zip(A_MULTIPLES, A_values):
        y = uniform_gaussian_convolution_pdf(x_conv, A, SIGMA)
        plt.plot(x_conv, y, linewidth=2, label=f"A = {mult} sigma ({A:.2f})")

    gaussian_y = gaussian_pdf(x_conv, SIGMA)
    plt.plot(
        x_conv,
        gaussian_y,
        linestyle="--",
        linewidth=2,
        color="black",
        label=f"Gaussian (sigma={SIGMA})",
    )

    plt.title("Analytic curves: Uniform[-A, A] * Gaussian(0, sigma=1.3)")
    plt.xlabel("x")
    plt.ylabel("PDF")
    if not args.linear_y:
        plt.yscale("log")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()

    # Figure 2: toy histograms with Gaussian and convolution fits.
    nrows, ncols = _grid_shape(len(A_values))
    fig, axes = plt.subplots(nrows, ncols, figsize=(6.0 * ncols, 4.4 * nrows), squeeze=False)

    true_A_points = []
    fitted_A_points = []
    fitted_sigma_points = []
    true_A_gauss_points = []
    fitted_sigma_gauss_points = []

    x_plot = np.linspace(HIST_RANGE[0], HIST_RANGE[1], 1000)
    bin_width = (HIST_RANGE[1] - HIST_RANGE[0]) / HIST_BINS

    for idx, (mult, A_true) in enumerate(zip(A_MULTIPLES, A_values)):
        ax = axes[idx // ncols][idx % ncols]

        uniform_samples = rng.uniform(-A_true, A_true, size=N_EVENTS)
        gaussian_samples = rng.normal(loc=0.0, scale=SIGMA, size=N_EVENTS)
        samples = uniform_samples + gaussian_samples

        counts, edges = np.histogram(samples, bins=HIST_BINS, range=HIST_RANGE)
        centers = 0.5 * (edges[:-1] + edges[1:])
        in_range_events = int(np.sum(counts))
        hist_max = max(float(np.max(counts)), 1.0)

        ax.hist(
            samples,
            bins=HIST_BINS,
            range=HIST_RANGE,
            histtype="stepfilled",
            color="lightsteelblue",
            alpha=0.6,
            edgecolor="black",
            linewidth=0.3,
            label=f"Toy data (N={N_EVENTS}, in-range={in_range_events})",
        )

        def gaussian_counts_model(x: np.ndarray, norm: float, mu: float, sigma_fit: float) -> np.ndarray:
            return norm * bin_width * gaussian_pdf(x - mu, sigma_fit)

        p0_gauss = [max(float(in_range_events), 1.0), 0.0, max(float(np.std(samples)), 0.5)]
        bounds_gauss = ([0.0, -2.0, 0.05], [np.inf, 2.0, 8.0])
        gauss_fit = None
        try:
            popt_g, _ = curve_fit(
                gaussian_counts_model,
                centers,
                counts,
                p0=p0_gauss,
                bounds=bounds_gauss,
                maxfev=50_000,
            )
            gauss_fit = popt_g
            y_gauss = gaussian_counts_model(x_plot, *popt_g)
            ax.plot(
                x_plot,
                y_gauss,
                color="crimson",
                linewidth=2,
                linestyle="--",
                label=(
                    "Gaussian fit: "
                    f"mu={popt_g[1]:.3f}, sigma={popt_g[2]:.3f}"
                ),
            )
            true_A_gauss_points.append(A_true)
            fitted_sigma_gauss_points.append(popt_g[2])
        except (RuntimeError, ValueError):
            ax.plot([], [], color="crimson", linestyle="--", label="Gaussian fit: failed")

        def conv_counts_model(
            x: np.ndarray, norm: float, mu: float, A_fit: float, sigma_fit: float
        ) -> np.ndarray:
            return norm * bin_width * shifted_uniform_gaussian_convolution_pdf(
                x, mu, A_fit, sigma_fit
            )

        mu0 = gauss_fit[1] if gauss_fit is not None else 0.0
        sigma0 = gauss_fit[2] if gauss_fit is not None else max(float(np.std(samples)), 0.7)
        p0_conv = [max(float(in_range_events), 1.0), mu0, max(0.1, 0.8 * A_true), sigma0]
        bounds_conv = ([0.0, -2.0, 0.001, 0.05], [np.inf, 2.0, 6.0, 8.0])
        try:
            popt_c, _ = curve_fit(
                conv_counts_model,
                centers,
                counts,
                p0=p0_conv,
                bounds=bounds_conv,
                maxfev=80_000,
            )
            y_conv = conv_counts_model(x_plot, *popt_c)
            ax.plot(
                x_plot,
                y_conv,
                color="darkgreen",
                linewidth=2,
                label=(
                    "Conv fit: "
                    f"mu={popt_c[1]:.3f}, A={popt_c[2]:.3f}, sigma={popt_c[3]:.3f}"
                ),
            )
            true_A_points.append(A_true)
            fitted_A_points.append(popt_c[2])
            fitted_sigma_points.append(popt_c[3])
        except (RuntimeError, ValueError):
            ax.plot([], [], color="darkgreen", label="Conv fit: failed")

        ax.set_title(f"A = {mult} sigma ({A_true:.3f})")
        ax.set_xlabel("x")
        ax.set_ylabel("Counts / bin")
        ax.set_xlim(*HIST_RANGE)
        if not args.linear_y:
            ax.set_yscale("log")
            ax.set_ylim(bottom=0.8)
        ax.set_ylim(top=1.5 * hist_max)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(fontsize=8, loc="upper right")

    for idx in range(len(A_values), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")

    fig.suptitle(
        "Toy histograms (10k events each): Gaussian fit vs Uniform*Gaussian convolution fit"
    )

    # Figure 3: fitted parameters and fractional biases vs true A.
    fig_params, axes_params = plt.subplots(3, 2, figsize=(11.0, 12.4))
    ax_A = axes_params[0][0]
    ax_sigma = axes_params[0][1]
    ax_A_frac = axes_params[1][0]
    ax_sigma_frac = axes_params[1][1]
    ax_sigma_gauss = axes_params[2][0]
    ax_sigma_gauss_frac = axes_params[2][1]

    has_conv_points = False
    if true_A_points:
        has_conv_points = True
        x_true = np.asarray(true_A_points)
        y_fit_A = np.asarray(fitted_A_points)
        y_fit_sigma = np.asarray(fitted_sigma_points)
        order = np.argsort(x_true)
        x_true = x_true[order]
        y_fit_A = y_fit_A[order]
        y_fit_sigma = y_fit_sigma[order]
        a_frac = (y_fit_A - x_true) / x_true
        sigma_true = np.full_like(x_true, SIGMA)
        sigma_frac = (y_fit_sigma - sigma_true) / sigma_true

        ax_A.plot(x_true, y_fit_A, "o-", color="darkgreen", label="Fitted A")
        min_a = float(np.min(x_true))
        max_a = float(np.max(x_true))
        ax_A.plot([min_a, max_a], [min_a, max_a], "k--", linewidth=1.5, label="y = x")

        ax_sigma.plot(x_true, y_fit_sigma, "o-", color="royalblue", label="Fitted sigma")
        ax_sigma.axhline(SIGMA, color="black", linestyle="--", linewidth=1.5, label=f"True sigma={SIGMA}")

        ax_A_frac.plot(x_true, a_frac, "o-", color="darkgreen", label="(A_fit-A_true)/A_true")
        ax_A_frac.axhline(0.0, color="black", linestyle="--", linewidth=1.2)

        ax_sigma_frac.plot(
            x_true,
            sigma_frac,
            "o-",
            color="royalblue",
            label="(sigma_fit-sigma_true)/sigma_true",
        )
        ax_sigma_frac.axhline(0.0, color="black", linestyle="--", linewidth=1.2)
    else:
        ax_A.text(0.5, 0.5, "No successful convolution fits", ha="center", va="center")
        ax_sigma.text(0.5, 0.5, "No successful convolution fits", ha="center", va="center")
        ax_A_frac.text(0.5, 0.5, "No successful convolution fits", ha="center", va="center")
        ax_sigma_frac.text(0.5, 0.5, "No successful convolution fits", ha="center", va="center")

    has_gauss_points = False
    if true_A_gauss_points:
        has_gauss_points = True
        x_true_gauss = np.asarray(true_A_gauss_points)
        y_fit_sigma_gauss = np.asarray(fitted_sigma_gauss_points)
        order_g = np.argsort(x_true_gauss)
        x_true_gauss = x_true_gauss[order_g]
        y_fit_sigma_gauss = y_fit_sigma_gauss[order_g]
        sigma_true_gauss = np.full_like(x_true_gauss, SIGMA)
        sigma_gauss_frac = (y_fit_sigma_gauss - sigma_true_gauss) / sigma_true_gauss
        sigma_uniform = 2.0 * x_true_gauss / np.sqrt(12.0)
        sigma_corr = np.sqrt(np.maximum(0.0, y_fit_sigma_gauss**2 - sigma_uniform**2))
        sigma_corr_frac = (sigma_corr - sigma_true_gauss) / sigma_true_gauss

        ax_sigma_gauss.plot(
            x_true_gauss,
            y_fit_sigma_gauss,
            "o-",
            color="crimson",
            label="Single-Gaussian fitted sigma",
        )
        ax_sigma_gauss.axhline(
            SIGMA,
            color="black",
            linestyle="--",
            linewidth=1.5,
            label=f"True sigma={SIGMA}",
        )
        ax_sigma_gauss.plot(
            x_true_gauss,
            sigma_corr,
            "--",
            color="darkorange",
            linewidth=2,
            label="Quadrature-corrected sigma",
        )

        ax_sigma_gauss_frac.plot(
            x_true_gauss,
            sigma_gauss_frac,
            "o-",
            color="crimson",
            label="(sigma_gauss_fit-sigma_true)/sigma_true",
        )
        ax_sigma_gauss_frac.plot(
            x_true_gauss,
            sigma_corr_frac,
            "--",
            color="darkorange",
            linewidth=2,
            label="(sigma_corr-sigma_true)/sigma_true",
        )
        ax_sigma_gauss_frac.axhline(0.0, color="black", linestyle="--", linewidth=1.2)
    else:
        ax_sigma_gauss.text(0.5, 0.5, "No successful Gaussian fits", ha="center", va="center")
        ax_sigma_gauss_frac.text(
            0.5, 0.5, "No successful Gaussian fits", ha="center", va="center"
        )

    ax_A.set_title("Fitted A vs True A")
    ax_A.set_xlabel("True A")
    ax_A.set_ylabel("Fitted A")
    ax_A.grid(True, linestyle="--", alpha=0.4)
    if has_conv_points:
        ax_A.legend()

    ax_sigma.set_title("Fitted sigma vs True A")
    ax_sigma.set_xlabel("True A")
    ax_sigma.set_ylabel("Fitted sigma")
    ax_sigma.set_ylim(bottom=0.0)
    ax_sigma.grid(True, linestyle="--", alpha=0.4)
    if has_conv_points:
        ax_sigma.legend()

    ax_A_frac.set_title("Fractional Bias of A")
    ax_A_frac.set_xlabel("True A")
    ax_A_frac.set_ylabel("(A_fit - A_true) / A_true")
    ax_A_frac.set_ylim(-0.75, 0.75)
    ax_A_frac.grid(True, linestyle="--", alpha=0.4)
    if has_conv_points:
        ax_A_frac.legend()

    ax_sigma_frac.set_title("Fractional Bias of sigma")
    ax_sigma_frac.set_xlabel("True A")
    ax_sigma_frac.set_ylabel("(sigma_fit - sigma_true) / sigma_true")
    ax_sigma_frac.set_ylim(-0.25, 0.25)
    ax_sigma_frac.grid(True, linestyle="--", alpha=0.4)
    if has_conv_points:
        ax_sigma_frac.legend()

    ax_sigma_gauss.set_title("Single-Gaussian Fitted sigma vs True A")
    ax_sigma_gauss.set_xlabel("True A")
    ax_sigma_gauss.set_ylabel("Fitted sigma (single Gaussian)")
    ax_sigma_gauss.set_ylim(0.0, 3.0)
    ax_sigma_gauss.grid(True, linestyle="--", alpha=0.4)
    if has_gauss_points:
        ax_sigma_gauss.legend()

    ax_sigma_gauss_frac.set_title("Fractional Bias of Single-Gaussian sigma")
    ax_sigma_gauss_frac.set_xlabel("True A")
    ax_sigma_gauss_frac.set_ylabel("(sigma_gauss_fit - sigma_true) / sigma_true")
    ax_sigma_gauss_frac.set_ylim(-0.5, 0.5)
    ax_sigma_gauss_frac.grid(True, linestyle="--", alpha=0.4)
    if has_gauss_points:
        ax_sigma_gauss_frac.legend()
    fig_params.tight_layout()

    fig_analytic.savefig("plotConv_analytic.png", dpi=150)
    fig_analytic.savefig("plotConv_analytic.pdf")
    fig.savefig("plotConv_toys.png", dpi=150)
    fig.savefig("plotConv_toys.pdf")
    fig_params.savefig("plotConv_fit_params.png", dpi=150)
    fig_params.savefig("plotConv_fit_params.pdf")

    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.97])
    plt.show()


if __name__ == "__main__":
    main()
