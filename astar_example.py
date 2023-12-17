## Hayden Feddock
## 12/3/2023

from PIL import Image
from Environment import Environment, img_to_dat
import heuristic
from Coordinate import Coordinate
from astar_search import astar_search

###################### Global Definitions ######################

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# Specify the path to your PNG image
image_path = "test1.png"

# Set the dat filename
dat_filename = 'temp.dat'

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

# Perform the A* search
astar = astar_search(env, Coordinate(start_coordinate), Coordinate(goal_coordinate), heuristic.euclidean_distance)
path = astar.search()

# Write the path to the image in blue
for coord in path:
    x, y, _ = coord.position.getVector()
    image.putpixel((x, y), BLUE)

# Save the resulting output
image.save('output.png')







