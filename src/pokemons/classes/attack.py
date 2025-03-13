import random
from math import ceil

from src.engine.logger import warn
from src.pokemons.classes.pokermon import Pokermon


class Attack:
    def __init__(self, name:str, damage:int):
        self.name = name
        self.damage = damage

    def calculate_damage(self, attacker: Pokermon, attacked: Pokermon, do_specials: bool=False) -> int:
        mult = 1
        if do_specials:
            r = int(random.random() * 100)
            if r <= 20:
                warn("Attack misses")
                mult = 0
            elif r <= 80:
                warn("Normal attack")
                mult = 1
            else:
                warn("Critical hit")
                mult = 1.5
        return ceil(ceil(self.damage * (attacker.attack/100) * (1 - (attacked.defense/100))) * mult)