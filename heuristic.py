# Hayden Feddock

from Coordinate import Coordinate
from math import sqrt

# Euclidean distance heuristic 
def euclidean_distance(start: Coordinate, end: Coordinate) -> float:
    return sqrt(sum((e - s)**2 for s, e in zip(start.getVector(), end.getVector())))