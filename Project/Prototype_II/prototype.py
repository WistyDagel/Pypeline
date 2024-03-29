import math
import random
import pygame
from enum import *
from pygame.locals import *

# sample color tuples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRID_BG = BLACK
GRID_FG = (40, 140, 160)

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)

YELLOW = (255, 227, 77)

GRAY = (128,128,128)

# set bike and powerup to arbitrary colors
bike_color = YELLOW
powerup_color = R

# GRID_FG = GRID_BG

#Font
font = "Assets/TRON.TTF"

# the scale of the grid and distance between cells
grid_cell_scl = 20  # width & height (scale) of each grid cell
grid_margin = 1  # amount of space on all sides of cells (must be odd for pygame line drawing)
grid_width = 40  # grid width cell count
grid_height = 32  # grid height cell count

screen_width = ((grid_margin + grid_cell_scl) * grid_width) + grid_margin  # width of the GUI window
screen_height = ((grid_margin + grid_cell_scl) * grid_height) + grid_margin  # height of the GUI window

CLOCK_SPD = 50  # the base clock speed, or arbitrary framerate - keep at 100
current_spd = CLOCK_SPD  # the current speed of the game (may change)
speed_timer = 0  # used to regulate when the current speed is changed
slow_timer = 0 # used to regulate when the user slows their bike

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Jeff bike')

def text_render(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


# represents a square on the grid
class Square:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def overlaps(self, other):
        return self.to_rect().colliderect(other.to_rect())


class Bike:
    # represents each of the 4 possible directions the bike may go
    # This is here because the bike should know it's own state of direction
    class Direction(IntEnum):
        RIGHT = auto()  # 1
        DOWN = auto()  # 2
        LEFT = auto()  # 3
        UP = auto()  # 4

        # returns x-y velocity multipliers
        def get_multipliers(self):
            # values used to multiply to x and y velocity, corresponding with the Direction(Enum) value
            # example: dir_vel[2] -> 0 * vel (x), 1 * vel (y). Effective velocity: Down
            dir_vel = (
                (1, 0),  # Right (1)
                (0, 1),  # Down (2)
                (-1, 0),  # Left (3)
                (0, -1),  # Right (4)
            )
            return dir_vel[self.value - 1]  # tuples are indexed from 0, Enums from 1 (Why? See Enum documentation)

    """
    :param x - the x position of the bike at the start of the game
    :param y - the y position of the bike at the start of the game
    :param scl - the size of each Piece of the line (scale)
    :param direction - the Direction that the bike will be going at the start of the game
    """
    def __init__(self, x: int, y: int, scl: int, direction: Direction, color):
        self.scl = scl
        self.line_pieces = [Square(x, y, self.scl, self.scl)]
        self.direction = direction
        self.color = color

        self.VEL = 1  # velocity - hard-coded to 1 pixel per frame
        self.v_multiplier = 1 #velocity modifier for when the bike slows down  
        self.alive = True  # used to quickly check the status of the bike

    # appends a new Square to the end of the line_pieces. The x and y of the new Square are the previous Square's
    # x and y plus the bike's directional velocity
    def move(self):
        bike = self.get_bike()
        vel_mult = self.direction.get_multipliers()  # velocity multipliers (x, y)

        self.line_pieces.append(Square(bike.x + (vel_mult[0] * self.VEL * self.v_multiplier),  # new x
                                       bike.y + (vel_mult[1] * self.VEL * self.v_multiplier),  # new y
                                       self.scl,  # same width
                                       self.scl))  # same height

    # sets the bike direction to the next enumerated value, and cycles when it reaches the end (clockwise)
    def turn_right(self):
        v = self.direction.value + 1
        if v > len(self.Direction):
            v = 1
        self.direction = self.Direction(v)

    # sets the bike direction to the previous enumerated value, and cycles when it reaches the end (counter-clockwise)
    def turn_left(self):
        v = self.direction.value - 1
        if v < 1:
            v = len(self.Direction)
        self.direction = self.Direction(v)

    # check if the bike overlaps its line and
    # check if the bike is outside the play area (defined by the x, y, w, h params)
    def check_die(self, x, y, w, h):
        head = self.get_bike()
        # TODO check if line overlaps itself
        if len(self.line_pieces) > self.scl * 2 / self.VEL:
            # for piece in self.line_pieces:
            for piece in bike.get_collision_body():
                if head.overlaps(piece):
                    self.alive = False

        # check if line is outside screen
        if head.x < x or head.x > w - self.scl or head.y < y or head.y > h - self.scl:
            self.alive = False

    # returns true if the bike is overlapping a given square at any point
    # should be used to determine if a given bike should interact with a given powerup
    def use(self, powerup):
        if self.get_bike().overlaps(powerup):
            return True
        return False

    # returns the last Square in line_pieces. For this prototype, that is all a bike is
    def get_bike(self):
        return self.line_pieces[len(self.line_pieces) - 1]

    def get_collision_body(self):
        return self.line_pieces[:len(bike.line_pieces) - math.floor(bike.scl * 2 / bike.VEL / bike.v_multiplier)]

    # print the direction of the bike and positional data (x and y) of all squares
    def print(self):
        print(f"Direction: {self.direction.name} {self.dir_vel[self.direction.value]}")
        for i in range(len(self.line_pieces)):
            print(f"{self.line_pieces[i].x}, {self.line_pieces[i].y}{(' <' if i == 0 else '')}")




# returns a powerup positioned at a random location on the screen
def c_powerup():
    scale = bike.scl * 1.5
    return Square(random.randint(0, int(screen_width - scale + 1)),  # random x
                  random.randint(0, int(screen_height - scale + 1)),  # random y
                  scale,  # 50% larger than the bike
                  scale)  # 50% larger than the bike


# returns a bike of scale 6 positioned at the center of the screen, going RIGHT
def c_bike():
    return Bike(grid_margin + (grid_width - math.ceil(grid_width / 2)) * (grid_cell_scl + grid_margin),
                grid_margin + (grid_height - math.ceil(grid_height/2)) * (grid_cell_scl + grid_margin),
                6, Bike.Direction.RIGHT, bike_color)


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
    for piece in bike.line_pieces:
        pygame.draw.rect(screen, bike.color if bike.alive else R, piece.to_rect())

    timer(time)

    # powerup
    pygame.draw.rect(screen, powerup_color, powerup.to_rect())

    # flip the screen (? not sure why needed ?)
    pygame.display.flip()


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

    # timer in top right corner
def timer(time):
    screen.fill(GRAY, (0, 0, grid_cell_scl * (grid_width + 2), grid_cell_scl * 2 + 2)) 
    screen.blit(text_render(str(time), font, 20, WHITE), ((grid_width * grid_cell_scl) - 10, 0))
# run while not done
done = False

pressed_down = False

first = True
pygame.time.set_timer(USEREVENT+1, 1000)
while not done:
    if(first):
        time = 100
        first = False
    for event in pygame.event.get():

        if event.type == USEREVENT+1:
            time -= 1

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
        timer(56)
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
