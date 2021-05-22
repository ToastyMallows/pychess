class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __copy__(self):
        return Coordinate(self.x, self.y)

    def is_valid(self):
        return self.x >= 0 and self.x < 8 and self.y >= 0 and self.y < 8
