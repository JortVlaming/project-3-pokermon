from typing import Tuple, Callable

import pygame

from src.engine.objects.gameObject import GameObject
from src.engine.globals import Globals


class Square(GameObject):
    def __init__(self, x:int, y:int, color: Tuple[int, int, int]|str, width: int, height: int):
        super().__init__(x, y)

        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.update_callback: None | Callable[[Square, list, dict], None] = None

    def set_update(self, function: None|Callable[["Square", list, dict], None]):
        self.update_callback = function

    def update(self, *args, **kwargs):
        if self.update_callback is not None:
            self.update_callback(self, list(args), dict(kwargs))

    def draw(self, *args, **kwargs):
        Globals.get_window().blit(self.image, (self.x, self.y))

    def set_width(self, width: int):
        if width < 0:
            width = 0
        self.width = width
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

    def set_height(self, height: int):
        if height < 0:
            height = 0
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
