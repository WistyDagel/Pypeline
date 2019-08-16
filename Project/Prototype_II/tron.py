import pygame, sys, color
import bike as b
import square as s
import color as c
import powerUps as pu

import pygame
import math
import random
import datetime

# import tron
from pygame.locals import *

pygame.init()

screen_width=800
screen_height=600

screen=pygame.display.set_mode((screen_width, screen_height))

def text_render(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (247, 148, 29)
YELLOW = (255, 242, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (102, 45, 145)
GRAY = (128,128,128)

#Font
font = "Assets/TRON.TTF"
timer_font = "Assets/clock.TTF"

#Framerate
clock = pygame.time.Clock()
FPS=30

grid_cell_scl = 20  # width & height (scale) of each grid cell
grid_margin = 1  # amount of space on all sides of cells (must be odd for pygame line drawing)
grid_width = 40  # grid width cell count
grid_height = 32  # grid height cell count

screen_width = ((grid_margin + grid_cell_scl) * grid_width) + grid_margin  # width of the GUI window
screen_height = ((grid_margin + grid_cell_scl) * grid_height) + grid_margin  # height of the GUI window

CLOCK_SPD = 100  # the base clock speed, or arbitrary framerate - keep at 100
current_spd = CLOCK_SPD  # the current speed of the game (may change)
speed_timer = 0  # used to regulate when the current speed is changed
slow_timer = 0 # used to regulate when the user slows their bike
duration_timer = 0


# decide on colors
bike_color = c.YELLOW
powerup_color = c.RED

GRID_BG = c.BLACK
GRID_FG = (40, 140, 160)

# initialize pygame module
# def initialize():

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Prototype II')

first = True
pygame.time.set_timer(USEREVENT+1, 1000)

def timer(time):
    screen.fill(GRAY, (0, 0, grid_cell_scl * (grid_width + 2), grid_cell_scl * 2 + 2)) 
    screen.blit(text_render(str(time), timer_font, 40, WHITE), ((grid_width * grid_cell_scl) - 10, 0))

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
    for powerup in powerups:
        pygame.draw.rect(screen, powerup.color, powerup.to_rect())

    #draw the top bar and the timer
    timer(time)

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()

# instantiate a bike object
bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_q, pygame.K_w, pygame.K_e), 
         b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
         b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.BLUE, pygame.K_z, pygame.K_x, pygame.K_c),
         b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.GREEN, pygame.K_i, pygame.K_o, pygame.K_p)]           

# Random number decides which power up is first
decidesStartingPowerUp = random.randint(0, 3)
if (decidesStartingPowerUp == 1 or decidesStartingPowerUp == 3):
    startingPowerUp = pu.PowerUps.Type.SPEED
elif (decidesStartingPowerUp == 2):
    startingPowerUp = pu.PowerUps.Type.MINE
else:
    startingPowerUp = pu.PowerUps.Type.NUKE

powerups = [pu.PowerUps(screen_width, screen_height, startingPowerUp)]

# start the clock (frames)
clock = pygame.time.Clock()

def main_menu():
    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        game_run()                      
                    if selected == "quit":
                        menu = False

        screen.fill(BLACK)
        title = text_render("TRON", font, 90, BLUE)
        if selected == "start":
            start_text = text_render("> START <", font, 50, YELLOW)
        else:
            start_text = text_render("START", font, 50, WHITE)
        if selected == "quit":
            quit_text = text_render("> QUIT <", font, 50, YELLOW)
        else:
            quit_text = text_render("QUIT", font, 50, WHITE)
    
        title_rect = title.get_rect()
        start_rect = start_text.get_rect()
        quit_rect = quit_text.get_rect()
    
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(start_text, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(quit_text, (screen_width/2 - (quit_rect[2]/2), 380))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Main Menu")

def game_run():
    # run while not done
    done = False

    pressed_down = False

    global CLOCK_SPD
    global current_spd
    global duration_timer
    
    global time
    time = 0
    pygame.time.set_timer(USEREVENT+1, 1000)

    while not done:
    
        for event in pygame.event.get():
            #increments time every second
            if event.type == USEREVENT+1:
                time += 1
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
                    elif event.key == bike.slow_key:
                        bike.cut()
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
            if bike.check_die(0,  (grid_cell_scl * 2), screen_width, screen_height):
                bikes.remove(bike)

            for other in bikes:
                if bike is not other and bike.touches(other.line_pieces):
                    bike.alive = False

                    
        delay = 10  # every x seconds, create a powerup
        decidesPowerUp = random.randint(0, 3)
        # Uses a random number to pick a random power up
        if (decidesPowerUp == 1 or decidesPowerUp == 3):
            randomPowerUp = pu.PowerUps.Type.SPEED
        elif (decidesPowerUp == 2):
            randomPowerUp = pu.PowerUps.Type.MINE
        else:
            randomPowerUp = pu.PowerUps.Type.NUKE

        if (pygame.time.get_ticks() % (CLOCK_SPD * delay) == 0):
            powerups.append(pu.PowerUps(screen_width, screen_height, randomPowerUp))

        for powerup in powerups:
            for bike in bikes:
                if (powerup.collides(bike)):
                    if (powerup.type is pu.PowerUps.Type.SPEED or
                        powerup.type is pu.PowerUps.Type.NUKE):
                        pu.PowerUps.apply_to_all(bikes, powerup.type)
                        powerups.remove(powerup)
                    # elif (powerup.type is pu.PowerUps.Type.NUKE):
                    #     for x in range(len(bikes)):
                    #         bikes[x] = powerup.apply_powerup(bike, powerup.type)
                    #     powerups.remove(powerup)

                        # After x amount of time, powerup affects disappear
                        duration_timer = 500
        duration_timer -= (1 if duration_timer > 0 else 0)
        if duration_timer == 0:
            for x in range(len(bikes)):
                bikes[x].s_multiplier = 1

        # calling the draw method after all the positioning and checking is done
        draw()

        # Pause the clock for a frame
        clock.tick(current_spd)
# when the loop is done, quit
#Initialize the Game
game_run()
pygame.quit()
quit()