import pygame, sys, color
import bike as b
import square as s
import color as c
import powerUps as pu
import json

import pygame
import math
import random
import datetime
from sys import exit

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
menu=True #Menu boolean that is set whenever the user is on the main menu
mode_menu=True #Mode menu boolean that is set whenever the user is on the game mode menu
leaderboard=True #leaderboard menu

# decide on colors
bike_color = c.YELLOW
powerup_color = c.RED

GRID_BG = c.BLACK
GRID_FG = c.GRID_BLUE

# initialize pygame module
# def initialize():

screen = pygame.display.set_mode([screen_width, screen_height], pygame.NOFRAME)

pygame.display.set_caption('Prototype II')

first = True
pygame.time.set_timer(USEREVENT+1, 1000)

powerups = []

def save_data(highscores, names, file):
    data = {}
    data['leaderboard'] = []
    data['leaderboard'].append({
        'names': names,
        'highscores': highscores
            
    })

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def load_data(file):
    with open(file) as json_file:
        data = json.load(json_file)
        global names
        global highscores
        for p in data['leaderboard']:
            names = p['names']
            highscores = p['highscores']


#takes in the time, bikes and when they died and prints to the topbar
def timer(time, timerbikes, finalTimes):
    bikesleft = len(timerbikes)
    posistion = 40 / (bikesleft + 1)
    for bike in timerbikes:
        if(bike.alive):
            screen.blit(text_render(str(time), timer_font, 40, bike.color), (((posistion * bikesleft) * (grid_cell_scl + grid_margin)), 0))
            bikesleft -= 1
        else:
            if(finalTimes[bikesleft - 1] == 0):
                finalTimes[bikesleft - 1] = time
            screen.blit(text_render(str(finalTimes[bikesleft - 1]), timer_font, 40, bike.color), (((posistion * bikesleft) * (grid_cell_scl + grid_margin)), 0))
            bikesleft -= 1

# draw the background, grid, and squares
def draw(endState, inTeams):
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

    # bike glow
    for bike in bikes:
        bike.draw_glow(screen)

    # bike squares
    for bike in bikes:
        bike.draw(screen)

    # powerup
    for powerup in powerups:
        for bike in bikes:
            # Stops the power ups from spawning on a line.
            # Removes the power up from the list so it does not spawn the second a player dies.
            if not bike.overlaps(powerup):
                pygame.draw.rect(screen, powerup.color, powerup.to_rect())
            else:
                powerups.remove(powerup)

    # draw the top bar and the timer
    screen.fill(GRAY, (0, 0, grid_cell_scl * (grid_width + 2), grid_cell_scl * 2 + 2)) 
    timer(time, timerbikes, finalTimes)

    if(endState):
        screen.fill(GRAY, (screen_width/6, screen_height/3, 2*screen_width/3, screen_height/3))
        if(inTeams == 2 or inTeams == 3):
            if(timerbikes[0].color == bikes[0].color):
                winner_text = text_render("Team 1 Wins", arcade_font, 40, bikes[0].color)
            else:
                winner_text = text_render("Team 2 Wins", arcade_font, 40, bikes[0].color)
        else:
            if(timerbikes[0].left_key == bikes[0].left_key):
                winner_text = text_render("Player 1 Wins", arcade_font, 40, bikes[0].color)
            elif(timerbikes[1].left_key == bikes[0].left_key):
                winner_text = text_render("Player 2 Wins", arcade_font, 40, bikes[0].color)
            elif(timerbikes[2].left_key == bikes[0].left_key):
                winner_text = text_render("Player 3 Wins", arcade_font, 40, bikes[0].color)
            elif(timerbikes[3].left_key == bikes[0].left_key):
                winner_text = text_render("Player 4 Wins", arcade_font, 40, bikes[0].color)
        continue_text = text_render("Press Enter/Return to continue", arcade_font, 15, GRID_FG)
        winner_rect = winner_text.get_rect()
        continue_rect = continue_text.get_rect()
        screen.blit(winner_text, (screen_width/2 - (winner_rect[2]/2), 3*screen_height/7))
        screen.blit(continue_text, (screen_width/2 - (continue_rect[2]/2), 3*screen_height/5))
    # flip the screen (? not sure why needed ?)
    pygame.display.flip()

# instantiate a bike object
def generate_bikes(gamemode):
    global bikes
    global powerups
    if(gamemode == 1):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PLAYER1, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.PLAYER4, pygame.K_i, pygame.K_o, pygame.K_p)]     
    if(gamemode == 2):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PLAYER1, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.PLAYER1, pygame.K_i, pygame.K_o, pygame.K_p),      
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.PLAYER4, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.PLAYER4, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)]     
    if(gamemode == 3):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PLAYER1, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.PLAYER1, pygame.K_i, pygame.K_o, pygame.K_p),      
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.PLAYER1, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.PLAYER4, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)]      
    if(gamemode == 4):
        bikes = [b.Bike(0, (grid_cell_scl * 2) + 2, b.Bike.Direction.RIGHT, c.PLAYER1, pygame.K_q, pygame.K_w, pygame.K_e), 
                b.Bike(screen_width - b.Bike.WEIGHT, grid_cell_scl * 2, b.Bike.Direction.DOWN, c.PLAYER2, pygame.K_i, pygame.K_o, pygame.K_p),      
                b.Bike(0, screen_height - b.Bike.WEIGHT, b.Bike.Direction.UP, c.PLAYER3, pygame.K_z, pygame.K_x, pygame.K_c),
                b.Bike(screen_width - b.Bike.WEIGHT, screen_height - b.Bike.WEIGHT, b.Bike.Direction.LEFT, c.PLAYER4, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)]
    
    powerups.clear()

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
    selected="start"
    global menu

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        game_mode_menu()
                    if selected == "quit":
                        exit()

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
        screen.blit(start_text, (screen_width/2 - (start_rect[2]/2), 400))
        screen.blit(quit_text, (screen_width/2 - (quit_rect[2]/2), 480))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Main Menu")

def game_mode_menu():
    selected = "1 V 1"
    global inTeams;
    global mode_menu
    #Esc key brings you back to main menu - Chris work on
    
    while mode_menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    mode_menu = False
                    pygame.quit()
                    exit()
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
                        inTeams = 1
                        tutorial_menu()
                    if selected == "2 V 2":
                        generate_bikes(2)
                        inTeams = 2
                        tutorial_menu()
                    if selected == "3 V 1":
                        generate_bikes(3)
                        inTeams = 3
                        tutorial_menu()
                    if selected == "Free For All":
                        generate_bikes(4)
                        inTeams = 4
                        tutorial_menu()

        screen.fill(BLACK)
        title = text_render("Game Modes", font, 75, GRID_FG)
        if selected == "1 V 1":
            one_text = text_render("> 1 V 1 <", arcade_font, 28, YELLOW)
        else:
            one_text = text_render("1 V 1", arcade_font, 28, WHITE)
        if selected == "2 V 2":
            two_text = text_render("> 2 V 2 <", arcade_font, 28, YELLOW)
        else:
            two_text = text_render("2 V 2", arcade_font, 28, WHITE)
        if selected == "3 V 1":
            three_text = text_render("> 3 V 1 <", arcade_font, 28, YELLOW)
        else:
            three_text = text_render(" 3 V 1 ", arcade_font, 28, WHITE)
        if selected == "Free For All":
            free_text = text_render("> Free For All <", arcade_font, 24, YELLOW)
        else:
            free_text = text_render(" Free For All ", arcade_font, 24, WHITE)
    
        title_rect = title.get_rect()
        one_rect = one_text.get_rect()
        two_rect = two_text.get_rect()
        three_rect = three_text.get_rect()
        free_rect = free_text.get_rect()
    
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(one_text, (screen_width/2 - (one_rect[2]/2), 300))
        screen.blit(two_text, (screen_width/2 - (two_rect[2]/2)+200, 400))
        screen.blit(three_text, (screen_width/2 - (three_rect[2]/2)-200, 400))  
        screen.blit(free_text, (screen_width/2 - (free_rect[2]/2), 525))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Game Mode")

# Chris notes
# Music for menu and game

def tutorial_menu():
    global mode_menu
    while mode_menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    mode_menu = False
                    pygame.quit()
                    exit()
                if event.key == pygame.K_RETURN:
                    game_run()

        screen.fill(BLACK)
        title = text_render("Controls", font, 75, GRID_FG)
        player1_text = text_render("Player 1: Q - Turn Left | W - Slow Bike | E - Turn right", arcade_font, 12, bikes[0].color)
        player2_text = text_render("Player 2: I - Turn Left | O - Slow Bike | P - Turn right", arcade_font, 12, bikes[1].color)
        continue_text = text_render("Press Enter/Return to start game...", arcade_font, 15, GRID_FG)
        title_rect = title.get_rect()
        player1_rect = player1_text.get_rect()
        player2_rect = player2_text.get_rect()
        continue_rect = continue_text.get_rect()

        if len(bikes) > 2: 
            position1 = 200 
        else: 
            position1 = 300

        if len(bikes) > 2: 
            position2 = 300 
        else: 
            position2 = 400

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
        screen.blit(player1_text, (screen_width/2 - (player1_rect[2]/2), position1))
        screen.blit(player2_text, (screen_width/2 - (player2_rect[2]/2), position2))
        screen.blit(continue_text, (screen_width/2 - (continue_rect[2]/2), 600))



        #Checks to see if the player count is 4
        if len(bikes) > 2:
            player3_text = text_render("Player 3: Z - Turn Left | X - Slow Bike | C - Turn right", arcade_font, 12, bikes[2].color)
            player4_text = text_render("Player 4: L Arrow - Turn Left | D Arrow - Slow Bike | R Arrow - Turn Right", arcade_font, 11, bikes[3].color)
            player3_rect = player3_text.get_rect()
            player4_rect = player4_text.get_rect()
            screen.blit(player3_text, (screen_width/2 - (player3_rect[2]/2), 400))  
            screen.blit(player4_text, (screen_width/2 - (player4_rect[2]/2), 500))
    
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Game Mode")

def Leader_Board(teams, winnerposition, file):
    global leaderboard
    global namenotassigned
    namenotassigned = True
    while leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    leaderboard = False
                    pygame.quit()
                    exit()
                if event.key == pygame.K_RETURN:
                    names.pop()
                    highscores.pop()
                    save_data(highscores, names, file)
                    main_menu()

        screen.fill(BLACK)
        title = text_render("LeaderBoard", arcade_font, 50, GRID_FG)
        title_rect = title.get_rect()
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), screen_height/60))
        if(teams == 1):
            subtitle = text_render("1 V 1", arcade_font, 40, GRID_FG)
            subtitle_rect = subtitle.get_rect()
            screen.blit(subtitle, (screen_width/2 - (subtitle_rect[2]/2), (title_rect[2]/9)))
        elif(teams == 2):
            subtitle = text_render("2 V 2", arcade_font, 40, GRID_FG)
            subtitle_rect = subtitle.get_rect()
            screen.blit(subtitle, (screen_width/2 - (subtitle_rect[2]/2), (title_rect[2]/9)))
        elif(teams == 3):
            subtitle = text_render("3 V 1", arcade_font, 40, GRID_FG)
            subtitle_rect = subtitle.get_rect()
            screen.blit(subtitle, (screen_width/2 - (subtitle_rect[2]/2), (title_rect[2]/9)))
        elif(teams == 4):
            subtitle = text_render("Free For All", arcade_font, 40, GRID_FG)
            subtitle_rect = subtitle.get_rect()
            screen.blit(subtitle, (screen_width/2 - (subtitle_rect[2]/2), (title_rect[2]/9)))
        
        highscoreLines = []
        highscore_rect = title.get_rect()
        if(len(names) < 11):
            names.insert(winnerposition, "AAA")
        if(len(names) > 11):
            names.pop()
        for x in range(10):
            if(x != 9):
                highscoreLines.append(str(x + 1) + ": " + names[x] + "     " + highscores[x])
            else:
                highscoreLines.append(str(x + 1) + ": " + names[x] + "     " + highscores[x] + " ")

        for x in range(len(highscoreLines)):
            highscore = text_render(highscoreLines[x], arcade_font, 20, GRID_FG)
            highscore_rect = highscore.get_rect()
            screen.blit(highscore, (screen_width/2 - (highscore_rect[2]/2), (title_rect[2]/9) + (subtitle_rect[3]) + (highscore_rect[3] * x)))

        letter = ''
        settingNameText = ">A< AA"
        while(namenotassigned):
            if(winnerposition != 10):
                screen.fill(BLACK, (0, 3*screen_height/4, screen_width, screen_height))
                screen.blit(text_render(">", arcade_font, 20, GRID_FG), (screen_width/2 - (highscore_rect[2]/2) - 25,
                                                                (title_rect[2]/9) + (subtitle_rect[3]) + (highscore_rect[3] * winnerposition)))
                settingName = text_render(settingNameText, arcade_font, 40, GRID_FG)
                settingName_rect = settingName.get_rect()
                screen.blit(settingName, (screen_width/2 - (settingName_rect[2]/2), (8*screen_height/10)))
                toNextLetter = text_render("Hit enter to lock in the letter", arcade_font, 15, GRID_FG)
                toNextLetter_rect = toNextLetter.get_rect()
                screen.blit(toNextLetter, (screen_width/2 - (toNextLetter_rect[2]/2), 9*screen_height/10))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_UP:
                            if(settingNameText.index(">") == 0):
                                letter = settingNameText[1]
                                if(letter == "Z"):
                                    settingNameText = settingNameText.replace(">Z", ">A")

                                else:
                                    letter = chr(ord(letter) + 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) - 1), ">" + letter)

                            elif(settingNameText.index(">") == 2):
                                letter = settingNameText[3]
                                if(letter == "Z"):
                                    settingNameText = settingNameText.replace(">Z", ">A")

                                else:
                                    letter = chr(ord(letter) + 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) - 1), ">" + letter)

                            elif(settingNameText.index(">") == 3):
                                letter = settingNameText[4]
                                if(letter == "Z"):
                                    settingNameText = settingNameText.replace(">Z", ">A")

                                else:
                                    letter = chr(ord(letter) + 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) - 1), ">" + letter)

                        elif event.key == pygame.K_DOWN:
                            if(settingNameText.index(">") == 0):
                                letter = settingNameText[1]
                                if(letter == "A"):
                                    settingNameText = settingNameText.replace(">A", ">Z")

                                else:
                                    letter = chr(ord(letter) - 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) + 1), ">" + letter)

                            elif(settingNameText.index(">") == 2):
                                letter = settingNameText[3]
                                if(letter == "A"):
                                    settingNameText = settingNameText.replace(">A", ">Z")

                                else:
                                    letter = chr(ord(letter) - 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) + 1), ">" + letter)

                            elif(settingNameText.index(">") == 3):
                                letter = settingNameText[4]
                                if(letter == "A"):
                                    settingNameText = settingNameText.replace(">A", ">Z")

                                else:
                                    letter = chr(ord(letter) - 1)
                                    settingNameText = settingNameText.replace(">" + chr(ord(letter) + 1), ">" + letter)
            
                        if event.key == pygame.K_RETURN:
                            if(settingNameText.index(">") == 0):
                                settingNameText = settingNameText.replace(">" + settingNameText[1] + "< A", settingNameText[1] +" >A< ", 1)

                            elif(settingNameText.index(">") == 2):
                                settingNameText = settingNameText.replace(" >" + settingNameText[3] + "< A", settingNameText[3] +" >A<", 1)

                            else:
                                names[winnerposition] = settingNameText[0] + settingNameText[1] + settingNameText[4]
                                namenotassigned = False;
            else:
                namenotassigned = False;
            screen.fill(BLACK, (0, 3*screen_height/4, screen_width, screen_height))
            screen.blit(text_render(">", arcade_font, 20, GRID_FG), (screen_width/2 - (highscore_rect[2]/2) - 25,
                                                            (title_rect[2]/9) + (subtitle_rect[3]) + (highscore_rect[3] * winnerposition)))
            settingName = text_render(settingNameText, arcade_font, 40, GRID_FG)
            settingName_rect = settingName.get_rect()
            screen.blit(settingName, (screen_width/2 - (settingName_rect[2]/2), (8*screen_height/10)))
            toNextLetter = text_render("Hit enter to lock in the letter", arcade_font, 15, GRID_FG)
            toNextLetter_rect = toNextLetter.get_rect()
            screen.blit(toNextLetter, (screen_width/2 - (toNextLetter_rect[2]/2), 9*screen_height/10))

            pygame.display.update()
            clock.tick(FPS)
            pygame.display.set_caption("LeaderBoard")

        settingName = text_render("Your Score: " + highscores[winnerposition], arcade_font, 35, GRID_FG)
        settingName_rect = settingName.get_rect()
        screen.blit(settingName, (screen_width/2 - (settingName_rect[2]/2), 8*screen_height/10))
        toMainMenu = text_render("Hit enter to go to the Main Menu", arcade_font, 15, GRID_FG)
        toMainMenu_rect = toMainMenu.get_rect()
        screen.blit(toMainMenu, (screen_width/2 - (toMainMenu_rect[2]/2), 9*screen_height/10))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("LeaderBoard")

def game_run():
    # run while not done
    done = False
    mode_menu = False

    pressed_down = False

    global CLOCK_SPD
    global current_spd
    global duration_timer
    global paused
    global slow_timer
    global endState
    endState = False
    global file
    if(inTeams == 1):
        file = "1v1_leaderboard.txt"
    elif(inTeams == 2):
        file = "2v2_leaderboard.txt"
    elif(inTeams == 3):
        file = "3v1_leaderboard.txt"
    elif(inTeams == 4):
        file = "FFA_leaderboard.txt"
    global highscorezeros
    highscorezeros = ""
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
                        bike.s_multiplier = 0.4
                        duration_timer = 100
                    elif event.key == bike.left_key:
                        bike.turn(-1)

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


        # advance the bike in the direction it is goings
        for bike in bikes:
            bike.move()

            # make the bike check if it is 'dead' (see method declaration for more info)
            if bike.check_die(0,  (grid_cell_scl * 2), screen_width, screen_height):
                for timerbike in timerbikes:
                    if(bike.left_key == timerbike.left_key):
                        timerbike.alive = False
                bikes.remove(bike)

            for other in bikes:
                if bike is not other:
                    if bike.phase is not True and bike.color is not other.color:
                        if bike.touches(other) & bike.alive:
                            bike.alive = False
                            for bike in timerbikes:
                                if(bike.left_key == other.left_key):
                                    bike.kills += 1

                    
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
                        duration_timer = 500

                    powerups.remove(powerup)
                
                # Pressing the down key closes the window 
                # Starts a timer allowing you to only slow down for a specific amount of time
                
                # slow_timer -= (1 if slow_timer > 0 else 0)

                # if slow_timer == 0:
                #     bike.s_multiplier = 1
                # if pressed_down:
                #     slow_timer = 500
                #     bike.s_multiplier = .2

                # slow_timer -= (1 if slow_timer > 0 else 0)

                # if slow_timer == 0:
                #     bike.s_multiplier = 1

        duration_timer -= (1 if duration_timer > 0 else 0)
        if duration_timer == 0:
            for x in range(len(bikes)):
                bikes[x].s_multiplier = 1
                bikes[x].phase = False

        # calling the draw method after all the positioning and checking is done
        draw(endState, inTeams)

        # Pause the clock for a frame
        clock.tick(current_spd)

        #check for win
        if(len(bikes) < 4):
            endState = False
            if(len(bikes) == 1):
                endState = True
            elif(len(bikes) == 2):
                if(bikes[0].color == bikes[1].color):
                    endState = True
            elif(len(bikes) == 3):
                if(bikes[0].color == bikes[1].color and bikes[1].color == bikes[2].color):
                    endState = True
        if(endState):        
            draw(endState, inTeams)
            winnerhighscore = 0
            killmult = 1
            load_data(file)
            place = 0

            if(inTeams == 2 or inTeams == 3):
                if(timerbikes[0].color == bikes[0].color):
                    if(inTeams == 2):
                        winnerhighscore += finalTimes[0]
                        winnerhighscore += finalTimes[1]
                        killmult += timerbikes[0].kills
                        killmult += timerbikes[1].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                    else:
                        winnerhighscore += finalTimes[0]
                        winnerhighscore += finalTimes[1]
                        winnerhighscore += finalTimes[2]
                        killmult += timerbikes[0].kills
                        killmult += timerbikes[1].kills
                        killmult += timerbikes[2].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                else:
                    if(inTeams == 2):
                        winnerhighscore += finalTimes[2]
                        winnerhighscore += finalTimes[3]
                        killmult += timerbikes[2].kills
                        killmult += timerbikes[3].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                    else:
                        winnerhighscore += finalTimes[3]
                        killmult += timerbikes[3].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 2
                        winnerhighscore *= 10
            else:
                if(timerbikes[0].left_key == bikes[0].left_key):
                        winnerhighscore += finalTimes[0]
                        killmult += timerbikes[0].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                elif(timerbikes[1].left_key == bikes[0].left_key):
                        winnerhighscore += finalTimes[1]
                        killmult += timerbikes[1].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                elif(timerbikes[2].left_key == bikes[0].left_key):
                        winnerhighscore += finalTimes[2]
                        killmult += timerbikes[2].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10
                elif(timerbikes[3].left_key == bikes[0].left_key):
                        winnerhighscore += finalTimes[3]
                        killmult += timerbikes[3].kills
                        winnerhighscore *= killmult
                        winnerhighscore *= 10

            for num in range(10 - len(str(winnerhighscore))):
                highscorezeros = highscorezeros + "0"
            winnerscore = highscorezeros + str(winnerhighscore)
            for highscore in highscores:
                if(highscore >= winnerscore):
                    place += 1
            highscores.insert(place, winnerscore)
            print(place)
            print(highscores[10])

            while(endState):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            print(place)
                            Leader_Board(inTeams, place, file)

# when the loop is done, quit
#Initialize the Game
main_menu()
pygame.quit()
quit()