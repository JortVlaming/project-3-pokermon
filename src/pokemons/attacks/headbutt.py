from src.pokemons.classes.attack import Attack


class Headbutt(Attack):
    def __init__(self):
        super().__init__("Headbutt", 70)