## Hayden Feddock
## 12/3/2023

from PIL import Image
from astar_search import astar_search

###################### Global Definitions ######################

# Colors
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)


###################### Main Function ######################

# Specify the path to your PNG image
image_path = "test1.png"

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
start_coordinates = None
goal_coordinates = None

# Find the start and end coordinates in the image
for y in range(image_height):
    for x in range(image_width):
        pixel_color = image.getpixel((x, y))
        if pixel_color == GREEN:
            start_coordinates = (x, y)
        elif pixel_color == RED:
            goal_coordinates = (x, y)

if start_coordinates is not None:
    print(f"Starting green pixel coordinates: {start_coordinates}")
else:
    print("Starting green pixel not found.")

if goal_coordinates is not None:
    print(f"Ending red pixel coordinates: {goal_coordinates}")
else:
    print("Ending red pixel not found.")

# Call the A* search algorithm
img_out = image.copy()
path = astar_search(img_out, start_coordinates, goal_coordinates)

# Save the resulting output
img_out.save('output.png')







