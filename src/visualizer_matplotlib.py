from models import Visualizer
from dataclasses import dataclass

import matplotlib.pyplot as plt

@dataclass
class MatplotLibVisualizer(Visualizer.Visualizer):
    def visualize(self):
        if self.points is not None:
            points = [(point.x, point.y) for point in self.points]
        elif self.path is not None:
            points = [(point.x, point.y) for point in self.path.points]
        else:
            raise Exception("either path or points needs to be defined")

        # add first point at last position to draw a perfect size
        points.append(points[0])

        # Unpack the points into separate x and y lists
        x, y = zip(*points)

        # Create the plot
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        
        plt.title('Best path generated')
        # plt.xlabel('X-axis')
        # plt.ylabel('Y-axis')

        # Mark the points with a scatter plot
        plt.scatter(x, y, color='red', label='Points')

        # Add grid and legend for clarity
        # plt.grid(True)
        # plt.legend()

        # Save the image to a file
        plt.savefig('points_image.png')

        # Display the plot
        plt.show()

        print(len(set(points)))
