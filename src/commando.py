import copy
from unit import Unit
from tank import Tank
import random

class Commando(Unit):
    """
    The commando unit has moderate hp and light armour.
    This unit is able to use a
    bazooka - effective against armoured targets
    rifle - effective against unarmoured targets
    knife - effective against unarmoured targets (also applies a bleeding effect)
    """

    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner
        self.name = "Commando"
        self.hitpoints = 350
        self.max_hp = 350
        self.armour = 10
        self.speed = 5
        self.range = 3
        self.attack_types = [1, 2, 3]
        self.bazooka_cd = 0     # How many turns the player must wait before he can attack with bazooka again

    def attack_options(self):
        return "1 - Bazooka: 300-350 damage, effective against tanks | 2 - Rifle: 100-149 damage, effective against " \
               "soldiers | 3 - Throwing knife: 200-300 damage, applies bleed, 50% chance to hit"

    def unit_description(self):
        """
        Returns a string describing the unit's hp, armour and name.
        Overwriting the default description to add bazooka cooldown counter.
        """
        string = "{} | HP: {}/{} | Armour: {} | Range: {} | Speed: {} | Bleeding: {} | Bazooka cooldown: {}".format(self.name, self.hitpoints, self.max_hp, self.armour, self.range, self.speed, self.bleed, self.bazooka_cd // 2)
        return string

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
                if self.bazooka_cd != 0:
                    return "You cannot use bazooka for {} more turns".format(self.bazooka_cd // 2), False
                else:
                    return self.bazooka(enemy), True

            elif attack_type == 2:
                return self.rifle(enemy), True

            else:
                return self.throwing_knife(enemy), True

    def bazooka(self, enemy):
        """
        Method for the bazooka attack. Bazooka has a 2-turn cooldown and has only a 33% chance to hit
        if used against a unit that is not a Tank. It also deals 25% damage to any unit other than a tank.
        """
        if type(enemy) is Tank:
            damage = random.randrange(300, 351)
            enemy.defend(damage)
            self.bazooka_cd += 6

            return self.attack_summary(damage, enemy.get_hitpoints())

        else:
            accuracy = random.randrange(1, 4)   # The hit misses if the accuracy roll is 1 or 2

            if accuracy == 3:
                damage = random.randrange(300, 351) // 4
                enemy.defend(damage)
                self.bazooka_cd += 6

                return self.attack_summary(damage, enemy.get_hitpoints())

            else:
                self.bazooka_cd += 6
                return "Your attack misses and the enemy laughs at you!"

    def rifle(self, enemy):
        damage = random.randrange(100, 151) - enemy.get_armour()
        enemy.defend(damage)
        return self.attack_summary(damage, enemy.get_hitpoints())

    def throwing_knife(self, enemy):
        if type(enemy) is Tank:
            return "Your knife bounces off the hard shell of the tank and does nothing..."

        else:
            accuracy = random.randrange(1,3)
            if accuracy == 2:
                damage = random.randrange(200, 301) - enemy.get_armour()
                enemy.defend(damage)
                if enemy.is_alive():
                    enemy.apply_bleed_effect(4)

                return self.attack_summary(damage, enemy.get_hitpoints())
            else:
                return "Your throwing knife misses!"

    def reduce_attack_cd(self):
        """
        Method for reducing bazooka cooldown after each turn.
        """
        if self.bazooka_cd > 0:
            self.bazooka_cd -= 1

    def average_damage(self, enemy):
        """
        Calculates and returns the average damage output on enemy
        """
        if type(enemy) is Tank:
            if self.bazooka_cd == 0:
                return 325
            else:
                return 125 - enemy.get_armour()
        else:
            return 125 - enemy.get_armour()

    def ai_attack(self, enemy):
        """
        Determines which attack does most damage to 'enemy'
        """
        attacks = []

        for attack in self.attack_types:
            temp_enemy = copy.deepcopy(enemy)
            temp_unit = copy.deepcopy(self)
            if attack == 1 and self.bazooka_cd != 0:    # If bazooka is on cooldown, make sure it's not useable
                attacks.append(-1)
                continue

            temp_unit.attack(temp_enemy, attack)
            damage = enemy.get_hitpoints() - temp_enemy.get_hitpoints()
            attacks.append(damage)

        attack = attacks.index(max(attacks)) + 1

        self.attack(enemy, attack)