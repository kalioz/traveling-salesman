from dataclasses import dataclass
from .Point import Point
from .Path import Path


@dataclass
class Visualizer:
    maxX: int
    maxY: int

    points: list[Point] = None
    path: Path = None


    def visualize(self):
        raise Exception("Not Implemented")
