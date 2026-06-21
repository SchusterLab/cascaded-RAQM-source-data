"""
Figure 4(a): cross-Kerr matrix between storage and buffer modes (log color scale).

Rows = spectator modes S1..S7, columns = target modes B, S1..S6.
Cell value = |cross-Kerr| (kHz):
  - column B  : |chi(B1, S_i)|  (buffer-storage cross-Kerr), every row
  - column S_j: |chi(S_i, S_j)| shown only for j < i  (strict lower triangle;
    each storage-storage pair once, no self-Kerr diagonal)

Data : fig4a_cross_kerr_matrix_kHz.csv  (full Q,C,B1,B2,S1..S7,R matrix)
Usage: python plot_fig4a.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
M = pd.read_csv(os.path.join(HERE, "fig4a_cross_kerr_matrix_kHz.csv"), index_col=0)

# Lower-triangular staircase: rows = spectator S1..S7, cols = target B, S1..S6.
# For target storage S_j show |chi(S_i, S_j)| only when j < i (each pair once,
# no self-Kerr diagonal); plus the buffer column for every row.
spectators = [f"S{i}" for i in range(1, 8)]        # rows S1..S7
targets = ["B"] + [f"S{j}" for j in range(1, 7)]   # cols B, S1..S6
grid = np.full((len(spectators), len(targets)), np.nan)
for r, sp in enumerate(spectators):
    i = r + 1
    grid[r, 0] = abs(M.loc[sp, "B1"])              # buffer-storage cross-Kerr
    for c in range(1, len(targets)):
        j = c                                       # target storage index
        if j < i:                                   # strict lower triangle
            grid[r, c] = abs(M.loc[sp, f"S{j}"])

fig, ax = plt.subplots(figsize=(5, 4.5))
im = ax.imshow(np.ma.masked_invalid(grid),
               norm=LogNorm(vmin=0.01, vmax=3.34), cmap=rs.CMAP, aspect="auto")
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
