from src.pokemons.classes.attack import Attack


class Peck(Attack):
    def __init__(self):
        super().__init__("Peck", 35)