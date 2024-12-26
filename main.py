import heapq
import itertools
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os

from typing import List, Tuple
from carClass import *
from env import *
from constants import *


# Adjusted A* function
def a_star(start: Tuple[Car], goal: Tuple[Car], neighbors_func, heuristic_func, distance_func):
    """
    General A* Algorithm.

    Args:
        start: Tuple[Car]: The start state (tuple of cars).
        goal: Tuple[Car]: The goal state (tuple of cars).
        neighbors_func: Function to get neighbors of a state.
        heuristic_func: Function to estimate distance from a state to the goal.
        distance_func: Function to calculate actual distance between two states.

    Returns:
        List: The path from start to goal, or None if no path is found.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_func(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in neighbors_func(current):
            tentative_g_score = g_score[current] + distance_func(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_func(neighbor, goal)

                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Tie-breaking counter
counter = itertools.count()

def a_star(start: Tuple[Car], goal: Tuple[Car], neighbors_func, heuristic_func, distance_func):
    open_set = []
    heapq.heappush(open_set, (0, next(counter), start))  # Priority queue with tie-breaking

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_func(start, goal)}

    visited = []
    gw = GridWorld()
    gw.generateGrid(start)
    visited.append(gw.grid)
    # print(visited)

    while open_set:
        _, _, current = heapq.heappop(open_set)

        currentGw = GridWorld()
        currentGw.generateGrid(current)

        if currentGw.grid[4][3] == 1 and currentGw.grid[5][3] == 1:
            return reconstruct_path(came_from, current)

        for neighbor in neighbors_func(current):
            gw = GridWorld()
            gw.generateGrid(neighbor)
            if not any(np.array_equal(gw.grid, visited_grid) for visited_grid in visited):
                tentative_g_score = g_score[current] + distance_func(current, neighbor)
                visited.append(gw.grid)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_func(neighbor, goal)

                    if neighbor not in [item[2] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], next(counter), neighbor))  # Tie-breaking
    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def neighbors(cars_array: Tuple[Car]):
    result = []
    for index, car in enumerate(cars_array):
        for direction in [0, 1]:  # 0 or 1 for direction
            for steps in range(1, 2):  # Steps of 1
                temp_car = copy.deepcopy(car)  # Clone the car to avoid mutating the original
                temp_car.move(direction, steps)
                temp_cars_array = list(cars_array)
                temp_cars_array[index] = temp_car
                temp_cars_array = tuple(temp_cars_array)  # Convert back to a tuple for hashing

                gw = GridWorld()
                gw.initGrid()
                if gw.generateGrid(temp_cars_array) == 0:  # Check if the grid is valid
                    result.append(temp_cars_array)
    
    return result

def heuristic(cars: Tuple[Car], goal: Tuple[Car]):
    temp_car = None
    goal_car = None
    for car in cars:
        if car.goalCar:
            temp_car = car
    
    for car in goal:
        if car.goalCar:
            goal_car = car
            
    return abs(temp_car.startingPoint[1] - goal_car.startingPoint[1])

def distance(node1, node2):
    # All edges have weight 1
    return 1

startingPoint = [[3,0], [3,1], [3,4],[1, 3]]
carLen = [3, 3, 2, 2]
orientations = [1, 0, 0, 1]
upDownLeftRight = [0, 1, 1, 0]
goalCar = [0, 0, 0, 1]
startCars = []

for i in range(len(startingPoint)):
    startCars.append(Car(startingPoint[i], carLen[i], orientations[i], upDownLeftRight[i], goalCar[i]))

startingPoint = [[4, 3]]
carLen = [2]
orientations = [1]
upDownLeftRight = [0]
goalCar = [1]

goalCars = [Car(startingPoint[0], carLen[0], orientations[0], upDownLeftRight[0], goalCar[0])]

start_cars = tuple(startCars)  # Convert list of cars to tuple for hashing
goal_cars = tuple(goalCars)

path = a_star(start_cars, goal_cars, neighbors, heuristic, distance)

grids = []

if path:
    print("Path found!")
    for step in path:
        gw = GridWorld()
        gw.generateGrid(step)
        grids.append(np.array(gw.grid))
else:
    print("No path found!")

fixed_colormap = {
    0: "white",
    1: "red",
    2: "yellow",
    3: "blue",
    4: "purple"
}

# Function to generate dynamic colors for undefined values
def get_dynamic_colormap(start_index, num_colors):
    cmap = plt.cm.tab20  # Use a colormap with a large number of unique colors
    dynamic_colors = [mcolors.rgb2hex(cmap(i / cmap.N)) for i in range(start_index, start_index + num_colors)]
    return dynamic_colors

# Create a combined colormap for the grids
def create_combined_colormap(grid):
    unique_values = np.unique(grid)
    combined_colormap = {}

    # Assign fixed colors for predefined values
    for val in fixed_colormap:
        combined_colormap[val] = fixed_colormap[val]

    # Assign dynamic colors for the remaining values
    undefined_values = [val for val in unique_values if val not in combined_colormap]
    dynamic_colors = get_dynamic_colormap(0, len(undefined_values))

    for val, color in zip(undefined_values, dynamic_colors):
        combined_colormap[val] = color

    return combined_colormap

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