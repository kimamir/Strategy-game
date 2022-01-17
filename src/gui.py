from PyQt5 import QtWidgets, QtCore
from unit_graphics_item import UnitGraphicsItem
from sniper import Sniper
from commando import Commando
from tank import Tank
from ravager import Ravager
from square_graphics_item import SquareGraphicsItem
import a_star
import sys
import timeit


class GUI(QtWidgets.QMainWindow):
    """
    GUI is a class that enables the drawing
    of the game world and interacting with it.
    """

    def __init__(self, game, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.vertical = QtWidgets.QVBoxLayout()  # Vertical main layout

        self.centralWidget().setLayout(self.vertical)
        self.game = game
        self.world = world
        self.square_size = square_size
        self.player_units_graphics_items = []
        self.ai_units_graphics_items = []
        self.started = False

        self.currently_selected = None  # Current UnitGraphicsItem selected (Used for moving units and attacking)
        self.defender = None  # Current UnitGraphicsItem that is getting attacked

        self.setup_window()
        self.draw_grid()
        self.setup_buttons()
        self.starting_time = 0

    def setup_window(self):
        """
        Sets up the window for the game
        """
        self.setGeometry(20, 40, 1200, 950)
        self.setWindowTitle('Strategy Game')
        self.show()

        # Sets up a scene for drawing the grid and characters
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.vertical.addWidget(self.view)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

    def draw_grid(self):
        """
        Creates a QGraphicsItem for each tile in the grid.
        Empty squares are drawn in light gray (211, 211, 211)
        Obstacles are drawn in black (0, 0, 0)
        """

        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                square = self.world.get_square(x, y)

                if square.is_obstacle():
                    square_gui = SquareGraphicsItem(x, y, self.square_size, self, 1)

                else:
                    square_gui = SquareGraphicsItem(x, y, self.square_size, self, 0)

                self.scene.addItem(square_gui)

    def setup_buttons(self):
        """
        Adds buttons to the window and connects them to their respective functions
        """
        self.sniper_btn = QtWidgets.QPushButton("Add Sniper")
        self.sniper_btn.clicked.connect(lambda: self.add_units_graphics_item(Sniper(self.game.get_player())))
        self.vertical.addWidget(self.sniper_btn)

        self.commando_btn = QtWidgets.QPushButton("Add Commando")
        self.commando_btn.clicked.connect(lambda: self.add_units_graphics_item(Commando(self.game.get_player())))
        self.vertical.addWidget(self.commando_btn)

        self.tank_btn = QtWidgets.QPushButton("Add Tank")
        self.tank_btn.clicked.connect(lambda: self.add_units_graphics_item(Tank(self.game.get_player())))
        self.vertical.addWidget(self.tank_btn)

        self.ravager_btn = QtWidgets.QPushButton("Add Ravager")
        self.ravager_btn.clicked.connect(lambda: self.add_units_graphics_item(Ravager(self.game.get_player())))
        self.vertical.addWidget(self.ravager_btn)

        self.start_btn = QtWidgets.QPushButton("Start Game")
        self.start_btn.clicked.connect(lambda: self.add_ai_units_and_start_game())
        self.vertical.addWidget(self.start_btn)

    def add_units_graphics_item(self, unit):
        """
        Creates a UnitGraphicsItem for the unit and adds it to the scene
        :param unit: Unit-object
        """
        if len(self.player_units_graphics_items) < 5:
            self.world.add_unit_to_battlefield(unit)
            item = UnitGraphicsItem(unit, self.square_size, 0, self)
            self.scene.addItem(item)
            self.player_units_graphics_items.append(item)

    def add_ai_units_and_start_game(self):
        """
        Adds ai units and creates a UnitGraphicsItem for each of them
        """
        self.world.reset_first_index()
        self.game.counterpick_ai_units()
        for unit in self.world.get_ai_units():
            self.world.add_unit_to_battlefield(unit)
            item = UnitGraphicsItem(unit, self.square_size, 1, self)  # 1 means the owner is the AI
            self.scene.addItem(item)
            self.ai_units_graphics_items.append(item)

        self.remove_starting_buttons()  # Removes buttons that add units
        self.world.update_square_neighbours()  # Update square neighbours now that all units have been added

        self.started = True  # Units can be now interacted with

        self.end_turn_btn = QtWidgets.QPushButton("End turn")
        self.end_turn_btn.clicked.connect(lambda: self.end_current_turn(True))
        self.vertical.addWidget(self.end_turn_btn)

        self.attack_options_btn = QtWidgets.QPushButton("Print attack options")
        self.attack_options_btn.clicked.connect(lambda: self.print_attack_options())
        self.vertical.addWidget(self.attack_options_btn)

        self.starting_time = timeit.default_timer()  # timer

    def end_current_turn(self, player):
        """
        Resets movement and attack counters and unselects currently selected unit.
        Loops over all units and reduces their hp by 5 if they are bleeding. Removes units that die from bleed.
        Parameter 'player' is True if the player's turn just ended and False if the AI's turn did.
        """
        self.game.end_turn()
        for item in self.player_units_graphics_items:
            unit = item.get_unit()
            unit.take_bleeding_damage()
            unit.reduce_attack_cd()  # Reduces bazooka cd if unit is a commando or a tank, otherwise does nothing

            if not unit.is_alive():
                self.world.remove_unit(unit, 0)
                self.player_units_graphics_items.remove(item)
                self.scene.removeItem(item)

        for item in self.ai_units_graphics_items:
            unit = item.get_unit()
            unit.take_bleeding_damage()
            unit.reduce_attack_cd()

            if not unit.is_alive():
                self.world.remove_unit(unit, 1)
                self.ai_units_graphics_items.remove(item)
                self.scene.removeItem(item)

        self.reset_selected_units()
        self.game_over()  # Checks if game is over

        if player:
            self.ai_turn()  # AI plays its turn

    def print_attack_options(self):
        """
        Prints the attack options of every unique unit on the battlefield
        """
        printed = []
        for item in self.player_units_graphics_items:
            unit = item.get_unit()
            if type(unit) not in printed:
                print(unit.get_name())
                print(unit.attack_options() + "\n")
                printed.append(type(unit))

        for item in self.ai_units_graphics_items:
            unit = item.get_unit()
            if type(unit) not in printed:
                print(unit.attack_options())
                printed.append(type(unit))

    def remove_starting_buttons(self):
        """
        Removes the buttons for adding new units as they are no longer needed
        """
        self.sniper_btn.deleteLater()
        self.commando_btn.deleteLater()
        self.tank_btn.deleteLater()
        self.ravager_btn.deleteLater()
        self.start_btn.deleteLater()

    def set_selected_unit(self, unit_graphics_item):
        """
        This method sets self.currently_selected to parameter unit_graphics_item
        """
        self.currently_selected = unit_graphics_item

    def reset_selected_units(self):
        """
        Sets self.currently_selected and self.defender to None
        """
        self.currently_selected = None
        self.defender = None

    def move_unit(self, x, y, unit):
        """
        Moves currently_selected unit to square in coordinates (x,y) if possible.
        """

        if self.world.get_square(x, y).is_free() and unit.get_owner() == self.game.whose_turn():
            current_location = unit.get_location()  # Unit's current location (x,y) tuple

            if a_star.a_star(self.world.get_grid(), self.world.get_square(current_location[0], current_location[1]),
                             self.world.get_square(x, y), False) <= unit.get_speed():
                self.world.get_square(current_location[0], current_location[1]).remove_unit_from_square()
                self.world.get_square(x, y).add_unit_to_square(unit)
                unit.update_location(x, y)
                self.currently_selected.update_position()

                self.world.update_square_neighbours()
                self.game.move()  # Makes it so you can't move anymore this turn

                self.reset_selected_units()

                self.statusBar.showMessage("", 1)

            else:
                self.statusBar.showMessage("This unit can't move that far!")

        else:
            self.statusBar.showMessage("This tile is occupied! Try a different one!")

    def attack(self, p_unit, e_unit):
        """
        :param p_unit: Attacking unit (UnitGraphicsItem)
        :param e_unit: Unit getting attacked (UnitGraphicsItem)

        Sets self.defender = e_unit
        Prints attack options of p_unit onto the status bar.
        Attacking is then performed via keyPressEvent
        """
        player_location = p_unit.get_unit().get_location()  # coordinates of attacking unit
        enemy_location = e_unit.get_unit().get_location()  # coordinates of defending unit
        x_diff = abs(player_location[1] - enemy_location[1])
        y_diff = abs(player_location[0] - enemy_location[0])

        if max(x_diff, y_diff) <= p_unit.get_unit().get_range():  # Check range

            if not self.world.line_of_sight(player_location, enemy_location):  # Check line of sight
                self.statusBar.showMessage("You don't have line of sight!", 1000)

            else:
                self.defender = e_unit
                self.statusBar.showMessage(p_unit.get_unit().attack_options())

        else:
            self.statusBar.showMessage("That unit is out of your range!", 1000)

    def keyPressEvent(self, key):
        """
        Rewriting keyPressEvent for attacking options
        """
        status = False  # False if a nonexistent attack option was chosen
        message = ""  # Attack summary (str)

        if self.currently_selected is not None and self.defender is not None:

            if key.key() == QtCore.Qt.Key_1:
                message, status = self.currently_selected.get_unit().attack(self.defender.get_unit(), 1)

            elif key.key() == QtCore.Qt.Key_2:
                message, status = self.currently_selected.get_unit().attack(self.defender.get_unit(), 2)

            elif key.key() == QtCore.Qt.Key_3:
                message, status = self.currently_selected.get_unit().attack(self.defender.get_unit(), 3)

            if status:
                self.statusBar.showMessage(message, 10000)  # Attack summary
                self.game.attack()  # Upon a successful attack, count it

                if not self.defender.get_unit().is_alive():
                    self.world.remove_unit(self.defender.get_unit(), 1)
                    self.ai_units_graphics_items.remove(self.defender)
                    self.scene.removeItem(self.defender)

            else:
                self.statusBar.showMessage(message, 10000)  # Failure message

            self.reset_selected_units()

    def ai_turn(self):
        """
        A method for the AI's turn
        """
        unit, square = self.world.get_best_move()

        if unit is not None:
            for unit_item in self.ai_units_graphics_items:
                if unit_item.get_unit() == unit:
                    self.currently_selected = unit_item
            x, y = square.get_location()
            self.move_unit(x, y, unit)

        unit, enemy = self.world.ai_attack()

        if unit is not None and enemy is not None:
            unit.ai_attack(enemy)
            self.statusBar.showMessage("An enemy {} attacked your {}, leaving it with {} HP".format(unit.get_name(), enemy.get_name(), enemy.get_hitpoints()), 10000)
            for enemy_item in self.ai_units_graphics_items:
                if enemy_item.get_unit() == enemy:
                    self.defender = enemy_item

                    if not self.defender.get_unit().is_alive():
                        self.world.remove_unit(self.defender.get_unit(), 1)
                        self.ai_units_graphics_items.remove(self.defender)
                        self.scene.removeItem(self.defender)

        self.end_current_turn(False)

    def game_over(self):
        if len(self.ai_units_graphics_items) == 0:
            print("You won!")
            print("The game lasted {} minutes and {} seconds.".format(
                int((timeit.default_timer() - self.starting_time) // 60),
                int((timeit.default_timer() - self.starting_time) % 60)))
            sys.exit()


        elif len(self.player_units_graphics_items) == 0:
            print("You lost!")
            print("The game lasted {} minutes and {} seconds.".format(
                int((timeit.default_timer() - self.starting_time) // 60),
                int((timeit.default_timer() - self.starting_time) % 60)))
            sys.exit()
