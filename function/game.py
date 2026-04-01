import time
import database.db as DB
import function.utils as Utils
import function.score as Score
import function.fight as Fight
import function.inventory as Inventory
from meta.person import Person as ObjectPerson

SIZE_TEAM = 3 # 3 Personnages dans l'équipe
MONSTER_MIN = 1 # Il faut au moins 1 monstre pour pouvori commencer la partie

Person = {}
def list_nameallies():
    """Mettre sous forme de dictionnaire les prénoms des alliés. La clé sera comme une table séquentielle."""

    name = {}
    for Data in DB.get_allies():
        name[len(name)] = Data["name"]

    return name

def show_allies(allies:dict):
    """Affiche dans la console les alliés qu'on peut prendre."""

    Utils.clear_console(1)
    print("Choisir votre équipe parmis cette liste :")

    count = 1
    for name in allies.values():
        if name in Person:
            count += 1
            continue

        print(f"{count}. {name}")
        count += 1

def create_person(name:str, team:str)->ObjectPerson:
    """Crée un personnage via ses données enregistrés dans la base de donnée ainsi l'objet."""

    data = DB.get_stats(name, team, {
        "_id": 0,
        "attack": 1,
        "defense": 1,
        "health": 1,
    })

    return ObjectPerson(name, data["attack"], data["defense"], data["health"])


def is_error(allies:dict)->bool:
    """Vérifie si on ne peut pas commencer une partie."""

    errors = {
        "Impossible de démarrer la partie car il n'a pas assez d'alliés enregistrer dans la base de donnée": len(allies) < SIZE_TEAM,
        "Impossible de démarrer la partie car il n'a pas assez de monstres enregistrer dans la base de donnée": DB.get_countmonsters() < MONSTER_MIN,
    }

    for error in errors:
        if errors[error]:
            Utils.return_main("Choisir son équipe", error)
            return True

    return False

def request_choose_allies(allies:list):
    """Demande à l'utilisateur de choisir un alliée"""

    choose = Utils.request_number("Choisir l'ID du personnage :", "Choisir son équipe")
    if not choose:
        return
    
    choose = max(choose - 1, 0)
    if choose not in allies.keys():
        Utils.PrintError("Choisir son équipe", "Ce personnage n'existe pas")
        return

    name = allies[choose]
    if name in Person:
        Utils.PrintError("Choisir son équipe", "Ce personnage est déjà dans votre équipe")
        return
    
    Person[name] = create_person(name, "allies")

def request_username()->str:
    """Demande à l'utilisateur d'entrer un nom d'utilisateur. On ne mettre pas ce qui rentre en minuscule. """

    return Utils.request("Merci d'entrer un nom d'utilisateur.", True)

def manage_party():
    """Gestion de la partie"""

    allies = list_nameallies()
    if is_error(allies): return

    username = request_username()

    while not team_iscomplete():
        show_allies(allies)
        request_choose_allies(allies)

    inventory_player = Inventory.create_inventory(username)
    request_inventory(inventory_player)
    (score, all_items) = Fight.fight()
    Score.save_score(username, score, all_items)

def team_iscomplete()->bool:
    """Vérifie si l'équipe est complet"""

    return len(Person) == SIZE_TEAM

def get_teams()->dict:
    """Liste de nos alliés qu'on a sélectionné et qu'ils sont toujours en vie."""

    return Person

introduce_inventory = f"""
Choisissez les actions que vous souhaitez appliquer à votre inventaire.
1. Voir les items ({Inventory.limit_items_per_page} par {Inventory.limit_items_per_page})
2. Supprimer des items dans l'inventaire
3. Equiper un personnage
4. Commencer le combat
"""

def in_progress(inventory):
    Utils.PrintError("Choix - Inventaire", "L'option choisi est en cours de développement.")
    time.sleep(1.5)
    request_inventory(inventory)

def request_inventory(inventory):
    Utils.clear_console()
    print(introduce_inventory)

    input = Utils.request("Quel action souhaitez-vous faire ?")

    match input:
        case "1":
            Inventory.showAllItems(inventory)
        case "2":
            in_progress(inventory)
        case "3":
            in_progress(inventory)
        case "4":
            return
        case _:
            Utils.PrintError("Gestion de l'inventaire", "Choissez une option valide.")
            time.sleep(1)
            request_inventory(inventory)