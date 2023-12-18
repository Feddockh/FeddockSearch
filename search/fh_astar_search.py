# Hayden Feddock

from core.Coordinate import Coordinate
from core.State import State
from core.Environment import Environment
from typing import Callable
from .bidirectional_astar_search import bidirectional_astar_search

## Debugging ##
debug = False
if debug == True:
    from PIL import Image
    BLUE = (0, 0, 255, 255)
    image_path = "test/test1_pose2"
    output_path = "temp_data/temp.png"
    img = Image.open(image_path)

## Fast Healing A* ##
class fh_astar_search:
    def __init__(self, env: Environment, coord_path: list[Coordinate], heuristic: Callable[[Coordinate, Coordinate], float]):
        self.env = env
        self.heuristic = heuristic
        self.coord_path = coord_path
        self.goal_coord = coord_path[len(coord_path)-1]
        self.path_cost = None

    def search(self) -> list[State]:

        # Create a state for the starting and next coordinate
        last_state = State(self.coord_path[0], 0, self.heuristic(self.coord_path[0], self.goal_coord))

        # Move through the path until the goal coordinate is reached
        i = 1
        current_coord = self.coord_path[i]
        while current_coord != self.goal_coord:

            ## Debugging ##
            if debug == True:
                x = current_coord.position.x
                y = current_coord.position.y
                img.putpixel((x, y), BLUE)
                img.save(output_path)
                input("Press button")

            # Check if there is a collision at the current coordinate and continue if not
            if self.env.iscollisionfree(current_coord):

                # Update the last state and current coordinate
                cost = self.env.getCost(current_coord)
                g = last_state.g + cost + 1
                h = self.heuristic(current_coord, self.goal_coord)
                last_state = State(current_coord, g, h, last_state)
                i += 1
                current_coord = self.coord_path[i]
                continue

            # If there is a collision, find the coordinate on both sides of the interuption
            j = i + 1
            while not self.env.iscollisionfree(self.coord_path[j]):
                j += 1
            
            # Plan a path using a bidirectional A* search from the start coordinate to the goal coordinates
            bi_astar = bidirectional_astar_search(self.env, [last_state.coordinate], self.coord_path[j:], self.heuristic)

            # Get a new coordinate path from the bidirectional A*
            new_path = bi_astar.search()
            
            # Fix the coordinate path list
            self.coord_path[i:j] = new_path

            # Update the current coordinate
            current_coord = self.coord_path[i]

            # Update the last state and current coordinate
            cost = self.env.getCost(current_coord)
            g = last_state.g + cost
            h = self.heuristic(current_coord, self.goal_coord)
            last_state = State(current_coord, g, h, last_state)
            i += 1
            current_coord = self.coord_path[i]

        # Set the path cost
        self.path_cost = last_state.g

        return self.coord_path

        
    

