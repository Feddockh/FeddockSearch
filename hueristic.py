# Hayden Feddock

from Coordinate import Coordinate
from math import sqrt

# Hueristic function (Euclidean distance)
def heuristic(start: Coordinate, end: Coordinate) -> float:
    return sqrt((end.x - start.x)**2 + (end.y - start.y)**2)