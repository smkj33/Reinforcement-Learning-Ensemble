from class_Maze_test import Maze
from functions import RL_model
import numpy as np

for i in range(int(1e2)):
    maze = Maze()
    maze.initDynGoalMaze()
    print(maze.maze, "\n\n")