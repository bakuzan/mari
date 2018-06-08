import random
import constants
from point import Point


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game.
    """

    translations = {
        'up': Point(0, -1),
        'left': Point(-1, 0),
        'down': Point(0, 1),
        'right': Point(1, 0)
    }

    def __init__(self, layout_lines, starting_point=None):
        self.layout = [list(line) for line in layout_lines]
        self.facing = 'up'
        self.location = self._get_random_point()

    def render(self):
        display = []
        for row_i, row in enumerate(self.layout):
            for col_i, col in enumerate(row):
                if Point(col_i, row_i) == self.location:
                    display.append(constants.character[self.facing])
                else:
                    display.append(col)
        print("".join(display))

    def move(self, move):
        if self._is_facing(move):
            translation = Maze.translations[self.facing]
            if self._can_move(translation):
                self._perform_move(translation)
            else:
                print("Mari can't move that way!")
        else:
            self.turn(move)

    def turn(self, move):
        self.facing = constants.movement_keys[move]

    def is_escaped(self):
        return self.layout[self.location.y][self.location.x] == 'X'

    """
    internals
    """

    def _get_random_point(self):
        height = len(self.layout)
        width = len(self.layout[0])
        p = Point(random.randrange(width), random.randrange(height))
        while not self.layout[p.y][p.x] == ' ':
            p = Point(random.randrange(width), random.randrange(height))
        return p

    def _is_facing(self, move):
        return self.facing == constants.movement_keys[move]

    def _can_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        return self.layout[target_y][target_x] != '#'

    def _perform_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        self.location = Point(target_x, target_y)
