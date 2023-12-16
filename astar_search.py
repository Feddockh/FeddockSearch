# Hayden Feddock

from Coordinate import Coordinate
from State import State
from hueristic import heuristic
from PIL import Image
import bisect

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# Recursize function for A* search algorithm
def get_path_astar(img: Image, goal: Coordinate, open_list: list[State], closed_list: list[State], current_path: list[State]) -> list[State]:

    # Check if there is anything in the open list
    if not open_list:
        return None

    # Get the next state to expand from the front of the open list
    s = open_list.pop(0)

    # Add the state to the closed list
    closed_list.append(s)

    # Update the path
    new_path = current_path.copy()
    new_path.append(s)

    # Check if the current state is the goal
    if s.coordinate == goal:
        return new_path
    
    # Update the pixel color to show progress
    pixels = img.load()
    pixels[s.coordinate.x, s.coordinate.y] = BLUE

    # Next coordinates (clockwise)
    next_coordinates = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    # Check for the neighboring states
    for dx, dy in next_coordinates:

        # Get the next coordinate
        x = s.coordinate.x + dx
        y = s.coordinate.y + dy

        # Check if the coordinate is valid
        image_width, image_height = img.size
        if 0 <= x < image_width and 0 <= y < image_height:

            # Check for obstacle
            pixel_color = img.getpixel((x, y))
            if pixel_color != BLACK:

                # Create the coordinate object
                new_coordinate = Coordinate(x, y)
                g = s.g + 1
                h = heuristic(new_coordinate, goal)
                s2 = State(new_coordinate, g, h)

                # Check if the coordinate has already been added to the closed list
                if s2 not in closed_list:

                    # If in the open list, then update state
                    if s2 in open_list:

                        # Find the index of the existing state 
                        idx = open_list.index(s2)

                        # Replace the state in the list if the f value is smaller
                        if s2.f < open_list[idx].f:
                            open_list.pop(idx)
                            bisect.insort_left(open_list, s2)

                    # If not in the open list either, then add the state to the open list
                    else:
                        bisect.insort_left(open_list, s2)
                        pixels[s2.coordinate.x, s2.coordinate.y] = YELLOW
    
    # Recursively call the function
    return get_path_astar(img, goal, open_list, closed_list, new_path)

# A* Search algorithm
def astar_search(img: Image, start_lst: list, goal_lst: list):

    # Intialize the open and closed lists
    start = Coordinate(start_lst[0], start_lst[1])
    goal = Coordinate(goal_lst[0], goal_lst[1])
    h = heuristic(start, goal)
    s0 = State(start, 0, h)
    open_list = [s0]
    closed_list = []

    # Call the recursive search function
    path = get_path_astar(img, goal, open_list, closed_list, [])

    return path