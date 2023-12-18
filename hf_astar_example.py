## Hayden Feddock

from PIL import Image
from core.Environment import Environment, img_to_dat
from core.heuristic import euclidean_distance
from core.Coordinate import Coordinate
from search.astar_search import astar_search
from search.fh_astar_search import fh_astar_search
import time

###################### Global Definitions ######################

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
PINK = (255, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

image1_path = "tests/test1_pose1.png"
image2_path = "tests/test1_pose2.png"
dat1_filename = "temp_data/temp1.dat"
dat2_filename = "temp_data/temp2.dat"
image1_out_path = "output/test1_pose1_out.png"
image2_out_path = "output/test1_pose2_out.png"

###################### Main Function ######################

# Define the images
frame1 = None
frame2 = None

# Open the image using PIL
try:
    frame1 = Image.open(image1_path).convert('RGBA')
    frame2 = Image.open(image2_path).convert('RGBA')       
except FileNotFoundError:
    print(f"File not found")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Get the size of the image
image_width, image_height = frame1.size
print(f"Image dimensions: {image_width}x{image_height} pixels")

# Initialize start and end coordinates
start_coordinate = None
goal_coordinate = None

# Find the start and end coordinates in the image
for y in range(image_height):
    for x in range(image_width):
        pixel_color = frame1.getpixel((x, y))
        if pixel_color == GREEN:
            start_coordinate = (x, y)
            frame1.putpixel((x, y), WHITE) # IMPORTANT: Set to white so that it is not included in the cost mapping
            frame2.putpixel((x, y), WHITE)
        elif pixel_color == RED:
            goal_coordinate = (x, y)
            frame1.putpixel((x, y), WHITE)
            frame2.putpixel((x, y), WHITE)

# User output
if start_coordinate is not None:
    print(f"Starting green pixel coordinates: {start_coordinate}")
else:
    print("Starting green pixel not found.")

if goal_coordinate is not None:
    print(f"Ending red pixel coordinates: {goal_coordinate}")
else:
    print("Ending red pixel not found.")


## OFFLINE PLANNING ##

# Create the environment
env1 = Environment(2, img_to_dat(frame1, dat1_filename))

# Find path for frame1 using A* search
astar = astar_search(env1, Coordinate(start_coordinate), Coordinate(goal_coordinate), euclidean_distance)
init_path = astar.search()

# Write the path for the first frame
for coord in init_path:
    x, y, _ = coord.position.getVector()
    frame1.putpixel((x, y), PINK)
frame1.save(image1_out_path)

## ONLINE PLANNING ##

# Create the environment
env2 = Environment(2, img_to_dat(frame2, dat2_filename))

# Compute average execution time across num_tests
num_tests = 10
astar_trial_times = []
fh_astar_trial_times = []
for i in range(num_tests):

    ## A* Search ##
    astar = astar_search(env2, Coordinate(start_coordinate), Coordinate(goal_coordinate), euclidean_distance)
    astar_start_time = time.time()
    astar_path = astar.search()
    astar_trial_times.append(time.time() - astar_start_time)

    ## Fast Healing A* ##
    fh_astar = fh_astar_search(env2, init_path, euclidean_distance)
    astar_start_time = time.time()
    fh_astar_path = fh_astar.search()
    fh_astar_trial_times.append(time.time() - astar_start_time)

astar_execution_time = sum(astar_trial_times)/num_tests
fh_astar_execution_time = sum(fh_astar_trial_times)/num_tests
print(f"The average execution time of A* over {num_tests} trials is {astar_execution_time} seconds.")
print(f"The average execution time of FHA* over {num_tests} trials is {fh_astar_execution_time} seconds.")

# Write the path for the second frame (FHA* = BLUE, A* = PINK)
for coord in astar_path:
    x, y, _ = coord.position.getVector()
    frame2.putpixel((x, y), PINK)
for coord in fh_astar_path:
    x, y, _ = coord.position.getVector()
    frame2.putpixel((x, y), BLUE)
frame2.save(image2_out_path)




