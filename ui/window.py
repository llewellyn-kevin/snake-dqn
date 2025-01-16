import pygame
from game.data_objects import Tile, CurrentGameState, UserAction
from game.game_state import PygameStateUpdate
from drivers import GameDriver
from enum import Enum
from ui.button import Button

pygame.init()

BG_COLOR = "#232937"
EMPTY_GRID_COLOR = "#33405a"
FOOD_COLOR = "#df4576"
SNAKE_COLOR = "#32ae85"

tile_color_map = {
    Tile.EMPTY: EMPTY_GRID_COLOR,
    Tile.SNAKE: SNAKE_COLOR,
    Tile.FOOD: FOOD_COLOR,
}
score_font = pygame.freetype.SysFont("Courier New", 48)

screen = pygame.display.set_mode((488, 728))

def draw_grid_square(cx: int, cy: int, color: str):
    rect = pygame.Rect(cx - 18, cy - 18, 36, 36)
    pygame.draw.rect(screen, color, rect, border_radius=3)

def draw_score(score: int):
    rect = pygame.Rect(screen.get_width() - 148, 20, 120, 50)
    pygame.draw.rect(screen, EMPTY_GRID_COLOR, rect, border_radius=3)
    score_font.render_to(screen, (screen.get_width() - 126, 30), "{:03d}".format(score), (255, 255, 255))

def handle_input(driver: GameDriver, pressed_keys):
    if pressed_keys[pygame.K_s]:
        driver.log_user_action(UserAction.MOVE_DOWN)
    if pressed_keys[pygame.K_d]:
        driver.log_user_action(UserAction.MOVE_RIGHT)
    if pressed_keys[pygame.K_a]:
        driver.log_user_action(UserAction.MOVE_LEFT)
    if pressed_keys[pygame.K_w]:
        driver.log_user_action(UserAction.MOVE_UP)

class GameMode(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    DEAD = 2
    WON = 3

current_mode = GameMode.MAIN_MENU

def start_game(driver: GameDriver):
    def nested():
        global current_mode
        current_mode = GameMode.PLAYING
        driver.restart()
    return nested

def draw_main_menu(driver: GameDriver):
    button = Button(screen.get_width() / 2 - 174, screen.get_height() / 2, 344, 60, button_text="Start", onclick_function=start_game(driver), one_press=False, screen=screen)
    def nested(driver: GameDriver, new_keys: dict):
        screen.fill(BG_COLOR)

        score_font.render_to(screen, (screen.get_width() / 2 - 172, screen.get_height() / 2 - 104), "Simple Snake", (255, 255, 255))
        button.process()

        pygame.display.flip()
    return nested

def draw_playing(driver: GameDriver, new_keys: dict):
    handle_input(driver, new_keys)
    screen.fill(BG_COLOR)
    state = driver.get_next_state()
    for y, row in enumerate(state.tiles):
        for x, tile in enumerate(row):
            draw_grid_square(40 * x + 24, 40 * y + 104, tile_color_map[tile])
    draw_score(state.score)
    pygame.display.flip()

def draw_dead(driver: GameDriver, new_keys: dict):
    pass

def draw_won(driver: GameDriver, new_keys: dict):
    pass

def run_ui(driver: GameDriver, mode: GameMode = GameMode.MAIN_MENU):
    draw_map = {
        GameMode.MAIN_MENU: draw_main_menu(driver),
        GameMode.PLAYING: draw_playing,
        GameMode.DEAD: draw_dead,
        GameMode.WON: draw_won,
    }

    global current_mode
    current_mode = mode
    running = True
    key_buffer = {
        pygame.K_w: False,
        pygame.K_a: False,
        pygame.K_s: False,
        pygame.K_d: False,
    }
    tracked_keys = list(key_buffer.keys())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_keys = pygame.key.get_pressed()
        new_keys = {}
        for v in tracked_keys:
            new_keys[v] = (all_keys[v] and not key_buffer[v])
        key_buffer = all_keys

        draw_map[current_mode](driver, new_keys)
    pygame.quit()
