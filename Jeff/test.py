# from pygame import *

# pygame.init()

# win = pygame.display.set_mode((500, 500))

# pygame.display.set_caption("First Game")

"""
 Simple snake example.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

"""
import math
from enum import Enum, auto
import pygame

# --- Globals ---
# Colors
BLACK = (0, 0, 20)
WHITE = (255, 255, 255)
BLUE = (0, 0, 150)
RED = (255, 100, 100)

# Set the width and height of each snake segment
segment_width = 15
segment_height = segment_width
# Margin between each segment
segment_margin = 2

snake_segments = []

# Set initial speed
vel = segment_width + segment_margin
x_change = vel
y_change = 0

slow = False


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(RED if slow else WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def next(self):
        v = self.value + 1
        if v > 3:
            v = 0
        return Direction(v)

    def prev(self):
        v = self.value - 1
        if v < 0:
            v = 3
        return Direction(v)


dir_tuples = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

direction = Direction.RIGHT

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()


# Create an initial snake
def create_snake(length):
    global snake_segments
    snake_segments = []
    for i in range(length):
        x = segment_margin
        y = segment_margin
        segment = Segment(x, y)
        snake_segments.append(segment)
        allspriteslist.add(segment)
        direction = Direction.RIGHT


create_snake(9)

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = direction.next()
                tup = dir_tuples[direction.value]
                x_change = vel * tup[0]
                y_change = vel * tup[1]

            if event.key == pygame.K_LEFT:
                direction = direction.prev()
                tup = dir_tuples[direction.value]
                x_change = vel * tup[0]
                y_change = vel * tup[1]

            if event.key == pygame.K_DOWN:
                slow = True

            if event.key == pygame.K_r:
                head = snake_segments[0]

                snake_segments.clear()
                allspriteslist.empty()

                snake_segments.insert(0, head)
                allspriteslist.add(head)

                x_change = 0
                y_change = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                slow = False




    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    # old_segment = snake_segments.pop()
    # allspriteslist.remove(old_segment)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)

    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    for i in range(math.ceil(800 / segment_width)):
        pygame.draw.line(screen, BLUE, (i * (segment_width + segment_margin), segment_margin/2),
                         (i * (segment_width + segment_margin), 600), segment_margin)

    for i in range(math.ceil(600 / segment_height)):
        pygame.draw.line(screen, BLUE, (segment_margin/2, i * (segment_height + segment_margin)),
                         (800, i * (segment_width + segment_margin)), segment_margin)

    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)

pygame.quit()
