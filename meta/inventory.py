import function.utils as Utils
import function.hooks as hook

class Inventory:
    def __init__( self, capacity:int=10 ):
        self.items = []
        self.person = None
        self.capacity = capacity

    def get_inventory( self ):
        return self.items
    
    def get_capacity( self ):
        return self.capacity
    
    def get_count_items( self ):
        return len(self.items)

    def can_add( self ):
        if self.get_count_items() > self.get_capacity():
            return False, "Vous avez plus de place dans votre inventaire"

        result = hook.run("Inventory::CanAdd", self.items)
        if result != None:
            r, error = result
            if r == False:
                return False, error

        return True, ""

    def set_item( self, item ):
        if not Utils.item_isvalid( item ):
            Utils.PrintError("Inventaire", "L'item n'existe pas")
            return
        
        passed, error = self.can_add()
        if not passed:
            Utils.PrintError("Inventaire", error or "Impossible de rajouter l'objet dans l'inventaire")
            return

        newindex = self.get_count_items() + 1
        self.items.append(item)

        return newindex
    
    def exist_items( self, slot ):
        return self.items in slot
    
    def get_item( self, slot ):
        if not self.exist_items( slot ):
            Utils.PrintError("Inventaire", "Impossible de trouver l'item")
            return
        
        return self.items[slot]
    
    def can_remove( self, slot ):
        if slot < 0 or slot > self.get_capacity():
            return False, "Vous ne pouvez pas supprimer un item en dehors de la capacité de l'inventaire"

        if not self.exist_items( slot ):
            return False, "Impossible de trouver l'item"

        result = hook.run("Inventory::CanRemove", self.items)
        if result != None:
            r, error = result
            if r == False:
                return False, error

        return True
    
    def remove_item( self, slot ):
        passed, error = self.can_remove( self, slot )
        if not passed:
            Utils.PrintError("Inventaire", error or "Impossible de supprimer l'objet de l'inventaire")
            return
        
        del self.items[slot]
    
    def reset( self ):
        del self.items