import database.db as DB
import function.admin as Admin
import function.utils as Utils
import function.game as Game
import function.score as Score

introduce = """
Bienvenue au jeu de la vague !

Merci de choisir ces options (1 et 7) pour commencer votre partie :
1. (ADMIN) Création/Modification de personnage
2. (ADMIN) Supprimer un personnage
3. (ADMIN) Création/Modification d'un objet
4. (ADMIN) Supprimer un objet
5. Jouer (Composition d'équipe)
6. Voir le classement
7. Quitter

"""

def choose_option():
    """Menu Principal"""

    request = input( "Choisir votre option (1 et 7) : ")
    match request:
        case "1":
            Admin.request_creations_choose_team()
        case "2":
            Admin.request_delete()
        case "3":
            Admin.request_create_item()
        case "4":
            Admin.request_delete_item()
        case "5":
            Game.manage_party()
        case "6":
            Score.showScore()
        case "7":
            print("Aurevoir !")
        case _:
            Utils.PrintError( "Option", "Merci de choisir une option correcte (entre 1 et 7)" )
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