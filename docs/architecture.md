# Architecture

## Goal

The game should be playable with pygame, but its rules must be testable on a
machine with no display and no pygame installation. That single constraint
drives the module split.

## Modules

| Module | Responsibility |
| --- | --- |
| `src/snake_game/core/game.py` | Pure state machine: directions, movement, food, collisions and score. No pygame import. |
| `src/snake_game/core/render.py` | Pygame rendering and the event loop. Imports the rules and the config. |
| `src/snake_game/config.py` | Constants and environment-variable parsing for cell size, FPS and board size. |
| `src/snake_game/__main__.py` | CLI parser, headless `--demo` mode, and lazy import of the renderer. |
| `src/snake_game/__init__.py` | Public package surface (`GameState`, `__version__`). |
| `logic.py`, `snake.py` | Thin compatibility shims for the original script names. |

## Data flow

```text
Keyboard / window events
        |
        v
core/render.py  -- queued direction -->  core/game.py (GameState.step)
        |                                      |
        |                                      +-- new snake, food, score, game_over
        v
core/render.py (draw)  <-- state ---------------+
        |
        v
pygame display
```

The CLI path is different and never touches pygame:

```text
python -m snake_game --demo
        |
        v
__main__.py -> simulate() -> GameState.new() + GameState.step() -> stdout
```

## Design decisions

1. **Rules are pure.** `GameState.step()` mutates only its own dataclass and
   uses an injectable `Random` for food. There is no clock, no I/O and no
   global state, so the nine rule tests are deterministic.
2. **The tail cell is legal.** On a normal step the tail vacates its cell, so
   collision checks use `snake[:-1]`. On an eating step the tail stays, so the
   full body is checked. This matches classic Snake behaviour.
3. **No 180-degree turns.** A requested direction equal to `opposite(direction)`
   is ignored; otherwise the head could move into the neck and die instantly.
4. **Food on a full board.** When no empty cell remains, `spawn_food()` returns
   the head cell as a sentinel. Rendering keeps working and no exception is
   raised even though the board is full.
5. **Lazy pygame import.** The renderer is imported inside `main()` only when
   the interactive game is requested. `--help` and `--demo` therefore work in
   CI containers without pygame or a display.
6. **One config source.** `CELL_SIZE`, `FPS` and `BOARD_SIZE` are parsed once in
   `config.py`. Invalid values fall back to defaults instead of crashing at
   startup. Both the renderer and the headless demo read the same values.
7. **Direction queue.** Key presses set `queued_direction`; exactly one is
   consumed per tick. This prevents two quick key presses from being applied
   within a single frame, which used to allow illegal reversals.

## Error handling

- Missing pygame: the renderer raises `RuntimeError`; the CLI catches it,
  prints an actionable message on stderr and exits with code 1.
- Bad CLI arguments: `argparse` exits with code 2.
- Invalid environment integers: ignored in favour of the documented default.

## Testing strategy

`tests/test_core.py` contains the original logic tests, now importing from the
package. `tests/test_main.py` covers parser defaults, the demo output and the
environment overrides. `tests/__init__.py` inserts `src/` into `sys.path`, so
the suite runs from the repository root without an editable install.
