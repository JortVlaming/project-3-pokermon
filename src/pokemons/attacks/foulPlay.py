from src.pokemons.classes.attack import Attack


class FoulPlay(Attack):
    def __init__(self):
        super().__init__("Foul Play", 90)