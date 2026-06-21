# Figure 4 — RAQM crosstalk benchmarking

## Fig 4(a) — cross-Kerr matrix  ✅
**Dataset:** `fig4a_cross_kerr_matrix_kHz.csv` — full self/cross-Kerr matrix (kHz)
over modes Q,C,B1,B2,S1..S7,R (= Supplementary Table 3). Diagonal = self-Kerr,
lower triangle = measured cross-Kerr.
**Script:** `plot_fig4a.py` → `fig4a.pdf/.png` — lower-triangular staircase,
rows = spectator S1..S7, cols = target B, S1..S6; B column for every row and
|chi(S_i,S_j)| for j<i (no self-Kerr diagonal), log color scale.
`build_fig4a_data.py` regenerates the CSV.

## Fig 4(c) — state-dependent access error  ✅
**Dataset:** `fig4c_state_dependent_access_error.csv` — `target_mode,
spectator_mode, eps, eps_err` (7×7). `eps` is the fractional error on the BS_target
access when a state occupies the spectator mode.
**Script:** `plot_fig4c.py` → `fig4c.pdf/.png` (eps in %, diagonal masked).

## Fig 4(d) — spectator-access dephasing  ✅
**Dataset:** `fig4d_spectator_access_dephasing.csv` — `target_mode, spectator_mode,
dephasing_kHz, dephasing_err_kHz`. The additional dephasing on storage S_i when
spectator S_j is randomly accessed: `|1/T2_with_spectator - 1/T2_bare|`.
Off-diagonal pair average = 2.773 kHz (paper: 2.772 kHz).
**Script:** `plot_fig4d.py` → `fig4d.pdf/.png`. `extract_fig4d.py` regenerates the CSV.

## Fig 4(e) — many-body dephasing rate  ✅
**Dataset:** `fig4e_many_body_dephasing.csv` — `mode, rate_kHz, rate_err_kHz`.
Rate = spread of 1/T2 as the other storages are swept over cardinal states.
Matches published S1 0.510±0.222 … S7 0.228±0.097 kHz exactly.
**Script:** `plot_fig4e.py` → `fig4e.pdf/.png`. `extract_fig4e.py` regenerates the CSV.

## Fig 4(f) — random-read error budget  ✅
**Dataset:** `fig4f_error_budget.csv` — per mode: `decay_pct, dephasing_pct,
spectator_access_dephasing_pct, many_body_dephasing_pct, state_dependent_access_pct,
swaps_pct, measured_pct, measured_err_pct`. Channels from `error_budget_new.ipynb`;
`measured_pct` = 1 - random_read_fidelity (bit-identical to all_rbam.csv).
**Script:** `plot_fig4f.py` → `fig4f.pdf/.png`. `extract_fig4f.py` documents the
per-channel formulas and regenerates the CSV.
