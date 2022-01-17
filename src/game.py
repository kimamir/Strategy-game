from player import Player
from ai import AI
import random
from sniper import Sniper
from commando import Commando
from tank import Tank
from ravager import Ravager

"""
The Game class sets the game world and creates the players. It is also responsible for the AI's 
decision-making and stores whether a player has already moved, or attacked.
"""
class Game():

    def __init__(self):

        self.world = None
        self.players = (Player(), AI())
        self.turn = [False, False] # A list representing the available actions left this turn (moved, attacked)
        self.current_turn = self.players[0]

    def set_world(self, world):
        """
        The parameter world is a World-object.
        Stores the World-object as the Game-object's attribute
        """
        self.world = world

    def get_world(self):
        """
        Returns the game world object
        """
        return self.world

    def get_player(self):
        """
        Returns the player object
        """
        return self.players[0]

    def get_ai(self):
        """
        Returns the ai object
        """
        return self.players[1]

    def counterpick_ai_units(self):
        """
        The AI counter-picks the units (with some degree of randomness) to increase difficulty
        """
        type_list = [type(Sniper), type(Commando), type(Tank), type(Ravager)]

        for i in range(5):
            weight = random.randint(0, 1)
            if i <= len(self.world.get_player_units()) - 1:
                unit = self.world.get_player_units()[i]

            else:   # If player chooses less than 5 units, AI keeps picking up till 5
                weight_2 = random.randint(0, 3)
                unit = type_list[weight_2]

            if type(unit) is Sniper:
                if weight:
                    self.world.add_ai_unit(Tank(self.get_ai()))
                else:
                    self.world.add_ai_unit(Sniper(self.get_ai()))

            elif type(unit) is Commando:
                if weight:
                    self.world.add_ai_unit(Sniper(self.get_ai()))
                else:
                    self.world.add_ai_unit(Ravager(self.get_ai()))

            elif type(unit) is Tank:
                if weight:
                    self.world.add_ai_unit(Ravager(self.get_ai()))
                else:
                    self.world.add_ai_unit(Commando(self.get_ai()))

            else:
                if weight:
                    self.world.add_ai_unit(Commando(self.get_ai()))
                else:
                    self.world.add_ai_unit(Tank(self.get_ai()))


    def has_moved(self):
        """
        Returns True if the player has moved his/her unit during this turn.
        This is represented by self.turn[0]
        """
        return self.turn[0]

    def move(self):
        """
        Sets self.turn[0] = True to indicate the player has moved a unit this turn
        """
        self.turn[0] = True

    def has_attacked(self):
        """
        Returns True if the player has attacked with his/her unit during this turn.
        This is represented by self.turn[1]
        """
        return self.turn[1]

    def attack(self):
        """
        Sets self.turn[1] = True to indicate the player has attacked this turn
        """
        self.turn[1] = True

    def end_turn(self):
        """
        Resets the self.turn tuple. Called every time a turn ends
        """
        self.turn = [False, False]
        if type(self.current_turn) is Player:
            self.current_turn = self.players[1]
        else:
            self.current_turn = self.players[0]

    def whose_turn(self):
        """
        Returns Player or AI object depending on whose turn it is
        """
        return self.current_turn
