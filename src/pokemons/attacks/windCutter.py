from src.pokemons.classes.attack import Attack


class WindCutter(Attack):
    def __init__(self):
        super().__init__("Wind Cutter", 80)