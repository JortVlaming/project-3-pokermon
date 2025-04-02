from src.pokemons.classes.attack import Attack


class Magic(Attack):
    def __init__(self):
        super().__init__("Magic", 50)