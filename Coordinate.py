# Hayden Feddock

# Define the coordinate class
class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coordinate):
            return (self.x == other.x) and (self.y == other.y)
        raise ValueError("Comparison with objects of different types is not allowed.")
