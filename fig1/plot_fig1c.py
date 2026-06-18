"""
Figure 1(c): Frequency spectrum and mode coherence of the RAQM device.

Left panel : mode frequency vs. object category (Readout, Qubit, Buffer,
             Coupler, Storage, Dump).
Right panel: mode frequency vs. coherence time (T1 filled, Ramsey T_R open),
             error bars from repeated fits (Supplementary Table 1).

Data: fig1c_frequencies_and_coherences.csv
Usage: python plot_fig1c.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "fig1c_frequencies_and_coherences.csv"))

# Categorical order for the left panel
cat_order = ["Readout", "Qubit", "Buffer", "Coupler", "Storage", "Dump"]
cat_pos = {c: i for i, c in enumerate(cat_order)}

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(7, 4), sharey=True,
    gridspec_kw={"width_ratios": [1, 1.2], "wspace": 0.05},
)

# ---- Left: frequency vs object category ----
for _, r in df.iterrows():
    axL.errorbar(cat_pos[r["category"]], r["frequency_GHz"],
                 marker="_", ms=16, mew=2, color=rs.PALETTE["ink"], linestyle="none")
axL.set_xticks(range(len(cat_order)))
axL.set_xticklabels(cat_order, rotation=45, ha="right")
axL.set_xlim(-0.5, len(cat_order) - 0.5)
axL.set_ylabel("Frequency (GHz)")
axL.set_xlabel("Object")

# ---- Right: frequency vs coherence (ms) ----
# T1 (filled) and Ramsey T_R (open) for every mode that has them.
fr = df["frequency_GHz"].values
T1, T1e = df["T1_us"].values / 1e3, df["T1_err_us"].values / 1e3
TR, TRe = df["TR_us"].values / 1e3, df["TR_err_us"].values / 1e3

axR.errorbar(T1, fr, xerr=T1e, marker="o", linestyle="none",
             color=rs.PALETTE["slate"], ms=5, label=r"$T_1$")
m = ~np.isnan(TR)
axR.errorbar(TR[m], fr[m], xerr=TRe[m], marker="o", linestyle="none",
             mfc="none", mec=rs.PALETTE["rust"], color=rs.PALETTE["rust"],
             ms=5, label=r"$T_R$")

axR.set_xscale("log")
axR.set_xlabel("Coherence (ms)")
axR.legend(loc="lower right", frameon=False)

fig.tight_layout()
out = os.path.join(HERE, "fig1c.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
