from src.pokemons.classes.attack import Attack


class Explosion(Attack):
    def __init__(self):
        super().__init__("Explosion", 250)