# Figure 4 — RAQM crosstalk benchmarking

## Fig 4(a) — cross-Kerr matrix  ✅
**Dataset:** `fig4a_cross_kerr_matrix_kHz.csv` — full self/cross-Kerr matrix (kHz)
over modes Q,C,B1,B2,S1..S7,R (= Supplementary Table 3). Diagonal = self-Kerr,
lower triangle = measured cross-Kerr.
**Script:** `plot_fig4a.py` → `fig4a.pdf/.png` (|chi| for the B,S1..S5 × S1..S6
block, log color scale). `build_fig4a_data.py` regenerates the CSV.

## Fig 4(c) — state-dependent access error  ✅
**Dataset:** `fig4c_state_dependent_access_error.csv` — `target_mode,
spectator_mode, eps, eps_err` (7×7). `eps` is the fractional error on the BS_target
access when a state occupies the spectator mode.
**Script:** `plot_fig4c.py` → `fig4c.pdf/.png` (eps in %, diagonal masked).

## Fig 4(d) — spectator-access dephasing  ⏳ pending
Source candidate: `t2s_with_spectators.csv` (per target/spectator T2 with random
gates on the spectator). The dephasing-rate (kHz) conversion comes from
`RAM_target_spectator_analysis.ipynb` — to be extracted.

## Fig 4(e) — many-body dephasing rate  ⏳ pending
Source candidate: `ManyBodyDephasing.csv` (per-mode Ramsey T2 with the other modes
loaded). Rate (kHz) conversion from `ManyBodyDephasing*.ipynb`. Published values:
S1 0.510±0.222 … S7 0.228±0.097 kHz.

## Fig 4(f) — random-read error budget  ⏳ pending
Source: `error_budget_new.ipynb` (stacked error channels per mode: swaps, decay,
dephasing, spectator-access dephasing, many-body dephasing, state-dependent access).
