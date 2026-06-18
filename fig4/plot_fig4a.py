"""
Figure 4(a): cross-Kerr matrix between storage and buffer modes (log color scale).

Rows = spectator modes S1..S6, columns = target modes B, S1..S5.
Cell value = |cross-Kerr| (kHz):
  - column B  : |chi(B1, S_i)|  (buffer-storage cross-Kerr)
  - column S_j: |chi(S_i, S_j)| (storage-storage; diagonal = storage self-Kerr)
The storage-storage block is symmetric and is symmetrized from the measured
lower triangle.

Data : fig4a_cross_kerr_matrix_kHz.csv  (full Q,C,B1,B2,S1..S7,R matrix)
Usage: python plot_fig4a.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

HERE = os.path.dirname(os.path.abspath(__file__))
M = pd.read_csv(os.path.join(HERE, "fig4a_cross_kerr_matrix_kHz.csv"), index_col=0)

# symmetric storage-storage block S1..S7
stor = [f"S{i}" for i in range(1, 8)]
S = M.loc[stor, stor].values
S = np.where(S == 0, S.T, S)        # symmetrize (fill upper triangle)

targets = ["B", "S1", "S2", "S3", "S4", "S5"]
spectators = [f"S{i}" for i in range(1, 7)]
grid = np.full((len(spectators), len(targets)), np.nan)
for r, sp in enumerate(spectators):
    i = int(sp[1:]) - 1
    grid[r, 0] = abs(M.loc[sp, "B1"])                # buffer-storage
    for c, tg in enumerate(targets[1:], start=1):
        j = int(tg[1:]) - 1
        grid[r, c] = abs(S[i, j])

fig, ax = plt.subplots(figsize=(5, 4.5))
im = ax.imshow(np.ma.masked_invalid(grid),
               norm=LogNorm(vmin=0.01, vmax=3.34), cmap="cividis", aspect="auto")
ax.set_xticks(range(len(targets)))
ax.set_xticklabels([r"$B$"] + [f"$S_{t[1:]}$" for t in targets[1:]])
ax.set_yticks(range(len(spectators)))
ax.set_yticklabels([f"$S_{s[1:]}$" for s in spectators])
ax.set_xlabel("Target Modes")
ax.set_ylabel("Spectator Modes")
cb = fig.colorbar(im, ax=ax)
cb.set_label("Cross Kerr (kHz)")
fig.tight_layout()
out = os.path.join(HERE, "fig4a.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
