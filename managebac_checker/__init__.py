"""Top-level package for managebac_checker.

Keep imports minimal to avoid heavy optional dependencies (e.g., Playwright,
tkinter) during package import, so lightweight modules like `analysis`,
`reporting`, and `config` can be imported in isolated unit tests without
requiring those extras.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as _version

# Expose package version if available; fallback for editable/dev installs.
try:  # pragma: no cover - resolved at runtime in packaged builds
    __version__ = _version("managebac-assignment-checker")
except PackageNotFoundError:  # pragma: no cover - development fallback
    __version__ = "0.0.0"

# Public API note: submodules should be imported directly, e.g.:
#   from managebac_checker.analysis import analyse_assignments
# to prevent importing optional heavy dependencies at package import time.

__all__ = ["__version__"]
