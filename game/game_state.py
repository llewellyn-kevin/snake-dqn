from game.snake import Snake
from game.game_board import GameBoard
from game.data_objects import CurrentGameState, Tile


class GameState:
    board: GameBoard

    def __init__(self):
        snake = Snake()
        self.board.add_snake(snake)


class PygameStateUpdate:
    tiles: list[list[Tile]]
    score: int
    state: CurrentGameState

    def __init__(self, tiles: list[list[Tile]], score: int, state: CurrentGameState):
        self.tiles = tiles
        self.score = score
        self.state = state


class UserInputMessage:
    action: UserAction
    time: int

    def __init__(self, action: UserAction, time: int):
        self.action = action
        self.time = time
