# Snake documentation

Snake is a small pygame game with a rules engine that can be tested without a
display. This documentation covers the implementation and the CLI.

- [Architecture](architecture.md) — modules, data flow and design decisions.
- [Usage](usage.md) — every command, environment variable and public API with
  examples and real output.

Quick start from a source checkout:

```bash
pip install -r requirements-dev.txt
python -m snake_game
python -m snake_game --demo --steps 4
```
