"""
Figure 4(c): state-dependent access error.

The error eps (%) incurred on the active BS_j access operation when a state is
stored in spectator mode S_i. Rows = occupied (spectator) modes S1..S7, columns
= active access operation BS1..BS7. The diagonal (accessing the occupied mode
itself) is not defined and is masked.

Data : fig4c_state_dependent_access_error.csv  (target_mode, spectator_mode, eps, eps_err)
Usage: python plot_fig4c.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig4c_state_dependent_access_error.csv"))
d = d[d["target_mode"] != 0]

n = 7
grid = np.full((n, n), np.nan)
for _, r in d.iterrows():
    t, s = int(r["target_mode"]), int(r["spectator_mode"])
    if t == s:
        continue
    grid[s - 1, t - 1] = 100 * r["eps"]   # % ; row = occupied/spectator, col = target

fig, ax = plt.subplots(figsize=(5, 4.5))
im = ax.imshow(np.ma.masked_invalid(grid), cmap=rs.CMAP,
               vmin=0.2, vmax=1.0, aspect="auto")
ax.set_xticks(range(n)); ax.set_xticklabels([f"BS$_{i+1}$" for i in range(n)])
ax.set_yticks(range(n)); ax.set_yticklabels([f"S$_{i+1}$" for i in range(n)])
ax.set_xlabel("Active Access Operation")
ax.set_ylabel("Occupied Modes")
cb = fig.colorbar(im, ax=ax)
cb.set_label("State-dependent Access Error (%)")
fig.tight_layout()
out = os.path.join(HERE, "fig4c.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
