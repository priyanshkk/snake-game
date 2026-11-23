"""A small, dependency-light Snake game built with pygame.

Run with::

    pip install -r requirements.txt
    python snake.py
"""

from __future__ import annotations

import sys

try:
    import pygame
except ImportError:  # pragma: no cover - friendly message for a missing dep
    sys.exit("pygame is required. Install it with: pip install -r requirements.txt")

from logic import DOWN, LEFT, RIGHT, UP, GameState

CELL = 28
FPS = 12
BACKGROUND = (18, 18, 24)
GRID = (34, 34, 44)
SNAKE = (80, 220, 140)
HEAD = (140, 255, 180)
FOOD = (255, 110, 120)
TEXT = (235, 235, 245)

KEY_TO_DIRECTION = {
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
    surface.fill(BACKGROUND)

    for x in range(state.width):
        for y in range(state.height):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            pygame.draw.rect(surface, GRID, rect, 1)

    fx, fy = state.food
    pygame.draw.circle(
        surface,
        FOOD,
        (fx * CELL + CELL // 2, fy * CELL + CELL // 2),
        CELL // 2 - 3,
    )

    for index, (x, y) in enumerate(state.snake):
        color = HEAD if index == 0 else SNAKE
        rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(surface, color, rect, border_radius=5)

    label = font.render(f"Score: {state.score}", True, TEXT)
    surface.blit(label, (10, 8))

    if state.game_over:
        message = font.render("Game over - press R to restart", True, TEXT)
        surface.blit(
            message,
            (surface.get_width() // 2 - message.get_width() // 2, surface.get_height() // 2),
        )

    pygame.display.flip()


def main() -> None:
    pygame.init()
    width, height = 20, 20
    screen = pygame.display.set_mode((width * CELL, height * CELL))
    pygame.display.set_caption("Snake - Python")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,arial", 18)
    state = GameState.new(width, height)
    queued_direction = None
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
                    state = GameState.new(width, height)
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
        clock.tick(FPS)


if __name__ == "__main__":
    main()
