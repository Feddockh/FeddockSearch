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


class bidirectional_astar_search:
    def __init__(self, env: Environment, start_coord_list: list[Coordinate], goal_coord_list: list[Coordinate], heuristic: Callable[[Coordinate, Coordinate], float]):
        self.env = env
        self.heuristic = heuristic
        self.coord_path = []
        self.path_cost = None
        UPDATE_WINDOW = 10 # A smaller update window trades faster processing time for lower optimality

        # Define forward list
        self.forward_open_list = PriorityQueueDictionary()
        self.forward_closed_set = set()

        # Fill the forward open list with states the start coordinate list
        for start_coord in start_coord_list:
            h = min(self.heuristic(start_coord, goal_coord) for goal_coord in goal_coord_list) # Compute the minimum heuristic value across all of the goal states
            start_state = State(start_coord, 0, h)
            self.forward_open_list.push(start_state.coordinate, start_state, start_state.f)

        # Define the backward list
        self.backward_open_list = PriorityQueueDictionary()
        self.backward_closed_set = set()

        # Fill the backward open list with states the goal coordinate list
        for goal_coord in goal_coord_list:
            h = min(self.heuristic(goal_coord, start_coord) for start_coord in start_coord_list) # Compute the minimum heuristic value across all of the start states
            goal_state = State(goal_coord, 0, h)
            self.backward_open_list.push(goal_state.coordinate, goal_state, goal_state.f)

    def search(self) -> list[Coordinate]:

        # Check if the forward and backward open lists are empty
        while not self.forward_open_list.isempty() and not self.backward_open_list.isempty():

            # Get the current forward state, add neighbors to the forward open list, and update the h values of the backward open list
            forward_state = self.search_step(self.forward_open_list, self.forward_closed_set, self.backward_open_list)

            ## Debugging ##
            if debug == True:
                x = forward_state.coordinate.position.x
                y = forward_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the forward state is in the open list for the backward search
            if forward_state.coordinate in self.backward_open_list:
                backward_open_state = self.backward_open_list.get(forward_state.coordinate)
                return self.construct_path(forward_state, backward_open_state)

            # Get the current backward state, add neighbors to the backward open list, and update the h values of the forward open list
            backward_state = self.search_step(self.backward_open_list, self.backward_closed_set, self.forward_open_list)

            ## Debugging ##
            if debug == True:
                x = backward_state.coordinate.position.x
                y = backward_state.coordinate.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if the backward state is in the open list for the forward search
            if backward_state.coordinate in self.forward_open_list:
                forward_open_state = self.forward_open_list.get(backward_state.coordinate)
                return self.construct_path(forward_open_state, backward_state)

    # Step through the search: update the current state, find neighboring states, update hueristic values for the other open list based on the new neighboring states
    def search_step(self, open_list: PriorityQueueDictionary, closed_set: set[State], other_open_list: PriorityQueueDictionary) -> State:

        # Check if the open list is empty
        if open_list.isempty():
            return None
        
        # Check the priority queue for the next state and add to closed list
        current_state = open_list.pop()
        closed_set.add(current_state)

        # Check for neighboring states with h values with respect to the other open list states
        new_states = []
        for neighbor_state in self.env.get_neighbors(current_state, other_open_list.slice(0, min(self.UPDATE_WINDOW, len(other_open_list))), self.heuristic):
            
            # Skip if the state is already in the closed list
            if neighbor_state in closed_set:
                continue

            # Check if the neighboring state is already in the open list
            if neighbor_state.coordinate in open_list:
            
                # If the g value of the neighbor state is lower that that of the state in the open set, then replace the state in the open set
                if neighbor_state.g < open_list.get(neighbor_state.coordinate).g:
                    open_list.push(neighbor_state.coordinate, neighbor_state, neighbor_state.f)

            # If the state does not already exist in the open set then add it
            else:
                open_list.push(neighbor_state.coordinate, neighbor_state, neighbor_state.f)
                new_states.append(neighbor_state)

        # Update the hueristic values of the states in the other open list for every new state
        if new_states != []:
            for i in range(min(self.UPDATE_WINDOW, len(other_open_list))):
                other_state = other_open_list.peek(i)
                other_state.h = min(self.heuristic(other_state.coordinate, new_state.coordinate) for new_state in new_states)
                other_state.f = other_state.g + other_state.h
                other_open_list.push(other_state.coordinate, other_state, other_state.f)

        return current_state
    
    # Construct the coordinate path from the parents of the path states
    def construct_path(self, forward_state: State, backward_state: State) -> list[Coordinate]:

        # Compute the path cost for each and combine
        self.path_cost = forward_state.parent.g + backward_state.g
        
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


