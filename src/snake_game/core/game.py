"""Pure Snake rules, independent of pygame and the terminal.

Keeping the state machine here means every rule can be unit-tested without a
display, and the renderer can be replaced without touching the game logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def opposite(direction: tuple[int, int]) -> tuple[int, int]:
    """Return the direction that would immediately reverse the snake.

    Args:
        direction: A unit vector such as :data:`RIGHT`.

    Returns:
        The negated vector.
    """
    return (-direction[0], -direction[1])


def next_head(head: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    """Return the cell directly in front of the snake's head.

    Args:
        head: Current ``(x, y)`` cell of the head.
        direction: Unit vector describing movement.

    Returns:
        The adjacent cell the head would occupy after one step.
    """
    return (head[0] + direction[0], head[1] + direction[1])


def is_out_of_bounds(position: tuple[int, int], width: int, height: int) -> bool:
    """Report whether a cell lies outside the board.

    Args:
        position: ``(x, y)`` cell to test.
        width: Number of columns.
        height: Number of rows.

    Returns:
        ``True`` when the cell is outside the rectangle.
    """
    x, y = position
    return x < 0 or y < 0 or x >= width or y >= height


@dataclass
class GameState:
    """The complete state of a single Snake game.

    Attributes:
        width: Board width in cells.
        height: Board height in cells.
        snake: Head-first list of occupied cells.
        direction: Current unit-vector direction.
        food: Cell containing food.
        score: Score in points; each food item is worth 10.
        game_over: Whether a collision has ended the game.
    """

    width: int
    height: int
    snake: list[tuple[int, int]]
    direction: tuple[int, int]
    food: tuple[int, int]
    score: int = 0
    game_over: bool = False

    @classmethod
    def new(cls, width: int = 20, height: int = 20, rng: Random | None = None) -> GameState:
        """Create a new game with the head at the board centre.

        Args:
            width: Board width in cells.
            height: Board height in cells.
            rng: Optional seeded random generator for deterministic food.

        Returns:
            A fresh :class:`GameState`.
        """
        center = (width // 2, height // 2)
        state = cls(width=width, height=height, snake=[center], direction=RIGHT, food=(0, 0))
        state.food = state.spawn_food(rng)
        return state

    def spawn_food(self, rng: Random | None = None) -> tuple[int, int]:
        """Pick a random cell that is not occupied by the snake.

        Args:
            rng: Optional random generator; a fresh one is used when omitted.

        Returns:
            An empty cell, or the head cell when the board is full (a harmless
            sentinel that keeps rendering safe when the player has won).
        """
        rng = rng or Random()
        occupied = set(self.snake)
        empty = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in occupied
        ]
        if not empty:
            return self.snake[0]
        return rng.choice(empty)

    def step(self, new_direction: tuple[int, int] | None = None) -> None:
        """Advance the game by one tick.

        A 180-degree turn is ignored, since it would make the head collide
        with the second segment instantly. The tail vacates its cell on a
        normal move, so entering the old tail cell is legal.

        Args:
            new_direction: Requested direction, or ``None`` to keep going.
        """
        if self.game_over:
            return

        if new_direction and new_direction != opposite(self.direction):
            self.direction = new_direction

        head = next_head(self.snake[0], self.direction)
        ate = head == self.food
        body = self.snake if ate else self.snake[:-1]

        if is_out_of_bounds(head, self.width, self.height) or head in body:
            self.game_over = True
            return

        self.snake.insert(0, head)
        if ate:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()


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
