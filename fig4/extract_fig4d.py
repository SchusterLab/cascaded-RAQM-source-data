"""Fig 4d source data: spectator-access dephasing matrix (kHz).

Rows  = storage mode S_i whose Ramsey dephasing is measured (target).
Cols  = spectator storage mode S_j that is randomly accessed via beam-splitter
        gates while S_i's Ramsey runs (spectator).
Value = ADDITIONAL (extra) dephasing rate induced on S_i, in kHz, defined as
        |kappa_with_spectator - kappa_bare|, where kappa = 1/T2 (T2 in us, so
        1/T2 is in MHz; *1e3 -> kHz). Diagonal (i==j) is undefined (masked).

This reproduces the `ckerr_m1_si_mat` matrix built in
analysis_notebooks/RAQM paper/error_budget_new.ipynb (cell In[54]):
    kappa_with_spec = 1/row['t2']
    bare_kappa      = 1/T2_bare(target)        # from ModeT2s_and_echoes.csv (type=='T2')
    matrix          = |kappa_with_spec - bare_kappa|   # plotted *1e3 -> kHz

Verification: mean of |extra| over the 42 off-diagonal pairs = 2.7726 kHz,
matching the paper's reported 2.772 kHz spectator-access dephasing rate.
"""
import os
import numpy as np
import pandas as pd

DS = "/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets"
SPEC = os.path.join(DS, "t2s_with_spectators.csv")
MODET2 = os.path.join(DS, "ModeT2s_and_echoes.csv")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "fig4d_spectator_access_dephasing.csv")

# bare (no-spectator) Ramsey dephasing rate per storage mode: kappa = 1/T2  [kHz]
mt = pd.read_csv(MODET2)
bare_df = mt[mt["type"] == "T2"]
bare_kappa = {int(t): 1.0e3 / t2 for t, t2 in zip(bare_df["target"], bare_df["t2"])}

df = pd.read_csv(SPEC)
rows = []
for _, r in df.iterrows():
    t, s = int(r["target"]), int(r["spectator"])
    if t == s:
        # diagonal undefined / masked
        rows.append((f"S{t}", f"S{s}", np.nan, np.nan))
        continue
    kappa_with = 1.0e3 / r["t2"]                       # kHz
    extra = abs(kappa_with - bare_kappa[t])            # kHz (additional dephasing)
    # error propagation on kappa = 1/T2 :  sigma_kappa = sigma_T2 / T2^2
    err = r["t2_err"] / (r["t2"] ** 2) * 1.0e3         # kHz
    rows.append((f"S{t}", f"S{s}", extra, err))

out = pd.DataFrame(rows, columns=["target_mode", "spectator_mode",
                                  "dephasing_kHz", "dephasing_err_kHz"])
out.to_csv(OUT, index=False)

offdiag = out.dropna(subset=["dephasing_kHz"])
mean_pairs = offdiag["dephasing_kHz"].mean()
mean_bare = np.mean(list(bare_kappa.values()))
print(f"Wrote {OUT}")
print(f"off-diagonal pairs: {len(offdiag)}")
print(f"mean spectator-access (extra) dephasing = {mean_pairs:.4f} kHz "
      f"(target 2.772 kHz)")
print(f"mean bare Ramsey dephasing               = {mean_bare:.4f} kHz "
      f"(paper baseline 2.105 kHz)")
