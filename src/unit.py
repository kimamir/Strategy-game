"""
The Unit class is inherited by all unit subclasses as it contains many methods shared by all units.
"""

class Unit():

    def __init__(self, owner):
        self.owner = owner
        self.hitpoints = 0
        self.max_hp = 0
        self.armour = 0
        self.alive = True
        self.location = None
        self.name = "unit"
        self.speed = 0
        self.range = 0
        self.attack_types = []
        self.bleed = 0


    def get_hitpoints(self):
        """
        Returns the current hitpoints of the character
        """
        return self.hitpoints

    def get_armour(self):
        """
        Returns the character's armour points
        """
        return self.armour

    def get_owner(self):
        """
        Returns the owner of the unit (Either Player or AI)
        """
        return self.owner

    def get_max_hp(self):
        """
        Returns the unit's max hp
        """
        return self.max_hp

    def update_location(self, x, y):
        """
        Updates the unit's location on the grid
        Parameters x and y are integers
        """
        self.location = (x, y)

    def get_location(self):
        """
        Returns the location of the unit as a tuple (x,y)
        """
        return self.location

    def get_name(self):
        """
        Returns the name of the unit
        """
        return self.name

    def get_range(self):
        """
        Returns unit's range
        """
        return self.range

    def unit_description(self):
        """
        Returns a string describing the unit's hp, armour and name.
        """
        string = "{} | HP: {}/{} | Armour: {} | Range: {} | Speed: {} | Bleeding: {} ".format(self.name, self.hitpoints, self.max_hp, self.armour, self.range, self.speed, self.bleed)
        return string

    def get_speed(self):
        """
        Returns the unit's speed
        """
        return self.speed

    def defend(self, damage):
        """
        Method for reducing the hitpoints of unit being attacked.
        Sets self.alive to False if unit falls under 1 hp
        """
        if damage < 0:
            damage = 0
        self.hitpoints -= damage
        self.update_status()

    def is_alive(self):
        """
        Method that returns True if unit is above 0 hitpoints.
        Otherwise, returns False
        """
        return self.alive

    def get_attack_types(self):
        """
        Returns attack types
        """
        return self.attack_types

    def update_status(self):
        """
        Method that checks the unit's hitpoints and updates self.alive
        """
        if self.hitpoints < 1:
            self.alive = False
            self.hitpoints = 0
            self.bleed = 0

    def apply_bleed_effect(self, rounds):
        """
        Applies bleed to the unit
        :param rounds: Number of bleeding rounds to add (cannot go over 4)
        """
        if self.bleed < 3:
            self.bleed += rounds

    def take_bleeding_damage(self):
        """
        Method for taking bleeding damage.
        Bleeding damage is always 5 and occurs at the end of the round.
        """
        if self.bleed > 0:
            self.hitpoints -= 5
            self.bleed -= 1
            self.update_status()

    def attack_summary(self, damage, enemy_hp):
        """
        Returns a summary of an attack (string)
        """
        if damage < 0:
            damage = 0
        return "You did {} damage to the enemy unit, leaving it with {} hp".format(damage, enemy_hp)

    def reduce_attack_cd(self):
        """
        Overwritten in commando.py and tank.py
        """
        pass