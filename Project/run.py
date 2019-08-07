import draw as draw
import bike as b
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
b = draw.c_bike(grid_margin, grid_width, grid_height, grid_cell_scl)
p = draw.c_powerup(screen_width, screen_height, b.scl)

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
                bike.turn_right()
            # press left to turn left
            if event.key == pygame.K_LEFT:
                bike.turn_left()

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

    # advance the bike in the direction it is going
    b.move()

    # if bike uses powerup, do stuff
    if b.use(p):
        p = draw.c_powerup(screen_width, screen_height, b.scl)  # create a new powerup
        current_spd = CLOCK_SPD * 3  # multiply the current clock speed
        speed_timer = 500  # set the timer to an arbitrary number
    speed_timer -= (1 if speed_timer > 0 else 0)  # count the timer down every frame unless it is 0
    if speed_timer == 0:  # if the timer is done running, set the current speed back to the clock speed
        current_spd = CLOCK_SPD  # this technically runs every frame, except when timer > 0

    # make the bike check if it is 'dead' (see method declaration for more info)
    b.check_die(0, 0, screen_width, screen_height)
    # if the bike is dead, regenerate it and the powerup
    if not b.alive:
        b = draw.c_bike(grid_margin, grid_width, grid_height, grid_cell_scl)
        powerup = draw.c_powerup(screen_width, screen_height, b.scl)
        current_spd = CLOCK_SPD
        speed_timer = 0

    # calling the draw method after all the positioning and checking is done
    draw.draw(b, screen, GRID_BG, GRID_FG, grid_width, grid_height, grid_margin, grid_cell_scl, screen_width, screen_height, bike_color, powerup_color, p)

    # Pause the clock for a frame
    clock.tick(current_spd)

pygame.quit()