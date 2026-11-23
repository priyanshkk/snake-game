"""Pygame rendering and the interactive event loop for Snake.

This module is imported lazily by :mod:`snake_game.__main__` so headless
commands such as ``--demo`` and ``--help`` work without pygame installed.
"""

from __future__ import annotations

try:
    import pygame
except ImportError as exc:  # pragma: no cover - exercised only without pygame
    raise RuntimeError(
        "pygame is required for the interactive game. "
        "Install it with: pip install -r requirements.txt"
    ) from exc

from snake_game import config
from snake_game.core.game import DOWN, LEFT, RIGHT, UP, GameState

KEY_TO_DIRECTION: dict[int, tuple[int, int]] = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}


def draw(surface: pygame.Surface, state: GameState, font: pygame.font.Font) -> None:
    """Draw one complete frame and flip the display.

    Args:
        surface: The pygame display surface.
        state: Current game state to render.
        font: Font used for the score and overlay text.
    """
    cell = config.CELL_SIZE
    surface.fill(config.BACKGROUND)

    for x in range(state.width):
        for y in range(state.height):
            rect = pygame.Rect(x * cell, y * cell, cell, cell)
            pygame.draw.rect(surface, config.GRID_COLOR, rect, 1)

    fx, fy = state.food
    pygame.draw.circle(
        surface,
        config.FOOD_COLOR,
        (fx * cell + cell // 2, fy * cell + cell // 2),
        cell // 2 - 3,
    )

    for index, (x, y) in enumerate(state.snake):
        color = config.HEAD_COLOR if index == 0 else config.SNAKE_COLOR
        rect = pygame.Rect(x * cell + 2, y * cell + 2, cell - 4, cell - 4)
        pygame.draw.rect(surface, color, rect, border_radius=5)

    label = font.render(f"Score: {state.score}", True, config.TEXT_COLOR)
    surface.blit(label, (10, 8))

    if state.game_over:
        message = font.render("Game over - press R to restart", True, config.TEXT_COLOR)
        surface.blit(
            message,
            (surface.get_width() // 2 - message.get_width() // 2, surface.get_height() // 2),
        )

    pygame.display.flip()


def run() -> None:
    """Run the interactive game loop until the player quits."""
    pygame.init()
    board = config.BOARD_SIZE
    screen = pygame.display.set_mode((board * config.CELL_SIZE, board * config.CELL_SIZE))
    pygame.display.set_caption(config.CAPTION)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,arial", 18)
    state = GameState.new(board, board)
    queued_direction: tuple[int, int] | None = None
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_r and state.game_over:
                    state = GameState.new(board, board)
                    queued_direction = None
                    paused = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key in KEY_TO_DIRECTION:
                    queued_direction = KEY_TO_DIRECTION[event.key]

        if not paused:
            state.step(queued_direction)
            queued_direction = None

        draw(screen, state, font)
        clock.tick(config.FPS)


__all__ = ["KEY_TO_DIRECTION", "draw", "run"]
