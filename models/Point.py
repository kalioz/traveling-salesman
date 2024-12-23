# A Point represent an object on the map.

from dataclasses import dataclass
import math
import functools

@dataclass
class Point:
    x: int
    y: int

    def distance(self, p) -> float:
        return math.dist([self.x, self.y], [p.x, p.y])

    def __hash__(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))