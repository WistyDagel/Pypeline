from enum import *


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

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


d = Direction.UP
print(d)

for i in range(10):
    d = d.next()
    print(d)

