import pygame, sys, color
import bike as b
import square as s
import color as c
import powerUps as pu
from pygame.locals import *
from os import path
import json

class highScore:
    def save_data(highscore, name, file):
        data = {}
        data['leaderboard'] = []
        data['leaderboard'].append({
            'name': name,
            'highscore': str(highscore)
            
        })

        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    def load_data(highscore, file):
        with open(file) as json_file:
            data = json.load(json_file)
            for p in data['leaderboard']:
                print('Name: ' + p['name'])
                print('Highscore: ' + p['highscore'])


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

screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

CLOCK_SPD = 100  # the base clock speed, or arbitrary framerate - keep at 100
current_spd = CLOCK_SPD  # the current speed of the game (may change)
speed_timer = 0  # used to regulate when the current speed is changed
slow_timer = 0 # used to regulate when the user slows their bike
duration_timer = 0 # Timer used when the speed is activated - lasts for 5 seconds
paused = False # Boolean for when the game is paused or not
game_modes = {"1 V 1" : 2, "2 V 2" : 4, "3 V 1" : 4, "Free For All" : 4} # Dictionary for game modes
menu=True #Menu boolean that is set whenever the user is on the main menu
mode_menu=True #Mode menu boolean that is set whenever the user is on the game mode menu

GRID_BG = c.BLACK
GRID_FG = c.GRID_BLUE


def Leader_Board():
    selected="start"
    global menu

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    mode_menu = False
                    pygame.quit()
                    exit()
                if event.key == pygame.K_RETURN:
                    main_menu()

        screen.fill(BLACK)
        title = text_render("LeaderBoard", font, 50, GRID_FG)
        subtitle = text_render("1 V 1", font, 50, GRID_FG)
    
        title_rect = title.get_rect()
        subtitle_rect = title.get_rect()
    
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 0))
        screen.blit(subtitle, (screen_width/2 - (subtitle_rect[2]/7), (title_rect[2]/9)))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("LeaderBoard")


#Initialize the Game
Leader_Board()
pygame.quit()
quit() 