from game.data_objects import Vector
from game.snake import Snake
from enum import Enum
from random import randint
from abc import ABC, abstractmethod


class Tile(Enum):
    EMPTY = 0
    FOOD = 1
    SNAKE = 2


class FoodGenerator(ABC):
    @abstractmethod
    def next(self, tiles: list[list[int]], count=0) -> Vector:
        pass


class RandomGenerator(FoodGenerator):
    def next(self, tiles: list[list[int]], count=0) -> Vector:
        if count > (len(tiles) * len(tiles[0])):
            return None

        new_food = self.random_vector(len(tiles[0])-1, len(tiles)-1)
        if tiles[new_food.y][new_food.x] == Tile.EMPTY:
            return new_food
        else:
            return self.next(tiles, count+1)
        

    def random_vector(self, w: int, h: int) -> Vector:
        return Vector(x=randint(0, w), y=randint(0, h))


class GameBoard:
    tiles: list[list[int]]
    snake: Snake
    score: int
    food_generator: FoodGenerator


    def __init__(self, width: int, height: int, food_generator: FoodGenerator = RandomGenerator()):
        self.width = width
        self.height = height
        self.tiles = [[Tile.EMPTY] * width for i in range(height)]
        self.score = 0
        self.food_generator = food_generator


    def add_snake(self, snake: Snake):
        self.snake = snake
        for body_location in snake.body:
            self.tiles[body_location.y][body_location.x] = Tile.SNAKE


    def update(self) -> bool:
        next = self.snake.get_next_location()
        if next.y < 0 or next.y >= len(self.tiles):
            return False
        if next.x < 0 or next.x >= len(self.tiles[0]):
            return False
        tile_type = self.tiles[next.y][next.x]
        if tile_type == Tile.SNAKE:
            return False

        if tile_type == Tile.FOOD:
            self.snake.grow()
            self.score = self.score + 1
            new_food = self.food_generator.next(self.tiles)
            if new_food is not None:
                self.tiles[new_food.y][new_food.x] = Tile.FOOD
            # ELSE WIN!
        
        self.snake.move()
        self.reset_board()
        return True


    def reset_board(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if not self.tiles[y][x] == Tile.FOOD:
                    self.tiles[y][x] = Tile.EMPTY
        for body_segment in self.snake.body:
            self.tiles[body_segment.y][body_segment.x] = Tile.SNAKE


    def add_food(self, location: Vector):
        self.tiles[location.y][location.x] = Tile.FOOD
