import random
from functools import lru_cache

from src.pokemons.pokemons.duck import Ducky
from src.pokemons.pokemons.eagle import Eagle
from src.pokemons.pokemons.fox import Fox
from src.pokemons.pokemons.froggo import Froggo
from src.pokemons.pokemons.llama import LLama
from src.pokemons.pokemons.racoon import Racoon
from src.pokemons.pokemons.snake import Snake
from src.pokemons.pokemons.spider import Spider
from src.pokemons.pokemons.turtles import Turtles
from src.pokemons.pokemons.whooper import Whooper


@lru_cache
def get_all():
    return [Ducky, Eagle, Fox, Froggo, LLama, Racoon, Snake, Spider, Turtles, Whooper]

def get_random():
    return random.choice(get_all())
