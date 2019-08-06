import math
import random
import pygame
from enum import *

# color tuples
GRID_BG = (0, 0, 0)
GRID_FG = (40, 140, 160)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

# GRID_FG = GRID_BG

# the scale of the grid and distance between cells
grid_scl = 20  # width & height of each grid cell
grid_margin = 1  # must be even for pygame line drawing
grid_width = 20  # 32
grid_height = 20  # 24

clock_spd = 100  # 10
current_spd = clock_spd
speed_timer = 0

print("something")

screen_width = ((grid_margin + grid_scl) * grid_width) + grid_margin
screen_height = ((grid_margin + grid_scl) * grid_height) + grid_margin

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Jeff Snake')


# represents an x and y value on the grid
class Piece:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def overlaps(self, piece):
        return True if self.x + self.w > piece.x and self.x < piece.x + piece.w and self.y + self.h > piece.y and self.y < piece.y + piece.h else False


# represents a snake object. includes a Direction and Piece[] instance
class Snake:
    # represents each of the 4 possible directions the snake may go
    class Direction(Enum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

    # values used to multiply to x and y values, corresponding with Direction
    dir_tuples = (
        (1, 0),  # Right
        (0, 1),  # Down
        (-1, 0),  # Left
        (0, -1),  # Right
    )

    """
    :param length - determines the size of the list that stores the position of snake Pieces
    :param x - the x position of the end of the tail
    :param y - the y position of the end of the tail
    :param direction - the Direction that the snake will be pointing
    """
    def __init__(self, length: int, x: int, y: int, direction: Direction, scl):
        # self.vel = grid_scl + grid_margin
        self.vel = 1
        self.scl = scl

        self.pieces = [Piece(x, y, self.scl, self.scl)]
        self.direction = direction

        # for _ in range(length - 1):
        #     self.move()

        self.alive = True
        self.slow = False
        self.add = length - 1
        self.grow_size = 50

        # self.bound_x = bound_x
        # self.bound_y = bound_y

    def move(self):
        head = self.pieces[0]
        tup = self.dir_tuples[self.direction.value]

        self.pieces.insert(0, Piece(head.x + (tup[0] * self.vel), head.y + (tup[1] * self.vel), self.scl, self.scl))
        # if self.add == 0:
        #     self.pieces.pop()
        self.add -= (1 if self.add > 0 else 0)

    def turn_right(self):
        v = self.direction.value + 1
        if v > 3:
            v = 0
        self.direction = self.Direction(v)

    def turn_left(self):
        v = self.direction.value - 1
        if v < 0:
            v = 3
        self.direction = self.Direction(v)

    def check_die(self, x_min, x_max, y_min, y_max):
        self.alive = True

        # check if snake overlaps itself
        # for piece in self.pieces:
        #     for check in self.pieces:
        #         if piece is not check:
        #             if piece.overlaps(check):
        #                 self.alive = False

        for piece in self.pieces:
            if piece.x < x_min or piece.x > x_max - self.scl or piece.y < y_min or piece.y > y_max - self.scl:
                self.alive = False

    def eat(self, food):
        if self.head().overlaps(food):
            return True
        return False

    def overlap(self, piece):
        for snake_piece in self.pieces:
            if snake_piece.x == piece.x and snake_piece.y == piece.y:
                return True
        return False

    def head(self):
        return self.pieces[0]

    def grow(self):
        self.add += self.grow_size

    def print(self):
        print(f"Direction: {self.direction.name} {self.dir_tuples[self.direction.value]}")
        for i in range(len(self.pieces)):
            print(f"{self.pieces[i].x}, {self.pieces[i].y}{(' H' if i == 0 else '')}")


def c_food(snake):
    while True:
        scale = snake.scl * 1.5
        food = Piece(random.randint(0, int(screen_width - scale + 1)),
                     random.randint(0, int(screen_height - scale + 1)), scale, scale)
        if not snake.overlap(food):
            break
    return food


def c_snake(l):
    return Snake(l, grid_margin + (grid_width - math.ceil(grid_width/2)) * (grid_scl + grid_margin),
                 grid_margin + (grid_height - math.ceil(grid_height/2)) * (grid_scl + grid_margin), Snake.Direction.RIGHT, 8)


def draw():
    # erase everything
    screen.fill(GRID_BG)

    # grid x
    for i in range(grid_width + 1):
        pygame.draw.line(screen, GRID_FG, (grid_margin/2 + (i * (grid_scl + grid_margin)), 0),
                         (grid_margin / 2 + (i * (grid_scl + grid_margin)), screen_height), grid_margin)

    # grid y
    for i in range(grid_height + 1):
        pygame.draw.line(screen, GRID_FG, (0, grid_margin/2 + (i * (grid_scl + grid_margin))),
                         (screen_width, grid_margin / 2 + (i * (grid_scl + grid_margin))), grid_margin)

    #snake
    for piece in snake.pieces:
        pygame.draw.rect(screen, WHITE if snake.alive else RED, pygame.Rect(piece.x, piece.y, piece.w, piece.h))

    # food
    pygame.draw.rect(screen, RED, pygame.Rect(food.x, food.y, food.w, food.h))

    # flip the screen (?)
    pygame.display.flip()


snake = c_snake(200)
food = c_food(snake)
cut = 0

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.turn_right()
            if event.key == pygame.K_LEFT:
                snake.turn_left()
            if event.key == pygame.K_ESCAPE:
                done = True

    snake.move()


    if snake.eat(food):
        food = c_food(snake)
        current_spd = clock_spd * 2
        speed_timer = 5000
    speed_timer -= 1 if speed_timer > 0 else 0
    if speed_timer == 0:
        current_spd = clock_spd

    # snake.print()

    score = len(snake.pieces)

    snake.check_die(0, screen_width, 0, screen_height)
    if not snake.alive:
        print(score)
        snake = c_snake(200)
        food = c_food(snake)

    draw()

    # Pause
    clock.tick(current_spd)

pygame.quit()
