import math
import random
import pygame
from enum import *

# color tuples
GRID_BG = (0, 0, 30)
GRID_FG = (0, 0, 70)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

GRID_FG = (0, 0, 30)

# the scale of the grid and distance between cells
grid_scl = 20  # width & height of each grid cell
grid_margin = 3  # must be even for pygame line drawing
grid_width = 60  # 32
grid_height = 30  # 24

print("something")

screen_width = ((grid_margin + grid_scl) * grid_width) + grid_margin
screen_height = ((grid_margin + grid_scl) * grid_height) + grid_margin

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Jeff Snake')


# represents an x and y value on the grid
class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def overlaps(self, piece):
        return True if self.x == piece.x and self.y == piece.y else False


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
    def __init__(self, length: int, x: int, y: int, direction: Direction):
        self.vel = grid_scl + grid_margin

        self.pieces = [Piece(x, y)]
        self.direction = direction

        # for _ in range(length - 1):
        #     self.move()

        self.alive = True
        self.slow = False
        self.add = length - 1
        self.grow_size = 10

        # self.bound_x = bound_x
        # self.bound_y = bound_y

    def move(self):
        head = self.pieces[0]
        tup = self.dir_tuples[self.direction.value]

        self.pieces.insert(0, Piece(head.x + (tup[0] * self.vel), head.y + (tup[1] * self.vel)))
        if self.add == 0:
            self.pieces.pop()
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
        for piece in self.pieces:
            for check in self.pieces:
                if piece is not check:
                    if piece.overlaps(check):
                        self.alive = False

        for piece in self.pieces:
            if piece.x < x_min or piece.x > x_max - grid_scl or piece.y < y_min or piece.y > y_max - grid_scl:
                self.alive = False

    def eat(self, food):
        if self.pieces[0].x == food.x and self.pieces[0].y == food.y:
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
        piece = Piece((random.randint(0, grid_width - 1) * (grid_scl + grid_margin)) + grid_margin,
                 (random.randint(0, grid_height - 1) * (grid_scl + grid_margin)) + grid_margin)
        if not snake.overlap(piece):
            break
    return piece


def c_snake(l):
    return Snake(l, grid_margin, grid_margin, Snake.Direction.RIGHT)


def draw():
    # erase everything
    screen.fill(GRID_BG)

    # grid x
    for i in range(grid_width + 1):
        pygame.draw.line(screen, GRID_FG, (grid_margin/2 + (i * (grid_scl + grid_margin)), 0),
                         (grid_margin / 2 + (i * (grid_scl + grid_margin)), screen_height), grid_margin)

    # grid y
    for i in range(math.floor(screen_height - grid_margin / grid_scl)):
        pygame.draw.line(screen, GRID_FG, (0, grid_margin/2 + (i * (grid_scl + grid_margin))),
                         (screen_width, grid_margin / 2 + (i * (grid_scl + grid_margin))), grid_margin)

    #snake
    for piece in snake.pieces:
        pygame.draw.rect(screen, WHITE if snake.alive else RED, pygame.Rect(piece.x, piece.y, grid_scl, grid_scl))

    # food
    pygame.draw.rect(screen, RED, pygame.Rect(food.x, food.y, grid_scl, grid_scl))

    # flip the screen (?)
    pygame.display.flip()


snake = c_snake(3)
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
        snake.grow()

    # snake.print()

    score = math.floor(len(snake.pieces) / (grid_width * grid_height) * 1000)

    snake.check_die(0, screen_width, 0, screen_height)
    if not snake.alive:
        print(score)
        snake = c_snake(3)

    draw()

    # Pause
    clock.tick(5)

pygame.quit()
