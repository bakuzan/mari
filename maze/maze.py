import random
from maze import constants
from .point import Point
from .character.mari import Mari
from .character.troll import Troll


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game. 
    """

    def __init__(self, layout_lines, starting_point=None, troll_count=3):
        self.layout = [list(line) for line in layout_lines]
        self.player = Mari(self.layout, self._get_random_point())
        self.trolls = [Troll(self.layout, self._get_random_point())
                       for i in range(1, 3)]

    def render(self):
        player_location = self.player.get_location()
        display = []
        for row_i, row in enumerate(self.layout):
            for col_i, col in enumerate(row):
                current_point = Point(col_i, row_i)
                if current_point == player_location:
                    display.append(self.player.render())
                elif current_point in [t.get_location() for t in self.trolls]:
                    [troll] = [t for t in self.trolls if current_point == t.get_location()]
                    display.append(troll.render())
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
