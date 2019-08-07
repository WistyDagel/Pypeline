import bike as bike
import random
import pygame
import math
from pygame import Rect

# returns a powerup positioned at a random location on the screen
def c_powerup(screen_width, screen_height, bike_scl):
    scale = bike_scl * 1.5
    powerup = Rect(random.randint(0, int(screen_width - scale + 1)),  # random x
                     random.randint(0, int(screen_height - scale + 1)),  # random y
                     scale,  # 50% larger than the bike
                     scale)  # 50% larger than the bike
    return powerup


# returns a bike of scale 6 positioned at the center of the screen, going RIGHT
def c_bike(grid_margin, grid_width, grid_height, grid_cell_scl):
    return bike(grid_margin + (grid_width - math.ceil(grid_width / 2)) * (grid_cell_scl + grid_margin),
                grid_margin + (grid_height - math.ceil(grid_height/2)) * (grid_cell_scl + grid_margin),
                6, bike.Direction.RIGHT)


# draw the background, grid, and squares
def draw(screen, GRID_BG, GRID_FG, grid_width, grid_height, grid_margin, grid_cell_scl, screen_width, screen_height, bike_color, powerup_color, powerup):
    # erase everything
    screen.fill(GRID_BG)

    # grid x lines (vertical)
    for i in range(grid_width + 1):
        pygame.draw.line(screen, GRID_FG, (grid_margin / 2 + (i * (grid_cell_scl + grid_margin)), 0),
                         (grid_margin / 2 + (i * (grid_cell_scl + grid_margin)), screen_height), grid_margin)

    # grid y lines (horizonal
    for i in range(grid_height + 1):
        pygame.draw.line(screen, GRID_FG, (0, grid_margin/2 + (i * (grid_cell_scl + grid_margin))),
                         (screen_width, grid_margin / 2 + (i * (grid_cell_scl + grid_margin))), grid_margin)

    # bike squares
    for piece in bike.line_pieces:
        pygame.draw.rect(screen, bike_color, bike)

    # powerup
    pygame.draw.rect(screen, powerup_color, powerup)

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()