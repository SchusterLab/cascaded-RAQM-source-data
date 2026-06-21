# Data provenance

Every figure panel's source data and the analysis that produced it.

**Slab drive root:** `/Volumes/slab/Multimode/experiment/240911/`
(on Windows this is `H:\Shared drives\SLab\Multimode\experiment\240911\`)
- `RAM_paper_results/datasets/` — processed/analysis CSVs
- `data/`, `data1/` — raw `.h5` measurement files

**Analysis notebooks:** copied into `notebooks/` here; originals live in the
`SchusterLab/multimode_expts` repo under `analysis_notebooks/RAQM paper/`.

| Panel | Repo dataset | Slab source | Notebook |
|---|---|---|---|
| 1c | `fig1/fig1c_frequencies_and_coherences.csv` | Suppl. Table 1; `datasets/system_frequencies_and_coherences.csv`, `ModeT2s_and_echoes.csv` | `cavity_temperature_and_echo.ipynb` |
| 2a | `fig2/fig2a_f0g1_rabi.csv` | `data1/00115_length_rabi_f0g1_sweep.h5` (f0g1 drive 2005.05 MHz) | `BS_rb.ipynb` |
| 2b | `fig2/fig2b_BS2_swap.csv` | `data1/00023_storage_sideband_sweep.h5` (flux_drive 520.9 MHz = w_b1-w_s2) | `BS_rb.ipynb` |
| 2c | `fig2/fig2c_beamsplitter_rb_vs_depth.csv` | `datasets/DualRail_BeamSplitters.csv` | `BS_rb.ipynb` |
| 2e | `fig2/fig2e_swap_infidelity.csv` | derived from `DualRail_BeamSplitters.csv` | `BS_rb.ipynb` |
| 3b | `fig3/fig3b_rbam_vs_depth.csv` | `data/00855..00878_MultiRBAM_sweep_depth.h5`, `data/00051..00061_SingleRB_sweep_depth.h5`; summaries `datasets/all_storage_rbam.csv`, `all_rbam.csv` | `rbam.ipynb`, `rbam_analysis.ipynb` |
| 3c | `fig3/fig3c_random_read_infidelity.csv` | `datasets/all_rbam.csv` | `rbam.ipynb`, `rbam_analysis.ipynb` |
| 4a | `fig4/fig4a_cross_kerr_matrix_kHz.csv` | `datasets/QubitBufferStorage_cross_kerr.csv` (= Suppl. Table 3) | `cross_kerr_scan.ipynb` |
| 4c | `fig4/fig4c_state_dependent_access_error.csv` | `datasets/StateDependentAccessError.csv` | `RAM_random_state_BS.ipynb` |
| 4d | `fig4/fig4d_spectator_access_dephasing.csv` | `datasets/t2s_with_spectators.csv`, `ModeT2s_and_echoes.csv` | `error_budget_new.ipynb` (cell In[54]) |
| 4e | `fig4/fig4e_many_body_dephasing.csv` | `datasets/ManyBodyDephasing.csv` | `ManyBodyDephasing.ipynb` |
| 4f | `fig4/fig4f_error_budget.csv` | `datasets/StateDependentAccessError.csv`, `ManyBodyDephasing.csv`, `t2s_with_spectators.csv`, `system_frequencies_and_coherences.csv`, `DualRail_BeamSplitters.csv`, `all_rbam.csv` | `error_budget_new.ipynb` (cells In[143], In[191]) |

Per-panel column definitions and the exact conversions are in each figure's
`README.md` and the `extract_*` / `build_*` scripts and `*_extraction_notes.txt`.

## Supplement

| Item | Repo data | Slab source (`RAM_paper_results/datasets/`) | Notebook |
|---|---|---|---|
| Cavity temperature | `Supplement_temperature/datasets/Cavity_Temp_Parity*.csv` | `Cavity_Temp_Parity.csv`, `_Full.csv`, `_Full_corrected.csv`, `_corrected1211.csv` | `Supplement_temperature/temperature/parity_temp_analysis*.ipynb` |

(Other merged supplement notebooks — `Supplement_1QRB`, `Supplement_filter`,
`Supplement_memory_scaling` — carry their own data/figures inline.)
