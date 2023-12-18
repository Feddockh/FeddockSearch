# Hayden Feddock

# Position class defined
class Position:
    def __init__(self, x: int, y: int, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
    def getVector(self) -> tuple[int]:
        return (self.x, self.y, self.z)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Position):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        raise ValueError("Comparison with objects of different types is not permitted")
    
# Orientation class defined (represented in quaternions)
class Orientation:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def getVector(self) -> tuple[float]:
        return (self.x, self.y, self.z, self.w)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Orientation):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z) and (self.w == other.w)
        raise ValueError("Comparison with objects of different types is not permitted")

# Coordinate class defined (supports 2, 3, 6, or 7 dimension coordinates)
class Coordinate:
    def __init__(self, args: tuple) -> None:

        # Check if all values in the list are either int or float
        if all(isinstance(val, (int, float)) for val in args):
            
            # Get the length of the list and determine which arguments to store
            self.dim = len(args)
            if self.dim == 2:
                self.position = Position(x=args[0], y=args[1])
                self.orientation = Orientation()
            elif self.dim == 3:
                self.position = Position(x=args[0], y=args[1], z=args[2])
                self.orientation = Orientation()
            elif self.dim == 6:
                self.position = Position(x=args[0], y=args[1], z=args[2])
                self.orientation = Orientation(x=args[3], y=args[4], z=args[5])
            elif self.dim == 7:
                self.position = Position(x=args[0], y=args[1], z=args[2])
                self.orientation = Orientation(x=args[3], y=args[4], z=args[5], w=args[6])
            else:
                raise ValueError("Invalid coordinate dimension")
        else:
            raise ValueError("Invalid argument type for coordinate")

    # Return a tuple with the combined position and orientation vectors
    def getVector(self) -> tuple:
        return self.position.getVector() + self.orientation.getVector()
    
    # Define coordinate equality (true for same position, orientation, and dimension)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coordinate):
            return (self.position == other.position) and (self.orientation == other.orientation) and (self.dim == other.dim)
        raise ValueError("Comparison with objects of different types is not permitted")
    
    def __hash__(self) -> int:
        return hash(self.getVector())
