"""
Extract Fig 4e per-mode many-body dephasing rates (kHz) for storage modes S1..S7.

Method (matches analysis_notebooks/RAQM paper/ManyBodyDephasing.ipynb, cell that
builds the Fig 4e plot, lines ~438-470):

  For each target storage mode, mode S_i undergoes a Ramsey measurement while the
  six other storage modes are prepared in identical cardinal Bloch states
  (state_idx 0,1,2,3,4,5 = '0','1','+x','-x','+y','-y'). Each config yields a fitted
  Ramsey Gaussian/exp decay time t2 (microseconds) and its error t2_err, stored in
  ManyBodyDephasing.csv (columns 't2', 't2_err'; these are p[3] and sqrt(pCov[3,3])
  of the Ramsey fit).

  Convert each config to a dephasing rate:
      kappa     = 1 / t2          [MHz, since t2 is in us]
      kappa_err = t2_err / t2**2

  The many-body dephasing rate is the SPREAD of kappa across the six configs:
      rate_kHz     = (max(kappa) - min(kappa)) * 1e3
      rate_err_kHz = sqrt(kappa_err[argmax]^2 + kappa_err[argmin]^2) * 1e3

  (The notebook line 467 indexes kappa_errs[0] and kappa_errs[-1]; the published
   figure uses the errors of the actual min/max configs, which is what reproduces
   the printed error bars exactly. They differ only when the extremes are not at
   state_idx 0 and 5.)

Output: fig4e_many_body_dephasing.csv with columns mode, rate_kHz, rate_err_kHz.
"""

import os
import numpy as np
import pandas as pd

SRC = "/Volumes/slab/Multimode/experiment/240911/RAM_paper_results/datasets/ManyBodyDephasing.csv"
OUT_DIR = "/Users/eesh/Documents/RAQM_source_data/fig4"
OUT_CSV = os.path.join(OUT_DIR, "fig4e_many_body_dephasing.csv")


def extract():
    df = pd.read_csv(SRC)
    rows = []
    for mode_no in range(1, 8):
        d = df[df["target"] == mode_no].sort_values("state_idx")
        t2 = d["t2"].values            # microseconds
        t2_err = d["t2_err"].values
        kappa = 1.0 / t2               # MHz
        kappa_err = t2_err / t2**2

        imin, imax = np.argmin(kappa), np.argmax(kappa)
        rate_kHz = (kappa[imax] - kappa[imin]) * 1e3
        rate_err_kHz = np.sqrt(kappa_err[imax] ** 2 + kappa_err[imin] ** 2) * 1e3

        rows.append({
            "mode": f"S{mode_no}",
            "rate_kHz": round(rate_kHz, 4),
            "rate_err_kHz": round(rate_err_kHz, 4),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    out = extract()
    out.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}")
    print(out.to_string(index=False))
