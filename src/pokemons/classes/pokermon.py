import pygame.image

from src.engine.renderer import Renderer


class Pokermon:
    name:str = ""
    hp:int = 0
    max_hp:int = 0
    speed:int = 0
    attack:int = 0
    defense:int = 0
    #       [(class, pp, max)]
    moves = []

    cost = 0

    def __init__(self, image: str):
        img = pygame.image.load(image)
        self.image = img
        self.x = 0
        self.y = 0

    def draw(self, renderer: Renderer):
        renderer.draw_image(self.image, self.x, self.y)
