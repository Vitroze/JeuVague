import os
import function.color as Color
import time
import math
import main

def number_isvalidpositive( number: int ):
    if isinstance(number, str) and number.isdigit():
        number = int(number)

    return isinstance(number, int) and number > 0

def string_isvalid( text: str ):
    return text and len(text) > 0

def PrintDebug( title: str, text: str ):
    print(Color.Text.DEBUG + f"[{title}] " + Color.Text.ENDC + text)

def PrintError( title: str, text: str ):
    print(Color.Text.FAIL + f"[{title}] " + Color.Text.ENDC + text)

def PrintSuccess( title: str, text: str ):
    print(Color.Text.SUCCESS + f"[{title}] " + Color.Text.ENDC + text)

def clear_console( delay: int=None ):
    if delay:
        time.sleep( delay )

    os.system('cls' if os.name == 'nt' else 'clear')

def request( text:str, no_lower:bool=False )->str:
    choose = input(f"{text} Marquer 'return' pour revenir au menu principal :")
    if not no_lower:
        choose = choose.lower()

    if choose == "return":
        main.main()
        return
    
    return choose

def request_number(text, title):
    choose = request( text )
    if not number_isvalidpositive( choose ):
        PrintError(title, "Merci de rentrer un nombre valide")
        time.sleep(1)
        return
    
    return int(choose)

def return_main( title, error ):
    PrintError(title, error)
    back_option()

def back_option( duration:int = 1 ):
    time.sleep( duration )
    main.main()

def format_time( time ):
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
