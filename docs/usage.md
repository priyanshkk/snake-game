# Usage

All commands assume an activated virtual environment created with
`pip install -r requirements-dev.txt`. From a source checkout you can also set
`PYTHONPATH=src` and skip installation.

## Interactive game

```bash
python -m snake_game
python snake.py            # backward-compatible launcher
```

| Key | Action |
| --- | --- |
| Arrow keys or WASD | Move |
| Space | Pause / resume |
| R | Restart after game over |
| Esc | Quit |

A pygame window opens with a 20×20 board by default. The score is drawn in the
top-left corner.

## CLI reference

```text
usage: snake-game [-h] [--demo] [--steps STEPS] [--seed SEED]

Play Snake in a pygame window, or run a headless demo.

options:
  -h, --help     show this help message and exit
  --demo         run a deterministic simulation instead of opening a window
  --steps STEPS  number of demo steps (default: 3)
  --seed SEED    seed for demo food placement (default: 7)
```

### Headless demo

`--demo` runs the real rules engine without pygame. The first food item is
placed directly in front of the head so the scoring path is visible; later food
uses the seeded generator.

```bash
python -m snake_game --demo --steps 4 --seed 7
```

Real output:

```text
Board: 20x20 | cell: 28px | fps: 12 | seed: 7
step 01 | head=(11,10) | length=2 | score=10 | food=(0,7)
step 02 | head=(12,10) | length=2 | score=10 | food=(0,7)
step 03 | head=(13,10) | length=2 | score=10 | food=(0,7)
step 04 | head=(14,10) | length=2 | score=10 | food=(0,7)
```

`--steps` must be at least 1; smaller values are rejected by `argparse` with
exit code 2.

## Environment configuration

Values are read once at import time by `snake_game.config`. Invalid integers
fall back to the defaults.

| Variable | Default | Effect |
| --- | --- | --- |
| `SNAKE_CELL_SIZE` | `28` | Cell size in pixels; positive integer. |
| `SNAKE_FPS` | `12` | Game-loop frames per second; positive integer. |
| `SNAKE_BOARD_SIZE` | `20` | Board width and height in cells; minimum 2. |

PowerShell:

```powershell
$env:SNAKE_BOARD_SIZE = "15"
$env:SNAKE_FPS = "20"
python -m snake_game --demo --steps 2
Remove-Item Env:SNAKE_BOARD_SIZE, Env:SNAKE_FPS
```

POSIX shells:

```bash
SNAKE_BOARD_SIZE=15 SNAKE_FPS=20 python -m snake_game --demo --steps 2
```

The demo report includes the effective config, so the override is visible:

```text
Board: 15x15 | cell: 28px | fps: 20 | seed: 7
step 01 | head=(8,7) | length=2 | score=10 | food=(11,2)
step 02 | head=(9,7) | length=2 | score=10 | food=(11,2)
```

## Public API

The rules engine can be used directly in another program:

```python
from random import Random

from snake_game.core.game import GameState, RIGHT

state = GameState.new(5, 5, Random(3))
state.food = (3, 2)
state.step()
print("head", state.snake[0], "score", state.score, "length", len(state.snake))
```

Real output:

```text
head (3, 2) score 10 length 2
```

`snake_game.config.env_int(name, default, *, minimum=1)` is the shared parser
for environment integers; it returns `default` when a value is absent,
non-numeric or below `minimum`.

## Testing and linting

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m mypy src/snake_game
```
