import unittest
from game.data_objects import Vector, Tile, CurrentGameState
from game.game_board import GameBoard, FoodGenerator
from game.snake import Snake


class GameBoardTest(unittest.TestCase):
    def test_create_empty_board(self):
        board = GameBoard(width=4, height=3)

        expected = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ]

        self.assertEqual(expected, board.tiles)


    def test_add_snake(self):
        snake = Snake(head=Vector(2, 1), tail=Vector(1, 1))
        board = GameBoard(width=4, height=3)
        board.add_snake(snake)

        expected = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.SNAKE, Tile.SNAKE, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ]

        self.assertEqual(expected, board.tiles)


    def test_add_large_snake(self):
        snake = Snake(head=Vector(3, 2), tail=Vector(0, 0))
        board = GameBoard(width=4, height=3)
        board.add_snake(snake)

        expected = [
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE],
        ]

        self.assertEqual(expected, board.tiles)


    def test_make_snake_backwards(self):
        snake = Snake(head=Vector(0, 1), tail=Vector(3, 2))
        board = GameBoard(width=4, height=3)
        board.add_snake(snake)

        expected = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.SNAKE],
        ]

        self.assertEqual(expected, board.tiles)


    def test_snake_can_move(self):
        snake = Snake(head=Vector(0, 2), tail=Vector(0, 0))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        start = [
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ]

        one = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ]

        two = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ]

        self.assertEqual(start, board.tiles)
        alive = board.update()
        self.assertTrue(alive)
        self.assertEqual(one, board.tiles)
        alive = board.update()
        self.assertTrue(alive)
        self.assertEqual(two, board.tiles)
        

    def test_it_dies_off_edge(self):
        snake = Snake(head=Vector(0, 2), tail=Vector(0, 0), direction=Vector(-1, 0))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        new_state = board.update()
        self.assertEqual(CurrentGameState.LOSS, new_state)

        snake = Snake(head=Vector(5, 2), tail=Vector(5, 0), direction=Vector(1, 0))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        new_state = board.update()
        self.assertEqual(CurrentGameState.LOSS, new_state)

        snake = Snake(head=Vector(2, 0), tail=Vector(0, 0), direction=Vector(0, -1))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        new_state = board.update()
        self.assertEqual(CurrentGameState.LOSS, new_state)

        snake = Snake(head=Vector(2, 7), tail=Vector(0, 7), direction=Vector(0, 1))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        new_state = board.update()
        self.assertEqual(CurrentGameState.LOSS, new_state)


    def test_it_dies_on_itself(self):
        snake = Snake(head=Vector(5, 0), tail=Vector(0, 0), direction=Vector(0, 1))
        board = GameBoard(width=6, height=8)
        board.add_snake(snake)

        new_state = board.update()
        self.assertEqual(CurrentGameState.PLAYING, new_state)
        board.snake.change_direction(Vector(-1, 0))
        new_state = board.update()
        self.assertEqual(CurrentGameState.PLAYING, new_state)
        new_state = board.update()
        self.assertEqual(CurrentGameState.PLAYING, new_state)
        board.snake.change_direction(Vector(0, -1))
        new_state = board.update()
        self.assertEqual(CurrentGameState.LOSS, new_state)


    def test_it_can_eat_food(self):
        snake = Snake(head=Vector(2, 0), tail=Vector(0, 0), direction=Vector(1, 0))
        board = GameBoard(width=5, height=2, food_generator=SetGenerator(
            spots=[Vector(2, 1), Vector(0, 0)],
        ))
        board.add_snake(snake)
        board.add_food(Vector(x=4, y=0))

        self.assertEqual(board.tiles, [
            [Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.EMPTY, Tile.FOOD],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ])
        board.update()
        self.assertEqual(snake.size, 3)
        self.assertEqual(board.score, 0)
        self.assertEqual(board.tiles, [
            [Tile.EMPTY, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.FOOD],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
        ])
        board.update()
        self.assertEqual(snake.size, 4)
        self.assertEqual(board.score, 1)
        self.assertEqual(board.tiles, [
            [Tile.EMPTY, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE],
            [Tile.EMPTY, Tile.EMPTY, Tile.FOOD, Tile.EMPTY, Tile.EMPTY],
        ])
        board.snake.change_direction(Vector(0, 1))
        board.update()
        self.assertEqual(snake.size, 4)
        self.assertEqual(board.score, 1)
        self.assertEqual(board.tiles, [
            [Tile.EMPTY, Tile.EMPTY, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE],
            [Tile.EMPTY, Tile.EMPTY, Tile.FOOD, Tile.EMPTY, Tile.SNAKE],
        ])
        board.snake.change_direction(Vector(-1, 0))
        board.update()
        self.assertEqual(snake.size, 4)
        self.assertEqual(board.score, 1)
        self.assertEqual(board.tiles, [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.SNAKE, Tile.SNAKE],
            [Tile.EMPTY, Tile.EMPTY, Tile.FOOD, Tile.SNAKE, Tile.SNAKE],
        ])
        board.update()
        self.assertEqual(snake.size, 5)
        self.assertEqual(board.score, 2)
        self.assertEqual(board.tiles, [
            [Tile.FOOD, Tile.EMPTY, Tile.EMPTY, Tile.SNAKE, Tile.SNAKE],
            [Tile.EMPTY, Tile.EMPTY, Tile.SNAKE, Tile.SNAKE, Tile.SNAKE],
        ])


class SetGenerator(FoodGenerator):
    ace: int


    def __init__(self, spots: list[Vector]):
        self.spots = spots
        self.ace = 0


    def next(self, tiles: list[list[int]], count=0) -> Vector:
        a = self.ace
        self.ace = self.ace + 1
        return self.spots[a % len(self.spots)]
