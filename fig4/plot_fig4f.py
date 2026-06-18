"""
Figure 4(f): random-read error budget per storage mode.

Stacked per-mode error contributions (%) from six channels, compared with the
measured random-read error (= 1 - random_read_fidelity from all_rbam.csv, shown
as black markers with error bars).

Data : fig4f_error_budget.csv
Usage: python plot_fig4f.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig4f_error_budget.csv"))
x = np.arange(len(d))

# stacking order (bottom -> top), earthy theme
channels = [
    ("decay_pct", "Decay", rs.PALETTE["teal"]),
    ("dephasing_pct", "Dephasing", rs.PALETTE["gold"]),
    ("swaps_pct", "Swaps", rs.PALETTE["purple"]),
    ("spectator_access_dephasing_pct", "Spectator-access Dephasing", rs.PALETTE["rust"]),
    ("many_body_dephasing_pct", "Many-body Dephasing", rs.PALETTE["slate"]),
    ("state_dependent_access_pct", "State-dependent Access Error", rs.PALETTE["olive"]),
]

fig, ax = plt.subplots(figsize=(6.5, 4.5))
bottom = np.zeros(len(d))
for col, lab, color in channels:
    ax.bar(x, d[col], bottom=bottom, color=color, label=lab, width=0.7)
    bottom += d[col].values

ax.errorbar(x, d["measured_pct"], yerr=d["measured_err_pct"], fmt="o",
            color=rs.PALETTE["ink"], capsize=3, ms=4, label="Measured")

ax.set_xticks(x)
ax.set_xticklabels([f"S$_{i+1}$" for i in range(len(d))])
ax.set_xlabel("Storage Modes")
ax.set_ylabel("Errors (%)")
ax.legend(frameon=False, fontsize=7, ncol=2, loc="upper right")
fig.tight_layout()
out = os.path.join(HERE, "fig4f.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
