# Hayden Feddock

from Coordinate import Coordinate
from State import State
from typing import Callable
from itertools import product
import numpy as np
from PIL import Image

MAX_COST = 255

# Define Environment class to handle multi-dimensional problems
class Environment:
    def __init__(self, dim: int, memmap_array: np.memmap) -> None:
        self.dim = dim
        self.memmap_array = memmap_array
        self.offsets = self.get_neighbor_offsets()
    
    # TODO: Update for 6 and 7 dimension orientation offsets
    def get_neighbor_offsets(self) -> list:
        return [offset for offset in product([-1, 0, 1], repeat=self.dim) if not all(o == 0 for o in offset)]

    def get_neighbors(self, current_state: State, goal_coords: Coordinate, heuristic: Callable[[Coordinate, Coordinate], float]) -> list[State]:

        # Define the list of neighbors
        neighbors = []

        # Get the bounds of the memory map array
        bounds = self.memmap_array.shape

        # Get the current coordinate vector
        current_coordinate_vector = current_state.coordinate.getVector()

        # Get the neighboring states
        for offset in self.offsets:

            # Get the new coordinates
            new_coord_vector = tuple(coord + delta for coord, delta in zip(current_coordinate_vector[:self.dim], offset))

            # Check bounds and convert to coordinate objects
            new_coord = None
            if all(0 <= coord < bound for coord, bound in zip(new_coord_vector, bounds)):
                new_coord = Coordinate(new_coord_vector)
            else:
                continue

            # Create the new state and add it to the neighbors list
            # Check the value in the memmory array
            cost = self.memmap_array[new_coord_vector[::-1]] # Reversing tuple because I am addressing the ... z, y, then x value
            if cost != MAX_COST:
                g = current_state.g + cost
                h = heuristic(new_coord, goal_coords)
                new_s = State(new_coord, g, h, current_state)
                neighbors.append(new_s)
        
        return neighbors
    

# Convert known datatype to a memmory mapped dat file
# Make sure any start and goal colors have been blanked
def img_to_dat(img: Image, filename) -> np.memmap:

    # Convert image to grayscale
    grayscale_img = img.convert('L')

    # Convert the grayscale image to a numpy array
    grayscale_array = np.array(grayscale_img)

    # Invert and scale the cost for each pixel to be between 0 (white) and MAX_COST (black)
    scaled_array = MAX_COST - (grayscale_array / 255) * MAX_COST

    # Convert to back to uint8
    uint8_scaled_array = scaled_array.astype(np.uint8)

    # Create the memmap array
    memmap_array = np.memmap(filename, dtype=uint8_scaled_array.dtype, mode='w+', shape=uint8_scaled_array.shape)

    # Write the data into the memmap array
    memmap_array[:] = uint8_scaled_array

    # Flush changes to ensure data is written to disk
    memmap_array.flush()

    return memmap_array