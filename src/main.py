import sys
from game import Game
from world import World
from gui import GUI
from PyQt5.QtWidgets import QApplication


def main():
    game = Game()
    world = World(10, 10)
    game.set_world(world)
    world.add_obstacles()

    global app
    app = QApplication(sys.argv)
    gui = GUI(game, world, 50)
    sys.exit(app.exec_())


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    main()
