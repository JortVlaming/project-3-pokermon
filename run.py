from src.main import run
from src.engine.logger import set_level, LogLevel

if __name__ == "__main__":
    try:
        set_level(LogLevel.DEBUG)

        run()
    except KeyboardInterrupt:
        print("Game stopped by keyboard interrupt")