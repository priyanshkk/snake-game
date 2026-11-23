import unittest
from random import Random

from logic import DOWN, LEFT, RIGHT, UP, GameState, is_out_of_bounds, next_head, opposite


class SnakeLogicTests(unittest.TestCase):
    def test_opposite(self):
        self.assertEqual(opposite(RIGHT), LEFT)
        self.assertEqual(opposite(UP), DOWN)

    def test_next_head(self):
        self.assertEqual(next_head((3, 4), RIGHT), (4, 4))
        self.assertEqual(next_head((3, 4), UP), (3, 3))

    def test_out_of_bounds(self):
        self.assertTrue(is_out_of_bounds((-1, 0), 5, 5))
        self.assertTrue(is_out_of_bounds((0, 5), 5, 5))
        self.assertFalse(is_out_of_bounds((4, 4), 5, 5))

    def test_new_game_has_food_on_empty_cell(self):
        state = GameState.new(5, 5, Random(1))
        self.assertNotIn(state.food, state.snake)

    def test_step_moves_head_and_removes_tail(self):
        state = GameState.new(5, 5, Random(2))
        state.snake = [(2, 2), (1, 2), (0, 2)]
        state.direction = RIGHT
        state.food = (4, 4)
        state.step()
        self.assertEqual(state.snake[0], (3, 2))
        self.assertEqual(len(state.snake), 3)
        self.assertEqual(state.snake[-1], (1, 2))

    def test_eating_food_grows_and_scores(self):
        state = GameState.new(5, 5, Random(3))
        state.snake = [(2, 2), (1, 2)]
        state.direction = RIGHT
        state.food = (3, 2)
        state.step()
        self.assertEqual(state.score, 10)
        self.assertEqual(len(state.snake), 3)
        self.assertEqual(state.snake[0], (3, 2))

    def test_reverse_direction_is_ignored(self):
        state = GameState.new(5, 5, Random(4))
        state.snake = [(2, 2), (1, 2)]
        state.direction = RIGHT
        state.food = (4, 4)
        state.step(LEFT)
        self.assertEqual(state.direction, RIGHT)
        self.assertEqual(state.snake[0], (3, 2))

    def test_wall_collision_ends_game(self):
        state = GameState.new(3, 3, Random(5))
        state.snake = [(2, 1), (1, 1)]
        state.direction = RIGHT
        state.food = (0, 0)
        state.step()
        self.assertTrue(state.game_over)

    def test_self_collision_ends_game(self):
        state = GameState.new(3, 3, Random(6))
        state.snake = [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]
        state.direction = UP
        state.food = (2, 2)
        state.step(RIGHT)  # head moves into (1, 0), which is not the tail
        self.assertTrue(state.game_over)


if __name__ == "__main__":
    unittest.main()
