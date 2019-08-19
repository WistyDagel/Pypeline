import pygame
import color
import square
import bike as b

import random
from enum import Enum
import math

class PowerUps(square.Square):
    @staticmethod
    class Type(Enum):
        SPEED = color.GREEN,
        NUKE = color.YELLOW,
        MINE = color.RED,
        PHASE = color.WHITE,
        ACTUALLY_MINE = color.BLACK

    def __init__(self, maxX: int, maxY: int, type: Type):
        self.w = 8
        self.h = 8
        self.x = math.ceil(random.randint(0, maxX - self.w / 2))
        self.y = math.ceil(random.randint(48, maxY - self.h / 2))
        self.type = type
        self.color = self.type.value
    
    @staticmethod
    def apply_to_all(bikes, type):
        if (type is PowerUps.Type.SPEED):
            for bike in bikes:
                bike.s_multiplier = 2.5
        elif (type is PowerUps.Type.NUKE):
            for bike in bikes:
                bike.cut()

    def collides(self, bike: b.Bike):
        if (bike):
            return self.overlaps(bike.get_leading_edge())
        return False