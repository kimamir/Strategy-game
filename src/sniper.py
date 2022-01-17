import copy

from unit import Unit
import random

class Sniper(Unit):

    def __init__(self, owner):
        """
        The sniper unit has low hp and low armour.
        It is very effective against unarmoured and lightly armoured targets
        but can be easily eliminated if not careful.
        The sniper uses a sniper rifle that causes a bleeding effect
        """

        super().__init__(owner)
        self.name = "Sniper"
        self.hitpoints = 150
        self.max_hp = 150
        self.armour = 20
        self.speed = 2
        self.range = 8
        self.attack_types = [1]

    def attack_options(self):
        return "1 - Snipe: 90-110 damage, causes bleed"

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
            return self.snipe(enemy), True

    def snipe(self, enemy):

        damage = random.randrange(90, 111) - enemy.get_armour()
        enemy.defend(damage)
        if enemy.is_alive():
            enemy.apply_bleed_effect(2)

        return self.attack_summary(damage, enemy.get_hitpoints())


    def average_damage(self, enemy):
        """
        Calculates and returns the average damage output on enemy
        """
        return (100 - enemy.get_armour()) + 10

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

