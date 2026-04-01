"""
    Inspiré de https://github.com/Facepunch/garrysmod/blob/master/garrysmod/lua/includes/modules/hook.lua
    Le système d'événement permet a d'autres développeurs d'intéragir avec le code sans modifier le code source.
"""
hooks = {}

def run(id, *args):
    if not exist(id):
        return
    
    for _, callback in hooks[id].items():
        r = callback(*args)

        if r != None:
            return r
        
def protect_run(id, *args):
    if not exist(id):
        return
    
    for _, callback in hooks[id].items():
        try:
            r = callback(*args)

            if r != None:
                return r
        except (RuntimeError, TypeError, NameError):
            pass

def add(id, uniqueid, callback):
    if not exist(id):
        hooks[id] = {}

    hooks[id][uniqueid] = callback

def remove(id, uniqueid):
    if not exist(id):
        return
    
    del hooks[id][uniqueid]

    if len(hooks[id]):
        del hooks[id]

def exist(id):
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