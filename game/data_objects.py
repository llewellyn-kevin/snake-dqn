class Vector:
    x: int = 0
    y: int = 0


    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def __str__(self):
        return '<{}, {}>'.format(self.x, self.y)


    def __eq__(self, o):
        if not isinstance(o, Vector):
            return NotImplemented

        return self.x == o.x and self.y == o.y


def add_vectors(a: Vector, b: Vector) -> Vector:
    return Vector(a.x + b.x, a.y + b.y)
