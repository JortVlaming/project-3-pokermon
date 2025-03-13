from src.pokemons.classes.attack import Attack


class Bite(Attack):
    def __init__(self):
        super().__init__("Bite", 60)