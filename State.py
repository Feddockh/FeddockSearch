# Hayden Feddock

from Coordinate import Coordinate

# Define the state class
class State:
    def __init__(self, coordinate: Coordinate, g: int, h: float, parent: object = None) -> None:
        self.coordinate = coordinate
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent
    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.coordinate == other.coordinate
        raise ValueError("Comparison with objects of different types is not permitted")
    def __lt__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.f < other.f
        raise ValueError("Comparison with objects of different types is not permitted")
    def __gt__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.f > other.f
        raise ValueError("Comparison with objects of different types is not permitted")


