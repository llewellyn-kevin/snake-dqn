from abc import ABC, abstractmethod
from game.data_objects import CurrentGameState, UserAction
from game.game_state import PygameStateUpdate

class GameDriver(ABC):
    @abstractmethod
    def get_next_state(self) -> PygameStateUpdate:
        pass

    @abstractmethod
    def log_user_action(self, action: UserAction) -> None:
        pass
