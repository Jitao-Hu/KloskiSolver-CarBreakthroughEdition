import numpy as np

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
# a goal car starts at row 4, column 3, length of 2, vertically grows down
startingPoint = [[4, 3]]
carLen = [2]
orientations = [1]
upDownLeftRight = [0]
goalCar = [1]
goalCars = [Car(startingPoint[0], carLen[0], orientations[0], upDownLeftRight[0], goalCar[0])]

# Convert list of cars to tuple for hashing
start_cars = tuple(startCars) 
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
outputDir = "grid_steps"
visualizeSteps(grids, outputDir)
print(f"Images saved in '{outputDir}' directory.")