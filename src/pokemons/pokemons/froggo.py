import pygame.transform

from src.pokemons.attacks.barbBarbrage import BarbBarrage
from src.pokemons.attacks.bodySlam import BodySlam
from src.pokemons.attacks.crossPoison import CrossPoison
from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.attacks.lick import Lick


class Froggo(Pokermon):
    def __init__(self):
        super().__init__("assets/Evil_frog.png")

        self.name = "Froggo"
        self.max_hp = 150
        self.hp = self.max_hp
        self.speed = 150
        self.attack = 120
        self.cost = 3

        self.moves = [
            #class, pp, max_pp
            [Lick(), 10, 10],
            [BodySlam(), 10, 10],
            [BarbBarrage(), 10, 10],
            [CrossPoison(), 10, 10],
        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))