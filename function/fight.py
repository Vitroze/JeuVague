import database.db as DB
import function.game as Game
import function.utils as Utils
from random import choice
from meta.person import Person as ObjectPerson
from time import sleep, time

Monster = None
all_items_drops = []
all_monsters = {}
def generator_monster()->ObjectPerson:
    """Sélectionne un monstre aléatoirement parmis la base de donnée."""

    monster_select = choice(all_monsters)
    Monster = ObjectPerson(monster_select["name"], monster_select["attack"], monster_select["defense"], monster_select["health"])
    if "name_item" in monster_select and "percentage_drop" in monster_select:
        Monster.set_item_droppable(monster_select["name_item"], monster_select["percentage_drop"])

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
        item_drop = Monster.take_damage(Person)

        if not Monster.is_alive():
            print(f"{Monster.get_name()} (MONSTRE) a été tuer")
            
            if item_drop:
                addItemDrop(item_drop)

            Monster = generator_monster()
            break

        sleep(1.5)

def fight()->tuple[int, dict]:
    """Gestion de combat"""

    global Monster
    global all_items_drops
    global all_monsters

    all_monsters = list(DB.get_monsters({
        "_id": 0,
        "attack": 1,
        "defense": 1,
        "health": 1,
        "name": 1,
        "name_item":1,
        "percentage_drop": 1,
    }))

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
    if len(all_items_drops) > 0:
        showAllItemDrop()

    return phase, all_items_drops

def addItemDrop(name_item):
    all_items_drops.append(name_item)

def showAllItemDrop():
    print("Liste de tous les items que vous avez récupérer")
    for name_item in all_items_drops:
        print(f" - {name_item}")

    Utils.anykey()