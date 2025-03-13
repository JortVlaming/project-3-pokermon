from src.pokemons.classes.attack import Attack


class FeintAttack(Attack):
    def __init__(self):
        super().__init__("Feint Attack", 60)