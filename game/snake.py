from game.node import Node
from game.data_objects import Vector, add_vectors, scalar_mult

class Snake(Node):
    body: list[Vector]
    size: int
    direction: Vector
    last_direction: Vector

    def __init__(self, head=Vector(3, 2), tail=Vector(2, 2), direction=Vector(1, 0)):
        self.body = []
        self.direction = direction
        self.last_direction = scalar_mult(direction, -1)
        self.initialize_body(head, tail)

    def initialize_body(self, head, tail):
        oy = head.y
        ox = tail.x
        for x in range(head.x, tail.x, -1 if head.x >= tail.x else 1):
            self.body.append(Vector(x=x, y=oy))
        for y in range(oy, tail.y, -1 if oy >= tail.y else 1):
            self.body.append(Vector(x=ox, y=y))
        self.body.append(tail)
        self.size = len(self.body)

    def head(self) -> Vector:
        return self.body[0]

    def tail(self) -> Vector:
        return self.body[len(self.body) - 1]

    def change_direction(self, new_direction: Vector):
        if not new_direction == self.last_direction:
            self.direction = new_direction
    
    def get_next_location(self) -> Vector:
        return add_vectors(self.head(), self.direction)

    def move(self):
        to_keep = self.body[:-1] if self.size == len(self.body) else self.body
        self.body = [self.get_next_location()] + to_keep
        self.last_direction = scalar_mult(self.direction, -1)

    def grow(self):
        self.size = self.size + 1
