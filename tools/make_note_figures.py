"""Figures for docs/number_of_events_summary.tex: fluxes and cross sections used in the simplified formula.

The figures are drawn at their final size in the document (text width 6.7 in), so font sizes are real sizes.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nuosc import simple_counting as sc
from nuosc.plotting import IBM_COLOR_CYCLE
from nuosc.paths import ROOT

LEGEND_SIZE = 12

# plot style: latex_style if available, otherwise an equivalent LaTeX look (serif, ticks inside on all sides)
if "latex_style" in plt.style.available:
    plt.style.use("latex_style")
else:
    plt.style.use("default")
    plt.rcParams.update({
        "text.usetex": True, "font.family": "serif", "font.size": 11,
        "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
        "xtick.minor.visible": True, "ytick.minor.visible": True,
        "xtick.major.size": 5, "ytick.major.size": 5, "xtick.minor.size": 2.5, "ytick.minor.size": 2.5,
        "axes.linewidth": 0.8, "legend.frameon": False, "savefig.bbox": "tight",
    })
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", IBM_COLOR_CYCLE)
c = IBM_COLOR_CYCLE
OUT = ROOT / "docs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- fluxes
panels = [("T2K", "T2K / Hyper-K", 2.0), ("NOvA", "NOvA", 5.0), ("DUNE", "DUNE", 8.0)]
fig, axes = plt.subplots(1, 3, figsize=(6.7, 2.6))
for ax, (name, title, xmax) in zip(axes, panels):
    txt = []
    for j, m in enumerate(sc.MODES):
        e, v = sc.flux_hist(name, m, sc.beam_flavour(m))
        g = sc.flux_summary(name, m)
        ax.stairs(v / 1e-14, e, color=c[j], lw=1.3)
        ax.axvline(g["E0"], color=c[j], ls="--", lw=0.9)
        txt.append(rf"$\Phi = {g['Phi'] / 1e-14:.2f}$")
    for j, t in enumerate(txt):
        ax.text(0.96, 0.93 - 0.11 * j, t, color=c[j], transform=ax.transAxes, ha="right", va="top", fontsize=10)
    ax.set_xlim(0, xmax)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$E_\nu$ [GeV]")
    ax.set_title(title, fontsize=11)
axes[0].set_ylabel(r"$d\Phi/dE$ [$10^{-14}$ cm$^{-2}$ GeV$^{-1}$ POT$^{-1}$]", fontsize=9)
handles = [plt.Line2D([], [], color=c[0], lw=1.5, label=r"$\nu_\mu$, $\nu$ beam"),
           plt.Line2D([], [], color=c[1], lw=1.5, label=r"$\bar\nu_\mu$, $\bar\nu$ beam"),
           plt.Line2D([], [], color="gray", ls="--", lw=1, label=r"$E_0$")]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=LEGEND_SIZE, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "fluxes.pdf")
plt.close()

# ---------------------------------------------------------------- cross sections
E = np.logspace(-1, np.log10(20), 500)
fig, ax = plt.subplots(figsize=(6.3, 3.3))
lines = []
for j, (fl, lab) in enumerate((("nue", r"$\nu_e$"), ("nuebar", r"$\bar\nu_e$"))):
    lines += ax.plot(E, sc.sigma_cc(E, fl, "GLoBES") / E / 1e-38, color=c[j], lw=1.3, label=f"{lab}, GLoBES")
    lines += ax.plot(E, sc.sigma_cc(E, fl, "GENIE-Ar") / E / 1e-38, color=c[j], lw=1.3, ls="--", label=f"{lab}, GENIE (Ar)")
marks = {"T2K": "o", "NOvA": "s", "DUNE": "D"}
for name, mk in marks.items():
    for j, m in enumerate(sc.MODES):
        g = sc.ingredients(name, m)
        ax.plot(g["E0"], g["sigma"] / g["E0"] / 1e-38, mk, color=c[j], mec="k", mew=0.5, ms=5)
    lines.append(plt.Line2D([], [], marker=mk, ls="none", color="gray", mec="k", mew=0.5,
                            label=(name if name != "T2K" else "T2K / HK") + r" at $E_0$"))
ax.set_xscale("log")
ax.set_ylim(0, 1.0)
ax.set_xlabel(r"$E_\nu$ [GeV]")
ax.set_ylabel(r"$\sigma_{CC}/E$ [$10^{-38}$ cm$^2$ GeV$^{-1}$]")
ax.legend(handles=lines, fontsize=LEGEND_SIZE, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
plt.tight_layout()
plt.savefig(OUT / "cross_sections.pdf")
plt.close()
print("written", sorted(p.name for p in OUT.iterdir()))
