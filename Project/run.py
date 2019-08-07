import draw as draw
import PowerUps.minePowerUp as mine
import PowerUps.nukePowerUp as nuke
import PowerUps.speedPowerUp as speed
import PowerUps.phasePowerUp as phase
import pygame

# Test color tuples
GRID_BG = (0, 0, 0)
GRID_FG = (40, 140, 160)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
# Set bike and powerup to test colors
bike_color = WHITE
powerup_color = RED
# the scale of the grid and distance between cells
grid_cell_scl = 20  # width & height (scale) of each grid cell
grid_margin = 1  # amount of space on all sides of cells (must be odd for pygame line drawing)
grid_width = 20  # grid width cell count
grid_height = 20  # grid height cell count

screen_width = ((grid_margin + grid_cell_scl) * grid_width) + grid_margin  # width of the GUI window
screen_height = ((grid_margin + grid_cell_scl) * grid_height) + grid_margin  # height of the GUI window

CLOCK_SPD = 50  # the base clock speed, or arbitrary framerate - keep at 100
current_spd = CLOCK_SPD  # the current speed of the game (may change)
speed_timer = 0  # used to regulate when the current speed is changed

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Jeff bike')

# Menu System

# If player chooses the Tron Light Cycle game
    # Calls the draw grid file and passes in constants
draw.c_powerup(screen_width, screen_height, bike.scl)
draw.c_bike(grid_margin, grid_width, grid_height, grid_cell_scl)
draw.draw(screen, GRID_BG, GRID_FG, grid_width, grid_height, grid_margin, grid_cell_scl,screen_width, screen_height, bike_color, powerup_color, null)