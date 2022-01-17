from PyQt5 import QtWidgets, QtGui

class SquareGraphicsItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, x, y, square_size, gui, colour):
        super().__init__()
        self.square_size = square_size
        self.gui = gui
        self.x = x
        self.y = y
        self.colour = colour
        self.construct()


    def construct(self):
        self.setRect(self.y * self.square_size, self.x * self.square_size, self.square_size, self.square_size)
        if self.colour == 0:
            QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, QtGui.QBrush(QtGui.QColor(211, 211, 211)))
        else:
            QtWidgets.QAbstractGraphicsShapeItem.setBrush(self, QtGui.QBrush(QtGui.QColor(20, 20, 20)))

    def mousePressEvent(self, event):
        if self.gui.currently_selected is not None and not self.gui.game.has_moved():
            if self.gui.started:    # Prevents players from moving units before the game begins
                self.gui.move_unit(int(event.scenePos().y() // self.square_size), int(event.scenePos().x() // self.square_size), self.gui.currently_selected.get_unit())

        elif self.gui.currently_selected is not None and self.gui.game.has_moved():
            self.gui.statusBar.showMessage("You have already moved a unit this turn!", 10000)