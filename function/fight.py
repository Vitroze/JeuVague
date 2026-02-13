import database.db as DB
import function.game as Game
import function.utils as Utils
from random import choice
from meta.person import Person as ObjectPerson
import time

Monster = None
def generator_monster()->ObjectPerson:
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

def monster_attack_ally( teams:dict, Monster:ObjectPerson ):
    allies = choice(list(teams.values()))
    allies.take_damage(Monster)
    nameperson = allies.get_name()
    
    if not allies.is_alive():
        print(f"{nameperson} (ALLIES) a été tuer")
        del teams[nameperson]

def ally_attack_monster( teams:dict, Monster:ObjectPerson ):
    for Person in teams.values():
        Monster.take_damage(Person)

        if not Monster.is_alive():
            print(f"{Monster.get_name()} (MONSTRE) a été tuer")
            break

        time.sleep(1.5)

def fight()->int:
    teams = Game.get_teams()

    phase = 0
    start_time = time.time()
    Monster = generator_monster()
    
    while len(teams) > 0:
        Utils.clear_console(1.5)
        phase += 1
        
        print(f"============ Phase : {phase} ============")
        ally_attack_monster(teams, Monster)
        monster_attack_ally(teams, Monster)

    print(f"Vous avez survéçu à {phase} phases pendant {Utils.format_time(time.time() - start_time)} secondes")
    return phase