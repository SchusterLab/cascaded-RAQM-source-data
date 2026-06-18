# Figure 3 — random access quantum memory operation

## Fig 3(b) — random read fidelity vs number of random accesses
**Dataset:** `fig3b_rbam_vs_depth.csv` — one row per (series, depth):
`series` in {S1..S7, Ref}, `depth`, `fidelity`, `fidelity_err`.
Re-extracted from the `_MultiRBAM_sweep_depth.h5` (7 storage modes) and
`_SingleRB_sweep_depth.h5` (buffer reference) files via the analysis pipeline in
`rbam.ipynb`. See `extract_fig3b.py` and `fig3b_extraction_notes.txt` for the
data path, reference file list, and verification against the published
per-gate / random-read fidelities.

**Script:** `plot_fig3b.py` → `fig3b.pdf/.png`. Single-exponential RB fit per
series; per-gate fidelity = 1 - (1-alpha) - (1-alpha)/3 with alpha=exp(-1/tau).

## Fig 3(c) — random read infidelity vs RAQM size
**Dataset:** `fig3c_random_read_infidelity.csv` — one row per (config, mode):
`raqm_size, config_id, mode, random_read_fidelity, random_read_fidelity_err,
infidelity, infidelity_err`. Built from `all_rbam.csv` (32 configs of size
1/2/3/7; `infidelity = 1 - random_read_fidelity`).

**Script:** `plot_fig3c.py` → `fig3c.pdf/.png`. The shaded region is the surface
-code depolarization threshold (17%) mapped to a per-access infidelity for a
size-N RAQM (a full cycle = 2N accesses): `1 - (1-0.17)**(1/(2N))`.

Provenance: `build_fig3c_data.py` regenerates the 3c CSV from `all_rbam.csv`.
