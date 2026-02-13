import os
import function.color as Color
import time
import math
import main

def number_isvalidpositive( number: int ):
    """Vérifie si la donnée saisie est un nombre. Si c'est une chaine de caractère alors on convertira en nombre si possible"""

    if isinstance(number, str) and number.isdigit():
        number = int(number)

    return isinstance(number, int) and number > 0

def string_isvalid( text: str ):
    """Vérifie si la donnée saisie est une chaine de caractère"""

    return text and len(text) > 0

def PrintDebug( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en bleu et le reste gardera du blanc"""

    print(Color.Text.DEBUG + f"[{title}] " + Color.Text.ENDC + text)

def PrintError( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en rouge et le reste gardera du blanc"""

    print(Color.Text.FAIL + f"[{title}] " + Color.Text.ENDC + text)

def PrintSuccess( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en vert et le reste gardera du blanc"""

    print(Color.Text.SUCCESS + f"[{title}] " + Color.Text.ENDC + text)

def clear_console( delay: int=None ):
    """Efface la console après un certain temps compatible avec les systèmes d'exploitations de MacOS, Windows et Linux"""

    if delay:
        time.sleep( delay )

    os.system('cls' if os.name == 'nt' else 'clear')

def request( text:str, no_lower:bool=False )->str:
    """Demande à l'utilisateur de rentrer une chaine de caractère"""

    choose = input(f"{text} Marquer 'return' pour revenir au menu principal :")
    if not no_lower:
        choose = choose.lower()

    if choose == "return":
        main.main()
        return
    
    return choose

def request_number(text, title):
    """Demande à l'utilisateur de rentrer une chaine de caractère qui sera transformé en nombre"""

    choose = request( text )
    if not number_isvalidpositive( choose ):
        PrintError(title, "Merci de rentrer un nombre valide")
        time.sleep(1)
        return
    
    return int(choose)

def return_main( title, error ):
    """Retourne dans le menu principal tout en envoyant un message d'erreur"""

    PrintError(title, error)
    back_option()

def back_option( duration:int = 1 ):
    """Retourner dans le menu principal après un certain temps"""

    time.sleep( duration )
    main.main()

def format_time( time:int )->str:
    """Transforme un nombre en une chaine de caractère qui sera mis en forme (ex : 2h30m15s)"""

    seconds = math.floor(time % 60)
    minuts = math.floor(time / 60)
    hours = math.floor(minuts / 60)
    hours = hours % 24
    minuts = minuts % 60

    text = ""
    if hours > 0:
        text += f"{text}{hours}h"

    if minuts > 0:
        text += f"{text}{minuts}m"

    if seconds > 0:
        text += f"{text}{seconds}s"

    return text
