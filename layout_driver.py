from drivers import GameDriver
from game.game_state import GameState
from game.data_objects import UserAction, CurrentGameState
from ui.window import run_ui, GameMode

class LayoutDriver(GameDriver):
    game: GameState

    def __init__(self):
        self.game = GameState()
        self.game.current_state = CurrentGameState.WIN

    def get_next_state(self) -> CurrentGameState:
        return self.game.to_pygame()

    def log_user_action(self, action: UserAction) -> None:
        return

    def restart(self):
        return

if __name__ == "__main__":
    driver = LayoutDriver()
    run_ui(driver, GameMode.MAIN_MENU)
