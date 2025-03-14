from src.pokemons.classes.attack import Attack


class BombThrow(Attack):
    def __init__(self):
        super().__init__("Bomb Throw", 90)