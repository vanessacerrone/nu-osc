# Number of νe appearance events: the short version

**N = P(νμ→νe; E₀, L) × σ_CC(E₀) × Φ × POT × N_T**, or in handy units **N ≈ 60.2 · P · [σ/10⁻³⁸ cm²] · [Φ/10⁻¹⁴ cm⁻² POT⁻¹] · [POT/10²¹] · [M/kt]**.

N is the number of νe (ν̄e) charged-current interactions in the fiducial volume, i.e. the number of events seen by a perfect detector (efficiency = 1). The last section explains why the experiments see a different number.

- **Φ × POT** is the beam side: the number of νμ crossing each cm² of the far detector (fluence). Φ = ∫ (dΦ/dE) dE = Σₖ (dΦ/dE)ₖ ΔEₖ is the νμ (ν̄μ) flux per proton on target **integrated over the whole energy spectrum** (not taken at E₀), summing the bins of the public flux histograms (T2K: PRD 87, 012001 (2013); NOvA: FERMILAB-DATA-2017-01; DUNE: arXiv:2103.04797). POT is the exposure, POT = beam power × time / proton energy.
- **σ_CC × N_T** is the detector side: the target area seen by a neutrino. N_T = M·N_A is the number of nucleons in the fiducial mass M. σ_CC is the inclusive charged-current cross section per nucleon (GLoBES tables, Comput. Phys. Commun. 167, 195 (2005); GENIE on argon for DUNE, arXiv:2103.04797).
- **P** is the oscillation probability in matter (NuFast, arXiv:2405.02400). The tables use the NuFIT 6.0 best fit (JHEP 12 (2024) 216); P is the only factor that depends on the oscillation parameters (δCP, mass ordering, θ23, …), so changing them changes N only through P.
- **E₀** replaces the energy spectrum by a single energy, the mean energy of the beam peak (≈ 0.6 GeV for T2K/Hyper-K, 1.8 GeV for NOvA, 2.3 GeV for DUNE).
- **Assumptions:** a pure νμ (ν̄μ) beam, one energy, every interaction detected, no backgrounds, constant matter density. The formula gives no energy spectrum.

![Schematic of an accelerator neutrino beam in neutrino mode (not to scale): protons on a graphite target, two magnetic horns focusing π⁺/K⁺ and defocusing π⁻, decay pipe (96 m T2K, 675 m NuMI, 194 m LBNF), absorber and rock. Reversing the horn current gives the ν̄μ beam.](figures/beamline.png)

**Inputs** (NuFIT 6.0 normal ordering for P):

| | L [km] | M [kt] | POT (ν / ν̄) | E₀ [GeV] | Φ [10⁻¹⁴ cm⁻² POT⁻¹] (ν / ν̄) | σ_CC(E₀) [10⁻³⁸ cm²] (ν / ν̄) | P(E₀) (ν / ν̄) |
|---|---|---|---|---|---|---|---|
| T2K | 295 | 22.5 | 1.494e21 / 1.635e21 | 0.57 / 0.55 | 1.207 / 0.976 | 0.407 / 0.116 | 0.0533 / 0.0316 |
| Hyper-K | 295 | 187 | 6.75e21 / 2.025e22 | 0.57 / 0.55 | 1.207 / 0.976 | 0.407 / 0.116 | 0.0533 / 0.0316 |
| NOvA | 810 | 14 | 2.661e21 / 1.25e21 | 1.80 / 1.79 | 1.806 / 1.467 | 1.43 / 0.631 | 0.0547 / 0.0249 |
| DUNE | 1300 | 40 | 7.15e21 / 7.15e21 | 2.31 / 2.27 | 1.548 / 1.385 | 1.78 / 0.729 | 0.0738 / 0.0178 |

**Worked out** (N_P=1 = 60.2 · σ · Φ · POT · M in the units above; then × P):

| | beam | N_P=1 | N = N_P=1 × P |
|---|---|---|---|
| T2K | ν | 60.2 × 0.407 × 1.207 × 1.494 × 22.5 = 994 | **53** |
| | ν̄ | 60.2 × 0.116 × 0.976 × 1.635 × 22.5 = 251 | **7.9** |
| Hyper-K | ν | 60.2 × 0.407 × 1.207 × 6.75 × 187 = 37 329 | **1990** |
| | ν̄ | 60.2 × 0.116 × 0.976 × 20.25 × 187 = 25 809 | **816** |
| NOvA | ν | 60.2 × 1.43 × 1.806 × 2.661 × 14 = 5792 | **317** |
| | ν̄ | 60.2 × 0.631 × 1.467 × 1.25 × 14 = 975 | **24** |
| DUNE | ν | 60.2 × 1.78 × 1.548 × 7.15 × 40 = 47 441 | **3501** |
| | ν̄ | 60.2 × 0.729 × 1.385 × 7.15 × 40 = 17 384 | **309** |

**Sensitivity to CP violation.** Each sample has a statistical error √N. Comparing the true δCP with the CP-conserving values (0, π) gives Δχ² = min over δ′ ∈ {0, π} of Σ (N(δCP) − N(δ′))² / N(δCP), with significance √Δχ² (PDG, Statistics review). With the numbers above (true normal ordering, statistics only) the maximum significance is 2.5σ (T2K), 4.4σ (NOvA), 17σ (Hyper-K), 18σ (DUNE).

## Why the experiments see a different number

The collaborations publish the expected appearance signal from full simulations. At the same oscillation parameters, the ratio r = N_published / N would be 1 if the formula were exact; it is 0.4–1.1. It splits as r = ε_det × c_mono:

- **Detection (ε_det < 1):** not every νe interaction is selected (efficiency and cuts); in practice it also absorbs the differences between our cross sections and the collaborations' generators.
- **One energy (c_mono):** in the ν beams E₀ is near the oscillation maximum while many neutrinos have energies where P is smaller, so the formula overestimates (c_mono ≈ 0.8). In the ν̄ beams the antineutrino cross section grows quickly with energy, so the high-energy flux weighs more (c_mono ≈ 1 at T2K/Hyper-K, 1.4 at DUNE).

So r < 1 in the ν beams and r ≈ 1 or > 1 in the ν̄ beams of Hyper-K and DUNE. r is not an efficiency, and it is not due to beam contamination (the references are right-sign signal only).

| | beam | N (formula) | N_published | r | c_mono | ε_det = r / c_mono | reference |
|---|---|---|---|---|---|---|---|
| T2K | ν | 61.6 | 54.8 | 0.89 | 0.81 | 1.10 | arXiv:2101.03779, Table XI (minus fitted background) |
| | ν̄ | 6.7 | 4.8 | 0.71 | 1.06 | 0.68 | arXiv:2101.03779, Table XI (minus fitted background) |
| Hyper-K | ν | 2064 | 1643 | 0.80 | 0.85 | 0.94 | arXiv:1805.04163, Tables XXXVI–XXXVII |
| | ν̄ | 1156 | 1183 | 1.02 | 1.00 | 1.02 | arXiv:1805.04163, Tables XXXVI–XXXVII |
| NOvA | ν | 290.5 | 125.3 | 0.43 | 0.79 | 0.54 | arXiv:2509.04361, Table 2 |
| | ν̄ | 37.2 | 18.9 | 0.51 | 0.83 | 0.61 | arXiv:2509.04361, Table 2 |
| DUNE | ν | 3486 | 2180 | 0.63 | 0.78 | 0.79 | arXiv:2103.04797, GLoBES configuration |
| | ν̄ | 409 | 438 | 1.07 | 1.39 | 0.77 | arXiv:2103.04797, GLoBES configuration |

**Consequences.** Everything that depends only on P (bi-probability plots, shape of the δCP dependence, degeneracies) is unchanged. The event numbers are those of a perfect detector (about twice the published ones for NOvA, within ~40 % for the others), so the significances are optimistic: multiplying each sample by r, the maximum CP-violation sensitivity (statistics only, true NO) becomes 2.3σ (T2K), 2.9σ (NOvA), 16σ (Hyper-K), 16σ (DUNE). With a 5 % normalization uncertainty Hyper-K and DUNE (8.6–9.4σ) hardly change.

- **Details, derivations and full references:** `docs/number_of_events.pdf`.
