import bike as b
import square as s
import color as c
import powerUps as pu

import pygame
import math
import random
import datetime


grid_cell_scl = 20  # width & height (scale) of each grid cell
grid_margin = 1  # amount of space on all sides of cells (must be odd for pygame line drawing)
grid_width = 40  # grid width cell count
grid_height = 30  # grid height cell count

screen_width = ((grid_margin + grid_cell_scl) * grid_width) + grid_margin  # width of the GUI window
screen_height = ((grid_margin + grid_cell_scl) * grid_height) + grid_margin  # height of the GUI window

CLOCK_SPD = 50  # the base clock speed, or arbitrary framerate - keep at 100
current_spd = CLOCK_SPD  # the current speed of the game (may change)
speed_timer = 0  # used to regulate when the current speed is changed
slow_timer = 0 # used to regulate when the user slows their bike

# decide on colors
bike_color = c.YELLOW
powerup_color = c.RED

GRID_BG = c.BLACK
GRID_FG = (40, 140, 160)

# initialize pygame module
pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Prototype II')

# draw the background, grid, and squares
def draw():
    # erase everything
    screen.fill(GRID_BG)

    # grid x lines (vertical)
    for i in range(grid_width + 1):
        pygame.draw.line(screen, GRID_FG, (grid_margin / 2 + (i * (grid_cell_scl + grid_margin)), 0),
                         (grid_margin / 2 + (i * (grid_cell_scl + grid_margin)), screen_height), grid_margin)

    # grid y lines (horizontal)
    for i in range(grid_height + 1):
        pygame.draw.line(screen, GRID_FG, (0, grid_margin/2 + (i * (grid_cell_scl + grid_margin))),
                         (screen_width, grid_margin / 2 + (i * (grid_cell_scl + grid_margin))), grid_margin)

    # bike squares
    for bike in bikes:
        bike.draw(screen)

    # powerup
    if (datetime.time.second == 0):
        for powerup in powerups:
            pygame.draw.rect(screen, powerup.returnColor(), powerup.speed_powerUp().to_rect())
            break

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()


# instantiate a bike object
bikes = [b.Bike(0, 0, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_a, pygame.K_s, pygame.K_d), 
         b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)]           

powerups = [pu.PowerUps(9, screen_width, screen_height, (0, 255, 0))]

# start the clock (frames)
clock = pygame.time.Clock()
# run while not done
done = False

pressed_down = False

while not done:
 
    for event in pygame.event.get():
        # click the 'X' to close the window
        if event.type == pygame.QUIT:
            done = True

        # key press events
        if event.type == pygame.KEYDOWN:
            # bike controls
            # press right to turn right
            for bike in bikes:
                if event.key == bike.right_key:
                    bike.turn(1)
                elif event.key == bike.left_key:
                    bike.turn(-1)

                # # press down to slow the bike
                # if event.key == pygame.K_DOWN:
                #     pressed_down = True

            # pressing esc also closes the window
            if event.key == pygame.K_ESCAPE:
                done = True

        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_DOWN:
        #         pressed_down = False
        #         bike.s_multiplier = 1

    # Pressing the down key closes the window 
    # Starts a timer allowing you to only slow down for a specific amount of time
    # if pressed_down:
    #     bike.s_multiplier = .6
    #     slow_timer = 500
    # slow_timer -= (1 if slow_timer > 0 else 0)
    # if slow_timer == 0:
    #     bike.v_multiplier = 1

    # advance the bike in the direction it is goings
    for bike in bikes:
        bike.move()

        # make the bike check if it is 'dead' (see method declaration for more info)
        bike.check_die(0, 0, screen_width, screen_height)

        for other in bikes:
            if bike is not other and bike.touches(other.line_pieces):
                bike.alive = False


    # calling the draw method after all the positioning and checking is done
    draw()

    # Pause the clock for a frame
    clock.tick(current_spd)

# when the loop is done, quit
pygame.quit()
