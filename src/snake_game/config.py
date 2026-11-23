"""Runtime configuration for Snake.

The three gameplay values are read from environment variables at import time so
the same build can be tuned without editing source code. Invalid or missing
values fall back to the documented defaults.

Attributes:
    CELL_SIZE: Pixel size of one board cell (``SNAKE_CELL_SIZE``).
    FPS: Frames per second of the game loop (``SNAKE_FPS``).
    BOARD_SIZE: Width and height of the square board (``SNAKE_BOARD_SIZE``).
"""

from __future__ import annotations

import os


def env_int(name: str, default: int, *, minimum: int = 1) -> int:
    """Read a positive integer from the environment.

    Args:
        name: Environment variable name.
        default: Value to use when the variable is absent or invalid.
        minimum: Smallest accepted value; smaller values use ``default``.

    Returns:
        The parsed integer, or ``default`` when parsing fails.
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= minimum else default


CELL_SIZE = env_int("SNAKE_CELL_SIZE", 28)
FPS = env_int("SNAKE_FPS", 12)
BOARD_SIZE = env_int("SNAKE_BOARD_SIZE", 20, minimum=2)

BACKGROUND = (18, 18, 24)
GRID_COLOR = (34, 34, 44)
SNAKE_COLOR = (80, 220, 140)
HEAD_COLOR = (140, 255, 180)
FOOD_COLOR = (255, 110, 120)
TEXT_COLOR = (235, 235, 245)
CAPTION = "Snake - Python"

__all__ = [
    "BOARD_SIZE",
    "CAPTION",
    "CELL_SIZE",
    "FPS",
    "env_int",
]
