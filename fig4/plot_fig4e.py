"""
Figure 4(e): many-body dephasing rate per storage mode.

For each storage mode S_i, the rate is the spread of the Ramsey dephasing rate
(1/T2) as the other storage modes are swept over the cardinal Bloch states, i.e.
the state-dependent dephasing induced by storage-storage cross-Kerr.

Data : fig4e_many_body_dephasing.csv  (mode, rate_kHz, rate_err_kHz)
Usage: python plot_fig4e.py
"""
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig4e_many_body_dephasing.csv"))

pos = range(len(d))   # row 0 = S1 at top
fig, ax = plt.subplots(figsize=(5, 4))
ax.errorbar(d["rate_kHz"], pos, xerr=d["rate_err_kHz"], fmt="o",
            color=rs.PALETTE["teal"], capsize=3, ms=5)
for p, (_, r) in zip(pos, d.iterrows()):
    ax.text(r["rate_kHz"] + r["rate_err_kHz"] + 0.02, p,
            f"{r['rate_kHz']:.3f}$\\pm${r['rate_err_kHz']:.3f}",
            va="center", fontsize=8)
ax.set_yticks(list(pos))
ax.set_yticklabels([f"S$_{m[1:]}$" for m in d["mode"]])
ax.set_ylim(len(d) - 0.5, -0.5)   # S1 top, S7 bottom
ax.set_xlabel("Many-body Dephasing Rate (kHz)")
ax.set_xlim(0, 0.9)
fig.tight_layout()
out = os.path.join(HERE, "fig4e.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
