# Figure 2 — single storage mode access

## Fig 2(a) — f0g1 (Q<->B) Rabi trace  *[PENDING raw trace]*
Qubit state vs time for the |f0> <-> |g1> four-wave-mixing drive used to prepare
|1> in the buffer. Drop the trace as `fig2a_f0g1_trace.csv`
(columns `time_us, qubit_state`) and add `plot_fig2a.py`.

## Fig 2(b) — B<->S2 beam-splitter swap trace  *[PENDING raw trace]*
Buffer state vs time during the 0.439 MHz B<->S2 swap. Drop as
`fig2b_BS2_swap_trace.csv` (columns `time_us, buffer_state`).

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
