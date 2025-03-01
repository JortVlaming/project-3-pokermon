from enum import Enum

import colorama
from colorama import Fore

class LogLevel(Enum):
    VERBOSE = (-1, Fore.BLUE, "[VERBOSE]")
    DEBUG = (0, Fore.LIGHTBLACK_EX, "[DEBUG]")
    INFO = (1, Fore.RESET, "[INFO]")
    WARN = (2, Fore.YELLOW, "[WARN]")
    ERROR = (3, Fore.RED, "[ERROR]")

__LOG_LEVEL = LogLevel.DEBUG
__COLORAMA_INITIALIZED = False

# set de filter level
def set_level(level:LogLevel):
    """
    Zet een nieuw filter level voor de logger

    :param level: De nieuwe filter level
    :return:
    """
    global __LOG_LEVEL
    __LOG_LEVEL = level

def __join(sep, to_join):
    res = ""
    for s in to_join:
        res = res + str(s) + sep

    res = res[:-(len(sep))]

    return res

def log(level:LogLevel, *args):
    """
    Log een bericht naar de console.
    Berichten worden gefilterd met het huidige loglevel.

    :param level: Het log level om te gebruiken
    :param args: Argumenten om het bericht te bouwen
    :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
    :return:
    """
    global __COLORAMA_INITIALIZED
    if not __COLORAMA_INITIALIZED:
        # zorg data colorama maar een keur wordt geïnitialiseerd
        colorama.init()
        __COLORAMA_INITIALIZED = True
    if len(args) == 0:
        # voor als er een clown is die geen argumenten meegeeft
        # meteen error gooien is misschien streng maar het is niet de bedoeling dat er geen argumenten worden meegegeven
        raise Exception("log called without arguments!")
    # check of level hoger light dan de filter level
    if level.value[0] >= __LOG_LEVEL.value[0]:
        # check of er meer argumenten zijn of maar een
        if len(args) == 1:
            if isinstance(args[0], tuple) or isinstance(args[0], list):
                # als het enkele argument een tuple of list is print het eerste element
                if len(args[0]) == 1:
                    # als er maar een element is print dat element
                    print(level.value[1] + level.value[2] + " " + str(args[0][0]) + Fore.RESET)
                else:
                    # als er meer elementen zijn print de normale lijst
                    print(level.value[1] + level.value[2] + " " + __join(" ", args[0]) + Fore.RESET)
            else:
                # argument can worden gecast naar string
                print(level.value[1] + level.value[2] + " " + str(args[0]) + Fore.RESET)
        else:
            # print alle argumenten in een keer
            print(level.value[1] + level.value[2] + " " + __join(" ", args) + Fore.RESET)

# standalone functies die shortcuts zijn voor de hoofdfunctie
def verbose(*args):
    """
    Logged een bericht met ``VERBOSE`` log level

    :param args: Argumenten om het bericht te bouwen
    :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
    :return:
    """
    log(LogLevel.VERBOSE, args)

def debug(*args):
    """
    Logged een bericht met ``DEBUG`` log level

    :param args: Argumenten om het bericht te bouwen
    :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
    :return:
    """
    log(LogLevel.DEBUG, args)

def info(*args):
    """
        Logged een bericht met ``INFO`` log level

        :param args: Argumenten om het bericht te bouwen
        :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
        :return:
        """

    log(LogLevel.INFO, args)

def warn(*args):
    """
        Logged een bericht met ``WARN`` log level

        :param args: Argumenten om het bericht te bouwen
        :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
        :return:
        """
    log(LogLevel.WARN, args)

def error(*args):
    """
        Logged een bericht met ``ERROR`` log level

        :param args: Argumenten om het bericht te bouwen
        :raises Exception: Als er geen argumenten zijn om een bericht te bouwen
        :return:
        """
    log(LogLevel.ERROR, args)

# als het bestand standalone wordt gebruikt print de test strings
if __name__ == "__main__":
    set_level(LogLevel.DEBUG)

    log(LogLevel.DEBUG, "Debug with single string")
    log(LogLevel.DEBUG, "Debug", "with", "multiple", "strings")
    debug("Standalone Debug")

    log(LogLevel.INFO, "Info with single string")
    log(LogLevel.INFO, "Info", "with", "multiple", "strings")
    info("Standalone Info")

    log(LogLevel.WARN, "Warn with single string")
    log(LogLevel.WARN, "Warn", "with", "multiple", "strings")
    warn("Standalone Warn")

    log(LogLevel.ERROR, "Error with single string")
    log(LogLevel.ERROR, "Error", "with", "multiple", "strings")
    error("Standalone Error")