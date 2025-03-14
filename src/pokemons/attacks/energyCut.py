from src.pokemons.classes.attack import Attack


class EnergyCut(Attack):
    def __init__(self):
        super().__init__("Energy Cut", 90)