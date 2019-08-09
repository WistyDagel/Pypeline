import bike as b
import square as s
import color as c

import pygame
import math
import random


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


#### TEMPORARY ####

# returns a powerup positioned at a random location on the screen
def c_powerup():
    return s.Square(random.randint(0, int(screen_width - bike.weight + 1)),  # random x
                  random.randint(0, int(screen_height - bike.weight + 1)),  # random y
                  bike.weight * 1.5,  # 50% larger than the bike
                  bike.weight * 1.5)  # 50% larger than the bike


# returns a bike of scale 6 positioned at the center of the screen, going RIGHT
def c_bike():
    return b.Bike(grid_margin + (grid_width - math.ceil(grid_width / 2)) * (grid_cell_scl + grid_margin),
                grid_margin + (grid_height - math.ceil(grid_height/2)) * (grid_cell_scl + grid_margin),
                b.Bike.Direction.RIGHT, bike_color)

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
    for rect in bike.line_pieces:
        pygame.draw.rect(screen, bike.color, rect.to_rect())

    # powerup
    pygame.draw.rect(screen, powerup_color, powerup.to_rect())

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()

#### /TEMPORARY ####


# instantiate a bike object
bike = c_bike()

# instantiate a powerup that does not collide with the bike (if no spaces are available, it stops after 100 iterations)
for i in range(100):
    valid = True
    powerup = c_powerup()
    for piece in bike.line_pieces:
        if powerup.overlaps(piece):
            valid = False
    if not valid:
        break

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
            if event.key == pygame.K_RIGHT:
                bike.turn(1)
            # press left to turn left
            if event.key == pygame.K_LEFT:
                bike.turn(-1)

            # press down to slow the bike
            if event.key == pygame.K_DOWN:
                pressed_down = True
                print(pressed_down)

            # pressing esc also closes the window
            if event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressed_down = False
                bike.v_multiplier = 1

    # Pressing the down key closes the window 
    # Starts a timer allowing you to only slow down for a specific amount of time
    if pressed_down:
        bike.v_multiplier = .7
    #     slow_timer = 500
    # slow_timer -= (1 if slow_timer > 0 else 0)
    # if slow_timer == 0:
    #     bike.v_multiplier = 1

    # advance the bike in the direction it is goings
    bike.move()

    # if bike uses powerup, do stuff
    if bike.use(powerup):
        powerup = c_powerup()  # create a new powerup
        current_spd = CLOCK_SPD * 3  # multiply the current clock speed
        speed_timer = 500  # set the timer to an arbitrary number
    speed_timer -= (1 if speed_timer > 0 else 0)  # count the timer down every frame unless it is 0
    if speed_timer == 0:  # if the timer is done running, set the current speed back to the clock speed
        current_spd = CLOCK_SPD  # this technically runs every frame, except when timer > 0

    # make the bike check if it is 'dead' (see method declaration for more info)
    bike.check_die(0, 0, screen_width, screen_height)
    # if the bike is dead, regenerate it and the powerup
    if not bike.alive:
        bike = c_bike()
        powerup = c_powerup()
        current_spd = CLOCK_SPD
        speed_timer = 0

    # calling the draw method after all the positioning and checking is done
    draw()

    # Pause the clock for a frame
    clock.tick(current_spd)

# when the loop is done, quit
pygame.quit()
