import pygame
import color
import square
import random

class PowerUps:
    # def __init__(self, powerupWeight: int, x: int, y: int, c: color):
    #     self.weight = powerupWeight
    #     self.x = x
    #     self.y = y
    #     self.c = c

    @staticmethod
    def speed_powerUp(maxX, maxY):
        return square.Square(random.randint(0, maxX - 3), random.randint(0, maxY - 3), 6, 6)

        # sPowerUp = square.Square(random.randint(0, int(self.x - self.weight + 1)),  # random x
        #     random.randint(0, int(self.y - self.weight + 1)),  # random y
        #     self.weight * 1.5,  # 50% larger than the bike
        #     self.weight * 1.5)  # 50% larger than the bike

        # return sPowerUp

    # def returnColor(self):
    #     return self.c