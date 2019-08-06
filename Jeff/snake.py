import pygame
from enum import *

# color tuples
GRID_BG = (0, 0, 50)
GRID_FG = (0, 0, 70)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

# the scale of the grid and distance between cells
grid_scl = 20
grid_margin = 2

pygame.init()

screen = pygame.display.set_mode([800, 600])

pygame.display.set_caption('Jeff Snake')


# represents an x and y value on the grid
class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# represents a snake object. includes a Direction and Piece[] instance
class Snake:
    # represents each of the 4 possible directions the snake may go
    class Direction(Enum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

    # values used to multiply to x and y values, corresponding with Direction
    dir_tuples = [
        (1, 0),  # Right
        (0, 1),  # Down
        (-1, 0),  # Left
        (0, -1),  # Right
    ]

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

        for _ in range(length - 1):
            self.move(False)

    def move(self, pop: bool):
        head = self.pieces[0]
        tup = self.dir_tuples[self.direction.value]

        self.pieces.insert(0, Piece(head.x + (tup[0] * self.vel), head.y + (tup[1] * self.vel)))
        if pop:
            self.pieces.pop()

    def turn_right(self):
        v = self.direction.value + 1
        if v > 4:
            v = 1
        self.direction = self.Direction(v)

    def turn_left(self):
        v = self.direction.value - 1
        if v < 1:
            v = 4
        self.direction = self.Direction(v)

    def print(self):
        print(f"Direction: {self.direction.name} {self.dir_tuples[self.direction.value]}")
        for i in range(len(self.pieces)):
            print(f"{self.pieces[i].x}, {self.pieces[i].y}{(' H' if i == 0 else '')}")


def draw():
    # Erase everything
    screen.fill(GRID_BG)

    

    # Flip the screen (?)
    pygame.display.flip()


snake = Snake(4, grid_margin, grid_margin, Snake.Direction.RIGHT)
snake.print()

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

    snake.move(True)
    draw()

    # Pause
    clock.tick(5)

pygame.quit()
