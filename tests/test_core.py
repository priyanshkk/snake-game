"""Unit tests for the pure Snake rules engine."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from random import Random

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from snake_game.core.game import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    GameState,
    is_out_of_bounds,
    next_head,
    opposite,
)


class SnakeLogicTests(unittest.TestCase):
    """Cover directions, movement, collisions, food and scoring."""

    def test_opposite(self) -> None:
        """Opposite vectors negate both axes."""
        self.assertEqual(opposite(RIGHT), LEFT)
        self.assertEqual(opposite(UP), DOWN)

    def test_next_head(self) -> None:
        """The next head cell is the head plus the direction vector."""
        self.assertEqual(next_head((3, 4), RIGHT), (4, 4))
        self.assertEqual(next_head((3, 4), UP), (3, 3))

    def test_out_of_bounds(self) -> None:
        """Coordinates outside either axis are detected."""
        self.assertTrue(is_out_of_bounds((-1, 0), 5, 5))
        self.assertTrue(is_out_of_bounds((0, 5), 5, 5))
        self.assertFalse(is_out_of_bounds((4, 4), 5, 5))

    def test_new_game_has_food_on_empty_cell(self) -> None:
        """A seeded new game never places food on the snake."""
        state = GameState.new(5, 5, Random(1))
        self.assertNotIn(state.food, state.snake)

    def test_step_moves_head_and_removes_tail(self) -> None:
        """A normal step grows at the head and drops the tail."""
        state = GameState.new(5, 5, Random(2))
        state.snake = [(2, 2), (1, 2), (0, 2)]
        state.direction = RIGHT
        state.food = (4, 4)
        state.step()
        self.assertEqual(state.snake[0], (3, 2))
        self.assertEqual(len(state.snake), 3)
        self.assertEqual(state.snake[-1], (1, 2))

    def test_eating_food_grows_and_scores(self) -> None:
        """Eating adds ten points and a segment."""
        state = GameState.new(5, 5, Random(3))
        state.snake = [(2, 2), (1, 2)]
        state.direction = RIGHT
        state.food = (3, 2)
        state.step()
        self.assertEqual(state.score, 10)
        self.assertEqual(len(state.snake), 3)
        self.assertEqual(state.snake[0], (3, 2))

    def test_reverse_direction_is_ignored(self) -> None:
        """A 180-degree turn is rejected."""
        state = GameState.new(5, 5, Random(4))
        state.snake = [(2, 2), (1, 2)]
        state.direction = RIGHT
        state.food = (4, 4)
        state.step(LEFT)
        self.assertEqual(state.direction, RIGHT)
        self.assertEqual(state.snake[0], (3, 2))

    def test_wall_collision_ends_game(self) -> None:
        """Leaving the board ends the game."""
        state = GameState.new(3, 3, Random(5))
        state.snake = [(2, 1), (1, 1)]
        state.direction = RIGHT
        state.food = (0, 0)
        state.step()
        self.assertTrue(state.game_over)

    def test_self_collision_ends_game(self) -> None:
        """Moving into a non-tail body cell ends the game."""
        state = GameState.new(3, 3, Random(6))
        state.snake = [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]
        state.direction = UP
        state.food = (2, 2)
        state.step(RIGHT)
        self.assertTrue(state.game_over)


if __name__ == "__main__":
    unittest.main()
