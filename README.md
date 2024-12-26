# Game Rules
The game rule is similar to Kloski. Each block can be treated as a car and the goal is to move the cars such that the goal car (red) can leave from the exit.
The starting state could vary in the number and arrangement of blocks, and the following graph is just an illustration.
## Rules
* The red block is the goal car
* The purple, blue, and orange blocks are other cars
* Cars in vertical orientation can only be moved vertically (up or down), and cars in horizontal can only be moved horizontally (left or right)
* Yellow and red cars are in vertical orientation
* Blue and purple cars are in horizontal orientation
* Cars can not overlap with each other (no car crushes!)
* The game ends if the red car can leave from the exit.

## Starting state:
![puzzle](https://github.com/user-attachments/assets/5d460cea-5b3a-41ca-9913-f2436bbcd5f8)

## Step 1
![3681735239347_ pic](https://github.com/user-attachments/assets/267b3815-bfbf-4901-a0bd-65811ebda89a)

## Step 2
![3691735239423_ pic](https://github.com/user-attachments/assets/d7ad82af-20e9-481f-99ad-a7820cf34216)

## Step 3 / End State
![3701735239492_ pic](https://github.com/user-attachments/assets/a309de5c-f7b6-4dcf-96ab-476488c83e9c)


# Solver
A representation of this game is implemented and the A* algorithm is applied to solve for the solution.

# Sample Usage
TBD

# Context
A small and nerdy project inspired by my cousin's Christmas gift.
Open to discuss and chat :)
