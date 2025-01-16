from game.data_objects import Vector, Tile, CurrentGameState
from game.snake import Snake
from enum import Enum
from random import randint
from abc import ABC, abstractmethod

class FoodGenerator(ABC):
    @abstractmethod
    def next(self, tiles: list[list[int]], count=0) -> Vector:
        pass

class RandomGenerator(FoodGenerator):
    def next(self, tiles: list[list[int]]) -> Vector:
        new_food = self.random_vector(len(tiles[0])-1, len(tiles)-1)
        if tiles[new_food.y][new_food.x] == Tile.EMPTY:
            return new_food
        else:
            return self.next(tiles)
        
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

    def game_won(self) -> bool:
        for i in self.tiles:
            for j in i:
                if j == Tile.EMPTY:
                    return False
        return True

    def add_snake(self, snake: Snake):
        self.snake = snake
        for body_location in snake.body:
            self.tiles[body_location.y][body_location.x] = Tile.SNAKE

    def update(self) -> CurrentGameState:
        next = self.snake.get_next_location()
        if next.y < 0 or next.y >= len(self.tiles):
            return CurrentGameState.LOSS
        if next.x < 0 or next.x >= len(self.tiles[0]):
            return CurrentGameState.LOSS

        tile_type = self.tiles[next.y][next.x]

        if tile_type == Tile.SNAKE:
            return CurrentGameState.LOSS

        if tile_type == Tile.FOOD:
            self.snake.grow()
            self.score = self.score + 1
            if self.game_won():
                return CurrentGameState.WIN
            new_food = self.food_generator.next(self.tiles)
            self.tiles[new_food.y][new_food.x] = Tile.FOOD
        
        self.snake.move()
        self.reset_board()
        return CurrentGameState.PLAYING

    def reset_board(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if not self.tiles[y][x] == Tile.FOOD:
                    self.tiles[y][x] = Tile.EMPTY
        for body_segment in self.snake.body:
            self.tiles[body_segment.y][body_segment.x] = Tile.SNAKE

    def add_food(self, location: Vector):
        self.tiles[location.y][location.x] = Tile.FOOD
