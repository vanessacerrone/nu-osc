"""
Download the public data files
==============================

The fluxes, cross sections and detector configurations belong to the experiments and
authors, so they are not redistributed with this repository. `fetch_data()` downloads
them once from the original sources (listed in CREDITS.md) into fluxes/ and data/,
checks their SHA-256, and does nothing when the files are already there.

The loaders (load_flux, DUNEGlobes, the cross-section tables) call it automatically.
To download everything by hand:

    python -m nuosc.fetch
"""

import hashlib
import shutil
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .paths import ROOT

_DUNE = "data/DUNE_GLoBES_2103.04797"
_DUNE_FLUX = _DUNE + "/dune_globes/flux/histos_g4lbne_v3r5p4_QGSP_BERT_OptimizedEngineeredNov2017_{}_LBNEFD_globes_flux.txt"
_NOVA_ND = "https://publicdocs.fnal.gov/cgi-bin/RetrieveFile?docid=8&filename={}&version=1"

# Each source: url, sha256 of the download, where it goes, and how to unpack it.
#   file    : saved as `dest`
#   archive : members starting with `keep` are extracted into `dest`, without the `strip` prefix
#   copies  : extra copies made after unpacking (new path -> unpacked path)
#   done    : files whose presence means the source is already downloaded
SOURCES = [
    dict(name="T2K 2020 flux release",
         url="https://t2k-experiment.org/wp-content/uploads/T2Kflux2020.gz",
         sha256="0c8e921ede08508d192cb203ebfb6386d15fbc7ab6ad099ebfd503cae12a8569",
         archive=True, dest="fluxes/T2K",
         done=["fluxes/T2K/t2kflux_2020_public_release/t2kflux_2020_plus250kA_nominal_sk.txt",
               "fluxes/T2K/t2kflux_2020_public_release/t2kflux_2020_minus250kA_nominal_sk.txt"]),
    dict(name="DUNE TDR GLoBES configuration (arXiv:2103.04797v2 ancillary files)",
         url="https://arxiv.org/src/2103.04797v2",
         sha256="574975ab4d1b7e77eb3e99dca0ae309050ff54145bcc380388fa805aef636824",
         archive=True, keep="anc/dune_globes/", strip="anc/", dest=_DUNE,
         copies={"fluxes/DUNE/DUNE_FD_FHC_flux_globes.txt": _DUNE_FLUX.format("neutrino"),
                 "fluxes/DUNE/DUNE_FD_RHC_flux_globes.txt": _DUNE_FLUX.format("antineutrino")},
         done=[_DUNE + "/dune_globes/DUNE_GLoBES.glb",
               "fluxes/DUNE/DUNE_FD_FHC_flux_globes.txt", "fluxes/DUNE/DUNE_FD_RHC_flux_globes.txt"]),
    dict(name="NOvA 2024 data release (doi:10.5281/zenodo.17822358)",
         url="https://zenodo.org/api/records/21284589/files/data_release_2024.zip/content",
         sha256="9ef7b65dda776590c07209f4c5a9879c41a9cc08677b3016189d87b57b365858",
         archive=True, dest="data/NOvA_2024_FD_release",
         done=["data/NOvA_2024_FD_release/data_release_2024/NOvA_2024_prediction_with_systs_histograms.root",
               "data/NOvA_2024_FD_release/data_release_2024/NOvA_2024_data_histograms.root"]),
    dict(name="GLoBES XCC.dat", url="https://www.mpi-hd.mpg.de/personalhomes/globes/glb/XCC.dat",
         sha256="c389fd6697b5fe860a52681dfe91cbedbd68c0b40be6ac3a2263728e233d7297",
         dest="data/GLoBES_xsec/XCC.dat"),
    dict(name="GLoBES XQE.dat", url="https://www.mpi-hd.mpg.de/personalhomes/globes/glb/XQE.dat",
         sha256="b112cd6ab57adfdee7eae77cc7e243502af427dc63d513cc841b494991a0e5f6",
         dest="data/GLoBES_xsec/XQE.dat"),
] + [
    dict(name=f"NOvA 2017 ND flux {f}", url=_NOVA_ND.format(f), sha256=h, dest=f"fluxes/NOvA/{f}")
    for f, h in [
        ("FHC_Flux_nue_NOvA_ND_2017.txt", "0e80cd4362f5e391039c43a31c18a124a0d7c1f97685c2ea50731ee29f59a56b"),
        ("FHC_Flux_nuebar_NOvA_ND_2017.txt", "d483e1a5c90e78066197c1b405cb2627c18f3aff13e4b291782faf3ed65d5e55"),
        ("FHC_Flux_numu_NOvA_ND_2017.txt", "c9477c7517e5269361994b8a39eccb2c54732920d1917e538339b1758a19c505"),
        ("FHC_Flux_numubar_NOvA_ND_2017.txt", "d429ccc573469a924815c248b521bd2aea396f8e46770b5884d3c5292c5be959"),
        ("RHC_Flux_nue_NOvA_ND_2017.txt", "0e3085fd495294dbf3e17dbdb32b9b29b0b5aab846cff08119b4443a913f81af"),
        ("RHC_Flux_nuebar_NOvA_ND_2017.txt", "1622dce9549da4bec50f63a018a19cac6450a01599b4f326511173382c8a7590"),
        ("RHC_Flux_numu_NOvA_ND_2017.txt", "edd8b876ed37d1f6f535d00f4434b7b93a8156212f9f151729aabf0bc1e59ed5"),
        ("RHC_Flux_numubar_NOvA_ND_2017.txt", "7ba49a5a3a2fdadd7fe095be6cb260c48c45328a9e4a9220d18cbe07942c664b"),
    ]
]


def _download(url, path):
    # some servers refuse Python's default user agent
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
        shutil.copyfileobj(r, f)


def _members(path):
    """(name, file object opener) for every regular file in a tar or zip archive."""
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        return [(i.filename, lambda i=i: z.open(i)) for i in z.infolist() if not i.is_dir()]
    t = tarfile.open(path)
    return [(m.name, lambda m=m: t.extractfile(m)) for m in t.getmembers() if m.isfile()]


def _unpack(path, dest, keep="", strip=""):
    dest = dest.resolve()
    for name, opener in _members(path):
        if not name.startswith(keep) or Path(name).name.startswith("._"):   # skip macOS metadata
            continue
        out = (dest / name[len(strip):]).resolve()
        if dest not in out.parents:           # refuse "../" tricks in archive names
            raise RuntimeError(f"unsafe path in archive: {name}")
        out.parent.mkdir(parents=True, exist_ok=True)
        with opener() as src, open(out, "wb") as f:
            shutil.copyfileobj(src, f)


def _is_done(s, root):
    return all((root / p).is_file() for p in s.get("done", [s["dest"]]))


def fetch_data(root=None, verbose=True):
    """Download every missing data file. Returns the list of sources downloaded."""
    root = Path(root) if root is not None else ROOT
    got = []
    for s in SOURCES:
        if _is_done(s, root):
            continue
        if verbose:
            print(f"downloading {s['name']}\n  from {s['url']}")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_file = Path(tmp) / "download"
            try:
                _download(s["url"], tmp_file)
            except OSError as e:
                raise RuntimeError(
                    f"could not download {s['name']} from {s['url']} ({e}).\n"
                    f"Check your internet connection, or download it by hand into {root / s['dest']}"
                ) from e
            h = hashlib.sha256(tmp_file.read_bytes()).hexdigest()
            if h != s["sha256"]:
                raise RuntimeError(f"{s['name']}: SHA-256 mismatch ({h}); the source file has changed. "
                                   "Please open an issue.")
            dest = root / s["dest"]
            if s.get("archive"):
                _unpack(tmp_file, dest, s.get("keep", ""), s.get("strip", ""))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(tmp_file, dest)
        for new, old in s.get("copies", {}).items():
            (root / new).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / old, root / new)
        got.append(s["name"])
    return got


if __name__ == "__main__":
    n = fetch_data()
    print(f"{len(n)} source(s) downloaded" if n else "all data files already present")
