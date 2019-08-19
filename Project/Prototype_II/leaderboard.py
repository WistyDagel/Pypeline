import pygame
import random
import sys, color
from pygame.locals import *
from os import path

class highScore:

    def load_data(highscore):
        # load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def save_data(highscore):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0



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

def Leader_Board():
        screen.fill(BLACK)
        title=text_render("High Scores", font, 75, BLUE)

        start_text = text_render("START", font, 50, YELLOW)
        quit_text = text_render("QUIT", font, 50, YELLOW)

        title_rect=title.get_rect()
        start_rect=start_text.get_rect()
        quit_rect=quit_text.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(start_text, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(quit_text, (screen_width/2 - (quit_rect[2]/2), 380))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Main Menu")

#Initialize the Game
main_menu()
pygame.quit()
quit() 