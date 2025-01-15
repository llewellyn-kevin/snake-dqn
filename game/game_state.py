from game.snake import Snake
from game.game_board import GameBoard
from game.data_objects import CurrentGameState, Tile, UserAction, Vector

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

class GameState:
    board: GameBoard
    current_state: CurrentGameState

    def __init__(self):
        self.current_state = CurrentGameState.PLAYING
        self.board = GameBoard(width=12, height=16)
        self.board.add_snake(Snake(head=Vector(3, 1), tail=Vector(1, 1)))
        self.board.add_food(self.board.food_generator.next(self.board.tiles))

    def to_pygame(self) -> PygameStateUpdate:
        return PygameStateUpdate(self.board.tiles, self.board.score, self.current_state)
