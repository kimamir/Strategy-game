import copy
from unit import Unit
import random


class Ravager(Unit):
    """
    The Ravager unit is a close-combat fighter with high hp but no armour.
    It can deal devastating damage to any type of unit but it has to get up close.
    """

    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner
        self.name = "Ravager"
        self.hitpoints = 300
        self.max_hp = 300
        self.armour = 0
        self.speed = 4
        self.range = 1
        self.attack_types = [1, 2]
        self.armour_boost = False  # Prevents players from spamming the Roar-attack and making a Ravager too tanky

    def attack_options(self):
        return "1 - Punch: 100-300 damage, unaffected by armour | 2 - Roar: Increase own armour by 20"

    def attack(self, enemy, attack_type):
        """
        Method for attacking another unit

        :param enemy: Enemy unit to attack
        :param attack_type: The attack type (int)
        :return: String describing the attack and damage AND a boolean indicating whether the attack succeeded or failed
        """

        if attack_type not in self.attack_types:
            return "This attack style doesn't exist", False

        else:
            if attack_type == 1:
                return self.punch(enemy), True

            else:

                if not self.armour_boost:
                    return self.roar(), True

                else:
                    return "You have already increased this unit's armour", False

    def punch(self, enemy):
        """
        Method for calculating punch damage
        """

        damage = random.randrange(100, 301)
        enemy.defend(damage)
        return self.attack_summary(damage, enemy.get_hitpoints())

    def roar(self):
        self.armour += 20
        self.armour_boost = True
        return "The Ravager roars and increases its armour by 20"

    def average_damage(self, enemy):
        """
        Calculates and returns the average damage output on enemy
        """
        return 200

    def ai_attack(self, enemy):
        """
        Determines which attack does most damage to 'enemy'
        """
        attacks = []

        for attack in self.attack_types:
            temp_enemy = copy.deepcopy(enemy)
            temp_unit = copy.deepcopy(self)

            temp_unit.attack(temp_enemy, attack)
            damage = enemy.get_hitpoints() - temp_enemy.get_hitpoints()
            attacks.append(damage)

        attack = attacks.index(max(attacks)) + 1

        self.attack(enemy, attack)
