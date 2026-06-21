# Analysis methods

The actual fitting/extraction routines used to turn raw measurements into the
figure data. Reproduced (verbatim logic, plotting/printing removed) from the lab
analysis stack `SchusterLab/multimode_expts` — `fit_display.py`,
`experiments/fitting.py`, and the notebooks in `../notebooks/`.

**See `METHODS.md` for the end-to-end narrative** (raw h5 shots → discrimination
→ post-selection → populations → survival → fit → fidelity).

## `readout_discrimination.py` — raw shots → g/e outcomes
| Function | What it does |
|---|---|
| `single_shot_calibration` | rotates the IQ blobs, finds the threshold maximizing cumulative-histogram contrast, returns g–e assignment fidelity + confusion matrix |
| `filter_data_IQ` | active-reset / herald post-selection on the interleaved readouts |

This is the **upstream step** that produces the binary outcomes the routines
below then count and fit.

## `rb_analysis.py` — randomized benchmarking
| Function | Used for | What it does |
|---|---|---|
| `expfunc`, `fitexp` | Fig 3b RBAM | single-exponential survival fit; `decay` = RB decay constant in gates |
| `single_exponential_fit` | Fig 2c BS-RB | fit `a e^{bx}+c`; per-gate fidelity `exp(-1/r)`, `r=1/|b|` |
| `double_exponential_fit` | BS-RB (two-rate) | two decay rates + their fidelities |
| `find_gate_fidelity` | Fig 3b/3c | depolarizing parameter `p` → average gate fidelity `1-(d-1)/d·(1-p)` (dim=3), with interleaved reference division |
| `swap_infidelity` | Fig 2e | `1 - gate_fid**1.5` (a SWAP = 1.5 beam-splitter gates) |
| `random_read_fidelity` | Fig 3b/3c | `sqrt(F_mode/F_ref)` with the size-N depth axis scaled by `n_modes` |

## `parity_extraction.py` — dual-rail populations
`extract_parity_populations` implements the two-parity-measurement readout for
Fig 2c. Mapping `00→ee, 01→eg, 10→ge, 11→gg`, i.e. `P00=ee, P01=eg, P10=ge,
P11=gg`; raw fidelity `= P11+P10`, post-selected `= P10/(P10+P01)`.

## Other analyses
- **RBAM survival / reference extraction** (`RBAM_extract`, `RB_extract`,
  `prev_data`, `filter_data_BS`) and the full end-to-end pipeline are in
  `../fig3/extract_fig3b.py`.
- **Dephasing-rate conversions** (T2 fits → kHz) are documented inline in
  `../fig4/extract_fig4d.py` (spectator access) and `../fig4/extract_fig4e.py`
  (many-body), with the exact formulas in their `*_extraction_notes.txt`.
- **Error-budget channel formulas** are in `../fig4/extract_fig4f.py`.

These are reference implementations; the raw `.h5`-reading wrappers depend on the
lab's `qick`/`slab` packages (not vendored here). See `../SOURCES.md` for the
data paths.
