"""
Figure 3(b): random read fidelity vs number of random accesses (size-7 RAQM).

Seven storage-mode survival curves (S1..S7) plus the buffer reference (Ref),
each fit with an exponential RB decay. For the size-7 multiplexed RBAM each RB
step accesses all seven modes, so the number of random accesses = 7 x RB depth;
the single-mode reference uses depth directly.

The legend fidelities are the per-access random-read fidelities (verified to
match all_rbam.csv to 5 decimals); Ref is the buffer's single-qubit RB fidelity.

Data : fig3b_rbam_vs_depth.csv   (series, depth, fidelity, fidelity_err)
       (extract_fig3b.py regenerates it from the h5 files)
Usage: python plot_fig3b.py
"""
import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig3b_rbam_vs_depth.csv"))
N_MODES = 7

# random-read fidelities (+errors) for the legend, from all_rbam.csv (size-7 row)
ALL = "/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets/all_rbam.csv"
read_fid = {}
try:
    a = pd.read_csv(ALL)
    for _, r in a.iterrows():
        if [int(x) for x in re.findall(r"\d+", str(r["mode_list"]))] == list(range(1, 8)):
            fs = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", str(r["rbam_fidelities"]))]
            es = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", str(r["rbam_fidelity_errs"]))]
            read_fid = {f"S{i+1}": (fs[i], es[i]) for i in range(7)}
            break
except FileNotFoundError:
    pass
REF_FID = (0.98641, 0.0006)   # buffer single-qubit RB fidelity (see extraction notes)

def expfunc(x, y0, yscale, x0, decay):
    return y0 + yscale * np.exp(-(x - x0) / decay)

cmap = plt.cm.viridis(np.linspace(0, 0.9, 7))
fig, ax = plt.subplots(figsize=(6, 4.5))

# reference (black)
ref = d[d["series"] == "Ref"].sort_values("depth")
xr = ref["depth"].values
ax.errorbar(xr, ref["fidelity"], yerr=ref["fidelity_err"], fmt="+", color="k",
            ms=7, capsize=2, label=f"Ref  {100*REF_FID[0]:.2f}$\\pm${100*REF_FID[1]:.2f}%")
try:
    p, _ = curve_fit(expfunc, xr, ref["fidelity"], p0=[0.4, 0.6, 0, 50], maxfev=20000)
    xf = np.linspace(0, xr.max(), 300); ax.plot(xf, expfunc(xf, *p), "k-", lw=1)
except RuntimeError:
    pass

# storage modes: x = 7 * depth
for i in range(1, 8):
    s = d[d["series"] == f"S{i}"].sort_values("depth")
    x = s["depth"].values * N_MODES
    c = cmap[i - 1]
    f, e = read_fid.get(f"S{i}", (np.nan, np.nan))
    ax.errorbar(x, s["fidelity"], yerr=s["fidelity_err"], fmt="x", color=c,
                ms=5, capsize=2,
                label=f"BS$_{i}$  {100*f:.2f}$\\pm${100*e:.2f}%")
    try:
        p, _ = curve_fit(expfunc, x, s["fidelity"], p0=[0.4, 0.6, 0, 200], maxfev=20000)
        xf = np.linspace(0, x.max(), 300); ax.plot(xf, expfunc(xf, *p), "-", color=c, lw=1)
    except RuntimeError:
        pass

ax.set_xlabel("Number of Random Accesses")
ax.set_ylabel("Process Fidelity")
ax.set_ylim(0.35, 1.02)
ax.legend(frameon=False, fontsize=7, ncol=2)
fig.tight_layout()
out = os.path.join(HERE, "fig3b.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
