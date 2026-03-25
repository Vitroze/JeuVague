import function.hooks as hook

AllItems = []
class Item:
    def __init__( self, name, description ):
        self.name, self.desc = name, description

        self.activate = False
        AllItems.append(self)

    def get_name( self ):
        return self.name
    
    def get_description( self ):
        return self.desc
    
    def set_boost_damage( self, damage ):
        self.boost_damage = damage

    def set_boost_defense( self, defense ):
        self.boost_defense = defense

    def get_boost_damage( self ):
        return self.boost_damage
    
    def get_boost_defense( self ):
        return self.boost_defense
    
    def get_stats( self ):
        return self.boost_damage, self.boost_defense
    
    def activate_item( self ):
        self.activate = True
        hook.run("Item::Activate", self)
    
    def is_activate( self ):
        return self.activate
    
    def remove( self ):
        AllItems.remove( self )
        del self