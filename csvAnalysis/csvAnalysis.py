#!/usr/bin/env python3

"""Read the CSV in this directory and plot:
1. 1D histograms of every numeric variable,
2. 2D scatter plots of every pair of variables,
3. 2D binned (density) plots of every pair of variables.
Each 2D plot is annotated with the Pearson correlation coefficient.
Non-numeric columns (e.g. Timestamp) are skipped.
"""
import itertools
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BINS_1D = 5
BINS_2D = 5


def find_csv():
    here = Path(__file__).resolve().parent
    files = sorted(here.glob("*.csv"))
    if not files:
        sys.exit(f"No CSV file found in {here}")
    return files[0]


def short(name, n=35):
    return name if len(name) <= n else name[: n - 1] + "…"


def grid(n, title):
    cols = min(3, n)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)
    fig.suptitle(title)
    flat = axes.ravel()
    for ax in flat[n:]:
        ax.set_visible(False)
    return fig, flat


def main():
    path = find_csv()
    df = pd.read_csv(path)
    num = df.apply(pd.to_numeric, errors="coerce")
    num = num.loc[:, num.notna().sum() > 0.5 * len(df)]  # keep mostly-numeric columns
    skipped = [c for c in df.columns if c not in num.columns]
    print(f"{path.name}: {len(df)} rows; numeric columns: {list(num.columns)}; skipped: {skipped}")

    corr = num.corr(method="pearson")
    print("\nPearson correlation matrix:\n", corr.round(3))

    # 1. 1D histograms
    fig, axes = grid(len(num.columns), "1D histograms")
    for ax, col in zip(axes, num.columns):
        s = num[col].dropna()
        ax.hist(s, bins=BINS_1D, color="steelblue", edgecolor="black")
        ax.set_title(short(col))
        ax.set_xlabel(short(col))
        ax.set_ylabel("Count")
        ax.text(0.97, 0.95, f"mean={s.mean():.3g}\nstd={s.std():.3g}", transform=ax.transAxes,
                ha="right", va="top", fontsize=8, bbox=dict(fc="white", alpha=0.7))
    fig.tight_layout()

    pairs = list(itertools.combinations(num.columns, 2))
    if pairs:
        # 2. scatter plots
        fig, axes = grid(len(pairs), "2D scatter plots")
        for ax, (x, y) in zip(axes, pairs):
            d = num[[x, y]].dropna()
            ax.scatter(d[x], d[y], color="darkorange", edgecolor="black")
            ax.set_xlabel(short(x))
            ax.set_ylabel(short(y))
            ax.set_title(f"r = {corr.loc[x, y]:.3f}  (n={len(d)})")
        fig.tight_layout()

        # 3. 2D binned plots
        fig, axes = grid(len(pairs), "2D binned plots")
        for ax, (x, y) in zip(axes, pairs):
            d = num[[x, y]].dropna()
            h = ax.hist2d(d[x], d[y], bins=BINS_2D, cmap="viridis")
            fig.colorbar(h[3], ax=ax, label="Count")
            ax.set_xlabel(short(x))
            ax.set_ylabel(short(y))
            ax.set_title(f"r = {corr.loc[x, y]:.3f}  (n={len(d)})")
        fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
