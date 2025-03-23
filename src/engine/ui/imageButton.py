import pygame

from src.engine.renderer import Renderer
from src.engine.ui.button import Button


class ImageButton(Button):
    def __init__(self, x:int, y:int, image:str|pygame.Surface, image_scale:float=1.0, **kwargs):
        if isinstance(image, pygame.Surface):
            self.image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))
        else:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * image_scale, self.image.get_height() * image_scale))

        super().__init__(x, y, self.image.get_width(), self.image.get_height())


    def draw(self, renderer: Renderer):
        renderer.draw_image(self.image, self.x, self.y)