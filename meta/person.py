class Person:
    def __init__( self, name, attack, defense, health ):
        self.name = name
        self.power_attack = attack
        self.power_defense = defense
        self.health = health

    def set_health( self, hp ):
        self.health = hp;

    def get_health( self ):
        return self.health

    def take_damage( self, Person ):
        power_attack = self.get_attack_with_defense( Person )
        self.health = max(self.health - power_attack, 0)

        print(f"{Person.get_name()} attaque {self.get_name()} et lui inflige {power_attack} dégâts")
        print(f"PV de {self.get_name()} : {self.get_health()}pv")

    
    def set_power_attack(self, power):
        self.power_attack = power

    def set_power_defense(self, power):
        self.power_defense = power

    def get_name( self ):
        return self.name
    
    def get_power_attack( self ):
        return self.power_attack
    
    def get_power_defense( self ):
        return self.power_defense
    
    def is_alive(self):
        return self.health > 0
    
    def get_attack_with_defense( self, Person ):
        return max(self.power_attack - Person.get_power_defense(), 1)
