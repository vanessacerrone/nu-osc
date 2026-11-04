# Public far-detector data

These files belong to the experiments and authors and are **not redistributed** with this repository.
`nuosc.fetch` downloads them from the original sources the first time they are needed (or run
`python -m nuosc.fetch`); the SHA-256 of every download is checked. Sources, terms and references to cite
are in [`../CREDITS.md`](../CREDITS.md).

## DUNE TDR GLoBES configuration — `DUNE_GLoBES_2103.04797/`

* Source: ancillary files of DUNE Collaboration, *Experiment Simulation Configurations Approximating
  DUNE TDR*, [arXiv:2103.04797](https://arxiv.org/abs/2103.04797) (v2), downloaded from
  <https://arxiv.org/src/2103.04797v2> (only `anc/dune_globes/` is extracted).
* `dune_globes/`: the GLoBES configuration (`DUNE_GLoBES.glb`, `definitions.inc`, flux, GENIE cross
  sections, smearing matrices, efficiencies), read directly by `nuosc.dune_globes.DUNEGlobes`.
* Default exposure: 6.5 + 6.5 years at 1.1e21 POT/yr (1.2 MW), 40 kt = 624 kt-MW-yr ("10 years staged").

## NOvA 2024 — `NOvA_2024_FD_release/`

* Source: <https://novaexperiment.fnal.gov/data-releases/> → "Oscillation results using 2024
  Bayesian approach" (FERMILAB-DATA-2025-05, [doi:10.5281/zenodo.17822358](https://doi.org/10.5281/zenodo.17822358),
  CC BY 4.0).
* Exposure: 26.61×10²⁰ POT neutrino beam (FHC) + 12.5×10²⁰ POT antineutrino beam (RHC).
* `data_release_2024/`: the content of the archive (ROOT files + NOvA's `README.md`). Only
  `tools/build_fd_spectra.py` reads it (through `nuosc.data.load_nova_2024_numu`, which needs `uproot`):
  the νμ CC sample vs reconstructed energy (all quartiles summed), NOvA's best-fit and no-oscillation
  predictions, and cosmics.

The NOvA predictions are at NOvA's best-fit oscillation parameters and systematic pulls; fits to
these histograms will not exactly reproduce the official NOvA results (see NOvA's README).

## T2K Run 1-9 — `T2K_OA2019_release/`

* T2K does not release far-detector spectra. `csv/T2K_OA2019_SK_event_rates.csv` contains the numbers of
  **Table XI** of T2K Collaboration, PRD 103, 112008 (2021), [arXiv:2101.03779](https://arxiv.org/abs/2101.03779)
  (14.94e20 POT FHC + 16.35e20 POT RHC): predicted events per SK sample for δCP = −π/2, 0, π/2, π, and observed
  events. It is used to normalize `far_detector_spectra/T2K_FD_spectra.csv`.
* `T2K_2101.03779.pdf` (the paper, for reference) is ignored by git.

## Hyper-K Design Report — `HyperK_DR_1805.04163/`

* `HyperK_DesignReport_1805.04163.pdf`: Hyper-Kamiokande Design Report, arXiv:1805.04163 (ignored by git).
  Tables XXXVI–XXXVII (expected νe/νμ candidate events) are used to calibrate
  `far_detector_spectra/HyperK_FD_spectra.csv`; the numbers are copied in `tools/build_fd_spectra.py`.

## GLoBES standard cross sections — `GLoBES_xsec/`

* `XCC.dat`, `XQE.dat`: σ/E per nucleon for CC inclusive and CC quasi-elastic, as distributed with
  GLoBES and its T2K / T2HK / NOvA configurations (<https://www.mpi-hd.mpg.de/personalhomes/globes/glb/>).
* Low energy from M. D. Messier, PhD thesis (1999) (Super-Kamiokande, water); high energy from
  Paschos & Yu, PRD 65, 033002 (2002). See `GLoBES_xsec/README.md`.
