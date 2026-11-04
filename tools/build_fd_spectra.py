"""
Rebuild far_detector_spectra/ from the downloaded public data (the code is in nuosc/fd_build.py).

    python tools/build_fd_spectra.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nuosc.fd_build import build_all    # noqa: E402

build_all()
