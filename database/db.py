import pymongo as DataBase
import function.utils as Utils

CONFIG = {
    "host": "localhost",
    "port": 27017,
    "database_name": "jeuvague",
}

DB, PLAYERDATA, CONFIGDATA, CONFIGITEMS = None, None, None, None

def connect():
    """Connexion à la base de donnée et création des documents si ils ne sont pas créer"""
    global DB, PLAYERDATA, CONFIGDATA, CONFIGITEMS

    oClient = DataBase.MongoClient(f"mongodb://{CONFIG['host']}:{CONFIG['port']}/")
    DB = oClient[CONFIG["database_name"]]
    collection_list = DB.list_collection_names()

    # Init Table
    if f"{CONFIG["database_name"]}_playerdata" not in collection_list:
        DB.create_collection(f"{CONFIG["database_name"]}_playerdata")
    
    if f"{CONFIG["database_name"]}_config" not in collection_list:
        DB.create_collection(f"{CONFIG["database_name"]}_config")

    if f"{CONFIG["database_name"]}_config_items" not in collection_list:
        DB.create_collection(f"{CONFIG["database_name"]}_config_items")

    PLAYERDATA = DB[f"{CONFIG["database_name"]}_playerdata"]
    CONFIGDATA = DB[f"{CONFIG["database_name"]}_config"]
    CONFIGITEMS = DB[f"{CONFIG["database_name"]}_config_items"]

    Utils.PrintSuccess("DataBase", "La base de donnée est connecté")

def update_person( name: str, team: str, attack:int, defense: int, health: int, name_item:str = None, percentage_drop:int = None ):
    """Met à jour le monstre ou alliés dans la base de donnée"""
    CONFIGDATA.update_one({
        "name": name,
        "team": team,
    }, { 
        "$set": {
            "attack": attack,
            "defense": defense,
            "health": health,
            "name_item": name_item,
            "percentage_drop": percentage_drop
        }
    })

    Utils.PrintSuccess("DataBase", f"Le personnage '{ name }' ({team}) a bien été modifier")

def create_allies( name: str, attack:int, defense:int, health: int ):
    """Enregistre l'alliée dans la base de donnée"""
    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom de l'alliée est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return
    
    if not Utils.number_isvalidpositive( attack ) or not Utils.number_isvalidpositive( defense ) or not Utils.number_isvalidpositive( health ):
        Utils.PrintError("DataBase", "L'argument (attack ou defense ou health) n'est pas un nombre ou n'est pas positive")
        return

    if is_exist_allies( name ):
        Utils.PrintDebug("DataBase", "Cette alliée existe déjà")
        update_person( name, "allies", attack, defense, health)
        return
    
    CONFIGDATA.insert_one({
        "name": name,
        "attack": attack,
        "defense": defense,
        "health": health,
        "team": "allies",
    })

    Utils.PrintSuccess("DataBase", f"L'alliée '{ name }' a bien été enregistré")


def create_monsters( name: str, attack:int, defense:int, health: int, name_item:str = None, percentage_drop:int = None):
    """Enregistre le monstre dans la base de donnée"""
    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom du monstre est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return
    
    if not Utils.number_isvalidpositive( attack ) or not Utils.number_isvalidpositive( defense ) or not Utils.number_isvalidpositive( health ):
        Utils.PrintError("DataBase", "L'argument (attack ou defense ou health) n'est pas un nombre ou n'est pas positive")
        return

    if is_exist_monsters( name ):
        Utils.PrintDebug("DataBase", "Ce monstre existe déjà.")
        update_person( name, "monsters", attack, defense, health, name_item, percentage_drop )
        return
    
    CONFIGDATA.insert_one({
        "name": name,
        "attack": attack,
        "defense": defense,
        "health": health,
        "name_item": name_item,
        "percentage_drop": percentage_drop,
        "team": "monsters",
    })

    Utils.PrintSuccess("DataBase", f"Le monstre '{ name }' a bien été enregistré")

def is_exist_monsters( name:str ) -> bool:
    """Vérifie si un monstre existe"""
    return CONFIGDATA.find_one({
        "name": name,
        "team": "monsters",
    }) != None


def is_exist_allies( name:str ) -> bool:
    """Vérifie si un alliés existe"""
    return CONFIGDATA.find_one({
        "name": name,
        "team": "allies",
    }) != None

def is_exist_character( name: str, team:str )->bool:
    """Vérifie si un personnage existe dans sa propre équipe"""
    if team not in ["allies", "monsters"]:
        Utils.PrintError("DataBase", "L'équipe n'existe pas")
        return
    
    return team == "allies" and is_exist_allies( name ) or team == "monsters" and is_exist_monsters( name ) 

def delete_monsters( name: str ):
    """Supprime un monstre"""
    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom du monstre est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return

    if not is_exist_monsters( name ):
        Utils.PrintError("DataBase", "Le monstre n'existe pas")
        return

    CONFIGDATA.delete_one({
        "name": name,
        "team": "monsters"
    })

    Utils.PrintSuccess("DataBase", f"Le monstre '{ name }' a bien été supprimé")

def delete_allies( name: str ):
    """Supprime un allié"""
    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom de l'alliés est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return

    if not is_exist_allies( name ):
        Utils.PrintError("DataBase", "L'alliée n'existe pas")
        return

    CONFIGDATA.delete_one({
        "name": name,
        "team": "allies"
    })

    Utils.PrintSuccess("DataBase", f"L'alliée '{ name }' a bien été supprimé")

def get_allies()->dict:
    """Récupère tous les alliés enregistrés dans la base de données"""
    return CONFIGDATA.find({
        "team": "allies"
    })

def get_monsters(exclude:dict={})->dict:
    """Récupère tous les monstres enregistrés dans la base de données"""
    return CONFIGDATA.find({
        "team": "monsters"
    }, exclude)

def get_countmonsters()->int:
    """Récupère le nombre de monstre enregistré dans la base de donnée"""
    return CONFIGDATA.count_documents({
        "team": "monsters"
    })

def get_stats(name:str, team: str, exclude:dict={})->dict:
    """Récupère les statistiques des personnages"""
    return CONFIGDATA.find_one({
        "name": name,
        "team": team,
    }, exclude)

def is_username_exists(username)->bool:
    return PLAYERDATA.find_one({
        "username": username
    }) != None

def save_score(username:str, value:int, inventory:dict=[]):
    """Sauvegarde les données utilisateurs du joueur (Score ainsi que l'inventaire)"""
    if is_username_exists(username):
        PLAYERDATA.update_one({
            "username": username,
        }, { 
            "$set": {
                "score": value,
                "inventory": inventory
            }
        })

        Utils.PrintSuccess("DataBase", f"Le score de {username} a bien été mis à jour")
        return
    
    PLAYERDATA.insert_one({
        "username": username,
        "score": value,
        "inventory": inventory
    })

    Utils.PrintSuccess("DataBase", f"Le score de {username} a bien été enregistré")

def getAllScore(limit:int=5)->dict:
    """Affiche les scores des joueurs. Par défaut les 5 premiers"""
    return PLAYERDATA.find({}, {"_id": 0}).sort("score", -1).limit(limit)

def get_item( name: str, exclude:dict={} )->dict:
    """Récupère l'item"""
    return CONFIGITEMS.find_one({
        "name": name,
    }, exclude)

def exist_items( name:str )->bool:
    """Vérifie si l'item existe dans la base de donnée"""
    return get_item( name ) != None

def create_item( name:str, desc:str, boost_damage:int, boost_defense:int ):
    """Crée ou met à jour l'item dans la configuration"""
    if exist_items( name ):
        CONFIGITEMS.update_one({
            "name": name,
        }, { 
            "$set": {
                "desc": desc,
                "boost_damage": boost_damage,
                "boost_defense": boost_defense,
            }
        })

        Utils.PrintSuccess("DataBase", f"L'item '{ name }' a bien été mis à jour")
        return
    
    CONFIGITEMS.insert_one({
        "name": name,
        "desc": desc,
        "boost_damage": boost_damage,
        "boost_defense": boost_defense,
    })

    Utils.PrintSuccess("DataBase", f"L'item '{ name }' a bien été enregistré")

def delete_item( name: str ):
    """Supprime l'item de la configuration"""

    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom de l'item est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return

    if not exist_items( name ):
        Utils.PrintError("DataBase", "L'item n'existe pas")
        return

    CONFIGITEMS.delete_one({
        "name": name,
    })

def get_playerdata( username:str )->dict:
    """Récupère les données du joueur"""

    return PLAYERDATA.find_one({
        "username": username
    })

def get_inventory( username:str ):
    """Récupère l'inventaire enregistré du joueurs"""

    data = get_playerdata(username)
    if data == None:
        Utils.PrintError("DataBase", "Les données du joueurs n'existent pas")
        return {}

    return data["inventory"] or {}