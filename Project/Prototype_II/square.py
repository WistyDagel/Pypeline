import pygame

class Square:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def overlaps(self, other):
        return self.to_rect().colliderect(other.to_rect())