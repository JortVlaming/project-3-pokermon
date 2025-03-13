from src.pokemons.classes.attack import Attack


class CrossPoison(Attack):
    def __init__(self):
        super().__init__("Cross Poison", 70)