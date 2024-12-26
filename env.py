from carClass import Car
from helper import pointWithinGrid
from typing import List, Tuple
import numpy as np
import logging

envLogger = logging.getLogger("envLog")
envLogger.setLevel(logging.DEBUG)
if not envLogger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    envLogger.addHandler(console_handler)
envLogger.disabled = True

class GridWorld:
    '''
    * Contains a 6 * 6 grid world with x-y axis, starting from top left corner (0,0) to bottom right corner (5, 5) 
        with one exit at (5, 3) which is row 5, column 3
    * The GridWorld class can contain multiple car objects
    * 0 means uninitialized, 1 for goal car, others for different cars
    '''
    def __init__(self):
        self.grid = []
        self.normalCarCounter = 2
        self.goalCarCounter = 0
        self.initGrid()
        
    def initGrid(self):
        self.grid = np.zeros((6, 6), dtype=int)
        
    def insertCar(self, car: Car):
        '''
        * starting point - the coordination of thew starting point, tuple of two ints, from (0, 0) to (5, 5)
        * carLen - the length of the car, has to be two or three
        * orientation - orientation of the car, can be either vertical or horizontal, 1 for vertical, 0 for horizontal
        * upDownLeftRight - 1 for up or right, 0 for down or left, depends on the orientation
        '''
        if not pointWithinGrid(car.startingPoint[0], car.startingPoint[1]):
            envLogger.debug(f"Invalid starting point {car.startingPoint}")
            return 1
        
        if car.carLen != 2 and car.carLen != 3:
            envLogger.debug(f"Invalid carLen {car.carLen}, need to be 2 or 3")
            return 1
        
        if car.orientation != 0 and car.orientation != 1:
            envLogger.debug(f"Invalid Orientation {car.orientation}, 0 for horizontal, 1 for vertical")
            return 1
        
        if car.upDownLeftRight != 0 and car.upDownLeftRight != 1:
            envLogger.debug(f"Invalid upDownLeftRight {car.upDownLeftRight}, 1 for up or left, 0 for down or right")
            return 1
        
        insertVal = self.normalCarCounter
        if car.goalCar:
            insertVal = 1 # 1 is reserved for the goal car

        rowNum = car.startingPoint[0]
        columNum = car.startingPoint[1]
        for i in range(car.carLen):
            if not pointWithinGrid(rowNum, columNum):
                envLogger.debug(f"Going to insert at invalid point {(rowNum, columNum)}, out of the grid world")
                return 1
            gridVal = self.grid[rowNum][columNum]
            if gridVal != 0:
                envLogger.debug(f"Invalid position {(rowNum, columNum)}, it already has nonzero value {gridVal} and trying to insert {self.normalCarCounter}")
                return 1
            
            self.grid[rowNum][columNum] = insertVal

            if car.orientation == 1: # vertical
                if car.upDownLeftRight == 1: # up
                    rowNum -= 1
                elif car.upDownLeftRight == 0: # down
                    rowNum += 1
            elif car.orientation == 0: # horizontal
                if car.upDownLeftRight == 1: # right
                    columNum += 1
                elif car.upDownLeftRight == 0: # left
                    columNum -= 1
        return 0
    
    def insertNormalCar(self, car: Car):
        error = self.insertCar(car)
        self.normalCarCounter += 1
        return error
    
    def insertGoalCar(self, car: Car):
        if self.goalCarCounter != 0:
            envLogger.debug("Can't insert more than 1 goal car")
            return 1
        error = self.insertCar(car)
        self.goalCarCounter += 1
        return error
    
    def generateGrid(self, cars: Tuple[Car]):
        self.initGrid()
        error = 0
        for car in cars:
            if car.goalCar:
                error = self.insertGoalCar(car)
            else:
                error = self.insertNormalCar(car)
            if error:
                envLogger.debug("Grid Generation Failed")
                return 1
        return 0

    def printGrid(self):
        for row in self.grid:
            print(row)
        print("\n_________________________\n")