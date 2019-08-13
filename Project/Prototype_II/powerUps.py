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
    # def __init__(self, powerupWeight: int, x: int, y: int, c: color):
    #     self.weight = powerupWeight
    #     self.x = x
    #     self.y = y
    #     self.c = c

    def __init__(self, maxX: int, maxY: int, type: Type):
        self.w = 8
        self.h = 8
        self.x = math.ceil(random.randint(0, maxX - self.w / 2))
        self.y = math.ceil(random.randint(0, maxY - self.h / 2))
        self.type = type
        self.color = self.type.value

        # sPowerUp = square.Square(random.randint(0, int(self.x - self.weight + 1)),  # random x
        #     random.randint(0, int(self.y - self.weight + 1)),  # random y
        #     self.weight * 1.5,  # 50% larger than the bike
        #     self.weight * 1.5)  # 50% larger than the bike

        # return sPowerUp
    def collides(self, bike: b.Bike):
        return self.overlaps(bike.get_leading_edge());

    # def returnColor(self):
    #     return self.c