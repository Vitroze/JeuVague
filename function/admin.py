import function.utils as Utils
import database.db as DB

def request_creation( team:str, name:str = None):
    """Processus de création d'un allié ou d'un monstre"""

    Utils.clear_console( 1 )
    print(f"============ {team} ============")

    name = name or Utils.request( f"Choisir le nom du personnage. Si vous prenez un nom déjà existant cela va modifier ces statistiques.", False )
    if not Utils.string_isvalid( name ):
        Utils.PrintError(f"Création de Personnage ({team})", "Le nom est invalide; Merci de rentrer un nom correcte")
        request_creation( team )
        return

    attack = Utils.request_number( "La puissance d'attaque (Nombre positive).", f"Création de Personnage ({team})")
    attack = int( attack )

    defense = Utils.request_number( "La puissance de défense (Nombre positive).", f"Création de Personnage ({team})")    
    defense = int( defense )

    health = Utils.request_number( "Le nombre de PV (Nombre positive).", f"Création de Personnage ({team})" )
    health = int( health )

    if team == "alliés":
        DB.create_allies( name, attack, defense, health )
    elif team == "monstre":
        item, percentage = request_add_item_monsters()

        DB.create_monsters( name, attack, defense, health, item, percentage )
    
    Utils.back_option()

def request_add_item_monsters():
    name_item = Utils.request( f"Ecrivez un item lorsque de la mort du personnage (Laissez vide si rien) ?", False )
    if not Utils.string_isvalid( name_item ):
        return
    
    if not Utils.getAllItems( name_item ):
        Utils.PrintError("Création de Personnage - Ajout d'item", "Impossible de trouver l'item.")
        return request_add_item_monsters()
    
    percentageDrop = Utils.request_percentage(f"Ecrivez le pourcentage de chance que l'item apparait après la mort du monstre", "Création de personnage - Item")
    
    return name_item, percentageDrop

def request_creations_choose_team():
    """Demande a l'utilisateur de choisir entre allies ou monstre pour le processus de création"""
    choose = Utils.request( "Merci de choisir entre 'allies' ou 'monstre'.")

    match choose:
        case "allies":
            request_creation("alliés")
        case "monstre":
            request_creation("monstre")
        case _:
            Utils.PrintError("Création de personnage", "Merci de choisir une équipe corrcete (allies ou monstre)")
            request_creations_choose_team()

def request_delete():
    """Processus de suppression d'un personnage"""

    Utils.clear_console(1)

    # Request
    choose = Utils.request( "Merci de rentrer exactement le nom du personnage que vous souhaitez supprimer.")
    team = Utils.request( "Merci de choisir l'équipe où le personnage doit être supprimer (allies ou monsters).")

    if not DB.is_exist_character( choose, team ):
        Utils.PrintError("Suppression de personnage", "Le personnage n'existe pas")
        request_delete()
        return
    
    match team:
        case "allies":
            DB.delete_allies( choose )
        case "monsters":
            DB.delete_monsters( choose )

    Utils.back_option( 0 )

def request_create_item( name:str=None, desc:str=None, boost_damage:int=None, boost_defense:int=None):
    pass