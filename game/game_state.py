from game.snake import Snake
from game.game_board import GameBoard


class GameState:
    board: GameBoard


    def __init__(self):
        snake = Snake()
        self.board.add_snake(snake)
