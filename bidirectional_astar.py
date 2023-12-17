# Hayden Feddock

from Coordinate import Coordinate
from State import State
from hueristic import heuristic
from PIL import Image
import bisect
import heapq

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

class bidirectional_astar:
    def __init__(self, img: Image, start_lst: list, goal_lst: list) -> None:
        self.img = img
        self.start = Coordinate(start_lst[0], start_lst[1])
        self.goal = Coordinate(goal_lst[0], goal_lst[1])
    
    def bidirectional_astar(self):

        # Initialize the open set for the start side
        h = heuristic(self.start, self.goal)
        start_side_open_list = [State(self.start, 0, h)]
        start_side_closed_list = []
        start_side_path = []

        # Initialize the open set for the goal side
        goal_side_open_list = [State(self.goal, 0, h)]
        goal_side_closed_list = []
        goal_side_path = []
        
        # 

    def search_step(self, open_list: list[State], closed_list, other_open_list: list[State]):

        current_state = heapq.heappop(open_list)

        # Check for a meeting point
        if current_state in other_open_list:
            return current_state, True
        
        
        for n in 

