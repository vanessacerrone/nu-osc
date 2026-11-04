# Credits, third-party material and how to cite

This repository builds on other people's code, algorithms, data and results. This file lists all of them,
with what we took, where it is used, the reference to cite and the terms of use as stated by the authors.
**If you use this repository, please cite the original works below**, not only this repository.

The repository is an educational project. It is not endorsed by, and does not speak for, any of the
collaborations whose public results are used. Our approximations do not reproduce their official results.

## 1. Code and algorithms

| what | used in | license / terms | cite |
|---|---|---|---|
| **NuFast** algorithm for oscillation probabilities in constant-density matter, by P. B. Denton and S. J. Parke. Our `prob_matter_nufast` is a NumPy re-implementation following the reference implementation <https://github.com/PeterDenton/NuFast> (see the notice below). | `nuosc/formulas.py` | MIT License, Copyright (c) 2024 Peter B. Denton | P. B. Denton and S. J. Parke, *Fast and accurate algorithm for calculating long-baseline neutrino oscillation probabilities with matter effects: NuFast*, [arXiv:2405.02400](https://arxiv.org/abs/2405.02400) |
| **GLoBES** event-rate recipe (flux × cross section × probability, smearing matrices, efficiencies, AEDL normalisation). We re-implemented the recipe in Python to read the DUNE configuration; no GLoBES code is included. | `nuosc/dune_globes.py` | GLoBES is free software under the GNU GPL | P. Huber, M. Lindner, W. Winter, Comput. Phys. Commun. 167, 195 (2005), [hep-ph/0407333](https://arxiv.org/abs/hep-ph/0407333); P. Huber, J. Kopp, M. Lindner, M. Rolinec, W. Winter, Comput. Phys. Commun. 177, 432 (2007), [hep-ph/0701187](https://arxiv.org/abs/hep-ph/0701187) |
| **IBM colour-blind-safe palette** (IBM Design Library) | `nuosc/plotting.py` | colour values only | — |
| **SciencePlots** (optional plot style, installed as a dependency) | `nuosc/plotting.py` | MIT License | J. D. Garrett, *SciencePlots*, Zenodo, [doi:10.5281/zenodo.4106649](https://doi.org/10.5281/zenodo.4106649) |
| NumPy, Matplotlib, Jupyter (dependencies) | everywhere | BSD-style licenses | C. R. Harris et al., Nature 585, 357 (2020); J. D. Hunter, Comput. Sci. Eng. 9, 90 (2007) |

### NuFast license notice

```
MIT License

Copyright (c) 2024 Peter B. Denton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 2. Physics inputs

| what | used in | cite |
|---|---|---|
| Default oscillation parameters: NuFIT 6.0 (IC24 with SK atmospheric data) | `nuosc/parameters.py` | I. Esteban, M. C. Gonzalez-Garcia, M. Maltoni, I. Martinez-Soler, J. P. Pinheiro, T. Schwetz, *NuFit-6.0*, JHEP 12 (2024) 216, [arXiv:2410.05380](https://arxiv.org/abs/2410.05380), <http://www.nu-fit.org> |
| T2K best fit | `nuosc/simple_counting.py` | T2K Collaboration, [arXiv:2506.05889](https://arxiv.org/abs/2506.05889) |
| NOvA best fit, with the Daya Bay sin²2θ13 constraint | `nuosc/simple_counting.py`, `tools/build_fd_spectra.py` | NOvA Collaboration, [arXiv:2509.04361](https://arxiv.org/abs/2509.04361), [doi:10.1103/x53y-2b86](https://doi.org/10.1103/x53y-2b86); Daya Bay Collaboration, Phys. Rev. Lett. 130, 161802 (2023) |
| Hyper-K exposure, detector and expected event numbers | `nuosc/experiments.py`, `nuosc/simple_counting.py`, `tools/build_fd_spectra.py` | Hyper-Kamiokande Collaboration, *Design Report*, [arXiv:1805.04163](https://arxiv.org/abs/1805.04163) |
| DUNE configuration and sensitivity definition | `nuosc/dune_globes.py`, docs | DUNE Collaboration, Eur. Phys. J. C 80, 978 (2020), [arXiv:2006.16043](https://arxiv.org/abs/2006.16043); DUNE Far Detector TDR Vol. II, [arXiv:2002.03005](https://arxiv.org/abs/2002.03005) |

All other references (cross sections, statistics) are listed in `docs/number_of_events.pdf`.

## 3. Data files (downloaded from the original sources)

The files below are public releases of the experiments and authors. **They are not redistributed with this
repository**: `nuosc.fetch` downloads them from the sources listed here the first time they are needed (or with
`python -m nuosc.fetch`), checks their SHA-256, and stores them in `fluxes/` and `data/`, which git ignores. They
are not covered by the license of this repository: all rights remain with their authors.

| folder | content | downloaded from | terms stated by the source | cite |
|---|---|---|---|---|
| `fluxes/T2K/` | T2K 2020 flux prediction at Super-K (and ND280) | <https://t2k-experiment.org/results/neutrino-beam-flux-prediction-2020/> | "© The T2K Collaboration, all rights reserved"; no explicit reuse terms | T2K Collaboration, Phys. Rev. D 87, 012001 (2013), [arXiv:1211.0469](https://arxiv.org/abs/1211.0469) |
| `fluxes/NOvA/` | NuMI flux at the NOvA near detector, 2017 analysis | NOvA, *Flux Histograms for 2017 Analysis*, FERMILAB-DATA-2017-01, [doi:10.15484/1959359](https://doi.org/10.15484/1959359) | "Any use of NOvA data releases or associated work must acknowledge the NOvA collaboration and appropriate funding agencies" (<https://novaexperiment.fnal.gov/data-releases/>) | the DOI |
| `fluxes/DUNE/`, `data/DUNE_GLoBES_2103.04797/` | DUNE far-detector flux (Optimized Engineered Nov 2017 beam) and GLoBES configuration: ancillary files of arXiv:2103.04797 (v2) | <https://arxiv.org/src/2103.04797v2> (only `anc/dune_globes/` is extracted) | DUNE "requests that any results making use of these files reference this arXiv posting" and the TDR oscillation paper | DUNE Collaboration, [arXiv:2103.04797](https://arxiv.org/abs/2103.04797) and Eur. Phys. J. C 80, 978 (2020), [arXiv:2006.16043](https://arxiv.org/abs/2006.16043) |
| `data/NOvA_2024_FD_release/` | NOvA 2024 data release (ROOT files, README); used only to rebuild `far_detector_spectra/` | NOvA, FERMILAB-DATA-2025-05, [doi:10.5281/zenodo.17822358](https://doi.org/10.5281/zenodo.17822358) | CC BY 4.0 (Zenodo record); acknowledge the NOvA collaboration and funding agencies (as above) | NOvA Collaboration, [doi:10.1103/x53y-2b86](https://doi.org/10.1103/x53y-2b86) and the release DOI |
| `data/GLoBES_xsec/` | standard GLoBES cross-section tables (XCC, XQE) | <https://www.mpi-hd.mpg.de/personalhomes/globes/glb/> | distributed with GLoBES | M. D. Messier, PhD thesis, Boston University (1999); E. A. Paschos and J. Y. Yu, Phys. Rev. D 65, 033002 (2002); GLoBES papers above |

Kept in the repository:

| file | content | cite |
|---|---|---|
| `data/T2K_OA2019_release/csv/T2K_OA2019_SK_event_rates.csv` | the numbers of Table XI of the T2K Run 1–9 paper (predicted and observed events per Super-K sample), transcribed from the paper | T2K Collaboration, Phys. Rev. D 103, 112008 (2021), [arXiv:2101.03779](https://arxiv.org/abs/2101.03779) |
| `far_detector_spectra/` | spectra built by us (`tools/build_fd_spectra.py`) from the inputs above | the inputs above |

Papers downloaded for reference (`*.pdf` in `data/`) are not redistributed (ignored by git).

## 4. How to cite this repository

See `CITATION.cff` (GitHub shows a "Cite this repository" button). Please also cite NuFast and NuFIT
when you use the probabilities, and the experiments' releases when you use their data.
