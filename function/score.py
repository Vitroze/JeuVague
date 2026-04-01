import database.db as DB
import function.utils as Utils

def showScore():
    """Affiche les scores dans la console"""

    Utils.clear_console()

    place = 1
    print("Classement :")
    for Data in DB.getAllScore():
        print(f"{place}. {Data["username"]} - {Data["score"]}")
        place += 1

    Utils.anykey("Appuyez sur ENTRER pour sortir du classement")
    Utils.back_option()

def save_score( username:str, score:int, all_items:list=[] ):
    """Sauvegarde les données dans la base de donnée tout en retournant dans le menu principale après 2 secondes"""

    DB.save_score( username, score, all_items )
    Utils.back_option( 2 )