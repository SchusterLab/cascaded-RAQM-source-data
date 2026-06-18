# Source Data — *A Cascaded Random Access Quantum Memory* (arXiv:2503.13953)

This repository contains the statistical source data and plotting scripts needed
to reproduce the main-text figures of the paper. For every figure panel there is
(1) a plain-text/CSV dataset and (2) a self-contained Python script that reads the
dataset and regenerates the panel.

## Layout

```
fig1/   Fig 1(c)  mode frequency spectrum & coherences
fig2/   Fig 2(a)  f0g1 (Q<->B) Rabi trace            [pending raw trace]
        Fig 2(b)  B<->S2 beam-splitter swap trace     [pending raw trace]
        Fig 2(c)  beam-splitter RB, all modes M1-S1..7
        Fig 2(e)  per-mode SWAP infidelity bar chart
fig3/   Fig 3(b)  random read fidelity vs # accesses (7 modes + ref)
        Fig 3(c)  random read infidelity vs RAQM size
fig4/   Fig 4(a)  cross-Kerr matrix
        Fig 4(c)  state-dependent access error matrix
        Fig 4(d)  spectator-access dephasing matrix
        Fig 4(e)  many-body dephasing rate per mode
        Fig 4(f)  random-read error budget
```

(Schematic / circuit / device panels — 1a,b, 2d, 3a, 4b — contain no statistical
data and are not included.)

## Requirements

```
python >= 3.9, numpy, pandas, matplotlib, scipy
```

## Usage

```bash
cd fig2 && python plot_fig2c.py      # writes fig2c_M1-S{1..7}.pdf/.png
```

Each script writes a `.pdf` and `.png` next to itself. Datasets are CSV with a
header row; column meanings are documented at the top of each plotting script
and in the per-figure `README.md`.
