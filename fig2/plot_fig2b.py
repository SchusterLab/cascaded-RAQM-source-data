"""
Figure 2(b): B<->S2 beam-splitter swap (sideband Rabi).

Buffer state vs beam-splitter pulse length, with the coupler flux modulated at
the B1-S2 difference frequency (520.9 MHz, ~= |w_b1 - w_s2| from Fig 1). The
swap oscillates at ~0.47 MHz. Source h5: 00023_storage_sideband_sweep.h5.
(This is a long-time sweep window that resolves the swap rate; the swap is
highly coherent so full contrast persists.)

Data : fig2b_BS2_swap.csv  (time_us, avgi, avgq [raw], buffer_pop_norm [0..1])
Usage: python plot_fig2b.py
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
d = pd.read_csv(os.path.join(HERE, "fig2b_BS2_swap.csv"))
t, y = d["time_us"].values, d["buffer_pop_norm"].values

def dsin(t, A, f, phi, tau, off):
    return A * np.exp(-t / tau) * np.cos(2 * np.pi * f * t + phi) + off
dt = np.median(np.diff(t)); fr = np.fft.rfftfreq(len(t), dt)
f0 = fr[1 + np.argmax(np.abs(np.fft.rfft(y - y.mean()))[1:])]
p, _ = curve_fit(dsin, t, y, p0=[0.5, f0, 0, t[-1] - t[0], 0.5], maxfev=20000)
tf = np.linspace(t.min(), t.max(), 800)

fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(t, y, "o", ms=4, color=rs.PALETTE["teal"], label=r"$B\leftrightarrow S_2$")
ax.plot(tf, dsin(tf, *p), "-", color=rs.PALETTE["teal"], lw=1.2, label="Fitting")
ax.set_xlabel(r"Time ($\mu$s)")
ax.set_ylabel("Buffer State")
ax.set_yticks([0, 1]); ax.set_yticklabels([r"$|0\rangle$", r"$|1\rangle$"])
ax.legend(loc="upper right", fontsize=8)
ax.set_title(f"swap rate {abs(p[1]):.3f} MHz", fontsize=8)
fig.tight_layout()
out = os.path.join(HERE, "fig2b.pdf")
fig.savefig(out, bbox_inches="tight"); fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print(f"wrote {out}  (swap rate = {abs(p[1]):.4f} MHz)")
