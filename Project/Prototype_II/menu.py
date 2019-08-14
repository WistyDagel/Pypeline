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

#Font
font = "Assets/TRON.TTF"

#Framerate
clock = pygame.time.Clock()
FPS=30

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
# def initialize():

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
            start_text = text_render("START", font, 50, WHITE)
        else:
            start_text = text_render("START", font, 50, YELLOW)
        if selected == "quit":
            quit_text = text_render("QUIT", font, 50, WHITE)
        else:
            quit_text = text_render("QUIT", font, 50, YELLOW)
    
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

                if event.key == pygame.K_SPACE:
                    if current_spd == CLOCK_SPD:
                        current_spd = -1
                    else:
                        current_spd = CLOCK_SPD
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
#Initialize the Game
main_menu()
pygame.quit()
quit()