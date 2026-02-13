import database.db as DB
import function.game as Game
import function.utils as Utils
from random import choice
from meta.person import Person as ObjectPerson
from time import sleep, time

Monster = None
def generator_monster()->ObjectPerson:
    """Sélectionne un monstre aléatoirement parmis la base de donnée."""

    all_monsters = DB.get_monsters({
        "_id": 0,
        "attack": 1,
        "defense": 1,
        "health": 1,
        "name": 1,
    })

    monster_select = choice(list(all_monsters))
    Monster = ObjectPerson(monster_select["name"], monster_select["attack"], monster_select["defense"], monster_select["health"])

    return Monster

def monster_attack_ally( teams:dict ):
    """Le monstre attaque un allié choisi aléatoirement. Si cette alliée meurt, il se fait supprimé de la liste fourni"""
    allies = choice(list(teams.values()))
    allies.take_damage(Monster)
    nameperson = allies.get_name()
    
    if not allies.is_alive():
        print(f"{nameperson} (ALLIES) a été tuer")
        del teams[nameperson]

def ally_attack_monster( teams:dict ):
    """Les alliés attaque le monstre. Si le monstre meurt, on casse la boucle"""
    global Monster

    for Person in teams.values():
        Monster.take_damage(Person)

        if not Monster.is_alive():
            print(f"{Monster.get_name()} (MONSTRE) a été tuer")
            Monster = generator_monster()
            break

        sleep(1.5)

def fight()->int:
    """Gestion de combat"""

    global Monster
    teams = Game.get_teams()
    phase = 0
    start_time = time()
    Monster = generator_monster()
    
    while len(teams) > 0:
        Utils.clear_console(1.5)
        phase += 1
        
        print(f"============ Phase : {phase} ============")
        ally_attack_monster( teams )
        monster_attack_ally( teams )

    print(f"Vous avez survéçu à {phase} phases pendant {Utils.format_time(time() - start_time)} secondes")
    return phase