# Hayden Feddock

import numpy as np
import PIL as Image
import 

# Define Environment class to handle multi-dimensional problems
class Environment:
    def __init__(self, memmap_array: np.memmap, start: State) -> None:
        self.memmap_array = memmap_array
        
    

# Convert known datatype to a memmory mapped dat file
def img_to_dat(img: Image, filename) -> np.memmap:

    # Convert image to grayscale
    grayscale_img = img.convert('L')

    # Convert the grayscale image to a numpy array
    grayscale_array = np.array(grayscale_img)

    # Invert and scale the pixel values to be between 0 (white) and 100 (black)
    scaled_array = 100 - (grayscale_array * 100 / 255)

    # Create the memmap array
    memmap_array = np.memmap(filename, dtype=scaled_array.dtype, mode='w+', shape=scaled_array.shape)

    return memmap_array