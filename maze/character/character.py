from maze import constants
from maze.point import Point

class Character:

    """
    Base class for maze entities 
    """

    translations = constants.translations

    valid_move_targets = [
        constants.maze_point_empty
    ]

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
        pass

    """
    internals
    """

    def _is_facing(self, move):
        pass

    def _can_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        print(Character.valid_move_targets)
        return self.maze[target_y][target_x] in Character.valid_move_targets

    def _perform_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        self.location = Point(target_x, target_y)

    def _can_push(self, translation):
        return False

    def _perform_push(self, translation):
        pass
