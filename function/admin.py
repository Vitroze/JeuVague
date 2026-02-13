import function.utils as Utils
import database.db as DB

def request_creation( team:str, name:str = None, attack:int = None, defense:int = None ):
    Utils.clear_console( 1 )
    print(f"============ {team} ============")

    name = name or Utils.request( f"Choisir le nom du personnage. Si vous prenez un nom déjà existant cela va modifier ces statistiques.", False )
    if not Utils.string_isvalid( name ):
        Utils.PrintError(f"Création de Personnage ({team})", "Le nom est invalide; Merci de rentrer un nom correcte")
        request_creation( team )
        return

    attack = attack or Utils.request_number( "La puissance d'attaque (Nombre positive).", f"Création de Personnage ({team})")
    if not attack:
        request_creation( team, name )
        return
    
    attack = int( attack )

    defense = defense or Utils.request_number( "La puissance de défense (Nombre positive).", f"Création de Personnage ({team})")
    if not defense:
        request_creation( team, name, attack )
        return
    
    defense = int( defense )

    health = Utils.request_number( "Le nombre de PV (Nombre positive).", f"Création de Personnage ({team})" )
    if not Utils.number_isvalidpositive( health ):
        request_creation( team, name, attack, defense )
        return
    
    health = int( health )

    if team == "alliés":
        DB.create_allies( name, attack, defense, health )
    elif team == "monstre":
        DB.create_monsters( name, attack, defense, health )
    
    Utils.back_option()

def request_creations_choose_team():
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
