from src.pokemons.classes.attack import Attack


class Tackle(Attack):
    def __init__(self):
        super().__init__("Tackle", 40)