import square
import math

from enum import IntEnum, auto

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
        self.line_pieces = [square.Square(x, y, self.scl, self.scl)]
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

        self.line_pieces.append(square.Square(bike.x + (vel_mult[0] * self.VEL * self.v_multiplier),  # new x
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
            for piece in self.get_collision_body():
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
        return self.line_pieces[:len(self.line_pieces) - math.floor(self.scl * 2 / self.VEL / self.v_multiplier)]