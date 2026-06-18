# Analysis notebooks

Reference copies of the Jupyter notebooks used to analyze the raw data and
produce the figure datasets. They are preserved **as run** (cell outputs
included) for transparency; they are not meant to be re-executed here, since
they depend on the lab's `qick`/`slab` stack and the raw `.h5` files on the slab
drive (paths in `../SOURCES.md`). Originals live in `SchusterLab/multimode_expts`
under `analysis_notebooks/RAQM paper/`.

| Notebook | Figure(s) |
|---|---|
| `BS_rb.ipynb` | 2c, 2e |
| `rbam.ipynb`, `rbam_analysis.ipynb` | 3b, 3c |
| `cross_kerr_scan.ipynb` | 4a |
| `RAM_random_state_BS.ipynb` | 4c |
| `error_budget_new.ipynb` | 4d, 4f |
| `ManyBodyDephasing.ipynb` | 4e |

The runnable, trimmed reproductions of just the figure-relevant steps are the
`extract_*.py` / `build_*.py` scripts in each `figN/` folder.
