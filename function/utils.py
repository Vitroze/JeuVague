import os
import function.color as Color
from meta.person import Person
from meta.item import Item, AllItems
import main
from time import sleep
from math import floor

def number_isvalidpositive( number: int ):
    """Vérifie si la donnée saisie est un nombre. Si c'est une chaine de caractère alors on convertira en nombre si possible"""

    if isinstance(number, str) and number.isdigit():
        number = int(number)

    return isinstance(number, int) and number >= 0

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
        sleep( delay )

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

def anykey():
    input("Appuyez sur n'import quel touche pour continuer")

def request_number(text, title):
    """Demande à l'utilisateur de rentrer une chaine de caractère qui sera transformé en nombre"""

    choose = request( text )
    if not number_isvalidpositive( choose ):
        PrintError(title, "Merci de rentrer un nombre valide")
        return request_number(text, title)
    
    return int(choose)

def request_percentage(text, title, no_superior=False):
    number = request_number(text, title)
    if number < 0 or (number > 100 and not no_superior):
        PrintError(title, "Merci de rentrer un pourcentage valide (entre 0 et 100%)")
        return request_percentage(text, title)

    return number

def return_main( title, error ):
    """Retourne dans le menu principal tout en envoyant un message d'erreur"""

    PrintError(title, error)
    back_option()

def back_option( duration:int = 1 ):
    """Retourner dans le menu principal après un certain temps"""

    sleep( duration )
    main.main()

def format_time( time:int )->str:
    """Transforme un nombre en une chaine de caractère qui sera mis en forme (ex : 2h30m15s)"""

    seconds = floor(time % 60)
    minuts = floor(time / 60)
    hours = floor(minuts / 60)
    hours = hours % 24
    minuts = minuts % 60

    text = ""
    if hours > 0:
        text += f"{hours}h"

    if minuts > 0:
        text += f"{minuts}m"

    if seconds > 0:
        text += f"{seconds}s"

    return text

def person_isvalid( person: Person ):
    return isinstance(person, Person)

def item_isvalid( item: Item):
    return isinstance(item, Item) and item.is_activate()

TestItem = Item("Test", "Ceci est un item de test")
TestItem.set_boost_damage(50)
TestItem.activate_item()
print("Item is valid : ", item_isvalid(TestItem))

def getAllItems():
    return AllItems

def find_item_by_name( name: str ):
    for item in getAllItems():
        if item.get_name() != name:
            continue
        
        return item
        
    PrintError("Recherche de l'Item", "Impossible de trouver l'item")
    return False

