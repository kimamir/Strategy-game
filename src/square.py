
class Square():

    def __init__(self, x, y):

        self.unit = None    # Current unit occupying the square. None if empty
        self.obstacle = False    # True if square is an obstacle, false otherwise
        self.neighbours = []    # A list of Square-objects
        self.x = x
        self.y = y

    def get_character(self):
        """
        Returns the unit object currently occupying the square.
        Returns None if empty.
        """
        return self.unit

    def is_obstacle(self):
        """
        Returns True if the square is an obstacle.
        Returns False otherwise.
        Used to check line of sight. The game assumes you can shoot past other units but not through walls!
        """
        return self.obstacle

    def turn_into_obstacle(self):
        """
        Turns the Square object into an obstacle i.e. sets self.obstacle = True
        """
        self.obstacle = True

    def is_free(self):
        """
        Returns True if the Square is unoccupied and is not an obstacle.
        Otherwise returns False
        """
        if self.unit is None and not self.obstacle:
            return True
        else:
            return False

    def add_unit_to_square(self, unit):
        self.unit = unit

    def remove_unit_from_square(self):
        """
        Removes unit from this square i.e. sets self.unit = None
        """
        self.unit = None

    def update_neighbours(self, grid, width, height):
        offsetx = [0, 1, 0, -1]  # LEFT, DOWN, RIGHT, UP
        offsety = [-1, 0, 1, 0]
        self.neighbours = []

        for i in range(4):
            nx = self.x + offsetx[i]
            ny = self.y + offsety[i]
            if nx < 0 or nx > width - 1 or ny < 0 or ny > height - 1:
                continue
            if not grid[nx][ny].is_free():
                continue
            self.neighbours.append(grid[nx][ny])

    def get_neighbours(self):
        return self.neighbours

    def get_location(self):
        return self.x, self.y




