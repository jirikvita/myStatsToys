import ROOT
import os

class PMTAnalyzer:
    def __init__(self, root_file_path):
        """Initialize the PMT analyzer with a ROOT file."""
        self.root_file = ROOT.TFile(root_file_path)
        self.tree = self.root_file.Get("pmt_events")
        
        if not self.tree:
            raise ValueError("TTree 'pmt_events' not found in ROOT file")
    
    def plot_variables(self, x_var="adc", y_var="tdc_coarse", output_file=None):
        """Plot two variables from the TTree."""
        n_entries = self.tree.GetEntries()

        if not hasattr(self.tree, x_var):
            raise ValueError(f"Branch '{x_var}' not found in TTree")
        if not hasattr(self.tree, y_var):
            raise ValueError(f"Branch '{y_var}' not found in TTree")
        if not hasattr(self.tree, "channel"):
            raise ValueError("Branch 'channel' not found in TTree")

        if n_entries == 0:
            raise ValueError("No entries found in TTree")

        x_min = 0
        x_max = 4096
        y_min = 0
        y_max = 128 # 256e6
        """
        x_min = None
        x_max = None
        y_min = None
        y_max = None
        print("Determining variable ranges...")
        for i in range(n_entries):
            self.tree.GetEntry(i)
            if i % 10000 == 0:
                print(f"Analyzing entry {i}/{n_entries} for range calculation...")
            x_val = float(getattr(self.tree, x_var))
            y_val = float(getattr(self.tree, y_var))

            if x_min is None or x_val < x_min:
                x_min = x_val
            if x_max is None or x_val > x_max:
                x_max = x_val
            if y_min is None or y_val < y_min:
                y_min = y_val
            if y_max is None or y_val > y_max:
                y_max = y_val

        def expanded_range(v_min, v_max):
            if v_min == v_max:
                width = 1.0 if v_min == 0.0 else abs(v_min) * 0.1
                return v_min - width, v_max + width
            margin = (v_max - v_min) * 0.05
            return v_min - margin, v_max + margin

        x_min, x_max = expanded_range(x_min, x_max)
        y_min, y_max = expanded_range(y_min, y_max)
        """
        bins_1d = 100
        bins_2d = 100
        channels = range(19)
        h_x = {}
        h_y = {}
        h_xy = {}

        for ch in channels:
            h_x[ch] = ROOT.TH1D(
                f"h_{x_var}_ch{ch}",
                f"{x_var} (channel {ch});{x_var};Counts",
                bins_1d,
                x_min,
                x_max,
            )
            h_y[ch] = ROOT.TH1D(
                f"h_{y_var}_ch{ch}",
                f"{y_var} (channel {ch});{y_var};Counts",
                bins_1d,
                y_min,
                y_max,
            )
            h_xy[ch] = ROOT.TH2D(
                f"h2_{y_var}_vs_{x_var}_ch{ch}",
                f"{y_var} vs {x_var} (channel {ch});{x_var};{y_var}",
                bins_2d,
                x_min,
                x_max,
                bins_2d,
                y_min,
                y_max,
            )
            h_x[ch].SetStats(0)
            h_y[ch].SetStats(0)
            h_xy[ch].SetStats(0)

        entriesToGoThrough = min(n_entries, 10000)
        print(f"Processing {entriesToGoThrough:,} entries...")
        skipped_channels = 0
        for i in range(entriesToGoThrough):
            self.tree.GetEntry(i)
            if i % 10000 == 0:
                print(f"Processing entry {i:1,}/{n_entries:,}...")

            channel = int(getattr(self.tree, "channel"))
            if channel < 0 or channel > 18:
                skipped_channels += 1
                continue

            x_val = float(getattr(self.tree, x_var))
            y_val = float(getattr(self.tree, y_var))
            h_x[channel].Fill(x_val)
            h_y[channel].Fill(y_val)
            h_xy[channel].Fill(x_val, y_val)

        if skipped_channels:
            print(f"Skipped {skipped_channels} entries with channel outside [0, 18].")

        ROOT.gStyle.SetPalette(1)
        canvas_xy = ROOT.TCanvas("canvas_xy", f"{y_var} vs {x_var} by channel", 2200, 1200)
        canvas_x = ROOT.TCanvas("canvas_x", f"{x_var} by channel", 2200, 1200)
        canvas_y = ROOT.TCanvas("canvas_y", f"{y_var} by channel", 2200, 1200)

        canvas_xy.Divide(5, 4)
        canvas_x.Divide(5, 4)
        canvas_y.Divide(5, 4)

        for pad, ch in enumerate(channels, start=1):
            canvas_xy.cd(pad)
            h_xy[ch].Draw("COLZ")

            canvas_x.cd(pad)
            h_x[ch].SetLineWidth(2)
            h_x[ch].Draw("HIST")

            canvas_y.cd(pad)
            h_y[ch].SetLineWidth(2)
            h_y[ch].Draw("HIST")

        canvas_xy.Update()
        canvas_x.Update()
        canvas_y.Update()
        
        if output_file:
            base, ext = os.path.splitext(output_file)
            if not ext:
                ext = ".png"
            canvas_xy.SaveAs(f"{base}_xy_by_channel{ext}")
            canvas_x.SaveAs(f"{base}_x_by_channel{ext}")
            canvas_y.SaveAs(f"{base}_y_by_channel{ext}")
        
        # Keep references to avoid premature garbage collection in PyROOT.
        canvas_xy._h_xy = h_xy
        canvas_x._h_x = h_x
        canvas_y._h_y = h_y

        return [canvas_xy, canvas_x, canvas_y]
    
    def close(self):
        """Close the ROOT file."""
        self.root_file.Close()


def main():
    print("Starting PMT event analysis...")
    analyzer = PMTAnalyzer("led_scan_20260427_165238/ledscan_att0_20260427_165325.root")
    print("Plotting variables...")
    canvases = analyzer.plot_variables(output_file="pmt_plot.png")
    print("Analysis complete. Plot saved as 'pmt_plot.png'.")
    ROOT.gApplication.Run()
    analyzer.close()


if __name__ == "__main__":
    main()