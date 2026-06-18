"""
Extract the random-read error-budget data for Figure 4f of the RAQM quantum-memory paper.

Reproduces the per-mode, per-channel error percentages used to draw the Fig 4f
stacked bar chart, plus the "Measured" random-read infidelity point per mode.

PRIMARY SOURCE NOTEBOOK
-----------------------
/Users/eesh/Documents/multimode_expts/analysis_notebooks/RAQM paper/error_budget_new.ipynb

The Fig 4f stacked bar is built in the cell labelled In[143] ("For eesh presentation").
The six stacked channels correspond to df_master_new_def columns (in stacking order
bottom -> top), with the figure legend / requested column names:

    measured_bare              -> "Swaps"                        (legend "Bare Swap")
    gate_mbd_err               -> "State-dependent Access Error" (legend "State Dependent Access Error")
    idle:decay_err             -> "Decay"
    idle:dephasing_err         -> "Dephasing"                    (legend "Pure Dephasing")
    idle_err_due_to_spec_gates -> "Spectator-access Dephasing"   (legend "Spectator Access Dephasing")
    MBD_idle_err               -> "Many-body Dephasing"          (legend "Many Body Dephasing")

The "Measured" point per mode is hard-coded in the notebook as `fidelities_new`
(and `fidelities_err_new`); these are EXACTLY the rbam_fidelities / rbam_fidelity_errs
of row 0 (mode_list=[1..7]) of all_rbam.csv. Measured infidelity = 1 - fidelity.

df_master_new_def is produced from df_master by the transforms in cell In[96]:
    idle:decay_err              -> 1 - (1 - x)**(1/14)
    idle:dephasing_err          -> 1 - (1 - x)**(1/14)
    MBD_idle_err                -> 1 - (1 - x)**(1/14)
    idle_err_due_to_spec_gates  -> 1 - (1 - x)**(1/14)
    measured_bare               -> 1 - (1 - x)**(1/7 * 3/2)
    gate_mbd_err                -> 1 - (1 - x)**(1/7)
(The (1/14) / (1/7) exponents convert a full 7-mode random-read sequence to the
per-storage-operation contribution; measured_bare additionally converts a dual-rail
gate to a single swap with the 3/2 factor.)

This script reproduces df_master from the supporting datasets following the notebook
exactly, applies the In[96] transforms, and writes fig4f_error_budget.csv.
"""

import os
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
DATASETS = "/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets"
MM_REPO = "/Users/eesh/Documents/multimode_expts"
OUT_DIR = "/Users/eesh/Documents/RAQM_source_data/fig4"
# The notebook (analysis_notebooks/RAQM paper/error_budget_new.ipynb) loads its
# gate times from the man1_storage_swap_dataset.csv co-located with it. That copy
# reproduces the notebook's printed In[45] decay output EXACTLY (verified maxdiff 0.0).
# The repo-root copy has slightly different pi-times and does NOT reproduce the figure.
SWAP_DS_CSV = os.path.join(MM_REPO, "analysis_notebooks", "RAQM paper", "man1_storage_swap_dataset.csv")

modes = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]

# ----------------------------------------------------------------------------
# Gate / idle times  (notebook cells In[30]-In[32])
# Uses man1_storage_swap_dataset.csv directly (stor_name -> 'pi (mus)').
# ----------------------------------------------------------------------------
df_swap = pd.read_csv(SWAP_DS_CSV)


def get_gate_time(mode):
    row = df_swap[df_swap["stor_name"] == "M1-" + str(mode)]
    return row["pi (mus)"].values[0]


def get_M1Si_idle_time(mode):
    t = 0.0
    for m in modes:
        if m != mode:
            t += get_gate_time(m)
    return t


def get_loading_time():
    ge_pulse = 35 * 4 * 1e-3 / 2
    ef_pulse = 35 * 4 * 1e-3
    M1_pulse = df_swap[df_swap["stor_name"] == "M1"]["pi (mus)"].values[0]
    return ge_pulse + ef_pulse + M1_pulse


def get_f0g1_time():
    return df_swap[df_swap["stor_name"] == "M1"]["pi (mus)"].values[0]


columns = ["Mode", "gate_time", "f0g1_other_spec_targ_idle", "M1_Si_other_spec_targ_idle"]
data = []
for mode in modes:
    gate_time = get_gate_time(mode)
    f0g1_idle_time = get_loading_time() * 6          # In[32]
    M1_Si_other_spec_targ_idle = get_M1Si_idle_time(mode)
    data.append([mode, gate_time, f0g1_idle_time, M1_Si_other_spec_targ_idle])
df_master = pd.DataFrame(data, columns=columns)

# ----------------------------------------------------------------------------
# Coherence: T1s (In[33], hard-coded in notebook) and T2 echo (In[39]-In[44])
# ----------------------------------------------------------------------------
t1s = [358.3, 1254.8, 799.0, 597.4, 355.7, 589.5, 371.2]   # In[33], matches system_frequencies_and_coherences.csv
df_master["kappa_t1s (MHz)"] = [1.0 / t1 for t1 in t1s]

df_t2_and_echo = pd.read_csv(os.path.join(DATASETS, "ModeT2s_and_echoes.csv"))
T2s = df_t2_and_echo[df_t2_and_echo["type"] == "T2"]["t2"].values
T2echoes = df_t2_and_echo[df_t2_and_echo["type"] == "T2_echo"]["t2"].values
df_master["kappa_T2 (MHz)"] = 1.0 / T2s
df_master["kappa_T2_echo (MHz)"] = 1.0 / T2echoes

# ----------------------------------------------------------------------------
# Idling coherence errors (In[45]):
#   decay_err     = 1 - exp(-kappa_t1 * (t_f0g1_idle + t_M1Si_idle) * 2)
#   dephasing_err = 1 - exp(-(kappa_t2 - kappa_t1/2) * (t_f0g1_idle + t_M1Si_idle) * 2)
# ----------------------------------------------------------------------------
decay_errs, dephasing_errs = [], []
for idx in range(len(modes)):
    kappa_t1 = df_master["kappa_t1s (MHz)"][idx]
    kappa_t2 = df_master["kappa_T2_echo (MHz)"][idx]
    f0g1_idle_time = df_master["f0g1_other_spec_targ_idle"][idx]
    M1_Si_idle_time = df_master["M1_Si_other_spec_targ_idle"][idx]
    t_tot = (f0g1_idle_time + M1_Si_idle_time) * 2
    decay_errs.append(1 - np.exp(-kappa_t1 * t_tot))
    dephasing_errs.append(1 - np.exp(-(kappa_t2 - kappa_t1 / 2) * t_tot))
df_master["idle:decay_err"] = decay_errs
df_master["idle:dephasing_err"] = dephasing_errs

# ----------------------------------------------------------------------------
# Spectator-access decoherence (cross-Kerr of M1-Si gates), In[52]-In[66]
#   ckerr_m1_si_mat[t][s] = (1/t2_with_spec) - bare_kappa_T2(target)
#   per spectator gate fidelity = 1 - ckerr * (2*gate_time(spec) + 2*f0g1_time)
#   net error = 1 - prod over spectators (idle_err_due_to_spec_prod)
# ----------------------------------------------------------------------------
df_ckerr = pd.read_csv(os.path.join(DATASETS, "t2s_with_spectators.csv"))
ckerr_mat = np.zeros((7, 7))
for _, row in df_ckerr.iterrows():
    target = int(row["target"])
    spec = int(row["spectator"])
    kappa_with_spec = 1.0 / row["t2"]
    bare_kappa = df_master[df_master["Mode"] == "S" + str(target)]["kappa_T2 (MHz)"].values[0]
    ckerr_mat[target - 1][spec - 1] = kappa_with_spec - bare_kappa

f0g1_time = get_f0g1_time()
idle_err_due_to_spec_prod = []
for target_mode in modes:
    net_fidelity = 1.0
    for spec_mode in modes:
        if target_mode != spec_mode:
            targ_idx = int(target_mode[1]) - 1
            spec_idx = int(spec_mode[1]) - 1
            ckerr = np.abs(ckerr_mat[targ_idx][spec_idx])
            total_time = get_gate_time(spec_mode) * 2 + f0g1_time * 2
            net_fidelity *= (1 - ckerr * total_time)
    idle_err_due_to_spec_prod.append(1 - net_fidelity)
df_master["idle_err_due_to_spec_gates"] = idle_err_due_to_spec_prod

# ----------------------------------------------------------------------------
# Many-body dephasing (In[67]-In[77])
#   del_kappa = max(kappa) - min(kappa) across the 6 spectator states, per target
#   MBD_idle_err = 1 - exp(-del_kappa * (t_f0g1_idle + t_M1Si_idle) * 2)
# ----------------------------------------------------------------------------
df_MBD = pd.read_csv(os.path.join(DATASETS, "ManyBodyDephasing.csv"))
df_MBD["kappas"] = 1.0 / df_MBD["t2"].values

del_kappas = []
for mode_no in [1, 2, 3, 4, 5, 6, 7]:
    kappas = df_MBD[df_MBD["target"] == mode_no]["kappas"].values
    del_kappas.append(abs(min(kappas) - max(kappas)))   # in MHz

MBD_idle_errs = []
for idx, mode in enumerate(modes):
    f0g1_idle_time = df_master[df_master["Mode"] == mode]["f0g1_other_spec_targ_idle"].values[0]
    M1_Si_idle_time = df_master[df_master["Mode"] == mode]["M1_Si_other_spec_targ_idle"].values[0]
    MBD_idle_errs.append(1 - np.exp(-del_kappas[idx] * (f0g1_idle_time + M1_Si_idle_time) * 2))
df_master["MBD_idle_err"] = MBD_idle_errs

# ----------------------------------------------------------------------------
# State-dependent access error (In[80]-In[90])
#   eps matrix from StateDependentAccessError.csv (per fetch), convert to swap:
#       eps_swap = 1 - (1 - eps)**(3/2)
#   gate_mbd_err[target] = sum over all 7 spectator columns of eps_swap
#   (diagonal included exactly as in notebook)
# ----------------------------------------------------------------------------
df_rb_spec = pd.read_csv(os.path.join(DATASETS, "StateDependentAccessError.csv"))
rb_spec_mat = np.zeros((7, 7))
for _, row in df_rb_spec.iterrows():
    target = int(row["target_mode"])
    spec = int(row["spectator_mode"])
    rb_spec_mat[target - 1][spec - 1] = row["eps"]

infidelities = np.abs(rb_spec_mat)
infidelities_swap = 1 - (1 - infidelities) ** (3 / 2)
gate_mbd_errs = [np.sum(infidelities_swap[i]) for i in range(7)]
df_master["gate_mbd_err"] = gate_mbd_errs

# ----------------------------------------------------------------------------
# Bare swap (measured dual-rail RB infidelity), In[93], hard-coded in notebook
# ----------------------------------------------------------------------------
df_master["measured_bare"] = np.array([0.00335, 0.00239, 0.00300, 0.00612, 0.00679, 0.00416, 0.00593])

# ----------------------------------------------------------------------------
# df_master_new_def transforms (In[96])
# ----------------------------------------------------------------------------
df_new = df_master.copy(deep=True)
for i in range(7):
    df_new.loc[i, "idle:decay_err"] = 1 - (1 - df_master["idle:decay_err"][i]) ** (1 / 14)
    df_new.loc[i, "idle:dephasing_err"] = 1 - (1 - df_master["idle:dephasing_err"][i]) ** (1 / 14)
    df_new.loc[i, "MBD_idle_err"] = 1 - (1 - df_master["MBD_idle_err"][i]) ** (1 / 14)
    df_new.loc[i, "idle_err_due_to_spec_gates"] = 1 - (1 - df_master["idle_err_due_to_spec_gates"][i]) ** (1 / 14)
    df_new.loc[i, "measured_bare"] = 1 - (1 - df_master["measured_bare"][i]) ** (1 / 7 * 3 / 2)
    df_new.loc[i, "gate_mbd_err"] = 1 - (1 - df_master["gate_mbd_err"][i]) ** (1 / 7)

# ============================================================================
# AUTHORITATIVE FIGURE VALUES
# ============================================================================
# The dataset-based df_master_new_def reproduction above matches the notebook
# pipeline, but the notebook was run incrementally and the *final* df_master_new_def
# state that the Fig 4f cell (In[143]) actually plotted is captured by the printed
# output of cell In[191] ("for i in errors: print(df_master_new_def[i])").
# Those exact arrays are pasted here (fractions, not %) and are the source of the
# CSV, so the per-mode channel percentages match the drawn figure to the digit.
# The recomputed df_new above agrees with these to ~1e-4 (gate-time drift between
# notebook runs); see fig4f_extraction_notes.txt for the cross-check table.
#
# In[191] of error_budget_new.ipynb:
NB_IN191 = {  # df_master_new_def[col], fractions
    "idle:decay_err":              [0.005589, 0.001585, 0.002454, 0.003286, 0.005254, 0.003266, 0.004932],
    "idle:dephasing_err":          [0.000838, 0.000540, 0.000270, 0.000376, 0.000191, 0.000204, 0.000177],
    "measured_bare":               [0.000719, 0.000513, 0.000644, 0.001315, 0.001459, 0.000893, 0.001274],
    "idle_err_due_to_spec_gates":  [0.009281, 0.007049, 0.004504, 0.003244, 0.002419, 0.007338, 0.001765],
    "MBD_idle_err":                [0.001023, 0.000462, 0.000304, 0.000256, 0.000303, 0.000283, 0.000418],
    "gate_mbd_err":                [0.001637, 0.002489, 0.000578, 0.002550, 0.000561, 0.001666, 0.001270],
}

# Cross-check: recomputed (df_new) vs authoritative (In[191])
print("\nChannel cross-check  recomputed-vs-notebook(In191)  max |diff| (% pts):")
_chanmap = {
    "idle:decay_err": "decay", "idle:dephasing_err": "dephasing",
    "idle_err_due_to_spec_gates": "spectator_access", "MBD_idle_err": "many_body",
    "gate_mbd_err": "state_dependent", "measured_bare": "swaps",
}
for col, nm in _chanmap.items():
    recomputed = df_new[col].values * 1e2
    notebook = np.array(NB_IN191[col]) * 1e2
    print(f"  {nm:18s} max|diff| = {np.max(np.abs(recomputed - notebook)):.4f}")

# ----------------------------------------------------------------------------
# Measured random-read infidelity (notebook fidelities_new / fidelities_err_new,
# == rbam_fidelities row 0 of all_rbam.csv)
# ----------------------------------------------------------------------------
fidelities_new = np.array([0.988286023993436, 0.9874131819599585, 0.9888830087682574,
                           0.9888627298370297, 0.9876800525303363, 0.9876819095515517,
                           0.9880764203490647])
fidelities_err_new = np.array([0.00041485755837685254, 0.00040563478820520595, 0.0004169635987301473,
                               0.000486199769967945, 0.0006624437266762003, 0.0005970754150193145,
                               0.0005608351111824674])
measured_pct = (1 - fidelities_new) * 1e2
measured_err_pct = fidelities_err_new * 1e2

# ----------------------------------------------------------------------------
# Assemble tidy CSV (one row per mode), percentages
# ----------------------------------------------------------------------------
# Use the authoritative In[191] arrays (the values the figure was drawn with).
out = pd.DataFrame({
    "mode": modes,
    "decay_pct": np.array(NB_IN191["idle:decay_err"]) * 1e2,
    "dephasing_pct": np.array(NB_IN191["idle:dephasing_err"]) * 1e2,
    "spectator_access_dephasing_pct": np.array(NB_IN191["idle_err_due_to_spec_gates"]) * 1e2,
    "many_body_dephasing_pct": np.array(NB_IN191["MBD_idle_err"]) * 1e2,
    "state_dependent_access_pct": np.array(NB_IN191["gate_mbd_err"]) * 1e2,
    "swaps_pct": np.array(NB_IN191["measured_bare"]) * 1e2,
    "measured_pct": measured_pct,
    "measured_err_pct": measured_err_pct,
})

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "fig4f_error_budget.csv")
out.to_csv(out_path, index=False)
print(f"Wrote {out_path}")

stacked_total = (out["decay_pct"] + out["dephasing_pct"] + out["spectator_access_dephasing_pct"]
                 + out["many_body_dephasing_pct"] + out["state_dependent_access_pct"] + out["swaps_pct"])
print("\nmode  stacked_total  measured  diff")
for i, m in enumerate(modes):
    print(f"{m}   {stacked_total[i]:.4f}        {out['measured_pct'][i]:.4f}   {stacked_total[i]-out['measured_pct'][i]:+.4f}")
