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
        PHASE = color.WHITE

    def __init__(self, maxX: int, maxY: int, type: Type):
        self.w = 8
        self.h = 8
        self.x = math.ceil(random.randint(0, maxX - self.w / 2))
        self.y = math.ceil(random.randint(0, maxY - self.h / 2))
        self.type = type
        self.color = self.type.value
        
    def collides(self, bike: b.Bike):
        return self.overlaps(bike.get_leading_edge())