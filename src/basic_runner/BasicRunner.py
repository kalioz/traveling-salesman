from models import Point, Path

import random

class Runner:
    points: list[Point.Point]

    paths: list[Path.Path]

    def __init__(self, points: list[Point.Point]):
        self.points = points
    
    """generate n random paths from the given points"""
    def generate_random_paths(self, n: int):
        self.paths = list()
        for i in range(n):
            points = list(self.points)
            random.shuffle(points)
            path = Path.Path(points=points).untangle_path()
            self.paths.append(path)

    """select the top n contenders of this Runner"""
    def select_top_n(self, n: int):
        self.paths.sort(key=lambda p: p.score())
        return self.paths[:n]

    def select_best(self):
        return self.select_top_n(1)[0]
    
    """generate the children of the current generation"""
    def generate_children(self, keep_top_n=5, children_per_path=3):
        output = self.select_top_n(keep_top_n)
        for i in range(keep_top_n):
            for c in range(children_per_path):
                output.append(output[i].mutate_random())
            output[i].untangle_path()
            # if output[i].intersects():
            #     output+=output[i].mutate_intersect()
        self.paths = output
