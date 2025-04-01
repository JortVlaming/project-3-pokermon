from src.pokemons.classes.attack import Attack


class MagicMissile(Attack):
    def __init__(self):
        super().__init__("Magic Missile", 70)