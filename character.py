import constants
from point import Point


class Character:

    """
    Base class for maze entities
    """

    translations = {
        'up': Point(0, -1),
        'left': Point(-1, 0),
        'down': Point(0, 1),
        'right': Point(1, 0)
    }

    def __init__(self, maze, starting_point):
        self.maze = maze
        self.facing = 'up'
        self.location = starting_point

    def render(self):
        return "@"

    def get_location(self):
        return self.location

    def move(self, move):
        if not self._is_facing(move):
            self.turn(move)
            return True
        else:
            translation = Character.translations[self.facing]
            if self._can_move(translation):
                self._perform_move(translation)
                return True
            elif self._can_push(translation):
                self._perform_push(translation)
                return True
            else:
                return False

    def turn(self, move):
        self.facing = constants.movement_keys[move]

    """
    internals
    """

    def _is_facing(self, move):
        return self.facing == constants.movement_keys[move]

    def _can_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        return self.maze[target_y][target_x] != constants.maze_point_wall

    def _perform_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        self.location = Point(target_x, target_y)

    def _can_push(self, translation):
        return False

    def _perform_push(self, translation):
        pass
