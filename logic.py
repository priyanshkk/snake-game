"""Backward-compatible import path for the pure Snake rules engine.

New code should import from :mod:`snake_game.core.game`. The ``src/`` path is
bootstrapped so this shim also works from a source checkout.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from snake_game.core.game import DOWN as DOWN  # noqa: E402
from snake_game.core.game import LEFT as LEFT  # noqa: E402
from snake_game.core.game import RIGHT as RIGHT  # noqa: E402
from snake_game.core.game import UP as UP  # noqa: E402
from snake_game.core.game import GameState as GameState  # noqa: E402
from snake_game.core.game import is_out_of_bounds as is_out_of_bounds  # noqa: E402
from snake_game.core.game import next_head as next_head  # noqa: E402
from snake_game.core.game import opposite as opposite  # noqa: E402

__all__ = [
    "DOWN",
    "LEFT",
    "RIGHT",
    "UP",
    "GameState",
    "is_out_of_bounds",
    "next_head",
    "opposite",
]
