from src.pokemons.classes.attack import Attack


class PoisonFang(Attack):
    def __init__(self):
        super().__init__("Poison Fang", 70)