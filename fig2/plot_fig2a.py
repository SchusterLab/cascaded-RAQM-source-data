"""
Figure 2(a): f0g1 (Q<->B) Rabi.

Qubit state vs drive length for the |f0> <-> |g1> four-wave-mixing interaction
used to prepare |1> in the buffer (pi time ~0.615 us). Source h5:
00115_length_rabi_f0g1_sweep.h5 (f0g1 drive 2005.05 MHz).

Data : fig2a_f0g1_rabi.csv  (time_us, avgi, avgq [raw], qubit_pop_norm [0..1])
Usage: python plot_fig2a.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raqm_style as rs
rs.apply()

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "fig2a_f0g1_rabi.csv"))
t, y = d["time_us"].values, d["qubit_pop_norm"].values

def dsin(t, A, f, phi, tau, off):
    return A * np.exp(-t / tau) * np.cos(2 * np.pi * f * t + phi) + off
p, _ = curve_fit(dsin, t, y, p0=[0.5, 0.81, 0, t[-1], 0.5], maxfev=20000)
tf = np.linspace(t.min(), t.max(), 600)
pi_time = 0.5 / abs(p[1])

fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(t, y, "o", ms=4, color=rs.PALETTE["rust"], label=r"$Q\leftrightarrow B$")
ax.plot(tf, dsin(tf, *p), "-", color=rs.PALETTE["rust"], lw=1.2, label="Fitting")
ax.axvline(pi_time, ls=":", color=rs.PALETTE["ink"], lw=1)
ax.set_xlabel(r"Time ($\mu$s)")
ax.set_ylabel("Qubit State")
ax.set_yticks([0, 1]); ax.set_yticklabels([r"$|g\rangle$", r"$|f\rangle$"])
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
out = os.path.join(HERE, "fig2a.pdf")
fig.savefig(out, bbox_inches="tight"); fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print(f"wrote {out}  (pi = {pi_time:.3f} us)")
