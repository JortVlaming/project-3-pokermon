from src.pokemons.classes.attack import Attack


class HeadSmash(Attack):
    def __init__(self):
        super().__init__("Head Smash", 90)