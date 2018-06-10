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
        if not self._is_facing(move):
            self.turn(move)
        else:
            translation = Maze.translations[self.facing]
            if self._can_move(translation):
                self._perform_move(translation)
            elif self._can_push(translation):
                self._perform_push(translation)
            else:
                print("Mari can't go that way!")
            

    def turn(self, move):
        self.facing = constants.movement_keys[move]

    def is_escaped(self):
        return self.layout[self.location.y][self.location.x] == constants.maze_point_exit

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

    def _is_facing(self, move):
        return self.facing == constants.movement_keys[move]

    def _can_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        return self.layout[target_y][target_x] != constants.maze_point_wall

    def _perform_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        self.location = Point(target_x, target_y)

    def _can_push(self, translation):
        x, y = translation
        beyond_target = Point(x + x, y + y)
        beyond_y = self.location.y + beyond_target.y
        beyond_x = self.location.x + beyond_target.x
        if (beyond_y <= 0 or beyond_y >= len(self.layout) - 1): return False
        if (beyond_x <= 0 or beyond_x >= len(self.layout[beyond_y]) - 1): return False
        return self.layout[beyond_y][beyond_x] != constants.maze_point_wall
    
    def _perform_push(self, translation):
        layout = self.layout[:]
        lx, ly = self.location
        tx, ty = translation
        x, y = Point(lx + tx, ly + ty)
        ux, uy = Point(x + tx, y + ty)
        layout[uy][ux], layout[y][x] = layout[y][x], layout[uy][ux]
        self.location = Point(x, y)
        self.layout = layout