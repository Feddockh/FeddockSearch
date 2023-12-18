# Hayden Feddock

from core.Coordinate import Coordinate
from core.State import State
from core.Environment import Environment
from typing import Callable
import heapq

## Debugging ##
debug = False
if debug == True:
    from PIL import Image
    BLUE = (0, 0, 255, 255)
    image_path = "test/test1_pose1"
    output_path = "temp_data/temp.png"
    img = Image.open(image_path)


# A smaller update window trades processing time for optimality
UPDATE_WINDOW = 10

class bidirectional_astar_search:
    def __init__(self, env: Environment, start_coord_list: list[Coordinate], goal_coord_list: list[Coordinate], heuristic: Callable[[Coordinate, Coordinate], float]):
        self.env = env
        self.heuristic = heuristic
        self.coord_path = []

        # Define forward list
        self.forward_open_list = []
        self.forward_closed_list = []

        # Fill the forward open list with states the start coordinate list
        for start_coord in start_coord_list:
            h = min(self.heuristic(start_coord, goal_coord) for goal_coord in goal_coord_list) # Compute the minimum heuristic value across all of the goal states
            start_state = State(start_coord, 0, h)
            heapq.heappush(self.forward_open_list, start_state)

        # Define the backward list
        self.backward_open_list = []
        self.backward_closed_list = []

        # Fill the backward open list with states the goal coordinate list
        for goal_coord in goal_coord_list:
            h = min(self.heuristic(goal_coord, start_coord) for start_coord in start_coord_list) # Compute the minimum heuristic value across all of the start states
            goal_state = State(goal_coord, 0, h)
            heapq.heappush(self.backward_open_list, goal_state)

    def search(self) -> list[Coordinate]:

        # Check if the forward and backward open lists are empty
        while self.forward_open_list and self.backward_open_list:

            # Get the current forward state, add neighbors to the forward open list, and update the h values of the backward open list
            forward_state = self.search_step(self.forward_open_list, self.forward_closed_list, self.backward_open_list)

            ## Debugging ##
            if debug == True:
                x = forward_state.coordinate.position.x
                y = forward_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the forward state is in the open list for the backward search
            for backward_open_state in self.backward_open_list:
                if forward_state == backward_open_state:
                    return self.construct_path(forward_state, backward_open_state)

            # Get the current backward state, add neighbors to the backward open list, and update the h values of the forward open list
            backward_state = self.search_step(self.backward_open_list, self.backward_closed_list, self.forward_open_list)

            ## Debugging ##
            if debug == True:
                x = backward_state.coordinate.position.x
                y = backward_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the backward state is in the open list for the forward search
            for forward_open_state in self.forward_open_list:
                if backward_state == forward_open_state:
                    return self.construct_path(forward_open_state, backward_state)


    def search_step(self, open_list: list[State], closed_list: list[State], other_open_list: list[State]) -> State:

        # Check if the open list is empty
        if not open_list:
            return None
        
        # Check the priority queue for the next state and add to closed list
        current_state = heapq.heappop(open_list)
        closed_list.append(current_state)

        # Check for neighboring states with h values with respect to the other open list states
        new_states = []
        for neighbor_state in self.env.get_neighbors(current_state, other_open_list[:UPDATE_WINDOW], self.heuristic):
            
            # Skip if the state is already in the closed list
            if neighbor_state in closed_list:
                continue

            # Add neighbor state to open list if it has not been already
            if neighbor_state not in open_list:
                heapq.heappush(open_list, neighbor_state)
                new_states.append(neighbor_state)

        # Update the hueristic values of the states in the other open list for every new state
        if new_states != []:

            for other_state in other_open_list[:UPDATE_WINDOW]:
                other_state.h = min(self.heuristic(other_state.coordinate, new_state.coordinate) for new_state in new_states)
                other_state.f = other_state.g + other_state.h

            # Rebuild the heap
            heapq.heapify(other_open_list)

        return current_state
    
    # Construct the coordinate path from the parents of the path states
    def construct_path(self, forward_state: State, backward_state: State) -> list[Coordinate]:
        
        # Unravel the forward states first
        current_state = forward_state
        forward_coord_path = []
        while current_state:
            forward_coord_path.append(current_state.coordinate)
            current_state = current_state.parent

        # Unravel the backward states next
        current_state = backward_state
        backward_coord_path = []
        while current_state:
            backward_coord_path.append(current_state.coordinate)
            current_state = current_state.parent

        # Join the state lists in front to back order
        self.coord_path = forward_coord_path[::-1] + backward_coord_path[1::]

        return self.coord_path


