import Environment
from PIL import Image
import numpy as np

img_path = "test2.png"

# Open the image using PIL
img = Image.open(img_path).convert('RGBA')

datFile = "test.dat"
e = Environment.img_to_dat(img, datFile)