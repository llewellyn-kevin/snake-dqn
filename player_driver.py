from drivers import GameDriver
from game.game_state import GameState, UserInputMessage, PygameStateUpdate
from game.data_objects import UserAction
from ui.window import run_ui, GameMode
import time
from pygame import math

slowest_frame = 1 / 4
fastest_frame = 1 / 20

class PlayerDriver(GameDriver):
    game: GameState
    max_score: int
    next_tick: float

    def __init__(self):
        self.game = GameState()
        self.max_score = len(self.game.board.tiles) * len(self.game.board.tiles[0])
        self.next_tick = time.time() + slowest_frame

    def get_next_state(self) -> PygameStateUpdate:
        state = self.game.to_pygame()
        if time.time() >= self.next_tick:
            self.next_tick = self.next_tick + self.get_tick_speed()
            new_game_status = self.game.board.update()
            self.game.current_state = new_game_status
            state = self.game.to_pygame()
        return state

    def get_tick_speed(self) -> float:
        score_percentile = self.game.board.score / self.max_score
        return math.lerp(slowest_frame, fastest_frame, score_percentile)

    def log_user_action(self, action: UserAction) -> None:
        self.game.do_player_action(UserInputMessage(action, time.time()))

    def restart(self):
        self.game = GameState()
        self.next_tick = time.time() + slowest_frame

if __name__ == "__main__":
    driver = PlayerDriver()
    run_ui(driver, GameMode.MAIN_MENU)
