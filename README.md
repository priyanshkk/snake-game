# Snake (Python + pygame)

A clean implementation of the classic Snake game. The rules live in `logic.py`
as pure functions and a dataclass, while `snake.py` only handles rendering and
input. That separation makes the game rules unit-testable without a display.

## Features

- Grid-based movement with smooth keyboard controls (arrows or WASD)
- Score tracking: +10 for every food item
- Pause (`Space`), restart after game over (`R`), quit (`Esc`)
- Collision detection for walls and the snake's own body
- No 180-degree turns into your own neck
- Deterministic food placement via an injectable `Random` instance (used in tests)

## Install & run

```bash
pip install -r requirements.txt
python snake.py
```

## Controls

| Key | Action |
| --- | --- |
| Arrow keys / WASD | Move |
| Space | Pause / resume |
| R | Restart (after game over) |
| Esc | Quit |

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
snake-game/
├── logic.py          # game rules, no pygame import
├── snake.py          # pygame rendering + input loop
├── tests/
│   └── test_logic.py # 9 unit tests for the rules
└── requirements.txt
```

## License

MIT
