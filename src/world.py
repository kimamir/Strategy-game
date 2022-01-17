from square import Square
from player import Player
from sniper import Sniper
from commando import Commando
from ravager import Ravager
import a_star
import random

"""
The class variable FIRST_UNIT_INDEX indicates the (x-axis) index in which to place the first unit
in the method add_units_to_battlefield().

The class variable NO_UNITS_PER_PLAYER determines how many units each
player is allowed to assign to the battlefield
"""


class World():
    FIRST_UNIT_INDEX = 0
    NO_UNITS_PER_PLAYER = 5

    def __init__(self, width, height):

        self.grid = [None] * width
        for x in range(width):
            self.grid[x] = [None] * height
            for y in range(height):
                self.grid[x][y] = Square(x, y)  # Fills every square of the grid with a Square object

        self.player_units = []  # A list of unit-objects owned by the player
        self.ai_units = []  # A list of unit-objects owned by the AI

    def get_width(self):
        """
        Returns the width of the grid in squares (int).
        """
        return len(self.grid)

    def get_height(self):
        """
        Returns the height of the grid in squares (int).
        """
        return len(self.grid[0])

    def get_square(self, x, y):
        """
        Returns the Square-object in given coordinates (x,y).
        """
        return self.grid[x][y]

    def add_obstacles(self):
        """
        Adds walls to randomly chosen squares.
        The number of walls to be added is determined by the grid's width
        Obstacles cannot be generated on the outer edges of the grid.
        """
        # random.seed(100)  # used for testing, will be removed in the final version
        width = self.get_width()

        for i in range(width):
            self.grid[random.randint(1, width - 2)][random.randint(1, width - 2)].turn_into_obstacle()

    def add_unit_to_battlefield(self, unit):
        """
        This method adds a unit to the battlefield.
        When the battlefield is empty, it calculates the index for the first unit to be placed
        in such way that the units are placed in the middle of the horizontal line with varying grid sizes.

        The method also ensures that the player cannot place more than 5 units on the field.
        :param unit: Sniper/Commando/Tank/Ravager-object
        """
        if World.FIRST_UNIT_INDEX == 0:
            World.FIRST_UNIT_INDEX = (self.get_width() // 2) - (World.NO_UNITS_PER_PLAYER // 2)

        if isinstance(unit.get_owner(), Player):  # Check if the player owns the piece
            if len(self.player_units) < 5:  # Check if the player has already placed 5 pieces
                square = self.get_square(self.get_height() - 1, World.FIRST_UNIT_INDEX)
                unit.update_location(self.get_height() - 1, World.FIRST_UNIT_INDEX)
                square.add_unit_to_square(unit)
                self.player_units.append(unit)
                World.FIRST_UNIT_INDEX += 1



        else:  # If the AI owns the piece
            square = self.get_square(0, World.FIRST_UNIT_INDEX)
            unit.update_location(0, World.FIRST_UNIT_INDEX)
            square.add_unit_to_square(unit)
            World.FIRST_UNIT_INDEX += 1

    def get_player_units(self):
        """
        Returns a list of units owned by player
        """
        return self.player_units

    def get_ai_units(self):
        """
        Returns a list of units owned by AI
        """
        return self.ai_units

    def add_ai_unit(self, unit):
        """
        Appends a unit-object to the ai's forces
        """
        self.ai_units.append(unit)

    def reset_first_index(self):
        """
        Resets the class variable FIRST_UNIT_INDEX to 0
        """
        World.FIRST_UNIT_INDEX = 0

    def update_square_neighbours(self):
        for row in self.grid:
            for square in row:
                square.update_neighbours(self.grid, self.get_width(), self.get_height())

    def get_grid(self):
        """
        Returns the world grid
        """
        return self.grid

    def remove_unit(self, unit, player):
        """
        Removes a dead unit from the world.

        :param unit: Unit to be removed
        :param player (int): 0 if the unit belongs to the player, 1 for AI
        """
        location = unit.get_location()
        square = self.get_square(location[0], location[1])
        square.remove_unit_from_square()

        if player == 0:
            self.player_units.remove(unit)

        else:
            self.ai_units.remove(unit)

        self.update_square_neighbours()

    def line_of_sight(self, start, end):
        """
        A modified Bresenham's Line Algorithm
        start and end are tuples of (x,y) coordinates.
        If there is a wall between them, return False. Otherwise return True.
        """
        width = self.get_width()
        height = self.get_height()

        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is (True if slope is larger than 1. False otherwise)
        is_steep = abs(dy) > abs(dx)

        # Rotate line around y = x to get a slope larger than 1
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        # Recalculate differentials (Doesn't change anything if start and end weren't swapped)
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        if ystep == -1 and x1 < x2:
            offsetx = [0, 1]
            offsety = [-1, 0]
            # Left descending

        elif ystep == -1 and x1 > x2:
            offsetx = [0, -1]
            offsety = [-1, 0]
            # Left ascending

        elif ystep == 1 and x1 < x2:
            offsetx = [0, 1]
            offsety = [1, 0]
            # Right descending

        else:
            offsetx = [0, -1]
            offsety = [1, 0]
            # Right ascending

        # Iterate over bounding box generating points between start and end
        y = y1

        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            neighbours = 0

            if self.grid[coord[0]][
                coord[1]].is_obstacle():  # If current tile is a wall, there is no line of sight, return False
                return False

            for i in range(2):
                nx = coord[0] + offsetx[i]
                ny = coord[1] + offsety[i]
                if nx < 0 or nx > width - 1 or ny < 0 or ny > height - 1:
                    continue
                if self.grid[nx][ny].is_obstacle():
                    neighbours += 1

            if neighbours == 2:
                return False

            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        return True

    def get_best_move(self):
        """
        Loops over all possible moves.
        Best move is defined here as one that gets you in range and line of sight to attack
        """
        moves = []
        for unit in self.ai_units:
            can_att = False
            for enemy in self.player_units:
                if self.can_attack(unit, enemy):
                    can_att = True
            if can_att:  # If unit can attack an enemy, it shouldn't move
                continue

            square, enemy = self.move_closer(unit)
            if square is not None:  # If unit can move closer
                moves.append((unit, square)) # remember the unit, square and enemy

        for move in moves:
            if self.can_attack_from_square(move[0], move[1]):
                return move[0], move[1]

        if len(moves) > 0:
            return moves[0][0], moves[0][1]

        return None, None

    def can_attack_from_square(self, unit, square):
        x, y = square.get_location()

        for enemy in self.player_units:
            delta_x = abs(x - enemy.get_location()[0])
            delta_y = abs(y - enemy.get_location()[1])

            if max(delta_x, delta_y) <= unit.get_range():
                if self.line_of_sight((x,y), enemy.get_location()):
                    return True

        return False


    def can_move(self, unit, square):
        """
        Returns True if unit can move to square
        Returns False otherwise
        """

        if not square.is_free():
            return False
        xs, ys = square.get_location()
        xu, yu = unit.get_location()[0], unit.get_location()[1]
        distance = abs(xs - xu) + abs(ys - yu)  # Manhattan distance

        if distance > unit.get_speed():
            return False

        if a_star.a_star(self.grid, self.get_square(xu, yu), self.get_square(xs, ys), False) <= unit.get_speed():
            return True

        return False

    def move_closer(self, unit):
        """
        Finds closest enemy to unit (Manhattan distance) and returns the closest square that 'unit' can move to
        """
        xu = unit.get_location()[0]
        yu = unit.get_location()[1]
        closest = None  # closest enemy
        distance = float("inf")

        for enemy in self.player_units:
            delta_x = abs(xu - enemy.get_location()[0])
            delta_y = abs(yu - enemy.get_location()[1])
            temp_dist = delta_y + delta_x
            if temp_dist < distance:
                distance = temp_dist
                closest = enemy

        enemy_square = self.get_square(closest.get_location()[0], closest.get_location()[1])
        for neighbour in enemy_square.get_neighbours():
            path, success = a_star.a_star(self.grid, self.get_square(xu, yu), neighbour, True)
            if success:
                for square in path:
                    if self.can_move(unit, square):
                        return square, closest

        return None, None

    def counters(self, unit, p_unit):
        """
        Returns True if unit counters p_unit, False otherwise
        """
        if type(unit) is Ravager or type(unit) is Commando:
            return True
        elif type(unit) is type(p_unit):
            return True
        elif type(unit) is Sniper:
            if type(p_unit) is Commando or type(p_unit) is Ravager:
                return True

        return False

    def can_kill(self, unit, p_unit):
        """
        Determines whether unit can kill p_unit
        """
        if p_unit.get_hitpoints() - unit.average_damage(p_unit) <= 0:
            return True
        else:
            return False

    def can_attack(self, unit, enemy):
        """
        Method that checks if unit can attack enemy
        """
        delta_x = abs(unit.get_location()[0] - enemy.get_location()[0])
        delta_y = abs(unit.get_location()[1] - enemy.get_location()[1])
        if not max(delta_x, delta_y) <= unit.get_range():
            return False

        if self.line_of_sight(unit.get_location(), enemy.get_location()):
            return True

        return False

    def best_attack(self, unit, enemy):
        """
        Returns a score based on current hp of 'enemy' and average damage dealt by unit
        """
        score = 0
        if enemy.get_hitpoints() < enemy.get_max_hp():
            score += 10

        if self.counters(unit, enemy):
            score += 10

        score += int((unit.average_damage(enemy) * 100) // 1)

        return score

    def ai_attack(self):
        """
        Finds the ai unit that should attack this turn and player unit to be attacked
        """
        score = 0
        attacks = {}

        for unit in self.ai_units:
            for enemy in self.player_units:

                if self.can_attack(unit, enemy):
                    if self.can_kill(unit, enemy):
                        return unit, enemy

                    temp_score = self.best_attack(unit, enemy)
                    if temp_score > score:
                        score = temp_score
                    attacks[temp_score] = (unit, enemy)

        if len(attacks) > 0:
            return attacks[score]

        return None, None
