from src.pokemons.classes.attack import Attack


class Gun(Attack):
    def __init__(self):
        super().__init__("Gun", 90)