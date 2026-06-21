"""
Single-shot readout discrimination: the step that turns raw shot data in the
h5 files into binary g/e outcomes (and the calibration that defines it).

This is the front of the pipeline that precedes the RB counting/fitting in
`rb_analysis.py` and `parity_extraction.py`. Verbatim logic (plotting removed)
from `MM_base.hist` / `MM_base.filter_data_IQ` — the discriminator the 240911
measurement code actually calls (the `hist` imported from
`experiments.single_qubit.single_shot` wraps `MM_base.hist`). The algorithm is
identical to the `hist` in `fit_display.py`.

Pipeline per experiment:
  raw h5 shots  ->  [active-reset post-selection]  ->  threshold discrimination
                ->  g/e counts  ->  survival probability  ->  RB fit  ->  fidelity
"""
import numpy as np


def filter_data_IQ(II, IQ, threshold, readout_per_experiment=2):
    """Active-reset / herald post-selection on interleaved readouts.

    Each experiment contributes `readout_per_experiment` consecutive shots; the
    second-to-last is the heralding readout and the last is the data readout.
    Keep only experiments whose herald shot is below `threshold` (transmon
    confirmed in |g> before the experiment). Returns the surviving data shots
    (I, Q). (verbatim from fit_display.py)
    """
    result_Ig, result_Ie = [], []
    n = readout_per_experiment
    for k in range(len(II) // n):
        herald = n * k + n - 2
        data = n * k + n - 1
        if data < len(II) and II[herald] < threshold:
            result_Ig.append(II[data])
            result_Ie.append(IQ[data])
    return np.array(result_Ig), np.array(result_Ie)


def single_shot_calibration(Ig, Qg, Ie, Qe, numbins=200):
    """Calibrate the readout discriminant from prepared-|g> and prepared-|e>
    single-shot clouds.

    Steps (verbatim logic from fit_display.hist):
      1. rotate the IQ plane so g and e separate along I:
         theta = -atan2(ye-yg, xe-xg)
      2. histogram the rotated I for g and e
      3. threshold = I maximizing the cumulative-histogram contrast
         |cumsum(ng) - cumsum(ne)| / (0.5*Ng + 0.5*Ne)  (= assignment fidelity)
      4. confusion matrix [Pgg, Pge, Peg, Pee]

    Returns dict: theta_deg, threshold, fidelity_ge, confusion_matrix.
    A shot is later classified |g> if (rotated I) < threshold.
    """
    Ig, Qg, Ie, Qe = map(np.asarray, (Ig, Qg, Ie, Qe))
    xg, yg = np.median(Ig), np.median(Qg)
    xe, ye = np.median(Ie), np.median(Qe)

    theta = -np.arctan2((ye - yg), (xe - xg))
    Ig_r = Ig * np.cos(theta) - Qg * np.sin(theta)
    Ie_r = Ie * np.cos(theta) - Qe * np.sin(theta)

    xg = np.median(Ig_r)
    span = (np.max(np.concatenate((Ie_r, Ig_r))) - np.min(np.concatenate((Ie_r, Ig_r)))) / 2
    xlims = [xg - span, xg + span]
    ng, binsg = np.histogram(Ig_r, bins=numbins, range=xlims, density=True)
    ne, _ = np.histogram(Ie_r, bins=numbins, range=xlims, density=True)

    contrast = np.abs((np.cumsum(ng) - np.cumsum(ne)) / (0.5 * ng.sum() + 0.5 * ne.sum()))
    tind = contrast.argmax()
    threshold = binsg[tind]
    fidelity_ge = contrast[tind]
    # Pgg, Pge, Peg, Pee  (prepare g/e, measure g/e)
    confusion_matrix = [np.cumsum(ng)[tind] / ng.sum(),
                        1 - np.cumsum(ng)[tind] / ng.sum(),
                        np.cumsum(ne)[tind] / ne.sum(),
                        1 - np.cumsum(ne)[tind] / ne.sum()]
    return dict(theta_deg=theta * 180 / np.pi, threshold=threshold,
                fidelity_ge=fidelity_ge, confusion_matrix=confusion_matrix)
