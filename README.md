# Snake

[![CI](https://github.com/priyanshkk/snake-game/actions/workflows/tests.yml/badge.svg)](https://github.com/priyanshkk/snake-game/actions/workflows/tests.yml)
[![Linter](https://github.com/priyanshkk/snake-game/actions/workflows/linter.yml/badge.svg)](https://github.com/priyanshkk/snake-game/actions/workflows/linter.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-2f6fab.svg)](https://mypy.readthedocs.io/)
[![Tests: unittest](https://img.shields.io/badge/tests-unittest-green.svg)](https://docs.python.org/3/library/unittest.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A classic Snake game whose rules are pure enough to test without a display.

## Overview / why

Most small games mix input, rendering and rules into one file, which makes the
rules impossible to test on a headless machine. Here the state machine lives in
`snake_game.core.game` with no pygame dependency; `snake_game.core.render`
handles the window, and the CLI can run a deterministic simulation of the real
rules with `--demo`. That separation gives fast unit tests, a safe place to add
features, and a game that is still one command to launch.

## Tech stack

| Area | Choice | Why |
| --- | --- | --- |
| Language | Python 3.10–3.13 | Modern type syntax, no exotic runtime requirements. |
| Game / rendering | pygame 2.5+ | Mature, small SDL-based 2D toolkit. |
| Rules engine | `dataclass` + `random.Random` | No I/O; seeded runs are reproducible. |
| Packaging | Hatchling, `src/` layout | Standard PEP 621 metadata and console script. |
| Tests | `unittest` (also pytest-compatible) | Zero extra test dependencies. |
| Static checks | Ruff, mypy | Style, lint and strict type checking. |

## Real demo output

The headless demo uses the same `GameState.step()` as the pygame window:

```console
$ python -m snake_game --demo --steps 4 --seed 7
Board: 20x20 | cell: 28px | fps: 12 | seed: 7
step 01 | head=(11,10) | length=2 | score=10 | food=(0,7)
step 02 | head=(12,10) | length=2 | score=10 | food=(0,7)
step 03 | head=(13,10) | length=2 | score=10 | food=(0,7)
step 04 | head=(14,10) | length=2 | score=10 | food=(0,7)
```

The interactive game adds a score overlay, wall/body collision and restart:

```text
Keys: arrows / WASD = move, Space = pause, R = restart, Esc = quit
```

## Install & setup

```bash
git clone https://github.com/priyanshkk/snake-game.git
cd snake-game
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Windows users can also run `powershell -File scripts\setup.ps1`; POSIX users
can run `bash scripts/setup.sh`. Both create `.venv` and install the dev extras.

## Usage

```bash
python -m snake_game                       # open the game window
python -m snake_game --demo                # 3-step headless simulation
python -m snake_game --demo --steps 10 --seed 42
python snake.py                            # backward-compatible launcher
snake-game --help                          # installed console script
```

| Key | Action |
| --- | --- |
| Arrow keys / WASD | Move |
| Space | Pause / resume |
| R | Restart after game over |
| Esc | Quit |

More examples and the public API are in [docs/usage.md](docs/usage.md).

## Project structure

```text
snake-game/
├── .github/
│   ├── ISSUE_TEMPLATE/{bug_report,feature_request}.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/{tests,linter}.yml
├── docs/{index,architecture,usage}.md
├── scripts/{setup.ps1,setup.sh}
├── src/snake_game/
│   ├── __init__.py
│   ├── __main__.py          # CLI + headless demo
│   ├── config.py            # env-backed constants
│   └── core/
│       ├── __init__.py
│       ├── game.py          # pure rules engine
│       └── render.py        # pygame view and event loop
├── tests/{__init__,test_core,test_main}.py
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── logic.py, snake.py       # compatibility shims
├── LICENSE
└── README.md
```

## Environment configuration

Copy `.env.example` and export the variables in your shell; the application
reads them from `os.environ` in `snake_game.config` at import time.

| Variable | Default | Meaning |
| --- | --- | --- |
| `SNAKE_CELL_SIZE` | `28` | Cell size in pixels (positive integer). |
| `SNAKE_FPS` | `12` | Frames per second of the game loop (positive integer). |
| `SNAKE_BOARD_SIZE` | `20` | Board width and height in cells (minimum 2). |

Invalid values are ignored and the defaults are used. The demo report shows the
effective values.

## Testing & quality

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m mypy src/snake_game
python -m build
```

The suite runs on Python 3.10, 3.11, 3.12 and 3.13 in GitHub Actions.
Architecture notes are in [docs/architecture.md](docs/architecture.md).

## Roadmap

- [ ] Optional difficulty presets that change the tick rate as the snake grows.
- [ ] High-score persistence to a local JSON file.
- [ ] Optional wrap-around board mode.
- [ ] A small settings screen for board size and speed.

## License

MIT — see [LICENSE](LICENSE).
