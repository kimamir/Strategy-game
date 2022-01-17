import copy
from unit import Unit
import random

class Tank(Unit):
    """
    The Tank unit has high hp and is heavily armoured.
    It does high damage against other tanks but is inaccurate against
    foot-soldiers.
    The tank has two attack options:
    A cannon - effective against other tanks
    A turret - moderately effective against foot soldiers
    """

    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner
        self.name = "Tank"
        self.hitpoints = 500
        self.max_hp = 500
        self.armour = 100
        self.speed = 2
        self.range = 5
        self.attack_types = [1, 2]
        self.cannon_cd = 0

    def attack_options(self):
        return "1 - Cannon: 200-300 damage, effective against tanks | 2 - Turret: 50-100 damage, effective aginst soldiers"


    def unit_description(self):
        """
        Returns a string describing the unit's hp, armour and name.
        """
        string = "{} | HP: {}/{} | Armour: {} | Range: {} | Speed: {} | Bleeding: {} | Cannon cooldown: {} ".format(self.name, self.hitpoints, self.max_hp, self.armour, self.range, self.speed, self.bleed, self.cannon_cd//2)
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
                if self.cannon_cd == 0:
                    return self.cannon(enemy), True
                else:
                    return "Your cannon can be fired in {} turns.".format(self.cannon_cd//2), False
            else:
                return self.turret(enemy), True

    def cannon(self, enemy):
        """
        A cannon has a 1 turn cooldown. If fired at a non-tank unit, the chance to hit is only 20% and the damage
        is reduced by 20%.

        """
        if type(enemy) is not Tank:
            accuracy = random.randrange(1,6)
            if accuracy == 5:
                damage = 80 * (random.randrange(200, 301) // 100)
                enemy.defend(damage)
                self.cannon_cd += 4
                return self.attack_summary(damage, enemy.get_hitpoints())

            else:
                self.cannon_cd += 4
                return "Your cannon fires... And misses!"

        else:
            damage = random.randrange(200, 301)
            enemy.defend(damage)
            self.cannon_cd += 4
            return self.attack_summary(damage, enemy.get_hitpoints())

    def turret(self, enemy):
        damage = random.randint(50, 101) - enemy.get_armour()
        enemy.defend(damage)
        return self.attack_summary(damage, enemy.get_hitpoints())


    def reduce_attack_cd(self):
        if self.cannon_cd > 0:
            self.cannon_cd -= 1

    def average_damage(self, enemy):
        """
        Calculates and returns the average damage output on enemy
        """
        if type(enemy) is Tank:
            return 250

        return 75

    def ai_attack(self, enemy):
        """
        Determines which attack does most damage to 'enemy'
        """
        attacks = []

        for attack in self.attack_types:
            temp_enemy = copy.deepcopy(enemy)
            temp_unit = copy.deepcopy(self)
            if attack == 1 and self.cannon_cd != 0:    # If cannon is on cooldown, make sure it's not useable
                attacks.append(-1)
                continue

            temp_unit.attack(temp_enemy, attack)
            damage = enemy.get_hitpoints() - temp_enemy.get_hitpoints()
            attacks.append(damage)

        attack = attacks.index(max(attacks)) + 1

        self.attack(enemy, attack)