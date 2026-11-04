"""
Simplified (one-energy) event counting
======================================

    N = eps_eff * P(numu -> nue; E0, L) * sigma_CC(E0) * Phi * POT * N_T

used in simplified_event_counting.ipynb, simplified_counting/*.ipynb and
docs/number_of_events.pdf (assumptions, derivation and references).

Everything is per experiment ("T2K", "HyperK", "NOvA", "DUNE") and beam mode
("FHC" = neutrino beam, "RHC" = antineutrino beam).
"""

import numpy as np

from .oscillator import NeutrinoOscillator
from .fluxes import load_flux
from .fetch import fetch_data
from .paths import ROOT

N_A = 6.02214076e23          # nucleons per gram (1 / atomic mass unit), CODATA 2018
MODES = {"FHC": False, "RHC": True}
EXPERIMENTS = ["T2K", "HyperK", "NOvA", "DUNE"]

# --------------------------------------------------------------------------- #
#  Detector and exposure                                                       #
# --------------------------------------------------------------------------- #
SETUP = {
    "T2K": dict(M_kt=22.5, POT={"FHC": 14.94e20, "RHC": 16.35e20}, xs="GLoBES",
                status="current: Run 1-9", target="water (Super-Kamiokande)",
                refs="T2K NIM A 659 (2011) 106; PRD 103 (2021) 112008 (arXiv:2101.03779)"),
    "HyperK": dict(M_kt=187.0, POT={"FHC": 0.675e22, "RHC": 2.025e22}, xs="GLoBES",
                   status="projected: 10 yr at 1.3 MW", target="water",
                   refs="Hyper-K Design Report, arXiv:1805.04163"),
    "NOvA": dict(M_kt=14.0, POT={"FHC": 26.61e20, "RHC": 12.5e20}, xs="GLoBES",
                 status="current: 2024 analysis", target="liquid scintillator (CH2)",
                 refs="PRD 106 (2022) 032004 (arXiv:2108.08219); arXiv:2509.04361"),
    "DUNE": dict(M_kt=40.0, POT={"FHC": 7.15e21, "RHC": 7.15e21}, xs="GENIE-Ar",
                 status="projected: 6.5+6.5 yr at 1.2 MW", target="liquid argon",
                 refs="DUNE TDR configuration, arXiv:2103.04797"),
}

FLUX_REFS = {
    "T2K": "T2K 2020 flux release at Super-K (PRD 87 (2013) 012001)",
    "HyperK": "T2K 2020 flux release at Super-K (same beam, off-axis angle and baseline)",
    "NOvA": "NOvA 2017 near-detector flux (FERMILAB-DATA-2017-01) x (1 km / 810 km)^2",
    "DUNE": "DUNE TDR far-detector flux (arXiv:2103.04797)",
}

# --------------------------------------------------------------------------- #
#  Cross sections                                                              #
# --------------------------------------------------------------------------- #
XCOL = {"nue": 1, "numu": 2, "nutau": 3, "nuebar": 4, "numubar": 5, "nutaubar": 6}
XS_FILES = {
    "GLoBES": (ROOT / "data" / "GLoBES_xsec" / "XCC.dat", False),
    "GLoBES-QE": (ROOT / "data" / "GLoBES_xsec" / "XQE.dat", False),
    "GENIE-Ar": (ROOT / "data" / "DUNE_GLoBES_2103.04797" / "dune_globes" / "xsec" / "xsec_cc.dat", True),
}
XS_REFS = {
    "GLoBES": "GLoBES XCC.dat: Messier PhD thesis (1999, water) + Paschos & Yu PRD 65 (2002) 033002",
    "GLoBES-QE": "GLoBES XQE.dat (quasi-elastic part)",
    "GENIE-Ar": "GENIE 2.12 on argon, DUNE TDR configuration (arXiv:2103.04797), smoothed",
}
_XS = {}


def xs_table(table):
    """sigma/E table [log10(E/GeV), sigma/E in 1e-38 cm^2/GeV per nucleon for 6 flavours]."""
    if table not in _XS:
        fetch_data()
        path, smooth = XS_FILES[table]
        t = np.loadtxt(path)
        if smooth:            # the GENIE table is a noisy MC histogram below ~1 GeV
            k = np.ones(7) / 7
            for j in range(1, t.shape[1]):
                t[:, j] = np.convolve(np.pad(t[:, j], 3, mode="edge"), k, mode="valid")
        _XS[table] = t
    return _XS[table]


def sigma_cc(E, flavour, table="GLoBES"):
    """Cross section per nucleon [cm^2] at energy E [GeV]."""
    t = xs_table(table)
    return np.interp(np.log10(E), t[:, 0], t[:, XCOL[flavour]]) * np.asarray(E) * 1e-38


# --------------------------------------------------------------------------- #
#  Flux, E0 and Phi                                                            #
# --------------------------------------------------------------------------- #
def flux_hist(name, mode, flavour):
    """Histogram of dPhi/dE at the far detector: (edges [GeV], values [nu/cm^2/GeV/POT])."""
    f = load_flux(name, mode)
    return f.edges[flavour], f.values[flavour]


def integrated_flux(name, mode, flavour):
    """Phi of one flavour: sum_k (dPhi/dE)_k dE_k [nu/cm^2/POT]."""
    e, v = flux_hist(name, mode, flavour)
    return np.sum(v * np.diff(e))


def beam_flavour(mode):
    return "numu" if mode == "FHC" else "numubar"


def flux_summary(name, mode, peak_fraction=0.1):
    """Phi = sum_k (dPhi/dE)_k dE_k [nu/cm^2/POT] and E0 = mean energy of the main peak."""
    e, v = flux_hist(name, mode, beam_flavour(mode))
    Ec, dE = 0.5 * (e[1:] + e[:-1]), np.diff(e)
    Phi = np.sum(v * dE)
    peak = v > peak_fraction * v.max()
    E0 = np.sum((v * dE * Ec)[peak]) / np.sum((v * dE)[peak])
    return dict(Phi=Phi, E0=E0, E_mean_all=np.sum(v * dE * Ec) / Phi,
                E_peak_range=(e[:-1][peak].min(), e[1:][peak].max()))


def ingredients(name, mode):
    s = SETUP[name]
    fs = flux_summary(name, mode)
    sig = sigma_cc(fs["E0"], "nuebar" if MODES[mode] else "nue", s["xs"])
    return dict(fs, sigma=sig, NT=s["M_kt"] * 1e9 * N_A, POT=s["POT"][mode], M_kt=s["M_kt"])


# --------------------------------------------------------------------------- #
#  Number of events                                                            #
# --------------------------------------------------------------------------- #
def oscillator(name, mode, ordering="NO", **params):
    return NeutrinoOscillator.from_experiment(name, ordering=ordering, antineutrino=MODES[mode], **params)


def n_events(name, mode, eps=1.0, ordering="NO", ing=None, **params):
    """eps * P(E0) * sigma(E0) * Phi * POT * N_T  (params: oscillation parameters, e.g. delta_cp)."""
    g = ingredients(name, mode) if ing is None else ing
    P = float(oscillator(name, mode, ordering, **params).matter("mu", "e", E=g["E0"]))
    return eps * P * g["sigma"] * g["Phi"] * g["POT"] * g["NT"]


# --------------------------------------------------------------------------- #
#  Effective efficiency: calibration on published predictions                 #
# --------------------------------------------------------------------------- #
_s2 = lambda x: (1 - np.sqrt(1 - x)) / 2          # sin^2(theta) from sin^2(2 theta)

REF_PARAMS = {
    # T2K Table III of arXiv:2101.03779 (delta_CP varied in the fit of Table XI)
    "T2K": dict(s2_12=0.304, s2_13=0.0212, s2_23=0.528, dm2_21=7.53e-5, dm2_31=2.509e-3 + 7.53e-5),
    # Hyper-K Design Report, arXiv:1805.04163, Tables XXXVI-XXXVII
    "HyperK": dict(s2_12=_s2(0.8704), s2_13=_s2(0.10), s2_23=0.5, delta_cp=0.0, dm2_21=7.6e-5,
                   dm2_31=2.4e-3 + 7.6e-5),
    # NOvA best fit, arXiv:2509.04361 (Daya Bay sin^2 2th13, PDG solar parameters)
    "NOvA": dict(s2_12=_s2(0.851), s2_13=_s2(0.0851), s2_23=0.547, delta_cp=0.87 * 180, dm2_21=7.53e-5,
                 dm2_31=2.441e-3 + 7.53e-5),
    # NuFIT 4.0 NO as in Table 1 of arXiv:2103.04797, delta_CP = 0
    "DUNE": dict(s2_12=np.sin(0.5903) ** 2, s2_13=np.sin(0.150) ** 2, s2_23=np.sin(0.866) ** 2,
                 delta_cp=0.0, dm2_21=7.39e-5, dm2_31=2.451e-3 + 7.39e-5),
}

REF_TEXT = {
    "T2K": "Table XI of arXiv:2101.03779: total single-ring e-like events for delta_CP = -pi/2, 0, pi/2, pi "
           "(fit N = eps * N_sig + B), parameters of Table III",
    "HyperK": "Tables XXXVI-XXXVII of the Hyper-K Design Report (arXiv:1805.04163): "
              "numu->nue = 1643, numubar->nuebar = 1183",
    "NOvA": "Table 2 of arXiv:2509.04361: numu->nue = 125.3, numubar->nuebar = 18.9 at the NOvA best fit",
    "DUNE": "right-sign appearance signal of the official GLoBES configuration (arXiv:2103.04797), "
            "NuFIT 4.0 NO, delta_CP = 0",
}

T2K_TABLE_XI = {-np.pi / 2: (74.4, 17.1), 0.0: (62.2, 19.6), np.pi / 2: (50.6, 21.7), np.pi: (62.7, 19.3)}
N_REF = {("HyperK", "FHC"): 1643.0, ("HyperK", "RHC"): 1183.0, ("NOvA", "FHC"): 125.3, ("NOvA", "RHC"): 18.9}


def dune_reference():
    from .dune_globes import DUNEGlobes
    S = DUNEGlobes().all_samples(NeutrinoOscillator("NO", **REF_PARAMS["DUNE"]))
    return {"FHC": S["nue_app"]["FHC_app_osc_nue"].sum(), "RHC": S["nuebar_app"]["RHC_app_osc_nuebar"].sum()}


def calibrate(name, verbose=True):
    """Effective efficiency per beam mode, {mode: eps}, fixed on the published predictions."""
    eps = {}
    for k, m in enumerate(MODES):
        if name == "T2K":
            x = np.array([n_events(name, m, **dict(REF_PARAMS["T2K"], delta_cp=np.degrees(d)))
                          for d in T2K_TABLE_XI])
            y = np.array([v[k] for v in T2K_TABLE_XI.values()])
            e, B = np.linalg.lstsq(np.vstack([x, np.ones_like(x)]).T, y, rcond=None)[0]
            if verbose:
                print(f"{m}: N(eps=1) = {np.round(x, 1)} vs Table XI {y}  ->  eps_eff = {e:.2f}, background B = {B:.1f}")
        else:
            Nref = dune_reference()[m] if name == "DUNE" else N_REF[(name, m)]
            N1 = n_events(name, m, **REF_PARAMS[name])
            e = Nref / N1
            if verbose:
                print(f"{m}: N(eps=1) = {N1:.1f} at the reference parameters, N_ref = {Nref:.1f}  ->  eps_eff = {e:.2f}")
        eps[m] = round(float(e), 2)
    return eps


# --------------------------------------------------------------------------- #
#  Best fits                                                                   #
# --------------------------------------------------------------------------- #
BF_EXP = {   # latest frequentist best fits; missing values -> NuFIT 6.0 of that ordering
    "T2K": {"NO": dict(delta_cp=np.degrees(-2.18) % 360, s2_23=0.559, dm2_32=+2.506e-3, s2_13=0.0221),
            "IO": dict(delta_cp=np.degrees(-1.37) % 360, s2_13=0.0221),
            "ref": "T2K, arXiv:2506.05889"},
    "NOvA": {"NO": dict(delta_cp=0.87 * 180, s2_23=0.547, dm2_32=+2.441e-3, s2_13=_s2(0.0851)),
             "IO": dict(delta_cp=1.53 * 180, s2_23=0.541, dm2_32=-2.481e-3, s2_13=_s2(0.0851)),
             "ref": "NOvA, arXiv:2509.04361"},
}


# --------------------------------------------------------------------------- #
#  CP-violation sensitivity                                                    #
# --------------------------------------------------------------------------- #
def counts(name, eps, ordering, delta_cp, ing=None, **params):
    ing = ing or {m: ingredients(name, m) for m in MODES}
    return np.array([n_events(name, m, eps[m], ordering, ing=ing[m], delta_cp=delta_cp, **params) for m in MODES])


def cpv_sensitivity(name, eps, true_ordering="NO", f=0.0, ordering_known=True, deltas=np.arange(0, 361, 2)):
    """sqrt(Delta chi^2) to exclude delta_CP = 0, pi, vs the true delta_CP (docs/number_of_events.pdf)."""
    ing = {m: ingredients(name, m) for m in MODES}
    tests = [(true_ordering, d) for d in (0, 180)]
    if not ordering_known:
        other = "IO" if true_ordering == "NO" else "NO"
        tests += [(other, d) for d in (0, 180)]
    Ntest = [counts(name, eps, o, d, ing) for o, d in tests]
    out = []
    for d in deltas:
        Nt = counts(name, eps, true_ordering, d, ing)
        var = Nt + (f * Nt) ** 2
        out.append(np.sqrt(min(np.sum((Nt - N0) ** 2 / var) for N0 in Ntest)))
    return deltas, np.array(out)
