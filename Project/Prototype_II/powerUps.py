import bike as bike
import pygame
import color as color
import square

class PowerUps:
    def __init__(self, b: bike, x: int, y: int, scl: int, c: color):
        self.scl = scl
        self.b = b
        self.c = c
        self.powerUpSqaure = [square.Square(x, y, self.scl, self.scl)]

    def speed_powerUp(self):
        return self.powerUpSqaure