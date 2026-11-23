"""Tests for the Snake CLI entry point and environment configuration."""

from __future__ import annotations

import importlib
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from snake_game import config  # noqa: E402
from snake_game.__main__ import build_parser, main, simulate  # noqa: E402

ENV_KEYS = ("SNAKE_CELL_SIZE", "SNAKE_FPS", "SNAKE_BOARD_SIZE")


class ParserTests(unittest.TestCase):
    """Cover argument parsing for the module entry point."""

    def test_defaults(self) -> None:
        """No arguments selects the interactive game with demo defaults."""
        args = build_parser().parse_args([])
        self.assertFalse(args.demo)
        self.assertEqual(args.steps, 3)
        self.assertEqual(args.seed, 7)

    def test_demo_flags(self) -> None:
        """Demo flags are parsed as integers."""
        args = build_parser().parse_args(["--demo", "--steps", "5", "--seed", "11"])
        self.assertTrue(args.demo)
        self.assertEqual(args.steps, 5)
        self.assertEqual(args.seed, 11)


class DemoTests(unittest.TestCase):
    """Cover the headless simulation used for demos and CI."""

    def test_report_includes_configuration(self) -> None:
        """The report shows the values actually read from config."""
        report = simulate(1, 7)
        self.assertIn(f"Board: {config.BOARD_SIZE}x{config.BOARD_SIZE}", report)
        self.assertIn(f"cell: {config.CELL_SIZE}px", report)
        self.assertIn(f"fps: {config.FPS}", report)

    def test_report_counts_steps_and_score(self) -> None:
        """The scripted first step eats food and scores ten points."""
        report = simulate(2, 7)
        self.assertIn("step 01", report)
        self.assertIn("step 02", report)
        self.assertIn("score=10", report)

    def test_invalid_step_count_is_rejected(self) -> None:
        """Zero steps is a parser error."""
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(["--demo", "--steps", "0"])
        self.assertEqual(caught.exception.code, 2)

    def test_main_demo_prints_report_and_returns_zero(self) -> None:
        """The CLI demo path writes to stdout and succeeds."""
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(["--demo", "--steps", "1"])
        self.assertEqual(result, 0)
        self.assertIn("step 01", output.getvalue())


class ConfigTests(unittest.TestCase):
    """Cover environment-variable parsing."""

    def tearDown(self) -> None:
        """Restore config constants after each test."""
        for key in ENV_KEYS:
            os.environ.pop(key, None)
        importlib.reload(config)

    def test_valid_environment_values_are_used(self) -> None:
        """All three supported variables are read."""
        env = {"SNAKE_CELL_SIZE": "32", "SNAKE_FPS": "20", "SNAKE_BOARD_SIZE": "15"}
        with patch.dict(os.environ, env):
            importlib.reload(config)
            self.assertEqual(config.CELL_SIZE, 32)
            self.assertEqual(config.FPS, 20)
            self.assertEqual(config.BOARD_SIZE, 15)

    def test_invalid_values_fall_back_to_defaults(self) -> None:
        """Bad integers and non-positive values are ignored."""
        env = {"SNAKE_CELL_SIZE": "wide", "SNAKE_FPS": "0", "SNAKE_BOARD_SIZE": "-3"}
        with patch.dict(os.environ, env):
            importlib.reload(config)
            self.assertEqual(config.CELL_SIZE, 28)
            self.assertEqual(config.FPS, 12)
            self.assertEqual(config.BOARD_SIZE, 20)

    def test_env_int_minimum(self) -> None:
        """The helper honours a custom minimum."""
        with patch.dict(os.environ, {"SNAKE_TEST_MIN": "2"}):
            self.assertEqual(config.env_int("SNAKE_TEST_MIN", 5, minimum=3), 5)
            self.assertEqual(config.env_int("SNAKE_TEST_MIN", 5, minimum=2), 2)


if __name__ == "__main__":
    unittest.main()
