#!/usr/bin/python3

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def resolve_input_txt(input_txt):
    p = Path(input_txt)
    if p.exists():
        return p

    cwd = Path.cwd()
    direct = cwd / p
    if direct.exists():
        return direct

    # Common case: file was moved into a results subdirectory.
    search_roots = [cwd, cwd.parent, cwd.parent.parent, cwd.parent.parent.parent]
    matches = []
    for root in search_roots:
        if root.exists():
            matches.extend(root.glob(f'results/**/{p.name}'))

    if not matches:
        for root in search_roots:
            if root.exists():
                matches.extend(root.rglob(p.name))

    if matches:
        return max(matches, key=lambda x: x.stat().st_mtime)

    raise FileNotFoundError(
        f'Could not find input file "{input_txt}" in current directory or results/**/'
    )


def read_second_column(txt_path):
    vals = []
    with Path(txt_path).open('r') as inp:
        for line in inp:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            try:
                vals.append(float(parts[1]))
            except ValueError:
                continue
    return np.asarray(vals, dtype=float)


def main():
    parser = argparse.ArgumentParser(
        description='Plot 1D histogram of event trace maxima from column 2 of event_trace_maxima_all_events.txt'
    )
    parser.add_argument(
        'input_txt',
        nargs='?',
        default='event_trace_maxima_all_events.txt',
        help='Input text file (default: event_trace_maxima_all_events.txt)'
    )
    parser.add_argument('--bins', type=int, default=100, help='Number of histogram bins (default: 100)')
    parser.add_argument(
        '--xmax',
        type=float,
        default=40.,
        help='Optional override for histogram maximum x-range. If omitted, use data max.'
    )
    parser.add_argument(
        '--xmin',
        type=float,
        default=None,
        help='Optional override for histogram minimum x-range. If omitted, use data min.'
    )
    args = parser.parse_args()

    try:
        input_path = resolve_input_txt(args.input_txt)
    except FileNotFoundError as ex:
        raise SystemExit(str(ex))

    vals = read_second_column(input_path)
    if vals.size == 0:
        raise SystemExit(f'No numeric values found in second column of {input_path}')

    data_min = float(np.min(vals))
    data_max = float(np.max(vals))
    xmin = data_min if args.xmin is None else float(args.xmin)
    xmax = data_max if args.xmax is None else float(args.xmax)

    if xmax <= xmin:
        raise SystemExit(f'Invalid x-range: xmin={xmin}, xmax={xmax}')

    vals_in_range = vals[(vals >= xmin) & (vals <= xmax)]
    if vals_in_range.size == 0:
        raise SystemExit(f'No values in selected range [{xmin}, {xmax}]')

    print(f'Input file: {input_path}')
    print(f'Rows read: {vals.size}')
    print(f'Data min/max: {data_min} / {data_max}')
    print(f'Histogram range: [{xmin}, {xmax}]')
    print(f'Values in range: {vals_in_range.size}')

    counts, edges = np.histogram(vals_in_range, bins=args.bins, range=(xmin, xmax))
    counts_plot = np.log1p(counts)
    widths = np.diff(edges)

    plt.figure(figsize=(10, 6))
    plt.bar(edges[:-1], counts_plot, width=widths, align='edge', color='steelblue', alpha=0.85)
    plt.xlabel('Event trace maxima (column 2)')
    plt.ylabel('log(1 + entries)')
    plt.title('Histogram of event trace maxima (log(1+n) counts)')
    plt.tight_layout()

    stem = input_path.stem
    out_png = f'{stem}_hist.png'
    out_pdf = f'{stem}_hist.pdf'
    plt.savefig(out_png)
    plt.savefig(out_pdf)
    print(f'Saved {out_png} and {out_pdf}')
    plt.show()


if __name__ == '__main__':
    main()
