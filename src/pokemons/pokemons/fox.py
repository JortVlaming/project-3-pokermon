import pygame.transform

from src.pokemons.attacks.bite import Bite
from src.pokemons.attacks.bladeHat import BladeHat
from src.pokemons.attacks.doubleKick import DoubleKick
from src.pokemons.classes.pokermon import Pokermon



class Fox(Pokermon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/Foxie.png")

        self.name = "Foxie"
        self.max_hp = 70
        self.hp = self.max_hp
        self.speed = 170
        self.attack = 160

        self.moves = [

            [Bite(), 10, 10],
            [DoubleKick(), 10, 10],
            [BladeHat(), 10, 10],

        ]



        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))