"""
Figure 2(c): Beam-splitter randomized benchmarking (RB) of the BS_i swaps.

For each storage mode M1-S_i (i = 1..7) two panels are produced:
  Top    : process fidelity vs number of gates, raw (blue) and post-selected
           (red), with per-depth error bars and a single-exponential fit.
  Bottom : joint buffer-storage population ratio P11, P10, P01, P00 vs number
           of gates (log scale), with a T1-decay reference line.

The panel shown in the paper is Mode 2 (the BS_2 swap).
Population mapping (from the parity readout): P00=ee, P01=eg, P10=ge, P11=gg.

Data : fig2c_beamsplitter_rb_vs_depth.csv  (per-depth fidelities + populations)
       fig2e_swap_infidelity.csv           (per-gate fidelities, for annotation)
       fig1/../fig1c_frequencies_and_coherences.csv (storage T1 for reference line)
Usage: python plot_fig2c.py          # all modes
       python plot_fig2c.py 2        # single mode
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "fig2c_beamsplitter_rb_vs_depth.csv"))
summ = pd.read_csv(os.path.join(HERE, "fig2e_swap_infidelity.csv")).set_index("mode")

# Storage T1 (us) for the reference decay line, from the Fig 1c source data.
coh = pd.read_csv(os.path.join(HERE, "..", "fig1",
                  "fig1c_frequencies_and_coherences.csv"))
T1_us = {i: float(coh.loc[coh["mode"] == f"Storage {i}", "T1_us"].iloc[0])
         for i in range(1, 8)}
T_GATE_US = 0.5   # approx. beam-splitter swap duration (see main text)

def single_exp(x, a, b, c):
    return a * np.exp(b * x) + c

def plot_mode(m):
    d = df[df["mode"] == m].sort_values("depth")
    x = d["depth"].values
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6), sharex=True)

    # ---- top: process fidelity ----
    for col, ecol, color, lab in [("fid_raw", "fid_raw_err", "navy", "Raw"),
                                   ("fid_post", "fid_post_err", "firebrick", "Post selection")]:
        y, ye = d[col].values, d[ecol].values
        ax1.errorbar(x, y, yerr=ye, fmt="o", ms=4, color=color, label=lab)
        try:
            p, _ = curve_fit(single_exp, x, y, p0=[1, -1e-3, 0], maxfev=10000)
            xf = np.linspace(x.min(), x.max(), 300)
            ax1.plot(xf, single_exp(xf, *p), "--", color=color, lw=1)
        except RuntimeError:
            pass
    # Annotated value is the per-SWAP fidelity = gate_fid**1.5 = 100 - swap_infid%
    swap_fid_raw = 100 - summ.loc[m, "swap_infid_raw_pct"]
    swap_fid_post = 100 - summ.loc[m, "swap_infid_post_pct"]
    swap_fid_raw_err = summ.loc[m, "swap_infid_raw_err_pct"]
    swap_fid_post_err = summ.loc[m, "swap_infid_post_err_pct"]
    ax1.text(0.97, 0.78, f"{swap_fid_post:.3f}$\\pm${swap_fid_post_err:.3f}%",
             color="firebrick", ha="right", transform=ax1.transAxes, fontsize=8)
    ax1.text(0.97, 0.62, f"{swap_fid_raw:.3f}$\\pm${swap_fid_raw_err:.3f}%",
             color="navy", ha="right", transform=ax1.transAxes, fontsize=8)
    ax1.set_yscale("log")
    ax1.set_ylabel("Process Fidelity")
    ax1.legend(loc="lower left", frameon=False, fontsize=8)
    ax1.set_title(f"M1-S{m}  beam-splitter RB")

    # ---- bottom: population ratio ----
    pops = [("P11", "P11_err", "teal"), ("P10", "P10_err", "firebrick"),
            ("P01", "P01_err", "orange"), ("P00", "P00_err", "gold")]
    for col, ecol, color in pops:
        ax2.errorbar(x, d[col].values, yerr=d[ecol].values, fmt="o", ms=4,
                     color=color, label=f"$P_{{{col[1:]}}}$")
    xf = np.linspace(x.min(), x.max(), 300)
    ax2.plot(xf, np.exp(-xf * T_GATE_US / T1_us[m]), "k--", lw=1,
             label="$T_1$ decay")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-3, 1.5)
    ax2.set_xlabel("Number of Gates")
    ax2.set_ylabel("Population Ratio")
    ax2.legend(loc="lower left", frameon=False, ncol=2, fontsize=8)

    fig.tight_layout()
    out = os.path.join(HERE, f"fig2c_M1-S{m}.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", os.path.basename(out))

if __name__ == "__main__":
    modes = [int(sys.argv[1])] if len(sys.argv) > 1 else range(1, 8)
    for m in modes:
        plot_mode(m)
