from PyQt5 import QtWidgets, QtGui, QtCore
from sniper import Sniper
from commando import Commando
from tank import Tank


class UnitGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class UnitGraphicsItem uses QGraphicsPolygonItem to create
    physical illustrations of the unit types.
    Parameter unit is a Unit-object
    Parameter square_size is the grid's square size
    Parameter owner is either 0 or 1 (0 indicates the unit belongs to the player and should be painted green)
    1 indicates the unit belongs to the AI and should be painted red.
    """

    def __init__(self, unit, square_size, owner, gui):
        super().__init__()
        self.owner = owner
        self.unit = unit
        self.square_size = square_size
        self.construct()
        self.brush = None
        self.gui = gui

    def construct(self):
        if self.owner == 0:
            self.brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        else:
            self.brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))

        if type(self.unit) is Sniper:
            self.add_sniper()
        elif type(self.unit) is Commando:
            self.add_commando()
        elif type(self.unit) is Tank:
            self.add_tank()
        else:
            self.add_ravager()

    def add_sniper(self):
        sniper = QtGui.QPolygonF()

        # The sniper is represented by an arrow
        sniper.append(QtCore.QPointF(1 / 3 * self.square_size, self.square_size))
        sniper.append(QtCore.QPointF(1 / 3 * self.square_size, 1 / 2 * self.square_size))
        sniper.append(QtCore.QPointF(1 / 6 * self.square_size, 1 / 2 * self.square_size))
        sniper.append(QtCore.QPointF(1 / 2 * self.square_size, 0))
        sniper.append(QtCore.QPointF(5 / 6 * self.square_size, 1 / 2 * self.square_size))
        sniper.append(QtCore.QPointF(2 / 3 * self.square_size, 1 / 2 * self.square_size))
        sniper.append(QtCore.QPointF(2 / 3 * self.square_size, self.square_size))
        sniper.append(QtCore.QPointF(1 / 3 * self.square_size, self.square_size))

        self.setPolygon(sniper)
        QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, self.brush)

        self.update_position()
        if self.owner == 1:
            self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)
            self.setRotation(180)

    def add_commando(self):
        commando = QtGui.QPolygonF()

        # The commando is represented by an X-shape
        commando.append(QtCore.QPointF(1 / 5 * self.square_size, self.square_size))
        commando.append(QtCore.QPointF(1 / 2 * self.square_size, 7 / 10 * self.square_size))
        commando.append(QtCore.QPointF(4 / 5 * self.square_size, self.square_size))
        commando.append(QtCore.QPointF(self.square_size, 4 / 5 * self.square_size))
        commando.append(QtCore.QPointF(7 / 10 * self.square_size, 1 / 2 * self.square_size))
        commando.append(QtCore.QPointF(self.square_size, 1 / 5 * self.square_size))
        commando.append(QtCore.QPointF(4 / 5 * self.square_size, 0))
        commando.append(QtCore.QPointF(1 / 2 * self.square_size, 3 / 10 * self.square_size))
        commando.append(QtCore.QPointF(1 / 5 * self.square_size, 0))
        commando.append(QtCore.QPointF(0, 1 / 5 * self.square_size))
        commando.append(QtCore.QPointF(3 / 10 * self.square_size, 1 / 2 * self.square_size))
        commando.append(QtCore.QPointF(0, 4 / 5 * self.square_size))
        commando.append(QtCore.QPointF(1 / 5 * self.square_size, self.square_size))

        self.setPolygon(commando)
        QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, self.brush)
        self.update_position()

    def add_tank(self):
        tank = QtGui.QPolygonF()

        # The tank is represented by a tank-like polygon
        tank.append(QtCore.QPointF(0, self.square_size))
        tank.append(QtCore.QPointF(self.square_size, self.square_size))
        tank.append(QtCore.QPointF(self.square_size, 3 / 8 * self.square_size))
        tank.append(QtCore.QPointF(5 / 8 * self.square_size, 3 / 8 * self.square_size))
        tank.append(QtCore.QPointF(5 / 8 * self.square_size, 0))
        tank.append(QtCore.QPointF(3 / 8 * self.square_size, 0))
        tank.append(QtCore.QPointF(3 / 8 * self.square_size, 3 / 8 * self.square_size))
        tank.append(QtCore.QPointF(0, 3 / 8 * self.square_size))
        tank.append(QtCore.QPointF(0, self.square_size))

        self.setPolygon(tank)
        QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, self.brush)
        self.update_position()

        if self.owner == 1:
            self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)
            self.setRotation(180)

    def add_ravager(self):
        ravager = QtGui.QPolygonF()

        # The ravager unit is represented by a fist-shaped polygon
        ravager.append(QtCore.QPointF(1 / 3 * self.square_size, self.square_size))
        ravager.append(QtCore.QPointF(1 / 3 * self.square_size, 1 / 2 * self.square_size))
        ravager.append(QtCore.QPointF(1 / 6 * self.square_size, 1 / 3 * self.square_size))
        ravager.append(QtCore.QPointF(1 / 6 * self.square_size, 1 / 6 * self.square_size))
        ravager.append(QtCore.QPointF(3 / 12 * self.square_size, 0))
        ravager.append(QtCore.QPointF(4 / 12 * self.square_size, 1 / 6 * self.square_size))
        ravager.append(QtCore.QPointF(5 / 12 * self.square_size, 0))
        ravager.append(QtCore.QPointF(1 / 2 * self.square_size, 1 / 6 * self.square_size))
        ravager.append(QtCore.QPointF(7 / 12 * self.square_size, 0))
        ravager.append(QtCore.QPointF(8 / 12 * self.square_size, 1 / 6 * self.square_size))
        ravager.append(QtCore.QPointF(9 / 12 * self.square_size, 0))
        ravager.append(QtCore.QPointF(10 / 12 * self.square_size, 1 / 6 * self.square_size))
        ravager.append(QtCore.QPointF(10 / 12 * self.square_size, 1 / 3 * self.square_size))
        ravager.append(QtCore.QPointF(8 / 12 * self.square_size, 1 / 2 * self.square_size))
        ravager.append(QtCore.QPointF(2 / 3 * self.square_size, self.square_size))
        ravager.append(QtCore.QPointF(1 / 3 * self.square_size, self.square_size))

        self.setPolygon(ravager)
        QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, self.brush)
        self.update_position()

        if self.owner == 1:
            self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)
            self.setRotation(180)

    def update_position(self):
        location = self.unit.get_location()
        x = location[0]
        y = location[1]
        self.setPos(y * self.square_size, x * self.square_size)

    def get_unit(self):
        """
        Returns the Unit-object of this UnitGraphicsItem
        """
        return self.unit

    def mousePressEvent(self, event):
        """
        Overrides mousePressEvent.
        This method is called every time a unit is clicked.
        """
        self.gui.statusBar.showMessage(self.unit.unit_description(), 10000)

        if self.owner == 0:  # If the player is the owner, give the ability to move units. Otherwise, print unit info

            if self.gui.currently_selected != self:
                if self.gui.started:
                    self.gui.set_selected_unit(self)
            else:
                self.gui.currently_selected = None
                self.gui.statusBar.showMessage("Unselected", 1000)

        else:

            if self.gui.currently_selected is not None and not self.gui.game.has_attacked():
                self.gui.attack(self.gui.currently_selected, self)

            elif self.gui.currently_selected is not None and self.gui.game.has_attacked():
                self.gui.statusBar.showMessage("You have already attacked this turn!", 1000)

