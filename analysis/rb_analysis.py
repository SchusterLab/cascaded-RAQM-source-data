"""
Randomized-benchmarking (RB) analysis used for the RAQM paper figures.

The fitting routines here are copied VERBATIM from the analysis library that the
240911 measurement code imports — `multimode_expts/experiments/fitting.py`
(`import experiments.fitting as fitter`) — i.e. the exact `fitter` functions used
to produce the published fidelities, not a re-implementation. Single-shot
readout discrimination is in `readout_discrimination.py` (= `MM_base.hist`).

RB model (Magesan et al., PRL 106 180504 / 109 080505):
    survival(depth) = a * p**depth + b
    average error per gate      r = (1 - (p + (1-p)/d))          # rb_error
    interleaved gate fidelity   F = 1 - (d-1)(1 - p_irb/p_rb)/d  # rb_gate_fidelity
with d the system dimension (d = 3 for the {|0>,|1>,|2>}-aware cavity RB here).
"""
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit


# --------------------------------------------------------------------------- #
# Standard RB fit  (verbatim from experiments/fitting.py)
# --------------------------------------------------------------------------- #
def rb_func(depth, p, a, b):
    return a * p ** depth + b


def rb_error(p, d):
    """Average error rate per gate; d = dim of system (= 2^#qubits)."""
    return 1 - (p + (1 - p) / d)


def rb_gate_fidelity(p_rb, p_irb, d):
    """Interleaved-RB gate fidelity from reference (p_rb) and interleaved (p_irb)
    decay parameters."""
    return 1 - (d - 1) * (1 - p_irb / p_rb) / d


def fitrb(xdata, ydata, fitparams=None):
    """Fit survival vs depth to rb_func; returns (popt, pcov), popt[0] = p."""
    if fitparams is None:
        fitparams = [None] * 3
    if fitparams[0] is None:
        fitparams[0] = 0.9
    if fitparams[1] is None:
        fitparams[1] = np.max(ydata) - np.min(ydata)
    if fitparams[2] is None:
        fitparams[2] = np.min(ydata)
    bounds = ([-1, -1, -1], [0.99999, 1, 1])
    for i, param in enumerate(fitparams):
        if not (bounds[0][i] < param < bounds[1][i]):
            fitparams[i] = np.mean((bounds[0][i], bounds[1][i]))
    pOpt = fitparams
    pCov = np.full((len(fitparams), len(fitparams)), np.inf)
    pOpt, pCov = sp.optimize.curve_fit(rb_func, xdata, ydata, p0=fitparams,
                                       method='trf', max_nfev=30000)
    return pOpt, pCov


# --------------------------------------------------------------------------- #
# Exponential decay fit (verbatim from experiments/fitting.py) — used by the
# multiplexed RBAM extraction (Fig 3); equivalent to rb_func via p = e^{-1/decay}
# --------------------------------------------------------------------------- #
def expfunc(x, *p):
    y0, yscale, x0, decay = p
    return y0 + yscale * np.exp(-(x - x0) / decay)


def fitexp(xdata, ydata, fitparams=None):
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
    pOpt = fitparams
    pCov = np.full((4, 4), np.inf)
    try:
        pOpt, pCov = sp.optimize.curve_fit(expfunc, xdata, ydata, p0=fitparams, maxfev=200000)
    except RuntimeError:
        print('Warning: fit failed!')
    return pOpt, pCov


def find_gate_fidelity(p_survival, p_survival_err, dim, interleaved=False,
                       p_survival_interleaved_upon=1, p_interleaved_err=1):
    """Depolarizing-parameter -> average gate fidelity, equivalent to
    1 - rb_error(p, dim). Used in the Fig 3 RBAM extraction (../fig3/extract_fig3b.py)
    and reproduces the published random-read fidelities exactly. (from fit_display.py)"""
    p, p_err = p_survival, p_survival_err
    if interleaved:
        p = p_survival / p_survival_interleaved_upon
        p_err = p * np.sqrt((p_err ** 2 / p_survival ** 2) +
                            (p_interleaved_err ** 2 / p_survival_interleaved_upon ** 2))
    r = (dim - 1) / dim * (1 - p)
    return 1 - r, (dim - 1) / dim * p_err


# --------------------------------------------------------------------------- #
# Derived figures of merit
# --------------------------------------------------------------------------- #
def swap_infidelity(gate_fid):
    """A SWAP = 1.5 RB beam-splitter gates -> 1 - gate_fid**1.5  (Fig 2e)."""
    return 1.0 - gate_fid ** 1.5


def random_read_fidelity(p_mode, p_ref, n_modes=7):
    """Random-read fidelity for multiplexed RBAM (Fig 3b/3c): F = sqrt(F_mode/F_ref),
    with the size-N RBAM depth axis scaled by n_modes before fitting
    (see ../fig3/extract_fig3b.py)."""
    return np.sqrt(p_mode / p_ref)
