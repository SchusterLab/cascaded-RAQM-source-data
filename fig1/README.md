# Figure 1(c) — mode frequency spectrum and coherence

**Dataset:** `fig1c_frequencies_and_coherences.csv` (from Supplementary Table 1)

Columns:
- `mode`, `symbol`, `category` — mode name, Hamiltonian symbol, object class
- `frequency_GHz` — mode frequency / 2π
- `T1_us`, `T1_err_us` — energy-relaxation time and 1σ fit error
- `TR_us`, `TR_err_us` — Ramsey coherence time and error
- `Techo_us`, `Techo_err_us` — echo coherence time and error (blank where not measured)

**Script:** `plot_fig1c.py` → `fig1c.pdf/.png`

Left panel: frequency vs object category. Right panel: frequency vs coherence
time (ms), T1 (filled) and Ramsey T_R (open), log x-axis.
