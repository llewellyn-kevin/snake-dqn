from abc import abstractmethod


class Node:
    @abstractmethod
    def process(self, delta):
        pass


    @abstractmethod
    def render(self):
        pass
