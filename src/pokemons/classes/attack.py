from math import ceil

from src.pokemons.classes.pokemon import Pokemon


class Attack:
    def __init__(self, name:str, damage:int):
        self.name = name
        self.damage = damage

    def calculate_damage(self, attacker: Pokemon, attacked: Pokemon) -> int:
        return ceil(self.damage * (attacker.attack/100) * (1 - (attacked.defense/100)))