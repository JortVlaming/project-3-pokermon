from src.pokemons.classes.attack import Attack


class DoubleKick(Attack):
    def __init__(self):
        super().__init__("Double Kick", 60)