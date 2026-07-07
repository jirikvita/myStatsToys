#!/usr/bin/python

# jk Oct 2025

import ROOT

import sys

# see $PYTHONPATH
from mystyle import *
from pathlib import Path


def safe_tag(name):
    """Return a filename-safe tag for ROOT object and image names."""
    return ''.join(ch if ch.isalnum() or ch in ('_', '-') else '_' for ch in name)


def parse_lecroy_txt(txt_path):
    """Parse LeCroy exported txt file and return a list of ROOT.TGraph waveforms."""
    waveforms = []
    current = None
    last_time = None
    in_data_section = False
    pending_segment_index = 0

    with open(txt_path, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # Segment marker line like: #1,02-Jul-2026 16:30:43,0
            if line.startswith('#') and ',' in line:
                pending_segment_index += 1
                tag = safe_tag(f'{txt_path.stem}_seg{pending_segment_index:04d}')
                current = ROOT.TGraph()
                current.SetName(f'gr_{tag}')
                waveforms.append(current)
                last_time = None
                in_data_section = False
                continue

            # Column header line that starts data rows
            if line.lower().startswith('time,'):
                in_data_section = True
                if current is None:
                    # Handles files that do not include explicit #segment lines.
                    pending_segment_index += 1
                    tag = safe_tag(f'{txt_path.stem}_seg{pending_segment_index:04d}')
                    current = ROOT.TGraph()
                    current.SetName(f'gr_{tag}')
                    waveforms.append(current)
                continue

            if not in_data_section:
                continue

            parts = line.split(',')
            if len(parts) < 2:
                continue

            try:
                t_ns = 1e9 * float(parts[0])
                amp = float(parts[1])
            except ValueError:
                continue

            if current is None:
                pending_segment_index += 1
                tag = safe_tag(f'{txt_path.stem}_seg{pending_segment_index:04d}')
                current = ROOT.TGraph()
                current.SetName(f'gr_{tag}')
                waveforms.append(current)

            # Fallback split: if time restarts/decreases, start a new waveform.
            if last_time is not None and t_ns < last_time and current.GetN() > 0:
                pending_segment_index += 1
                tag = safe_tag(f'{txt_path.stem}_seg{pending_segment_index:04d}')
                current = ROOT.TGraph()
                current.SetName(f'gr_{tag}')
                waveforms.append(current)

            current.AddPoint(t_ns, amp)
            last_time = t_ns

    # Drop empty graphs if any were created while parsing malformed sections.
    return [gr for gr in waveforms if gr.GetN() > 0]


def choose_color(index):
    colors = [
        ROOT.kRed + 1,
        ROOT.kAzure + 1,
        ROOT.kGreen + 2,
        ROOT.kOrange + 7,
        ROOT.kMagenta + 1,
        ROOT.kCyan + 1,
        ROOT.kYellow + 2,
        ROOT.kViolet + 1,
        ROOT.kTeal + 2,
        ROOT.kPink + 6,
    ]
    return colors[index % len(colors)]


def plot_waveforms(txt_path, waveforms):
    """Plot all waveforms of a file on one canvas and save PNG output."""
    if not waveforms:
        return

    cn = f'can_{safe_tag(txt_path.stem)}'
    c = ROOT.TCanvas(cn, cn, 0, 0, 1000, 700)
    mg = ROOT.TMultiGraph()
    mg.SetTitle('')

    leg = ROOT.TLegend(0.70, 0.70, 0.93, 0.93)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.025)
    leg.SetTextColor(ROOT.kWhite)

    for i, gr in enumerate(waveforms):
        col = choose_color(i)
        gr.SetLineColor(col)
        gr.SetMarkerColor(col)
        gr.SetLineWidth(2)
        mg.Add(gr, 'L')

        if i < 20:
            leg.AddEntry(gr, f'wf {i + 1}', 'l')

    mg.Draw('A')
    mg.GetXaxis().SetTitle('t [ns]')
    mg.GetYaxis().SetTitle('A [V]')
    mg.GetXaxis().SetAxisColor(ROOT.kWhite)
    mg.GetXaxis().SetLabelColor(ROOT.kWhite)
    mg.GetXaxis().SetTitleColor(ROOT.kWhite)
    mg.GetYaxis().SetAxisColor(ROOT.kWhite)
    mg.GetYaxis().SetLabelColor(ROOT.kWhite)
    mg.GetYaxis().SetTitleColor(ROOT.kWhite)

    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)
    if len(waveforms) <= 20:
        leg.Draw()
    ROOT.gPad.Update()

    out_name = f'gr_waveforms_{safe_tag(txt_path.stem)}.png'
    c.Print(out_name)
    return c, mg, leg


##########################################
def main(argv):
    if len(argv) < 2:
        print(f'Usage: {argv[0]} input_path [-b]')
        print(f'  input_path: concrete .txt file or directory containing .txt files')
        print(f'Example (single file): {argv[0]} MCP/data.txt -b')
        print(f'Example (directory):   {argv[0]} MCP/ -b')
        return

    input_path = Path(argv[1])
    if not input_path.exists():
        print(f'Error: {input_path} does not exist')
        return

    batch = False
    if len(argv) > 2:
        if argv[2] == '-b':
            batch = True
    if batch:
        ROOT.gROOT.SetBatch(1)

    SetDarkStyle()

    txt_files = []
    if input_path.is_file():
        if input_path.suffix.lower() != '.txt':
            print(f'Error: {input_path} is not a .txt file')
            return
        txt_files = [input_path]
    elif input_path.is_dir():
        txt_files = sorted(input_path.glob('*.txt'))
        if not txt_files:
            print(f'No .txt files found in {input_path}')
            return
    else:
        print(f'Error: {input_path} is neither a file nor a directory')
        return

    total_waveforms = 0
    plot_objects = []
    for txt_file in txt_files:
        print(f'Processing {txt_file} ...')
        waveforms = parse_lecroy_txt(txt_file)
        n_wf = len(waveforms)
        total_waveforms += n_wf
        print(f'  -> recognized {n_wf} waveform(s)')

        if n_wf == 0:
            print('  -> warning: no waveform points found')
            continue

        objs = plot_waveforms(txt_file, waveforms)
        if objs is not None:
            plot_objects.append(objs)

    if not batch:
        print('Interactive mode: close ROOT canvas window(s) to exit.')
        ROOT.gApplication.Run()



###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################
