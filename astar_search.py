# Hayden Feddock

from Coordinate import Coordinate
from State import State
from Environment import Environment
from typing import Callable
import heapq

## Debugging ##
debug = False
if debug == True:
    from PIL import Image
    BLUE = (0, 0, 255, 255)
    image_path = 'test1.png'
    output_path = 'temp.png'
    img = Image.open(image_path)


class astar_search:
    def __init__(self, env: Environment, start_coords: Coordinate, goal_coords: Coordinate, heuristic: Callable[[Coordinate, Coordinate], float]):
        self.env = env
        self.start_state = State(start_coords, 0, heuristic(start_coords, goal_coords))
        self.goal_coords = goal_coords
        self.heuristic = heuristic

        # TODO: Switch open and closed lists to mapped datatypes for speed
        self.coord_path = []
        self.open_list = []
        self.closed_list = []

    def search(self) -> list[State]:

        # Get the start state and add to the priority queue
        heapq.heappush(self.open_list, self.start_state)

        # Iterate until the open list is empty
        while self.open_list:

            # Get the current state from the priority queue
            current_state = heapq.heappop(self.open_list)
            self.closed_list.append(current_state)

            ## Debugging ##
            if debug == True:
                x = current_state.coordinate.position.x
                y = current_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the current state's coordinates are equal to the goal coordinates
            if current_state.coordinate == self.goal_coords:
                return self.construct_path(current_state)
            
            # Explore the neighboring states
            for neighbor_state in self.env.get_neighbors(current_state, self.goal_coords, self.heuristic):

                # Skip state if it has already been added to the closed list
                if neighbor_state in self.closed_list:
                    continue

                # Add the neighboring states to the open list priority queue if they are not already in it
                # TODO: Update state if the f value is lower
                if neighbor_state not in self.open_list:
                    heapq.heappush(self.open_list, neighbor_state)
        
        return None

    # Construct the coordinate path from the parents of the path states
    def construct_path(self, goal_state: State) -> list[Coordinate]:
        current_state = goal_state
        while current_state:
            self.coord_path.append(current_state.coordinate)
            current_state = current_state.parent
        return self.coord_path

