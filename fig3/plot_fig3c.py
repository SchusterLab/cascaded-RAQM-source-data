"""
Figure 3(c): random read infidelity vs RAQM size.

Each point is the random-read infidelity (1 - F) of one storage mode within a
RAQM configuration of a given size; configurations of size 1, 2, 3 and 7 are
shown. The shaded region marks where a full memory cycle stays below the surface
-code depolarization threshold (~17%). For a size-N RAQM a full cycle is a read
+ write on each mode (2N accesses), so the per-access threshold infidelity is
1 - (1 - 0.17)**(1/(2N)).

Data : fig3c_random_read_infidelity.csv
Usage: python plot_fig3c.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig3c_random_read_infidelity.csv"))

DEPOL = 0.17  # surface-code depolarization threshold
colors = {1: "#d62728", 2: "#1f77b4", 3: "#2ca02c", 7: "#9467bd"}

fig, ax = plt.subplots(figsize=(6, 4.5))

# threshold line + shaded region (above the line is "bad")
N = np.logspace(0, 2, 200)
thr = 1 - (1 - DEPOL) ** (1.0 / (2 * N))
ax.fill_between(N, thr, 1, color="#f3b6b6", alpha=0.5, lw=0)
ax.plot(N, thr, "k--", lw=1)
ax.text(8, 0.045, "Depolarization Error\nCorrection Threshold",
        rotation=-18, fontsize=8, va="center")

# data points, jittered slightly in x within each size for visibility
rng = np.random.default_rng(0)
for size, g in d.groupby("raqm_size"):
    jit = size * (1 + 0.04 * rng.standard_normal(len(g)))
    ax.errorbar(jit, g["infidelity"], yerr=g["infidelity_err"], fmt="o",
                ms=5, color=colors.get(size, "k"), capsize=2,
                label=f"RAQM Size={size}")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.9, 100)
ax.set_ylim(1e-3, 1.2e-1)
ax.set_xlabel("RAQM Size")
ax.set_ylabel("Random Read Infidelity")
ax.legend(frameon=False, fontsize=8, loc="lower left")
fig.tight_layout()
out = os.path.join(HERE, "fig3c.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
