from math import ceil

from src.pokemons.classes.pokermon import Pokermon


class Attack:
    def __init__(self, name:str, damage:int):
        self.name = name
        self.damage = damage

    def calculate_damage(self, attacker: Pokermon, attacked: Pokermon) -> int:
        return ceil(self.damage * (attacker.attack/100) * (1 - (attacked.defense/100)))