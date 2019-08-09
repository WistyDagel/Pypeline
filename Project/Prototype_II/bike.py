import color
import square

import math
from enum import IntEnum

class Bike:
    # represents each of the 4 possible directions the bike may go
    # This is here because the bike should know it's own state of direction
    class Direction(IntEnum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

        # returns x-y speed multipliers
        def get_multipliers(self):
            # values used to multiply to x and y speed, corresponding with the Direction(Enum) value
            # example: dir_vel[1] -> 0 * vel (x), 1 * vel (y). Effective direction: Down
            dir_vel = (
                (1, 0),  # Right (0)
                (0, 1),  # Down (1)
                (-1, 0),  # Left (2)
                (0, -1),  # Up (3)
            )
            return dir_vel[self.value]

    """
    :param x - the x position of the bike at the start of the game
    :param y - the y position of the bike at the start of the game
    :param scl - the size of each Piece of the line (scale)
    :param direction - the Direction that the bike will be going at the start of the game
    """
    def __init__(self, x: int, y: int, direction: Direction, color = color.WHITE):
        self.weight = 6  # weight - the width and height of each square at it's lowest point
        self.SPD = 1  # speed - hard-coded to 1 pixel per frame
        self.s_multiplier = 1 # speed modifier for when the bike slows down  
        self.alive = True  # used to quickly check the status of the bike
        self._turn = False  # used to determine if a new rectangle should be inserted into the list
        
        self.line_pieces = [square.Square(x, y, self.weight, self.weight)]
        self.direction = direction
        self.color = color

    # appends a new Square to the end of the line_pieces. The x and y of the new Square are the previous Square's
    # x and y plus the bike's directional speed
    def move(self):
        bike = self.get_bike()
        spd_mult = self.direction.get_multipliers()  # speed multipliers (x, y)
        dir_val = self.direction.value

        if self._turn != 0:
            x = bike.x + bike.w #- self._dX(self.turn, dir_val, bike.w)
            y = bike.y + bike.h #- self._dY(self.turn, dir_val, bike.h)
            if self._turn == 1:  # clockwise rotation of direction
                if dir_val == 0:  # RIGHT
                    x = x - 0
                    y = y - bike.h
                if dir_val == 1:  # DOWN
                    x = x - self.weight
                    y = y - 0
                if dir_val == 2:  # LEFT
                    x = x - bike.w
                    y = y - self.weight
                if dir_val == 3:  # UP
                    x = x - bike.w
                    y = y - self.weight
            else:  # counter-clockwise rotation of direction (must be -1)
                if dir_val == 0:
                    x = x - 0
                    y = y - self.weight
                if dir_val == 1:
                    x = x - bike.w
                    y = y - 0
                if dir_val == 2:
                    x = x - self.weight
                    y = y - bike.h
                if dir_val == 3:
                    x = x - self.weight
                    y = y - bike.h

            w = abs(spd_mult[1]) * self.weight
            h = abs(spd_mult[0]) * self.weight
                
            
            self.line_pieces.append(square.Square(x, y, w, h))
            # self.line_pieces.insert(0, square.Square(x, y, w, h))
                                       
            self._turn = 0
        else:
            if dir_val > 1:
                bike.x = bike.x + (spd_mult[0] * self.eff_spd())
                bike.y = bike.y + (spd_mult[1] * self.eff_spd())
            bike.w = bike.w + (spd_mult[0] * self.eff_spd() * (-1 if dir_val > 1 else 1))
            bike.h = bike.h + (spd_mult[1] * self.eff_spd() * (-1 if dir_val > 1 else 1))


    # sets the direction to the Direction of value + index % 4 
    # when calling this method, you MUST specify which direction to cycle through the enum, 
    # using -1 for left and 1 for right. 0 is not allowed
    def turn(self, value: int):
        if not value == -1 and not value == 1:
            raise ValueError('value must be -1 or 1')
        self._turn = value
        self.direction = self.Direction((self.direction.value + self._turn) % len(self.Direction))

    # check if the bike overlaps its previous squares and
    # check if the bike is outside the play area (defined by the x, y, w, h params)
    def check_die(self, x, y, w, h):
        bike = self.get_bike()
        for sq in self.get_line():
            if bike.overlaps(sq):
                self.alive = False
                break

        # check if square is outside screen
        if bike.x < x or bike.x + bike.w > w or bike.y < y or bike.y + bike.h > h:
            self.alive = False

    # returns true if the bike is overlapping a given square at any point
    # should be used to determine if a given bike should interact with a given powerup
    def use(self, powerup):
        if self.get_bike().overlaps(powerup):
            return True
        return False

    # returns the last Square in line_pieces
    def get_bike(self):
        return self.line_pieces[-1]
        # return self.line_pieces[0]
    
    def get_line(self):
        return self.line_pieces[0:-1]
        # return self.line_pieces[1:0]  # BROKEN

    def eff_spd(self):
        return self.SPD * self.s_multiplier
