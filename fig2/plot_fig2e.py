"""
Figure 2(e): SWAP infidelity for all beam-splitter mode pairs BS_1 .. BS_7.

Raw and post-selected swap infidelities (%) per mode, with error bars.
A swap = 1.5 RB beam-splitter gates, so infidelity = 1 - (gate_fid)**1.5.

Data : fig2e_swap_infidelity.csv
Usage: python plot_fig2e.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig2e_swap_infidelity.csv")).sort_values("mode")

x = np.arange(len(d))
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(x, d["swap_infid_raw_pct"], yerr=d["swap_infid_raw_err_pct"],
       color=rs.PALETTE["slate"], capsize=3, label="Raw")
ax.bar(x, d["swap_infid_post_pct"], yerr=d["swap_infid_post_err_pct"],
       color=rs.PALETTE["rust"], capsize=3, label="Post selection")
for xi, (_, r) in zip(x, d.iterrows()):
    ax.text(xi, r["swap_infid_raw_pct"], f"{r['swap_infid_raw_pct']:.3f}%",
            ha="center", va="bottom", fontsize=7, color=rs.PALETTE["slate"])
    ax.text(xi, r["swap_infid_post_pct"], f"{r['swap_infid_post_pct']:.3f}%",
            ha="center", va="bottom", fontsize=7, color=rs.PALETTE["rust"])
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels([f"BS$_{int(m)}$" for m in d["mode"]])
ax.set_ylabel("SWAP Infidelity (%)")
ax.set_xlabel("Mode Pairs")
ax.legend(frameon=False)
fig.tight_layout()
out = os.path.join(HERE, "fig2e.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
