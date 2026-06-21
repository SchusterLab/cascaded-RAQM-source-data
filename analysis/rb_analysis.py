"""
Randomized-benchmarking (RB) analysis used for the RAQM paper figures.

These are the exact fitting/extraction routines behind Fig 2 (beam-splitter RB),
Fig 3 (multiplexed RBAM), and the derived fidelities. They are reproduced here
(verbatim logic, side-effects removed) from the lab analysis stack
`multimode_expts` — `fit_display.py`, `experiments/fitting.py`, and the
notebooks `BS_rb.ipynb` / `rbam.ipynb` (see ../notebooks and ../SOURCES.md).

Survival model and gate-fidelity conversion follow Magesan et al.,
PRL 106, 180504 / 109, 080505.
"""
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit


# --------------------------------------------------------------------------- #
# Exponential survival fits
# --------------------------------------------------------------------------- #
def expfunc(x, *p):
    """Single-exponential survival: y0 + yscale * exp(-(x - x0)/decay)."""
    y0, yscale, x0, decay = p
    return y0 + yscale * np.exp(-(x - x0) / decay)


def fitexp(xdata, ydata, fitparams=None):
    """Fit `expfunc`; returns (popt, pcov). decay (popt[3]) is the RB decay
    constant in 'gates'. (verbatim from experiments/fitting.py)"""
    xdata, ydata = list(xdata), list(ydata)
    if fitparams is None:
        fitparams = [None] * 4
    if fitparams[0] is None:
        fitparams[0] = ydata[-1]
    if fitparams[1] is None:
        fitparams[1] = ydata[0] - ydata[-1]
    if fitparams[2] is None:
        fitparams[2] = xdata[0]
    if fitparams[3] is None:
        fitparams[3] = (xdata[-1] - xdata[0]) / 5
    pOpt, pCov = fitparams, np.full((4, 4), np.inf)
    try:
        pOpt, pCov = sp.optimize.curve_fit(expfunc, xdata, ydata, p0=fitparams, maxfev=200000)
    except RuntimeError:
        print('Warning: fit failed!')
    return pOpt, pCov


def single_exponential_fit(x_data, y_data):
    """Fit a*exp(b*x)+c (used for beam-splitter RB survival, Fig 2c).
    Returns dict with params, decay r=1/|b|, and per-gate fidelity exp(-1/r)."""
    def f(x, a, b, c):
        return a * np.exp(b * x) + c
    popt, pcov = curve_fit(f, x_data, y_data, p0=[1, -1, 1], maxfev=10000)
    r = 1 / np.abs(popt[1])
    r_err = np.abs(np.sqrt(pcov[1][1]) / popt[1] ** 2)
    fid = np.exp(-1 / r)
    fid_err = fid * r_err / (r ** 2)
    return dict(popt=popt, pcov=pcov, r=r, r_err=r_err, fid=fid, fid_err=fid_err)


def double_exponential_fit(x_data, y_data):
    """Fit a*exp(b*x)+c*exp(d*x)+e (two-rate beam-splitter RB survival).
    Returns the two decay rates and their per-gate fidelities."""
    def f(x, a, b, c, d, e):
        return a * np.exp(b * x) + c * np.exp(d * x) + e
    popt, pcov = curve_fit(f, x_data, y_data, p0=[0.5, -1, 0.5, -1, -0.2], maxfev=10000,
                           bounds=([0.3, -np.inf, 0, -np.inf, -np.inf], [1, 0, 1, 0, 0]))
    r1, r2 = 1 / np.abs(popt[1]), 1 / np.abs(popt[3])
    r1_err = np.abs(np.sqrt(pcov[1][1]) / popt[1] ** 2)
    r2_err = np.abs(np.sqrt(pcov[3][3]) / popt[3] ** 2)
    return dict(popt=popt, pcov=pcov,
                r1=r1, r1_err=r1_err, r1_fid=np.exp(-1 / r1),
                r2=r2, r2_err=r2_err, r2_fid=np.exp(-1 / r2))


# --------------------------------------------------------------------------- #
# Depolarizing-parameter -> gate fidelity
# --------------------------------------------------------------------------- #
def find_gate_fidelity(p_survival, p_survival_err, dim, interleaved=False,
                       p_survival_interleaved_upon=1, p_interleaved_err=1):
    """Average gate fidelity from the RB depolarizing parameter p (dim = system
    dimension; dim=3 for the {|0>,|1>,|2>}-aware cavity RB here). For interleaved
    RB, divide by the reference survival. (verbatim from fit_display.py)"""
    p, p_err = p_survival, p_survival_err
    if interleaved:
        p = p_survival / p_survival_interleaved_upon
        p_err = p * np.sqrt((p_err ** 2 / p_survival ** 2) +
                            (p_interleaved_err ** 2 / p_survival_interleaved_upon ** 2))
    r = (dim - 1) / dim * (1 - p)
    r_err = (dim - 1) / dim * p_err
    return 1 - r, r_err


# --------------------------------------------------------------------------- #
# Derived figures of merit
# --------------------------------------------------------------------------- #
def swap_infidelity(gate_fid):
    """A SWAP = 1.5 RB beam-splitter gates -> 1 - gate_fid**1.5  (Fig 2e)."""
    return 1.0 - gate_fid ** 1.5


def random_read_fidelity(p_mode, p_ref, n_modes=7):
    """Random-read fidelity for multiplexed RBAM (Fig 3b/3c). The size-N RBAM
    depth axis is scaled by n_modes before fitting; the per-mode survival is
    divided by the (per-mode) reference and a square root taken for a one-way
    read/write: F = sqrt(F_mode / F_ref). p_ref should already be scaled by
    p_ref**(1/n_modes) before calling find_gate_fidelity (see extract_fig3b.py)."""
    return np.sqrt(p_mode / p_ref)
