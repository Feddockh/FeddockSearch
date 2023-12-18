# Hayden Feddock

from core.Coordinate import Coordinate
from core.State import State
from core.Environment import Environment
from core.PriorityQueueDictionary import PriorityQueueDictionary
from typing import Callable

## Debugging ##
debug = False
if debug == True:
    from PIL import Image
    BLUE = (0, 0, 255, 255)
    image_path = "test/test1_pose1"
    output_path = "temp_data/temp.png"
    img = Image.open(image_path)


class astar_search:
    def __init__(self, env: Environment, start_coord: Coordinate, goal_coord: Coordinate, heuristic: Callable[[Coordinate, Coordinate], float]):
        self.env = env
        h = heuristic(start_coord, goal_coord)
        self.start_state = State(start_coord, 0, h)
        self.goal_state = State(goal_coord, 0, 0)
        self.heuristic = heuristic

        self.open_list = PriorityQueueDictionary()
        self.closed_set = set() # Set for access in O(n)
        self.coord_path = []
        self.path_cost = None

    def search(self) -> list[State]:

        # Get the start state and add to the priority queue
        self.open_list.push(self.start_state.coordinate, self.start_state, self.start_state.f)

        # Iterate until the open list is empty
        while not self.open_list.isempty():

            # Get the current state from the priority queue
            current_state = self.open_list.pop()
            self.closed_set.add(current_state)

            ## Debugging ##
            if debug == True:
                x = current_state.coordinate.position.x
                y = current_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the current state's coordinates are equal to the goal coordinates
            if current_state == self.goal_state:
                return self.construct_path(current_state)
            
            # Explore the neighboring states
            for neighbor_state in self.env.get_neighbors(current_state, [self.goal_state], self.heuristic):

                # Skip state if it has already been added to the closed list
                if neighbor_state in self.closed_set:
                    continue

                # Check if the neighboring state is already in the open list
                if neighbor_state.coordinate in self.open_list:

                    # If the g value of the neighbor state is lower that that of the state in the open set, then replace the state in the open set
                    if neighbor_state.g < self.open_list.get(neighbor_state.coordinate).g:
                        self.open_list.push(neighbor_state.coordinate, neighbor_state, neighbor_state.f)

                # If the state does not already exist in the open set then add it
                else:
                    self.open_list.push(neighbor_state.coordinate, neighbor_state, neighbor_state.f)
                    
        return None

    # Construct the coordinate path from the parents of the path states
    def construct_path(self, goal_state: State) -> list[Coordinate]:
        self.path_cost = goal_state.g
        current_state = goal_state
        coord_path = []
        while current_state:
            coord_path.append(current_state.coordinate)
            current_state = current_state.parent
        self.coord_path = coord_path[::-1]
        return self.coord_path

