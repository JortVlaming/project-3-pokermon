from typing import Tuple

import pygame

from src.engine.globals import Globals
from src.engine.ui.button import Button


class TextButton(Button):
    def __init__(self, x:int, y:int, width: int, height: int, color: str|Tuple[int, int, int], text: str, text_color:str|Tuple[int, int, int]="Black"):
        super().__init__(x, y, width, height)

        self.color = color

        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.text = text
        self.text_color = text_color

    def draw(self):
        Globals.get_renderer().screen.blit(self.image, (self.x, self.y))
        text_surface = Globals.get_renderer().font.render(self.text, True, self.text_color)

        x = self.x + self.width/2
        y = self.y + self.height/2

        text_pos = text_surface.get_rect(centerx=x, centery=y)
        Globals.get_renderer().screen.blit(text_surface, text_pos)