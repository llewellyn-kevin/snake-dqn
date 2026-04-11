from abc import ABC, abstractmethod
from game.data_objects import CurrentGameState, UserAction, Vector
from game.game_state import PygameStateUpdate

class ReplayData:
    tick_actions: list[UserAction]
    food_list: list[Vector]

    def __init__(self, tick_actions: list[UserAction], food_list: list[Vector]):
        self.tick_actions = tick_actions
        self.food_list = food_list

    def __str__(self) -> str:
        actions = "".join([str(action.value) for action in self.tick_actions])
        food = ":".join([str(food) for food in self.food_list])
        return f"{actions}|{food}"

    @staticmethod
    def from_string(string: str):
        actions_str, food_str = string.split("|")
        tick_actions = [UserAction(int(action)) for action in actions_str]
        food_list = [Vector.from_string(food) for food in food_str.split(":")]
        return ReplayData(tick_actions, food_list)

class GameDriver(ABC):
    @abstractmethod
    def get_next_state(self) -> PygameStateUpdate:
        pass

    @abstractmethod
    def log_user_action(self, action: UserAction) -> None:
        pass

    @abstractmethod
    def restart(self):
        pass

    def get_replay_data(self) -> ReplayData:
        return None

    def should_save_replay(self):
        return False
