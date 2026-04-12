from drivers import GameDriver, ReplayData
from game.game_state import GameState, UserInputMessage, PygameStateUpdate
from game.data_objects import UserAction, Vector
from ui.window import run_ui, GameMode
import time
from pygame import math
import argparse

slowest_frame = 1 / 4
fastest_frame = 1 / 20

class PlayerDriver(GameDriver):
    game: GameState
    max_score: int
    next_tick: float
    tick_actions: list[UserAction] = []
    food_list: list[Vector] = []
    save_replay: bool

    def __init__(self, save_replay: bool = False):
        self.save_replay = save_replay
        self.game = GameState()
        self.max_score = len(self.game.board.tiles) * len(self.game.board.tiles[0])
        self.restart()

    def get_next_state(self) -> PygameStateUpdate:
        state = self.game.to_pygame()
        self.food_list = self.game.food_list
        if time.time() >= self.next_tick:
            self.next_tick = self.next_tick + self.get_tick_speed()
            self.tick_actions.append(UserAction.NOTHING)
            new_game_status = self.game.board.update()
            self.game.current_state = new_game_status
            state = self.game.to_pygame()
        return state

    def get_tick_speed(self) -> float:
        score_percentile = self.game.board.score / self.max_score
        return math.lerp(slowest_frame, fastest_frame, score_percentile)

    def log_user_action(self, action: UserAction) -> None:
        self.tick_actions[-1] = action
        self.game.do_player_action(UserInputMessage(action, time.time()))

    def restart(self) -> None:
        self.game = GameState()
        self.next_tick = time.time() + slowest_frame
        self.tick_actions = [UserAction.NOTHING]
        self.game.restart()
        self.food_list = self.game.food_list

    def get_replay_data(self) -> ReplayData:
        return ReplayData(self.tick_actions, self.food_list)

    def should_save_replay(self):
        return self.save_replay

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a game of snake using WASD for controls.")
    parser.add_argument("--save-replay", "-r", action="store_true", help="Whether to save a replay of the game after it ends.")
    args = parser.parse_args()

    driver = PlayerDriver(save_replay=args.save_replay)
    run_ui(driver, GameMode.MAIN_MENU)
