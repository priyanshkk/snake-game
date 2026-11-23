"""Command-line entry point for Snake.

Running ``python -m snake_game`` launches the pygame window. The ``--demo``
flag runs the same rules engine headlessly, which is useful on servers and in
continuous integration.
"""

from __future__ import annotations

import argparse
import sys
from random import Random

from snake_game import config
from snake_game.core.game import GameState, next_head


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the Snake CLI.

    Returns:
        A parser with the interactive and headless demo options.
    """
    parser = argparse.ArgumentParser(
        prog="snake-game",
        description="Play Snake in a pygame window, or run a headless demo.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="run a deterministic simulation instead of opening a window",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=3,
        help="number of demo steps (default: 3)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="seed for demo food placement (default: 7)",
    )
    return parser


def simulate(steps: int, seed: int) -> str:
    """Run a deterministic, headless simulation of the real game rules.

    Food is placed directly in front of the head for the first step so the
    growth and scoring path is visible. Subsequent food uses the seeded
    generator, exactly as in an interactive game.

    Args:
        steps: Maximum number of ticks to simulate; must be positive.
        seed: Seed used for random food placement.

    Returns:
        A multi-line report of the simulation.
    """
    state = GameState.new(config.BOARD_SIZE, config.BOARD_SIZE, Random(seed))
    state.food = next_head(state.snake[0], state.direction)
    lines = [
        f"Board: {state.width}x{state.height} | cell: {config.CELL_SIZE}px "
        f"| fps: {config.FPS} | seed: {seed}"
    ]
    for step in range(1, steps + 1):
        state.step()
        head_x, head_y = state.snake[0]
        food_x, food_y = state.food
        lines.append(
            f"step {step:02d} | head=({head_x},{head_y}) | length={len(state.snake)} "
            f"| score={state.score} | food=({food_x},{food_y})"
        )
        if state.game_over:
            lines.append("game over")
            break
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Run the Snake CLI.

    Args:
        argv: Optional argument list; defaults to ``sys.argv[1:]``.

    Returns:
        ``0`` on success, ``1`` if pygame is unavailable, and ``2`` for bad
        arguments (raised by :mod:`argparse`).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.demo:
        if args.steps < 1:
            parser.error("--steps must be at least 1")
        print(simulate(args.steps, args.seed))
        return 0

    try:
        from snake_game.core.render import run
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
