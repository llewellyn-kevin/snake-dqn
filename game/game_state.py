from game.snake import Snake
from game.game_board import GameBoard, FoodGenerator, RandomGenerator
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
    food_list: list[Vector] = []

    def __init__(self, food_generator: FoodGenerator = RandomGenerator()):
        self.current_state = CurrentGameState.PLAYING
        self.board = GameBoard(width=12, height=16, food_generator=food_generator)
        self.board.add_snake(Snake(head=Vector(3, 1), tail=Vector(1, 1)))
        self.board.add_food(self.board.food_generator.next(self.board.tiles))

    def do_player_action(self, message: UserInputMessage):
        if message.action == UserAction.MOVE_UP:
            self.board.snake.change_direction(Vector(0, -1))
        if message.action == UserAction.MOVE_DOWN:
            self.board.snake.change_direction(Vector(0, 1))
        if message.action == UserAction.MOVE_RIGHT:
            self.board.snake.change_direction(Vector(1, 0))
        if message.action == UserAction.MOVE_LEFT:
            self.board.snake.change_direction(Vector(-1, 0))

    def to_pygame(self) -> PygameStateUpdate:
        if self.board.added_food is not None:
            if len(self.food_list) == 0 or self.food_list[-1] != self.board.added_food:
                self.food_list.append(self.board.added_food)
        return PygameStateUpdate(self.board.tiles, self.board.score, self.current_state)

    def restart(self):
        self.food_list = []
