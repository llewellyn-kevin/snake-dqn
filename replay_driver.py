from drivers import GameDriver, ReplayData
from game.game_state import GameState, UserInputMessage, PygameStateUpdate
from game.data_objects import UserAction, Vector
from game.game_board import FoodGenerator
from ui.window import run_ui, GameMode
import time
import argparse

class ListGenerator(FoodGenerator):
    food_list: list[Vector]
    index: int = 0

    def __init__(self, food_list: list[Vector]):
        self.food_list = food_list

    def next(self, tiles: list[list[int]]) -> Vector:
        if self.index >= len(self.food_list):
            return Vector(0, 0)
        food = self.food_list[self.index]
        self.index += 1
        return food

class ReplayDriver(GameDriver):
    game: GameState
    next_tick: float
    tick_count: int = 0
    tick_actions: list[UserAction] = []
    food_list: list[Vector] = []
    cached_data: ReplayData

    def __init__(self, replay_data: ReplayData):
        self.cached_data = replay_data
        self.game = GameState(food_generator=ListGenerator(replay_data.food_list))
        self.next_tick = time.time() + self.get_tick_speed()
        self.tick_actions = replay_data.tick_actions

    def get_next_state(self) -> PygameStateUpdate:
        state = self.game.to_pygame()
        if time.time() >= self.next_tick:
            self.next_tick = self.next_tick + self.get_tick_speed()

            new_game_status = self.game.board.update()
            self.game.current_state = new_game_status
            state = self.game.to_pygame()

            self.tick_count += 1
            action = self.tick_actions[self.tick_count]
            self.game.do_player_action(UserInputMessage(action, time.time()))
        return state

    def get_tick_speed(self) -> float:
        return 1 / 20

    def log_user_action(self, action) -> None:
        pass

    def restart(self) -> None:
        self.tick_count = 0
        self.__init__(self.cached_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay a game of snake")
    parser.add_argument("replay", type=str, help="The replay file to load")
    args = parser.parse_args()

    replay_data = None
    try:
        with open(args.replay, "r") as f:
            replay_data = ReplayData.from_string(f.read())
    except Exception as e:
        print(f"Error loading replay data, could not load file: {args.replay}")
        exit()

    if replay_data is None:
        print("No replay data found")
        exit()

    driver = ReplayDriver(replay_data)
    run_ui(driver, GameMode.MAIN_MENU)
