import random

from maze import constants
from maze.point import Point
from maze.character.mari import Mari
from maze.character.troll import Troll
from maze.generator import MazeGenerator


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game.
    """

    def __init__(self, w, h, troll_count=3):
        self.__width = w
        self.__height = h
        self.__factory = MazeGenerator(w, h)
        self.layout = self.__factory.generate(True)
        self.player = None
        self.trolls = []
        self.message = ""

    def is_ready(self):
        if not self.layout:
            return False
        return True

    def render(self):
        self._place_entities()
        player_location = self.player.get_location()
        display = []
        for row_i, row in enumerate(self.layout):
            for col_i, col in enumerate(row):
                current_point = Point(col_i, row_i)
                if current_point == player_location:
                    display.append(self.player.render())
                elif current_point in [t.get_location() for t in self.trolls]:
                    trolls = [
                        t for t in self.trolls if current_point == t.get_location()]
                    troll = trolls[0]
                    display.append(troll.render())
                else:
                    display.append(col)
            display.append('\n')

        print("".join(display), flush=True)
        print(self.message)

    def take_turn(self, key):
        direction = constants.movement_keys[key]
        self.message = self.player.move(direction)
        self._perform_trolls_turn()

    def is_escaped(self):
        if self.player:
            x, y = self.player.get_location()
            return self.layout[y][x] == constants.maze_point_exit
        else:
            return False

    """
    internals 
    """

    def _place_entities(self):
        if not self.player:
            self.player = Mari(self, self._get_random_point())
            self.trolls = [Troll(i, self.layout, self._get_random_point())
                           for i in range(0, 3)]

    def _get_random_point(self):
        height = self.__height
        width = self.__width
        p = Point(random.randrange(width), random.randrange(height))
        while not self.layout[p.y][p.x] == constants.maze_point_empty or self.layout[p.y][p.x] in [t.get_location() for t in self.trolls]:
            p = Point(random.randrange(width), random.randrange(height))
        return p

    def _perform_trolls_turn(self):
        player_location = self.player.get_location()
        for troll in self.trolls:
            troll.move(player_location)
