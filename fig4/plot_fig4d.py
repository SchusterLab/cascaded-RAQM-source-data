"""
Figure 4(d): spectator-access dephasing.

The additional dephasing rate (kHz) induced on storage mode S_i (rows) when a
spectator mode is randomly accessed via BS_j (columns), above S_i's bare Ramsey
baseline: dephasing = |1/T2_with_spectator - 1/T2_bare|. The diagonal is masked.

Data : fig4d_spectator_access_dephasing.csv
       (target_mode, spectator_mode, dephasing_kHz, dephasing_err_kHz)
Usage: python plot_fig4d.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig4d_spectator_access_dephasing.csv"))

n = 7
grid = np.full((n, n), np.nan)
for _, r in d.iterrows():
    if pd.isna(r["dephasing_kHz"]):
        continue
    t = int(str(r["target_mode"]).lstrip("S"))
    s = int(str(r["spectator_mode"]).lstrip("S"))
    grid[t - 1, s - 1] = r["dephasing_kHz"]   # row = storage dephased, col = spectator accessed

fig, ax = plt.subplots(figsize=(5, 4.5))
im = ax.imshow(np.ma.masked_invalid(grid), cmap="cividis",
               vmin=2.5, vmax=17.5, aspect="auto")
ax.set_xticks(range(n)); ax.set_xticklabels([f"BS$_{i+1}$" for i in range(n)])
ax.set_yticks(range(n)); ax.set_yticklabels([f"S$_{i+1}$" for i in range(n)])
ax.set_xlabel("Inactive Access Operation")
ax.set_ylabel("Storage Modes")
cb = fig.colorbar(im, ax=ax)
cb.set_label("Spectator Access Dephasing (kHz)")
fig.tight_layout()
out = os.path.join(HERE, "fig4d.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
