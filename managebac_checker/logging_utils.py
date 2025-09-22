"""Logging helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def setup_logging(debug: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Configure application logging and return the root logger."""
    level = logging.DEBUG if debug else logging.INFO
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_dir / log_file))
    else:
        handlers.append(logging.FileHandler(log_dir / "managebac_checker.log"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )

    logger = logging.getLogger("managebac_checker")
    logger.debug("Logging configured (debug=%s)", debug)
    return logger
