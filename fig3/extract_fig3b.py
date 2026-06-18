"""
Extract per-depth RBAM fidelity decay curves for Figure 3b of the RAQM
quantum-memory paper, and write a tidy CSV plus an extraction-notes file.

This reproduces the size-7 RAQM (mode_list = [1..7]) pipeline from
    analysis_notebooks/RAQM paper/rbam_analysis.ipynb   (compute_rbam_fidelity)
    analysis_notebooks/RAQM paper/rbam.ipynb            (Fig 3b cell, file_list 855..878)

Pipeline (faithful to the repo functions in multimode_expts/fit_display.py and
multimode_expts/experiments/fitting.py):

  prev_data(expt_path, filename)      -> open h5, return (datasets dict, attrs dict)
  RBAM_extract(temp_data, mode_idxs)  -> per-mode (mean survival, sem) over reps,
                                         with active-reset pre-selection (filter_data_BS)
  RB_extract(temp_data, conf=False)   -> per-rep ground-state probability (reference)
  fitter.fitexp / expfunc             -> exponential survival fit; p_survival = exp(-1/decay)
  find_gate_fidelity(p, dim=3, ...)   -> interleaved gate fidelity wrt reference

DERIVED NUMBERS (verification):
  * Per-mode survival fids and reference fids are fit with fitexp.
  * "random-read fidelity" per mode (== all_rbam.csv `rbam_fidelities`):
        xlist is scaled by mode_length (=7) before fitting   <-- KEY STEP
        p_survival_i = exp(-1/decay_i)        (per scaled-gate)
        p_ref        = exp(-1/decay_ref)      (reference, per ref gate)
        p_ref_scaled = p_ref ** (1/mode_length)
        p_div        = p_survival_i / p_ref_scaled
        r            = (dim-1)/dim * (1 - p_div),  dim = 3
        fid_wrt_ref  = 1 - r            (two-way: load + store)
        rbam_fid_i   = sqrt(fid_wrt_ref)   (one-way read/write)
  This reproduces all_rbam.csv rbam_fidelities EXACTLY (5+ decimals):
        [0.98829 0.98741 0.98888 0.98886 0.98768 0.98768 0.98808]

NOTE ON DATA PATH / IMPORTS
  The notebook hard-codes Windows paths:
      data_parent   = r'H:\\Shared drives\\SLab\\Multimode\\experiment\\240911'
      expt_path     = data_parent + '\\data1'
      expt_path_old = data_parent + '\\data'
  On this machine the mounted drive is /Volumes/slab/Multimode/experiment/240911.
  The MultiRBAM files in .../data1 are 800-byte stubs (no real data); the real
  22 MB MultiRBAM files (855..878) AND the SingleRB reference files (51..61) both
  live in .../data  (== expt_path_old). compute_rbam_fidelity also reads from
  expt_path_old, so the POSIX path used here is .../data .

  fit_display.py imports `qick` at module top (not installed off-instrument), so
  the small, self-contained analysis functions are reproduced verbatim below
  (copied from fit_display.py / experiments/fitting.py) and h5 files are read with
  h5py instead of slab.datamanagement.SlabFile (identical content: datasets +
  JSON-encoded attrs).
"""

import os
import sys
import json
import csv

import numpy as np
import scipy as sp
import h5py

# Repo location (kept for reference / if functions are ever imported directly).
REPO_PATH = '/Users/eesh/Documents/multimode_expts'
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# Discovered POSIX data directory (== Windows expt_path_old).
EXPT_PATH = '/Volumes/slab/Multimode/experiment/240911/data'

OUT_DIR = '/Users/eesh/Documents/RAQM_source_data/fig3'
CSV_PATH = os.path.join(OUT_DIR, 'fig3b_rbam_vs_depth.csv')
NOTES_PATH = os.path.join(OUT_DIR, 'fig3b_extraction_notes.txt')

# Size-7 RAQM run (mode_list = [1..7])
MULTIRBAM_NAME = '_MultiRBAM_sweep_depth.h5'
MULTIRBAM_FILE_LIST = list(range(855, 879))          # 855..878

SINGLERB_NAME = '_SingleRB_sweep_depth.h5'
SINGLERB_FILE_LIST = list(range(51, 62))             # 51..61  (reference)

DIM = 3
N_MODES = 7


# --------------------------------------------------------------------------- #
# prev_data  (h5py port of the notebook's SlabFile-based prev_data)
# --------------------------------------------------------------------------- #
def prev_data(expt_path, filename):
    full = os.path.join(expt_path, filename)
    with h5py.File(full, 'r') as a:
        attrs = {}
        for key in list(a.attrs):
            attrs[key] = json.loads(a.attrs[key])
        temp_data = {}
        for key in list(a.keys()):
            temp_data[key] = np.array(a[key])
    return temp_data, attrs


# --------------------------------------------------------------------------- #
# Analysis helpers (verbatim from multimode_expts/fit_display.py)
# --------------------------------------------------------------------------- #
def filter_data_BS(a1, a2, a3, threshold, post_selection=False):
    result_1 = []
    result_2 = []
    for k in range(len(a1)):
        if a1[k] < threshold:
            result_1.append(a2[k])
            if post_selection:
                result_2.append(a3[k])
    return np.array(result_1), np.array(result_2)


def discriminate_for_g(raw_data, threshold):
    """Return # of g counts."""
    counting = 0
    for j in raw_data:
        if j < threshold:
            counting += 1
    return counting


def RBAM_extract(temp_data, mode_idxs=[1], active_reset=True, post_select=False):
    """returns rb survival fidelity per mode, assumes active reset is on"""
    mean_list = []
    err_list = []
    for mode_idx in mode_idxs:
        avg_readout = []
        for i in range(len(temp_data['Idata'][mode_idx])):
            if active_reset:
                if post_select:
                    raw_data, post_select_data = filter_data_BS(
                        temp_data['Idata'][mode_idx][i][2],
                        temp_data['Idata'][mode_idx][i][3],
                        temp_data['Idata'][mode_idx][i][4],
                        temp_data['thresholds'], post_selection=True)
                else:
                    raw_data, _ = filter_data_BS(
                        temp_data['Idata'][mode_idx][i][2],
                        temp_data['Idata'][mode_idx][i][3],
                        None, temp_data['thresholds'])
            else:
                raw_data = temp_data['Idata'][mode_idx][i][0]

            if post_select:
                g_counts = discriminate_for_g(raw_data, temp_data['thresholds'])
                e_counts = discriminate_for_g(post_select_data, temp_data['thresholds'])
                prob = g_counts / (g_counts + e_counts)
                avg_readout.append(prob)
            else:
                counting = discriminate_for_g(raw_data, temp_data['thresholds'])
                avg_readout.append(counting / len(raw_data))

        mean = np.average(avg_readout)
        err = np.std(avg_readout) / np.sqrt(len(avg_readout))
        mean_list.append(mean)
        err_list.append(err)
    return mean_list, err_list


def RB_extract(temp_data, conf=False):
    temp_data['confusion_matrix'] = [0.9922999999999998, 0.007700000000000151,
                                     0.024050000000000002, 0.97595]
    avg_readout = []
    for i in range(len(temp_data['Idata'])):
        counting = 0
        for j in temp_data['Idata'][i]:
            if j < temp_data['thresholds']:
                counting += 1
        g_out = counting / len(temp_data['Idata'][i])
        if conf:
            P_matrix = np.matrix([[temp_data['confusion_matrix'][0], temp_data['confusion_matrix'][2]],
                                  [temp_data['confusion_matrix'][1], temp_data['confusion_matrix'][3]]])
            e_out = 1 - g_out
            counts_new = np.linalg.inv(P_matrix) * np.matrix([[g_out], [e_out]])
            g_out = counts_new[0, 0]
        avg_readout.append(g_out)
    return avg_readout


def find_gate_fidelity(p_survival, p_survival_err, dim, interleaved=False,
                       p_survival_interleaved_upon=1, p_interleaved_err=1):
    """Gate fidelity per PRL 109.080505 (verbatim from fit_display.py)."""
    p = p_survival
    p_err = p_survival_err
    if interleaved:
        p = p_survival / p_survival_interleaved_upon
        p_err = p * np.sqrt((p_err ** 2 / p_survival ** 2) +
                            (p_interleaved_err ** 2 / p_survival_interleaved_upon ** 2))
    r = (dim - 1) / dim * (1 - p)
    r_err = (dim - 1) / dim * p_err
    return 1 - r, r_err


# --------------------------------------------------------------------------- #
# Fit helpers (verbatim from multimode_expts/experiments/fitting.py)
# --------------------------------------------------------------------------- #
def expfunc(x, *p):
    y0, yscale, x0, decay = p
    return y0 + yscale * np.exp(-(x - x0) / decay)


def fitexp(xdata, ydata, fitparams=None):
    xdata = list(xdata)
    ydata = list(ydata)
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
    pCov = np.full(shape=(len(fitparams), len(fitparams)), fill_value=np.inf)
    try:
        pOpt, pCov = sp.optimize.curve_fit(expfunc, xdata, ydata, p0=fitparams, maxfev=200000)
    except RuntimeError:
        print('Warning: fit failed!')
    return pOpt, pCov


# --------------------------------------------------------------------------- #
def main():
    # --- MultiRBAM storage modes S1..S7: per-depth survival fids ---------- #
    fids_list = [[] for _ in range(N_MODES)]
    ebars_list = [[] for _ in range(N_MODES)]
    xlist = []
    for file_no in MULTIRBAM_FILE_LIST:
        full = str(file_no).zfill(5) + MULTIRBAM_NAME
        temp_data, attrs = prev_data(EXPT_PATH, full)
        mean, err = RBAM_extract(temp_data, mode_idxs=list(range(N_MODES)),
                                 active_reset=True, post_select=False)
        for i in range(N_MODES):
            fids_list[i].append(mean[i])
            ebars_list[i].append(err[i])
        xlist.append(attrs['config']['expt']['depth_list'][0])

    # --- SingleRB reference: per-depth survival fids ---------------------- #
    fids_ref = []
    ebars_ref = []
    xlist_ref = []
    for file_no in SINGLERB_FILE_LIST:
        full = str(file_no).zfill(5) + SINGLERB_NAME
        temp_data, attrs = prev_data(EXPT_PATH, full)
        avg_readout = RB_extract(temp_data, conf=False)
        fids_ref.append(float(np.average(avg_readout)))
        ebars_ref.append(float(np.std(avg_readout) / np.sqrt(len(avg_readout))))
        xlist_ref.append(attrs['config']['expt']['rb_depth'])

    # --- Reference fit (per ref-gate) ------------------------------------- #
    fit_ref, cov_ref = fitexp(xlist_ref, fids_ref)
    p_ref = np.exp(-1 / fit_ref[3])
    p_ref_err = np.sqrt(cov_ref[3][3]) * p_ref / (fit_ref[3] ** 2)
    fidelity_ref, _ = find_gate_fidelity(p_ref, p_ref_err, DIM, False)  # 2-way ref single-qubit

    # --- Per-mode random-read fidelity (matches all_rbam.csv) ------------- #
    # KEY: scale depth axis by mode_length (=N_MODES) before fitting.
    xs = np.array(xlist) * N_MODES
    p_surv_list = []
    p_surv_err_list = []
    for i in range(N_MODES):
        fit, cov = fitexp(xs, fids_list[i])
        ps = np.exp(-1 / fit[3])
        p_surv_list.append(ps)
        p_surv_err_list.append(abs(ps * np.sqrt(cov[3][3]) / fit[3] ** 2))

    p_ref_scaled = p_ref ** (1.0 / N_MODES)
    p_ref_scaled_err = (1.0 / N_MODES) * p_ref_err * p_ref ** (-(N_MODES - 1) / N_MODES)

    random_read_fids = []
    random_read_errs = []
    fid_wrt_ref_list = []  # two-way (load+store) gate fidelity per mode
    for i in range(N_MODES):
        fid_wrt, fid_wrt_err = find_gate_fidelity(
            p_surv_list[i], p_surv_err_list[i], DIM, True,
            p_ref_scaled, p_ref_scaled_err)
        fid_wrt_ref_list.append(fid_wrt)
        random_read_fids.append(float(np.sqrt(fid_wrt)))
        random_read_errs.append(float(fid_wrt_err / (2 * np.sqrt(fid_wrt))))

    # --- Per-mode gate fidelity for the all_storage_rbam.csv column ------- #
    # (same plot_fidelity formula but with the UNSCALED depth axis; this is the
    #  'fidelity' column in all_storage_rbam.csv == sqrt(fid_wrt) unscaled)
    storage_fids = []
    for i in range(N_MODES):
        fit, cov = fitexp(xlist, fids_list[i])
        ps = np.exp(-1 / fit[3])
        ps_err = abs(ps * np.sqrt(cov[3][3]) / fit[3] ** 2)
        fid_wrt, _ = find_gate_fidelity(ps, ps_err, DIM, True, p_ref_scaled, p_ref_scaled_err)
        storage_fids.append(float(np.sqrt(fid_wrt)))

    # --- Write tidy CSV (raw per-(series,depth) decay curves) ------------- #
    order = np.argsort(xlist)
    order_ref = np.argsort(xlist_ref)
    rows = []
    for i in range(N_MODES):
        for j in order:
            rows.append({'series': f'S{i+1}', 'depth': xlist[j],
                         'fidelity': fids_list[i][j],
                         'fidelity_err': ebars_list[i][j]})
    for j in order_ref:
        rows.append({'series': 'Ref', 'depth': xlist_ref[j],
                     'fidelity': fids_ref[j], 'fidelity_err': ebars_ref[j]})

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(CSV_PATH, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['series', 'depth', 'fidelity', 'fidelity_err'])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # --- Notes / verification --------------------------------------------- #
    L = []
    L.append('Fig 3b RBAM extraction notes (size-7 RAQM, mode_list = [1..7])')
    L.append('=' * 64)
    L.append(f'Data directory used   : {EXPT_PATH}')
    L.append(f'MultiRBAM name        : {MULTIRBAM_NAME}')
    L.append(f'MultiRBAM file_list   : {MULTIRBAM_FILE_LIST[0]}..{MULTIRBAM_FILE_LIST[-1]} '
             f'({len(MULTIRBAM_FILE_LIST)} files)')
    L.append(f'Reference name        : {SINGLERB_NAME}')
    L.append(f'Reference file_list   : {SINGLERB_FILE_LIST[0]}..{SINGLERB_FILE_LIST[-1]} '
             f'({len(SINGLERB_FILE_LIST)} files)')
    L.append(f'dim (RB)              : {DIM}')
    L.append('')
    L.append('Fitted per-gate (storage) fidelities, modes S1..S7')
    L.append('  (= all_storage_rbam.csv `fidelity` column):')
    L.append('  ' + repr([round(x, 4) for x in storage_fids]))
    L.append('  reference: [0.9236, 0.9184, 0.9273, 0.9271, 0.9200, 0.9200, 0.9224]')
    L.append('')
    L.append(f'Reference single-qubit gate fidelity (dim=3, two-way): {fidelity_ref:.5f}')
    L.append(f'Reference p_survival (per ref gate)                  : {p_ref:.5f}')
    L.append('')
    L.append('Derived random-read fidelities (one-way; depth axis x7)')
    L.append('  (= all_rbam.csv `rbam_fidelities` column):')
    L.append('  ' + repr([round(x, 5) for x in random_read_fids]))
    L.append('  reference: [0.98829, 0.98741, 0.98888, 0.98886, 0.98768, 0.98768, 0.98808]')
    L.append('  paper text: modes range 98.74-98.89 %')
    L.append('')
    L.append(f'CSV written to: {CSV_PATH}')

    note = '\n'.join(L)
    print(note)
    with open(NOTES_PATH, 'w') as f:
        f.write(note + '\n')

    return storage_fids, fidelity_ref, random_read_fids


if __name__ == '__main__':
    main()
