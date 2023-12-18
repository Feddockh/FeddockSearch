## Hayden Feddock
## 12/3/2023

from PIL import Image
from .core.Environment import Environment, img_to_dat
from .core.heuristic import euclidean_distance
from .core.Coordinate import Coordinate
from .search.astar_search import astar_search
from .search.bidirectional_astar_search import bidirectional_astar_search
import time

###################### Global Definitions ######################

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# Specify the path to your PNG image
image_path = "tests/test1_pose1.png"
dat_filename = "temp_data/temp.dat"
image_out_path = "output/output.png"

###################### Main Function ######################

# Define the image
image = None

try:
    # Open the image using PIL
    image = Image.open(image_path).convert('RGBA')
                
except FileNotFoundError:
    print(f"File not found: {image_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Get the size of the image
image_width, image_height = image.size
print(f"Image dimensions: {image_width}x{image_height} pixels")

# Initialize start and end coordinates
start_coordinate = None
goal_coordinate = None

# Find the start and end coordinates in the image
for y in range(image_height):
    for x in range(image_width):
        pixel_color = image.getpixel((x, y))
        if pixel_color == GREEN:
            start_coordinate = (x, y)
            image.putpixel((x, y), WHITE) # IMPORTANT: Set to white so that it is not included in the cost mapping
        elif pixel_color == RED:
            goal_coordinate = (x, y)
            image.putpixel((x, y), WHITE)

# User output
if start_coordinate is not None:
    print(f"Starting green pixel coordinates: {start_coordinate}")
else:
    print("Starting green pixel not found.")

if goal_coordinate is not None:
    print(f"Ending red pixel coordinates: {goal_coordinate}")
else:
    print("Ending red pixel not found.")

# Create the environment
env = Environment(2, img_to_dat(image, dat_filename))

# Compute average execution time across num_tests
num_tests = 10
trial_times = []
for i in range(num_tests):

    # Initialize search method
    astar = astar_search(env, Coordinate(start_coordinate), Coordinate(goal_coordinate), euclidean_distance)
    # bi_astar = bidirectional_astar_search(env, [Coordinate(start_coordinate)], [Coordinate(goal_coordinate)], euclidean_distance)

    # Record start time
    start_time = time.time()

    # Compute the path
    path = astar.search()
    # path = bi_astar.search()

    # Compute elapsed time
    trial_times.append(time.time() - start_time)

execution_time = sum(trial_times)/num_tests
print(f"The average execution time over {num_tests} trials is {execution_time} seconds.")

# Write the path to the image in blue
for coord in path:
    x, y, _ = coord.position.getVector()
    image.putpixel((x, y), BLUE)

# Save the resulting output
image.save(image_out_path)







