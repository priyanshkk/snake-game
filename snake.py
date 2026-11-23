"""Backward-compatible launcher for the pygame game.

New code should use ``python -m snake_game``. The ``src/`` path is bootstrapped
so this shim also works from a source checkout.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from snake_game.__main__ import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
