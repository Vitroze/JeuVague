import database.db as DB
import function.admin as Admin
import function.utils as Utils
import function.game as Game
import function.score as Score

introduce = """
Bienvenue au jeu de la vague !

Merci de choisir ces options (1 et 4) pour commencer votre partie :
1. Création/Modification de personnage
2. Supprimer un personnage
3. Jouer (Composition d'équipe)
4. Voir le classement
5. Quitter

"""

def choose_option():
    """Menu Principal"""

    request = input( "Choisir votre option (1 et 5) : ")
    match request:
        case "1":
            Admin.request_creations_choose_team()
        case "2":
            Admin.request_delete()
        case "3":
            Game.manage_party()
        case "4":
            Score.showScore()
        case "5":
            print("Aurevoir !")
        case _:
            Utils.PrintError( "Option", "Merci de choisir une option corrcete (entre 1 et 5)" )
            choose_option()

def main():
    """Démarrage de la partie"""
    Utils.clear_console()
    print(introduce)

    choose_option()

# Evite que lorsqu'on charge le fichier main depuis les autres ficheirs qu'on lance pas le début partie.
if __name__ == "__main__":
    DB.connect()
    main()