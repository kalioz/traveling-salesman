# a Path represent an ensemble of Points, in an ordered set.

from dataclasses import dataclass
import random
import copy

from . import Point

@dataclass
class Path():
    points: list[Point.Point]
    isUntangled: bool = False

    def distance(self) -> float:
        return sum(point.distance(self.points[i+1 if i+1 < len(self.points) else 0]) for i, point in enumerate(self.points))

    """return the score of the current path"""
    def score(self) -> float:
        return self.distance()

    # check if some paths intersects each others
    def intersects(self) -> bool:
        for i in range(1, len(self.points)):
            for j in range(1, len(self.points)):
                if abs(i-j) <= 1:
                    continue
                if segments_intersect(self.points[i], self.points[i-1], self.points[j], self.points[j-1]):
                    return True
        return []

    """mutate the path randomly by moving a point"""
    def mutate_random(self):
        return Path(self.points.copy()).mutate_change_position(random.randint(0, len(self.points) - 1), random.randint(0, len(self.points) - 1))
    
    """mutate the first intersection in the path so that it isn't anymore an intersection. returns the two possible options."""
    def mutate_intersect(self):
        self.isUntangled = False
        # find the first intersection
        for i in range(1, len(self.points)):
            for j in range(1, len(self.points)):
                if abs(i-j) <= 1:
                    continue
                if segments_intersect(self.points[i], self.points[i-1], self.points[j], self.points[j-1]):
                    return [
                        Path(self.points.copy()).inverse_segment(i, j),
                        Path(self.points.copy()).inverse_segment(i, j-1)
                    ]
        return []

    """"exchange the position of the points at index i and j"""
    def mutate_exchange_positions(self, i, j):
        self.isUntangled = False
        self.points[i],self.points[j] = self.points[j],self.points[i]
        return self
    
    """will inverse the segment between [i, j], with both extremities included"""
    def inverse_segment(self, i, j):
        if i > j:
            i,j = j,i
        
        for x in range(1+int(abs(j-i)/2)):
            self.mutate_exchange_positions(i+x, j-x)

        return self

    """mutate the path until there is no segment overlapping each other."""
    def untangle_path(self):
        # if self.isUntangled == True:
        #     return self

        class Found(Exception): pass

        is_tangled = True
        while is_tangled:
            is_tangled = False
            try:
                for i in range(1, len(self.points)):
                    for j in range(i+1, len(self.points)):
                        if abs(i-j) <= 1:
                            continue
                        if segments_intersect(self.points[i], self.points[i-1], self.points[j], self.points[j-1]):
                            x = min(i, j)
                            y = max(i, j)
                            self.inverse_segment(x,y-1)
                            is_tangled = True
                            raise Found
            except Found:
                pass
        self.isUntangled = True
        return self

    """move the point at index i so that it goes to index j.
    note: index j is computed keeping the point at index i.
    """
    def mutate_change_position(self, i, j):
        self.isUntangled = False
        if i > j:
            i, j = j, i
        self.points.insert(j, self.points[i])
        self.points.pop(i)
        return self


def segments_intersect(p1, p2, q1, q2) -> bool:
    """Check if line segment (p1, p2) intersects with line segment (q1, q2)."""
    def ccw(a, b, c):
        """Check if three points are listed in counter-clockwise order."""
        return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))
