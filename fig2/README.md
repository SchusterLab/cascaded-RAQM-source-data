# Figure 2 — single storage mode access

## Fig 2(a) — f0g1 (Q<->B) Rabi
**Dataset:** `fig2a_f0g1_rabi.csv` — `time_us, avgi, avgq` (raw rotated-readout
quadratures) and `qubit_pop_norm` (0..1, min-max of the principal-axis
projection). Source h5 `00115_length_rabi_f0g1_sweep.h5` (f0g1 drive 2005.05 MHz);
fitted pi-time = 0.614 us (paper: ~0.615 us).
**Script:** `plot_fig2a.py` -> `fig2a.pdf/.png`.

## Fig 2(b) — B<->S2 beam-splitter swap
**Dataset:** `fig2b_BS2_swap.csv` — `time_us, avgi, avgq` (raw) and
`buffer_pop_norm` (0..1). Source h5 `00023_storage_sideband_sweep.h5`, coupler
flux modulated at 520.9 MHz (= |w_b1 - w_s2| from Fig 1); fitted swap rate
0.472 MHz (paper claim ~0.44 MHz). The sweep window is 50-60 us (a long-time
run that resolves the rate; the swap stays full-contrast, i.e. highly coherent).

## Fig 2(c) — beam-splitter randomized benchmarking, all modes
**Dataset:** `fig2c_beamsplitter_rb_vs_depth.csv` — one row per (mode, depth):
- `fid_raw, fid_raw_err` — raw process fidelity vs depth + error
- `fid_post, fid_post_err` — post-selected process fidelity + error
- `P00,P01,P10,P11` (+`_err`) — joint buffer-storage populations.
  Parity-readout mapping: `P00=ee, P01=eg, P10=ge, P11=gg`; raw fidelity = P11+P10,
  post-selected fidelity = P10/(P10+P01).

**Script:** `plot_fig2c.py [mode]` → `fig2c_M1-S{i}.pdf/.png`. Mode 2 is the panel
shown in the paper. The annotated fidelity is the per-SWAP fidelity
(= gate_fid**1.5). The T1-decay line is a reference using the storage T1 from
`../fig1` and a 0.5 us swap duration.

## Fig 2(e) — per-mode SWAP infidelity
**Dataset:** `fig2e_swap_infidelity.csv` — per mode:
- `gate_fid_raw/post (+_err)` — per-gate RB fidelities
- `swap_infid_raw/post_pct (+_err_pct)` — SWAP infidelity (%), = 1 - gate_fid**1.5

**Script:** `plot_fig2e.py` → `fig2e.pdf/.png`

## Provenance
`build_fig2_data.py` regenerates the two tidy CSVs from the raw analysis output
`DualRail_BeamSplitters.csv` (notebook `BS_rb.ipynb`). The raw file is included
in `raw/` for reference.
