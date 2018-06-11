import random
from maze import constants
from .point import Point
from .character.mari import Mari


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game. 
    """

    def __init__(self, layout_lines, starting_point=None):
        self.layout = [list(line) for line in layout_lines]
        self.player = Mari(self.layout, self._get_random_point())

    def render(self):
        player_location = self.player.get_location()
        display = []
        for row_i, row in enumerate(self.layout):
            for col_i, col in enumerate(row):
                if Point(col_i, row_i) == player_location:
                    display.append(self.player.render())
                else:
                    display.append(col)
        print("".join(display))

    def take_turn(self, player_move):
        self.player.move(player_move)

    def is_escaped(self):
        x, y = self.player.get_location()
        return self.layout[y][x] == constants.maze_point_exit

    """
    internals 
    """

    def _get_random_point(self):
        height = len(self.layout)
        width = len(self.layout[0])
        p = Point(random.randrange(width), random.randrange(height))
        while not self.layout[p.y][p.x] == constants.maze_point_empty:
            p = Point(random.randrange(width), random.randrange(height))
        return p
