from src.pokemons.classes.attack import Attack


class BugBite(Attack):
    def __init__(self):
        super().__init__("Bug Bite", 60)