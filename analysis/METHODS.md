# From raw shots to fidelities — the full analysis pipeline

This walks the complete chain behind the RB-based figures (Fig 2, Fig 3), from
the single-shot data in the `.h5` files to the published fidelities. Each step
names the function that implements it.

```
 raw single-shot I/Q  ──►  discrimination calibration  ──►  active-reset
 (h5, N readouts/expt)     (threshold, θ, confusion)        post-selection
        │                                                        │
        ▼                                                        ▼
   g/e classification  ──►  per-depth survival probability  ──►  exponential
   (shot < threshold)       (counts of |g> / total)              RB fit
        │                                                        │
        ▼                                                        ▼
   joint populations    gate fidelity  ──►  swap / random-read fidelity
   (dual-rail, Fig 2c)  (depolarizing)      (derived figures of merit)
```

## 1. What the h5 holds
Each experiment is run many times; the readout records **several single shots per
repetition** (`readout_per_experiment`). The leading shots are *heralds* (used
for active reset / state preparation post-selection) and the final shot is the
**data** readout. Values are the demodulated `I` (and `Q`) ADC levels per shot.

## 2. Discrimination calibration — `readout_discrimination.single_shot_calibration`
From separate prepared-|g> and prepared-|e> single-shot clouds:
1. rotate the IQ plane so the two blobs separate along `I`
   (`θ = -atan2(ye-yg, xe-xg)`);
2. histogram the rotated `I` for g and e;
3. pick the **threshold** that maximizes the cumulative-histogram contrast — this
   contrast *is* the g–e assignment fidelity;
4. read off the **confusion matrix** `[Pgg, Pge, Peg, Pee]`.

A data shot is then classified `|g>` iff its rotated `I < threshold`.

## 3. Active-reset post-selection — `readout_discrimination.filter_data_IQ`
Keep only repetitions whose herald shot confirmed `|g>` before the experiment
(herald `< threshold`); return the surviving data shots. This removes residual
thermal population and reset failures.

## 4. Counts → survival probability
For each RB depth, classify every surviving data shot and take the fraction in
the target state:
- **Fig 3 (RBAM)** — `fig3/extract_fig3b.py`: `RBAM_extract` / `RB_extract`
  (with `filter_data_BS`, `discriminate_for_g`) produce the per-depth survival
  for each storage mode and the buffer reference.
- **Fig 2c (dual-rail BS-RB)** — `parity_extraction.extract_parity_populations`:
  two sequential parity measurements give joint buffer–storage populations
  `P00=ee, P01=eg, P10=ge, P11=gg`; raw fidelity `= P11+P10`, post-selected
  `= P10/(P10+P01)`.

## 5. Survival → fidelity — `rb_analysis.py`
Fit survival vs depth to an exponential (`fitexp`/`expfunc` for RBAM,
`single_exponential_fit` for BS-RB), then convert the decay to an **average gate
fidelity** with `find_gate_fidelity` (depolarizing model, `dim=3`; interleaved
reference division for the multiplexed case).

## 6. Derived figures of merit — `rb_analysis.py`
- **Fig 2e**: `swap_infidelity = 1 - gate_fid**1.5` (a SWAP = 1.5 BS gates).
- **Fig 3b/3c**: `random_read_fidelity = sqrt(F_mode/F_ref)`, with the size-N
  RBAM depth axis scaled by `n_modes` before fitting (see `extract_fig3b.py`).

## Fig 4 (crosstalk) analyses
These use Ramsey rather than RB. The shot→population step is the same
discrimination above; the rate extraction (T2 fits → kHz) and the error-budget
channel formulas are documented inline in `fig4/extract_fig4d.py`,
`fig4/extract_fig4e.py`, `fig4/extract_fig4f.py` and their `*_extraction_notes.txt`.

## Dependency note
The `.h5` readers (`prev_data`) and the on-instrument acquisition wrappers depend
on the lab's `qick`/`slab` packages, which are not vendored here. The functions
above are the analysis logic applied to the already-loaded shot arrays; the
notebooks in `../notebooks/` show them running end-to-end on the real data.
