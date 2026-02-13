import pymongo as DataBase
import function.utils as Utils

CONFIG = {
    "host": "localhost",
    "port": 27017,
    "database_name": "jeuvague",
}

DB, PLAYERDATA, CONFIGDATA = None, None, None

def connect():
    global DB, PLAYERDATA, CONFIGDATA

    oClient = DataBase.MongoClient(f"mongodb://{CONFIG['host']}:{CONFIG['port']}/")
    DB = oClient[CONFIG["database_name"]]
    collection_list = DB.list_collection_names()

    # Init Table
    if f"{CONFIG["database_name"]}_playerdata" not in collection_list:
        DB.create_collection(f"{CONFIG["database_name"]}_playerdata")
    
    if f"{CONFIG["database_name"]}_config" not in collection_list:
        DB.create_collection(f"{CONFIG["database_name"]}_config")

    PLAYERDATA = DB[f"{CONFIG["database_name"]}_playerdata"]
    CONFIGDATA = DB[f"{CONFIG["database_name"]}_config"]

    Utils.PrintSuccess("DataBase", "La base de donnée est connecté")

def update_person( name: str, team: str, attack:int, defense: int, health: int ):
    CONFIGDATA.update_one({
        "name": name,
        "team": team,
    }, { 
        "$set": {
            "attack": attack,
            "defense": defense,
            "health": health,
        }
    })

    Utils.PrintSuccess("DataBase", f"Le personnage '{ name }' ({team}) a bien été modifier")

def create_allies( name: str, attack:int, defense:int, health: int ):
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


def create_monsters( name: str, attack:int, defense:int, health: int ):
    if not Utils.string_isvalid( name ):
        Utils.PrintError("DataBase", "Le nom du monstre est incorrecte. Merci de mettre une chaine de caractère et un text avec au moins 1 caractère")
        return
    
    if not Utils.number_isvalidpositive( attack ) or not Utils.number_isvalidpositive( defense ) or not Utils.number_isvalidpositive( health ):
        Utils.PrintError("DataBase", "L'argument (attack ou defense ou health) n'est pas un nombre ou n'est pas positive")
        return

    if is_exist_monsters( name ):
        Utils.PrintDebug("DataBase", "Ce monstre existe déjà.")
        update_person( name, "monsters", attack, defense, health)
        return
    
    CONFIGDATA.insert_one({
        "name": name,
        "attack": attack,
        "defense": defense,
        "health": health,
        "team": "monsters",
    })

    Utils.PrintSuccess("DataBase", f"Le monstre '{ name }' a bien été enregistré")

def is_exist_monsters( name:str ) -> bool:
    return CONFIGDATA.find_one({
        "name": name,
        "team": "monsters",
    }) != None


def is_exist_allies( name:str ) -> bool:
    return CONFIGDATA.find_one({
        "name": name,
        "team": "allies",
    }) != None

def is_exist_character( name: str, team:str ):
    if team not in ["allies", "monsters"]:
        Utils.PrintError("DataBase", "L'équipe n'existe pas")
        return
    
    return team == "allies" and is_exist_allies( name ) or team == "monsters" and is_exist_monsters( name ) 

def delete_monsters( name: str ):
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

def get_allies():
    return CONFIGDATA.find({
        "team": "allies"
    })

def get_monsters(exclude:list={}):
    return CONFIGDATA.find({
        "team": "monsters"
    }, exclude)

def get_countmonsters():
    return CONFIGDATA.count_documents({
        "team": "monsters"
    })

def get_stats(name:str, team: str, exclude:list={})->list:
    return CONFIGDATA.find_one({
        "name": name,
        "team": team,
    }, exclude)

def is_username_exists(username)->bool:
    return PLAYERDATA.find_one({
        "username": username
    }) != None

def save_score(username, value):
    if is_username_exists(username):
        PLAYERDATA.update_one({
            "username": username,
        }, { 
            "$set": {
                "score": value
            }
        })

        Utils.PrintSuccess("DataBase", f"Le score de {username} a bien été mis à jour")
        return
    
    PLAYERDATA.insert_one({
        "username": username,
        "score": value,
    })

    Utils.PrintSuccess("DataBase", f"Le score de {username} a bien été enregistré")

def getAllScore(limit:int=5):
    return PLAYERDATA.find({}, {"_id": 0}).sort("score", -1).limit(limit)

# create_allies("Ceci est un test", 5, 5, 100)
# delete_allies( "Ceci est un test" )
# create_monsters("Ceci est un test", 500, 25, 100)