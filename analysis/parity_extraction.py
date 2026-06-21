"""
Joint buffer-storage population extraction for the dual-rail beam-splitter RB
(Fig 2c), via two parity measurements with post-selection.

Verbatim logic from `multimode_expts/fit_display.py`
(`RB_extract_postselction_parity_fixed_excited`).

Parity-readout mapping (two sequential parity measurements on the buffer):
    00 -> ee,  01 -> eg,  10 -> ge,  11 -> gg
so in terms of the paper's joint buffer-storage populations P_nm:
    P00 = ee,  P01 = eg,  P10 = ge,  P11 = gg
Figures of merit:
    raw fidelity            = (gg + ge) / total           # = P11 + P10
    post-selected fidelity  = ge / (ge + eg)              # = P10 / (P10 + P01)
Post-selection keeps single-photon-conserving outcomes, isolating
non-decoherence errors.
"""
import numpy as np


def extract_parity_populations(idata_per_depth, thresholds):
    """
    idata_per_depth : list over RB depths; each element is [Idata_init, Idata_post]
                      arrays of the two parity-measurement readout values.
    thresholds      : [thr] discriminator; value > thr is classified |e>.

    Returns dict of lists (over depth): P00, P01, P10, P11, fid_raw, fid_post.
    """
    P00, P01, P10, P11, fid_raw, fid_post = [], [], [], [], [], []
    for data_init, data_post in idata_per_depth:
        gg = ge = eg = ee = 0
        for j in range(len(data_init)):
            if data_init[j] > thresholds[0]:          # first parity -> |e>
                if data_post[j] > thresholds[0]:
                    ee += 1
                else:
                    eg += 1
            else:                                     # first parity -> |g>
                if data_post[j] > thresholds[0]:
                    ge += 1
                else:
                    gg += 1
        tot = gg + ge + eg + ee
        P11.append(gg / tot); P10.append(ge / tot)
        P01.append(eg / tot); P00.append(ee / tot)
        fid_raw.append((gg + ge) / tot)
        fid_post.append(ge / (ge + eg) if (ge + eg) else np.nan)
    return dict(P00=P00, P01=P01, P10=P10, P11=P11,
                fid_raw=fid_raw, fid_post=fid_post)
