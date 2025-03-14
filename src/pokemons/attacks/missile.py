from src.pokemons.classes.attack import Attack


class Missile(Attack):
    def __init__(self):
        super().__init__("Missile", 70)