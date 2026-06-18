"""
Figure 4(f): random-read error budget per storage mode.

Stacked per-mode error contributions (%) from six channels, compared with the
measured random-read error (= 1 - random_read_fidelity from all_rbam.csv, shown
as black markers with error bars).

Data : fig4f_error_budget.csv
Usage: python plot_fig4f.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig4f_error_budget.csv"))
x = np.arange(len(d))

# stacking order (bottom -> top) with paper-like colors
channels = [
    ("decay_pct", "Decay", "#5fb3a6"),
    ("dephasing_pct", "Dephasing", "#f2d65c"),
    ("swaps_pct", "Swaps", "#b8a6d9"),
    ("spectator_access_dephasing_pct", "Spectator-access Dephasing", "#ef8a7f"),
    ("many_body_dephasing_pct", "Many-body Dephasing", "#6fa8dc"),
    ("state_dependent_access_pct", "State-dependent Access Error", "#f4b860"),
]

fig, ax = plt.subplots(figsize=(6.5, 4.5))
bottom = np.zeros(len(d))
for col, lab, color in channels:
    ax.bar(x, d[col], bottom=bottom, color=color, label=lab, width=0.7)
    bottom += d[col].values

ax.errorbar(x, d["measured_pct"], yerr=d["measured_err_pct"], fmt="o",
            color="k", capsize=3, ms=4, label="Measured")

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
