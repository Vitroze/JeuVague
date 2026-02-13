import database.db as DB
import function.utils as Utils
import function.score as Score
import function.fight as Fight
from meta.person import Person as ObjectPerson

SIZE_TEAM = 3 # 3 Personnages dans l'équipe
MONSTER_MIN = 1 # Il faut au moins 1 monstre pour pouvori commencer la partie

Person = {}
def list_nameallies():
    name = {}
    for Data in DB.get_allies():
        name[len(name)] = Data["name"]

    return name

def show_allies(list):
    Utils.clear_console(1)
    print("Choisir votre équipe parmis cette liste :")

    count = 1
    for name in list.values():
        if name in Person:
            count += 1
            continue

        print(f"{count}. {name}")
        count += 1

def create_person(name, team):
    data = DB.get_stats(name, team, {
        "_id": 0,
        "attack": 1,
        "defense": 1,
        "health": 1,
    })

    person = ObjectPerson(name, data["attack"], data["defense"], data["health"])
    
    return person


def is_error(allies):
    errors = {
        "Impossible de démarrer la partie car il n'a pas assez d'alliés enregistrer dans la base de donnée": len(allies) != SIZE_TEAM,
        "Impossible de démarrer la partie car il n'a pas assez de monstres enregistrer dans la base de donnée": DB.get_countmonsters() < MONSTER_MIN,
    }

    for error in errors:
        if errors[error]:
            Utils.return_main("Choisir son équipe", error)
            return True
    return False

def request_choose_allies(allies):
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

def request_username():
    return Utils.request("Merci d'entrer un nom d'utilisateur.", True)

def choose_team():
    allies = list_nameallies()
    if is_error(allies): return

    username = request_username()

    while not team_iscomplete():
        show_allies(allies)
        request_choose_allies(allies)

    score = Fight.fight()

    Score.save_score(username, score)

def team_iscomplete():
    return len(Person) == SIZE_TEAM

def get_teams():
    return Person