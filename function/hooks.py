"""
    Inspiré de https://github.com/Facepunch/garrysmod/blob/master/garrysmod/lua/includes/modules/hook.lua
    Le système d'événement permet a d'autres développeurs d'intéragir avec le code sans modifier le code source.
    Pour plus de détail : 
        - https://wiki.facepunch.com/gmod/Hook_Library_Usage
        - https://wiki.facepunch.com/gmod/hook
"""
hooks = {}

def run( id:str, *args )->tuple|None:
    """Lancer un événement"""

    if not exist(id):
        return
    
    for _, callback in hooks[id].items():
        r = callback(*args)

        if r != None:
            return r
        
    return None
        
def protect_run( id:str, *args )->tuple|None:
    """Lancer un événement tout en se protégeant des erreurs qui arrête le programme"""

    if not exist(id):
        return
    
    for _, callback in hooks[id].items():
        try:
            r = callback(*args)

            if r != None:
                return r
        except (RuntimeError, TypeError, NameError):
            pass

def add( id:str, uniqueid:str, callback ):
    """Cible un événement et intéragir avec"""
    if not exist(id):
        hooks[id] = {}

    hooks[id][uniqueid] = callback

def remove( id:str, uniqueid:str ):
    """Supprime l'événement enregistré"""

    if not exist(id):
        return
    
    del hooks[id][uniqueid]

    if len(hooks[id]):
        del hooks[id]

def exist( id:str )->bool:
    """Vérifie que l'événement existe"""
    return id in hooks

#Test fonction
# def mon_message_de_mort(victim, attacker):
#     #print(f"RIP {victim}, tué par {attacker}")
#     print(victim - attacker)

#     return 5 - 10, False

# add("PlayerDeath", "Test", mon_message_de_mort)

# import time
# time.sleep(3)
# protect_run("PlayerDeath", "Yanis Marc", "Jean Michel") # No return error
# print(run("PlayerDeath", 5, 10))