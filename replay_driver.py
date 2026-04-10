from drivers import GameDriver
from game.game_state import GameState, UserInputMessage, PygameStateUpdate
from game.data_objects import UserAction
from ui.window import run_ui, GameMode
import time

class ReplayDriver(GameDriver):
    game: GameState
    next_tick: float
    tick_count: int = 0
    tick_actions: list[UserAction] = []

    def __init__(self):
        self.game = GameState()
        self.next_tick = time.time() + self.get_tick_speed()
        self.tick_actions = [UserAction.NOTHING] * 1000
        self.tick_actions[5] = UserAction.MOVE_DOWN
        self.tick_actions[10] = UserAction.MOVE_LEFT
        self.tick_actions[15] = UserAction.MOVE_UP
        self.tick_actions[20] = UserAction.MOVE_RIGHT

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
        self.__init__()


if __name__ == "__main__":
    driver = ReplayDriver()
    run_ui(driver, GameMode.MAIN_MENU)
