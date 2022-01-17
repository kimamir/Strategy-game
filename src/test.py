import unittest
from game import Game
from world import World

class Test(unittest.TestCase):

    def setUp(self):
        """
        Sets up the game and world for testing.
        """
        self.test_game = Game()
        self.test_world = World(10, 10)
        self.test_game.set_world(self.test_world)
        self.test_world.add_obstacles()

    def test_world_generation(self):
        self.assertEqual(10, self.test_world.get_width(), "Width of the world should be 10")
        self.assertEqual(10, self.test_world.get_height(), "Height of the world should be 10")

    def test_obstacles(self):
        """
        Testing whether obstacles are being generated correctly by the method
        add_obstacles() in world.py.
        Seed value used: 100
        """
        square = self.test_world.get_square(3, 8)
        self.assertTrue(square.is_obstacle(), "The square in (3,8) should be an obstacle")

        square = self.test_world.get_square(8, 3)
        self.assertTrue(square.is_obstacle(), "The square in (8,3) should be an obstacle")

        square = self.test_world.get_square(7, 6)
        self.assertTrue(square.is_obstacle(), "The square in (7,6) should be an obstacle")

if __name__ == "__main__":
    unittest.main()