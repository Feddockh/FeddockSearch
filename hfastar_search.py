# Hayden Feddock

from Coordinate import Coordinate
from State import State
from hueristic import heuristic
from PIL import Image
from astar_search import astar_search
import bisect
import heapq

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

## Healing Fast A* ##
class hfastar_search:
    def __init__(self, img1: Image, img2: Image, start_lst: list, goal_lst: list) -> None:

        self.img1 = img1
        self.img2 = img2
        self.start = Coordinate(start_lst[0], start_lst[1])
        self.goal = Coordinate(goal_lst[0], goal_lst[1])
        h = heuristic(self.start, self.goal)
        s0 = State(self.start, 0, h)
        self.open_list = [s0]
        self.closed_list = []

        # Call the astar search function to get the optimal path for the first img
        astar = astar_search(img1, start_lst, goal_lst)
        self.path = astar.getPath()

    # TODO: Check for if goal state has been covered
    def hfastar(self):

        # Check the trajectory
        current_state = self.start
        i = 1
        while current_state != self.goal:

            # Check if the next state is valid
            x = self.path[i].coordinate.x
            y = self.path[i].coordinate.y
            pixel_color = self.img2.getpixel((x, y))
            if pixel_color == BLACK:

                # If there is an obstacle blocking the path to the next object, find the state on either side of the object
                s1 = self.path[i-1]
                j = i
                while pixel_color == BLACK:
                    j += 1
                    x = self.path[j].coordinate.x
                    y = self.path[j].coordinate.y
                    pixel_color = self.img2.getpixel((x, y))
                s2 = self.path[j]

                # Heal the path


    def healPath(self, s1: State, s2: State) -> list[State]:

        

        # Call recursive search
        return
    

