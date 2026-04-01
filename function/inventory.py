import database.db as DB
import function.utils as Utils
import function.game as Game
from meta.inventory import Inventory as InventoryObject
from meta.item import Item as ItemObject
from math import ceil

def create_inventory( username:str )->InventoryObject:
    """Crée l'inventaire du joueur avec les données sauvegardés sur son nom d'utilisateur"""
    inventory_data = DB.get_inventory(username)
    inventory = InventoryObject()
    
    if len(inventory_data) > 0:
        for name_item in inventory_data:
            item_data = DB.get_item(name_item, {
                "_id": 0,
                "name": 1,
                "desc": 1,
                "boost_damage": 1,
                "boost_defense": 1,
            })

            item = ItemObject(name_item, item_data["desc"])
            item.set_boost_damage(item_data["boost_damage"])
            item.set_boost_defense(item_data["boost_defense"])
            item.activate_item()

            inventory.set_item(item)

    return inventory

def request_page( inventory:InventoryObject )->int:
    """Demande a l'utilisateur d'écrire un nombre pour le système de page"""

    numberTotalPage = ceil( inventory.get_count_items() / 5 )
    page = Utils.request_number(f"Merci d'entrer le numéro de la page (Entre 1 et {numberTotalPage} pages). Appuyer sur 0 pour sortir du menu", "Système d'inventaire")
    if page > numberTotalPage:
        return numberTotalPage
    elif page < 1:
        Game.request_inventory( inventory )
        return 0 
    else:
        return page 

limit_items_per_page = 5
def showAllItems( inventory:InventoryObject, start:int=0, end:int=limit_items_per_page, page:int=1 ):
    """Affiche tous les items de l'inventaire"""

    Utils.clear_console()

    print(f"--------- Page {page} ---------")
    i = start + 1
    for item in inventory.get_inventory()[start:end]:
        print(f"{i}. {item.get_name()}")

        i+=1
    
    if inventory.get_count_items() > 5:
        page = request_page(inventory)
        showAllItems(inventory, (page - 1) * limit_items_per_page, page * limit_items_per_page, page)
    else:
        Utils.anykey()
        Game.request_inventory(inventory)