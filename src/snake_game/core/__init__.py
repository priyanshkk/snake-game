"""Core Snake modules: pure rules and the pygame presentation layer."""

from __future__ import annotations

from snake_game.core.game import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    GameState,
    is_out_of_bounds,
    next_head,
    opposite,
)

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
