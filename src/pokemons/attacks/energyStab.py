from src.pokemons.classes.attack import Attack


class EnergyStab(Attack):
    def __init__(self):
        super().__init__("Energy Stab", 60)