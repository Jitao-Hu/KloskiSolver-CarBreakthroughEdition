from helper import pointWithinGrid
import logging
carLogger = logging.getLogger("carLog")
carLogger.disabled = True

class Car:
    def __init__(self, startingPoint, carLen, orientation, upDownLeftRight, goalCar = 0):
        '''
        * starting point - the coordination of thew starting point, tuple of (row num, col num), from (0, 0) to (5, 5)
        * carLen - the length of the car, has to be two or three
        * orientation - orientation of the car, can be either vertical or horizontal, 1 for vertical, 0 for horizontal
        * upDownLeftRight - 1 for up or right, 0 for down or left, depends on the orientation
        '''
        self.startingPoint = startingPoint
        self.carLen = carLen
        self.orientation = orientation
        self.upDownLeftRight = upDownLeftRight
        self.goalCar = goalCar
    
    def clone(self):
        """
        Create a deep copy of the Car object.
        """
        return Car(
            self.startingPoint,  # Copy the list
            self.carLen,
            self.orientation,
            self.upDownLeftRight,
            self.goalCar
        )
    
    def move(self, direction, steps):
        """
        direction - 1 for up or right, 0 for down or left
        """
        if direction != 1 and direction != 0:
            carLogger.debug(f"Invalid move direction {direction}")
            return 0
        if self.orientation: # vertical
            if direction: # up
                self.startingPoint[0] -= steps
            else: # down
                self.startingPoint[0] += steps
        else:
            if direction: # right
                self.startingPoint[1] += steps
            else:
                self.startingPoint[1] -= steps
        if not pointWithinGrid(self.startingPoint[0], self.startingPoint[1]):
            carLogger.debug(f"Invalid starting point after move: {self.startingPoint}")
            return 0
        return 1