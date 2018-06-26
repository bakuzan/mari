from maze import constants
from maze.point import Point


class Character:

    """
    Base class for maze entities 
    """

    translations = constants.translations.copy()

    valid_move_targets = [
        constants.maze_point_empty,
        constants.hammer
    ]

    def __init__(self, id, maze, starting_point):
        self.id = id
        self.maze = maze
        self.facing = 'up'
        self.location = starting_point

    def render(self):
        return "@"

    def get_location(self):
        return self.location

    def get_facing(self):
        return self.facing

    def move(self, direction):
        if not self._is_facing(direction):
            self.turn(direction)
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

    def turn(self, direction):
        self.facing = direction

    """
    internals
    """

    def _is_facing(self, direction):
        return self.facing == direction

    def _can_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        return self.maze[target_y][target_x] in self.valid_move_targets

    def _perform_move(self, translation):
        target_y = self.location.y + translation.y
        target_x = self.location.x + translation.x
        self.location = Point(target_x, target_y)

    def _can_push(self, translation):
        return False

    def _perform_push(self, translation):
        pass
