import pygame.transform

from src.pokemons.attacks.bodySlam import BodySlam
from src.pokemons.attacks.doubleKick import DoubleKick
from src.pokemons.attacks.headbutt import Headbutt
from src.pokemons.attacks.missile import Missile
from src.pokemons.attacks.tackle import Tackle
from src.pokemons.classes.pokermon import Pokermon



class LLama(Pokermon):
    def __init__(self):
        super().__init__("assets/lama.png")

        self.name = "Llllama"
        self.max_hp = 165
        self.hp = self.max_hp
        self.speed = 150
        self.attack = 120
        self.cost = 3

        self.moves = [
            #class, pp, max_pp
            [Tackle(), 10, 10],
            [Headbutt(), 10, 10],
            [DoubleKick(), 10, 10],
            [Missile(), 10, 10],
        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))