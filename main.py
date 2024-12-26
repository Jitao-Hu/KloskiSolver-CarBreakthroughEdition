import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os

from carClass import *
from env import *
from constants import *
from algorithm import *
from helper import *

# configuration for the initial state in the example
startingPoint = [[3,0], [3,1], [3,4],[1, 3]]
carLen = [3, 3, 2, 2]
orientations = [1, 0, 0, 1]
upDownLeftRight = [0, 1, 1, 0]
goalCar = [0, 0, 0, 1]
startCars = []
for i in range(len(startingPoint)):
    startCars.append(Car(startingPoint[i], carLen[i], orientations[i], upDownLeftRight[i], goalCar[i]))

# configuration for the goal state in the example
startingPoint = [[4, 3]]
carLen = [2]
orientations = [1]
upDownLeftRight = [0]
goalCar = [1]
goalCars = [Car(startingPoint[0], carLen[0], orientations[0], upDownLeftRight[0], goalCar[0])]
start_cars = tuple(startCars)  # Convert list of cars to tuple for hashing
goal_cars = tuple(goalCars)

path = aStar(start_cars, goal_cars, neighbors, heuristic, distance)
grids = []
if path:
    print("Path found!")
    for step in path:
        gw = GridWorld()
        gw.generateGrid(step)
        grids.append(np.array(gw.grid))
else:
    print("No path found!")

# Output directory
output_dir = "grid_steps"
os.makedirs(output_dir, exist_ok=True)

# Visualize each step and save as an image
for i, grid in enumerate(grids):
    # Create a combined colormap for the current grid
    colormap = create_combined_colormap(grid)

    # Map grid values to color indices
    color_grid = np.array([[mcolors.to_rgba(colormap[val]) for val in row] for row in grid])

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(color_grid, extent=[0, 6, 0, 6])

    # Add grid lines
    ax.set_xticks(np.arange(0, 6, 1))
    ax.set_yticks(np.arange(0, 6, 1))
    ax.grid(color="black", linestyle="-", linewidth=1)

    # Remove axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Title for visualization
    title = "init" if i == 0 else f"step{i}"
    ax.set_title(title.capitalize())

    # Save the figure
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    plt.close(fig)

print(f"Images saved in '{output_dir}' directory.")