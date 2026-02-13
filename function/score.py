import database.db as DB
import function.utils as Utils
from time import sleep

def showScore():
    Utils.clear_console()

    place = 1
    print("Classement :")
    for Data in DB.getAllScore():
        print(f"{place}. {Data["username"]} - {Data["score"]}")
        place += 1

    Utils.request("Appuyez sur ENTRER pour sortir du classement")
    Utils.back_option()

def save_score( username, score ):
    DB.save_score( username, score )
    Utils.back_option( 2 )