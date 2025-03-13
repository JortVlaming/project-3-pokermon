from src.pokemons.classes.attack import Attack


class Lunge(Attack):
    def __init__(self):
        super().__init__("Lunge", 80)