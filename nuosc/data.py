"""
Public far-detector data used to build far_detector_spectra/
=============================================================

Only tools/build_fd_spectra.py needs this module; the notebooks read the finished spectra.

NOvA 2024 data release (FERMILAB-DATA-2025-05, doi:10.5281/zenodo.17822358, CC BY 4.0):
26.61e20 POT neutrino beam + 12.5e20 POT antineutrino beam. `nuosc.fetch` downloads it into
data/NOvA_2024_FD_release/data_release_2024/; reading the ROOT files needs `uproot`
(pip install uproot).

  load_nova_2024_numu(mode) : numu CC sample vs reconstructed energy, all quartiles summed
      keys E_lo, E_hi, data, osc_total, osc_signal, osc_beam_bkg,
           noosc_total, noosc_signal, noosc_beam_bkg, cosmic_bkg
      (predictions at the NOvA best fit and without oscillations)

The NOvA "no oscillation" prediction already contains the true FD flux,
cross sections, efficiencies and energy resolution.
"""

from pathlib import Path

from .fetch import fetch_data
from .paths import ROOT

import numpy as np

DATA_DIR = ROOT / "data"
NOVA_2024_DIR = DATA_DIR / "NOvA_2024_FD_release" / "data_release_2024"
NOVA_2024_POT = {"FHC": 26.61e20, "RHC": 12.5e20}

_NOVA_BEAM = {"FHC": "neutrino", "RHC": "antineutrino"}
_NOVA_PRED = {"osc_total": "Oscillated_Total_pred", "osc_signal": "Oscillated_Signal",
              "osc_beam_bkg": "Oscillated_Beam_bkg", "noosc_total": "NoOscillations_Total_pred",
              "noosc_signal": "NoOscillations_Signal", "noosc_beam_bkg": "NoOscillations_Beam_bkg",
              "cosmic_bkg": "Cosmic_bkg"}


def load_nova_2024_numu(mode="FHC", directory=None):
    """NOvA 2024 FD numu CC sample: dict of arrays (see module docstring) + 'edges', 'pot'."""
    import uproot

    if directory is None:
        fetch_data()
    directory = Path(directory) if directory is not None else NOVA_2024_DIR
    data = uproot.open(directory / "NOvA_2024_data_histograms.root")
    pred = uproot.open(directory / "NOvA_2024_prediction_with_systs_histograms.root")
    quartiles = [data[f"{_NOVA_BEAM[mode]}_mode_numu_quartile{q}"] for q in range(1, 5)]
    edges = quartiles[0].axis().edges()
    out = {"E_lo": edges[:-1], "E_hi": edges[1:], "edges": edges, "pot": NOVA_2024_POT[mode],
           "data": sum(h.values() for h in quartiles)}
    group = pred[f"prediction_components_numu_{mode.lower()}_all"]
    out.update({k: group[name].values() for k, name in _NOVA_PRED.items()})
    return out


# --------------------------------------------------------------------------- #
#  T2K Run 1-9 (arXiv:2101.03779, PRD 103, 112008)                            #
# --------------------------------------------------------------------------- #
# T2K does not publish its far-detector spectra; the public information used here is
#   Table XI of the paper: predicted total events per Super-K sample for four values
#   of delta_CP, plus the observed numbers of events (copied in csv/, with the reference).
T2K_OA2019_CSV = DATA_DIR / "T2K_OA2019_release" / "csv"
T2K_OA2019_POT = {"FHC": 14.94e20, "RHC": 16.35e20}

# Table III of the paper (reference oscillation parameters)
T2K_OA2019_PARAMS = dict(s2_12=0.304, s2_13=0.0212, s2_23=0.528, dm2_21=7.53e-5,
                         dm2_32_NO=2.509e-3, dm2_31_IO=-2.509e-3, delta_cp_rad=-1.601)

T2K_SAMPLES = ("FHC_mu_like", "RHC_mu_like", "FHC_e_like", "RHC_e_like", "FHC_e_CC1pi")


def t2k_oscillator(delta_cp_rad=T2K_OA2019_PARAMS["delta_cp_rad"], ordering="NO"):
    """NeutrinoOscillator with the T2K Table III parameters (delta_CP in radians)."""
    from .oscillator import NeutrinoOscillator
    p = T2K_OA2019_PARAMS
    dm2_31 = p["dm2_32_NO"] + p["dm2_21"] if ordering == "NO" else p["dm2_31_IO"]
    return NeutrinoOscillator(ordering, s2_12=p["s2_12"], s2_13=p["s2_13"], s2_23=p["s2_23"],
                              dm2_21=p["dm2_21"], dm2_31=dm2_31,
                              delta_cp=np.degrees(delta_cp_rad))


def load_t2k_oa2019_rates(directory=None):
    """
    T2K Table XI. Returns (predictions, observed):
      predictions : dict delta_cp_rad -> dict sample -> events
      observed    : dict sample -> events
    """
    directory = Path(directory) if directory is not None else T2K_OA2019_CSV
    pred, obs = {}, {}
    for line in open(directory / "T2K_OA2019_SK_event_rates.csv"):
        if line.startswith("#") or not line.strip():
            continue
        v = line.strip().split(",")
        vals = dict(zip(T2K_SAMPLES, map(float, v[1:])))
        if v[0] == "observed":
            obs = vals
        else:
            pred[float(v[0])] = vals
    return pred, obs
