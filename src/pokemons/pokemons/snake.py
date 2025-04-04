import pygame.transform

from src.pokemons.attacks.bombThrow import BombThrow
from src.pokemons.attacks.coil import Coil
from src.pokemons.attacks.explosion import Explosion
from src.pokemons.attacks.poisonFang import PoisonFang
from src.pokemons.classes.pokermon import Pokermon


class Snake(Pokermon):
    def __init__(self):
        super().__init__("assets/snek.png")

        self.name = "Snek"
        self.max_hp = 160
        self.hp = self.max_hp
        self.speed = 140
        self.attack = 170
        self.cost = 3

        self.moves = [
            [PoisonFang(), 10, 10],
            [BombThrow(), 10, 10],
            [Explosion(), 1, 1],
            [Coil(), 10, 10],

        ]


        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))