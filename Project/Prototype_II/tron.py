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
arcade_font = "Assets/ARCADE_N.TTF"

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
duration_timer = 0 # Timer used when the speed is activated - lasts for 5 seconds
paused = False # Boolean for when the game is paused or not
game_modes = {"1 V 1" : 2, "2 V 2" : 4, "3 V 1" : 4, "Free For All" : 4} # Dictionary for game modes

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

#takes in the time, bikes and when they died and prints to the topbar
def timer(time, timerbikes, finalTimes):
    timerspot = 4;
    for bike in timerbikes:
        if(bike.alive):
            screen.blit(text_render(str(time), timer_font, 40, bike.color), (((8 * timerspot) * grid_cell_scl), 0))
            timerspot -= 1
        else:
            if(finalTimes[timerspot - 1] == 0):
                finalTimes[timerspot - 1] = time
            screen.blit(text_render(str(finalTimes[timerspot - 1]), timer_font, 40, bike.color), (((8 * timerspot) * grid_cell_scl), 0))
            timerspot -= 1


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
        for bike in bikes:
            if not bike.overlaps(powerup):
                pygame.draw.rect(screen, powerup.color, powerup.to_rect())

    # draw the top bar and the timer
    screen.fill(GRAY, (0, 0, grid_cell_scl * (grid_width + 2), grid_cell_scl * 2 + 2)) 
    timer(time, timerbikes, finalTimes)

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()

# instantiate a bike object
def generate_bikes(gamemode):
    global bikes
    if(gamemode == 1):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.BLUE, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.GREEN, pygame.K_i, pygame.K_o, pygame.K_p)]      
    if(gamemode == 2):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.BLUE, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.GREEN, pygame.K_i, pygame.K_o, pygame.K_p)]      
    if(gamemode == 3):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.BLUE, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.GREEN, pygame.K_i, pygame.K_o, pygame.K_p)]      
    if(gamemode == 4):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PURPLE, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.YELLOW, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.BLUE, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.GREEN, pygame.K_i, pygame.K_o, pygame.K_p)]      

# bikes[0].phase = True
# bikes[1].phase = True
# bikes[2].phase = True
# bikes[3].phase = True

# Random number decides which power up is first
decidesStartingPowerUp = random.randint(0, 3)
if (decidesStartingPowerUp == 1):
    startingPowerUp = pu.PowerUps.Type.SPEED
elif (decidesStartingPowerUp == 2):
    startingPowerUp = pu.PowerUps.Type.MINE
elif (decidesStartingPowerUp == 3):
    startingPowerUp = pu.PowerUps.Type.PHASE
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
                        game_mode_menu()                      
                    if selected == "quit":
                        menu = False

        screen.fill(BLACK)
        title = text_render("TRON", font, 90, GRID_FG)
        if selected == "start":
            start_text = text_render("> START <", arcade_font, 50, YELLOW)
        else:
            start_text = text_render("START", arcade_font, 50, WHITE)
        if selected == "quit":
            quit_text = text_render("> QUIT <", arcade_font, 50, YELLOW)
        else:
            quit_text = text_render("QUIT", arcade_font, 50, WHITE)
    
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

def game_mode_menu():
    mode_menu = True
    selected = "1 V 1"

    while mode_menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "1 V 1"
                elif event.key == pygame.K_RIGHT:
                    selected = "2 V 2"
                elif event.key == pygame.K_DOWN:
                    selected = "Free For All"
                elif event.key == pygame.K_LEFT:
                    selected = "3 V 1"
                if event.key == pygame.K_RETURN:
                    if selected == "1 V 1":
                        generate_bikes(1)
                        game_run()                
                    if selected == "2 V 2":
                        generate_bikes(2)
                        game_run()
                    if selected == "3 V 1":
                        generate_bikes(3)
                        game_run()
                    if selected == "Free For All":
                        generate_bikes(4)
                        game_run()

        screen.fill(BLACK)
        title = text_render("Game Modes", font, 75, GRID_FG)
        if selected == "1 V 1":
            one_text = text_render("> 1 V 1 <", arcade_font, 30, YELLOW)
        else:
            one_text = text_render("1 V 1", arcade_font, 30, WHITE)
        if selected == "2 V 2":
            two_text = text_render("> 2 V 2 <", arcade_font, 30, YELLOW)
        else:
            two_text = text_render("2 V 2", arcade_font, 30, WHITE)
        if selected == "3 V 1":
            three_text = text_render("> 3 V 1 <", arcade_font, 30, YELLOW)
        else:
            three_text = text_render(" 3 V 1 ", arcade_font, 30, WHITE)
        if selected == "Free For All":
            free_text = text_render("> Free For All <", arcade_font, 24, YELLOW)
        else:
            free_text = text_render(" Free For All ", arcade_font, 24, WHITE)
    
        title_rect = title.get_rect()
        one_rect = one_text.get_rect()
        three_rect = three_text.get_rect()
    
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(one_text, (screen_width/2 - (one_rect[2]/2), 300))
        screen.blit(two_text, (625, 400))
        screen.blit(three_text, (50, 410))  
        screen.blit(free_text, (260, 525))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Game Mode")

def game_run():
    # run while not done
    done = False

    pressed_down = False

    global CLOCK_SPD
    global current_spd
    global duration_timer
    global paused
    
    global time
    global finalTimes
    global timerbikes
    timerbikes = bikes.copy()       
    finalTimes = [0, 0, 0, 0]
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
                    main_menu()

            #Pressing space bar pauses the game
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = True

            #Waits for user input to unpause the game
            while paused == True:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == pygame.K_SPACE:
                            paused = False
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
                for timerbike in timerbikes:
                    if(bike.color == timerbike.color):
                        timerbike.alive = False
                bikes.remove(bike)

            for other in bikes:
                if bike is not other:
                    if bike.phase is not True:
                        if bike.touches(other):
                            bike.alive = False

                    
        delay = 10  # every x seconds, create a powerup
        decidesPowerUp = random.randint(0, 3)
        # Uses a random number to pick a random power up
        if (decidesPowerUp == 1):
            randomPowerUp = pu.PowerUps.Type.SPEED
        elif (decidesPowerUp == 2):
            randomPowerUp = pu.PowerUps.Type.MINE
        elif (decidesPowerUp == 3):
            randomPowerUp = pu.PowerUps.Type.PHASE
        else:
            randomPowerUp = pu.PowerUps.Type.NUKE

        if (pygame.time.get_ticks() % (CLOCK_SPD * delay) == 0):
            powerups.append(pu.PowerUps(screen_width, screen_height, randomPowerUp))

        for powerup in powerups:
            for bike in bikes:
                # Stops the powerup from spawning ontop of a line
                # If it spawns on a line, then it will remove it from the list and recreate a new powerup
                # NEEDS WORK
                if (powerup.collides(bike)):
                    if (powerup.type is pu.PowerUps.Type.SPEED or
                        powerup.type is pu.PowerUps.Type.NUKE):
                        pu.PowerUps.apply_to_all(bikes, powerup.type)
                        # After x amount of time, powerup affects disappear
                        duration_timer = 500
                    elif (powerup.type is pu.PowerUps.Type.MINE):
                        p = pu.PowerUps(screen_width, screen_height, pu.PowerUps.Type.ACTUALLY_MINE)
                        p.h *= 2
                        p.w *= 2
                        powerups.append(p)
                    elif (powerup.type is pu.PowerUps.Type.ACTUALLY_MINE):
                        bike.alive = False
                    elif (powerup.type is pu.PowerUps.Type.PHASE):
                        bike.phase = True

                    powerups.remove(powerup)
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
main_menu()
pygame.quit()
quit()