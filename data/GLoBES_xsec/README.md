# GLoBES standard neutrino cross sections

Original files distributed with GLoBES and with its T2K / T2HK / NOvA experiment configurations.
They are not redistributed here: `nuosc.fetch` downloads them, unchanged, from
<https://www.mpi-hd.mpg.de/personalhomes/globes/glb/> (`XCC.dat`, `XQE.dat`).

| file | content |
|------|---------|
| `XCC.dat` | charged-current **inclusive** cross section |
| `XQE.dat` | charged-current **quasi-elastic** cross section |

Format (one row per energy): `log10(E/GeV)`, then σ/E in units of 10⁻³⁸ cm²/GeV **per nucleon** for
νe, νμ, ντ, ν̄e, ν̄μ, ν̄τ (log10 E from −1 to 3, i.e. 0.1 GeV – 1 TeV).
At high energy σ/E → 0.67 (ν) and 0.335 (ν̄) × 10⁻³⁸ cm²/GeV, the isoscalar deep-inelastic values.

**References to cite** (from the file headers):

* low energy: M. D. Messier, *Evidence for neutrino mass from observations of atmospheric neutrinos with
  Super-Kamiokande*, PhD thesis, Boston University (1999), UMI-99-23965 — cross sections for water used in
  Super-Kamiokande;
* high energy: E. A. Paschos and J. Y. Yu, *Neutrino interactions in oscillation experiments*,
  Phys. Rev. D 65, 033002 (2002), hep-ph/0107261;
* GLoBES: P. Huber, M. Lindner, W. Winter, Comput. Phys. Commun. 167, 195 (2005), hep-ph/0407333;
  P. Huber, J. Kopp, M. Lindner, M. Rolinec, W. Winter, Comput. Phys. Commun. 177, 432 (2007), hep-ph/0701187.
