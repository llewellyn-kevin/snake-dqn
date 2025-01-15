import pygame
from game.data_objects import Tile, CurrentGameState, UserAction
from game.game_state import PygameStateUpdate
from drivers import GameDriver

BG_COLOR = "#232937"
EMPTY_GRID_COLOR = "#33405a"
FOOD_COLOR = "#df4576"
SNAKE_COLOR = "#32ae85"

tile_color_map = {
    Tile.EMPTY: EMPTY_GRID_COLOR,
    Tile.SNAKE: SNAKE_COLOR,
    Tile.FOOD: FOOD_COLOR,
}

pygame.init()
screen = pygame.display.set_mode((488, 728))
clock = pygame.time.Clock()

def draw_grid_square(cx: int, cy: int, color: str):
    rect = pygame.Rect(cx - 18, cy - 18, 36, 36)
    pygame.draw.rect(screen, color, rect, border_radius=3)

def run_ui(driver: GameDriver):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        state = driver.get_next_state()
        for y, row in enumerate(state.tiles):
            for x, tile in enumerate(row):
                draw_grid_square(40 * x + 24, 40 * y + 104, tile_color_map[tile])

        pygame.display.flip()

    pygame.quit()
