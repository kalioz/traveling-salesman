from src import basic_runner, visualizer_matplotlib
from models import Point
import time

import random

NUMBER_OF_POINTS=100
X_MAX=1000
Y_MAX=1000

NUMBER_OF_ITERATIONS=10000
STOP_AFTER_N_STALE=50
NUMBER_OF_PATHS_MAX=200
KEEP_TOP_N=3

def main():
    # generate random points
    points = []
    while len(points) < NUMBER_OF_POINTS:
        point = Point.Point(x=random.randint(0, X_MAX), y=random.randint(0, Y_MAX))
        # ensure the points generated are distincts
        if point not in points:
            points.append(point)

    print("Number of points: ", len(set(points)))
    print("Generating first random paths... this may take a while")
    runner = basic_runner.BasicRunner.Runner(points)
    runner.generate_random_paths(NUMBER_OF_PATHS_MAX)
    visualizer = visualizer_matplotlib.MatplotLibVisualizer(maxX=X_MAX, maxY=Y_MAX, path = runner.select_top_n(1)[0])

    print("first random paths generated")

    best_distance = runner.select_best().distance()
    n_stale = 0

    for _ in range(NUMBER_OF_ITERATIONS):
        local_best_distance=runner.select_best().distance()
        print("Current best distance :", local_best_distance)
        if local_best_distance == best_distance:
            n_stale+=1
            if n_stale > STOP_AFTER_N_STALE:
                break
        else:
            best_distance = local_best_distance
            n_stale = 0
        runner.generate_children(KEEP_TOP_N, int(NUMBER_OF_PATHS_MAX/KEEP_TOP_N))

    best_run = runner.select_best()

    print("best distance achieved:", best_run.distance())
    print("path intersects ? ", best_run.intersects())

    visualizer = visualizer_matplotlib.MatplotLibVisualizer(maxX=X_MAX, maxY=Y_MAX, path = best_run)
    visualizer.visualize()
        
if __name__ == "__main__":
    main()