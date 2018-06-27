from maze import constants
from maze.point import Point


class Character:

    """
    Base class for maze entities 
    """

    translations = constants.translations.copy()

    valid_move_targets = [
        constants.maze_tile_passage,
        constants.hammer
    ]

    def __init__(self, id, starting_point, render_value=None):
        self.id = id
        self.__facing = 'up'
        self.__location = starting_point
        self.__render = render_value

    def render_value(self):
        return self.__render

    def render(self):
        pass

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_facing(self):
        return self.__facing

    def move(self, maze, direction):
        if not self._is_facing(direction):
            self.turn(direction)
            return True
        else:
            translation = Character.translations[self.__facing]
            if self._can_move(maze, translation):
                self._perform_move(maze, translation)
                return True
            elif self._can_push(maze, translation):
                self._perform_push(maze, translation)
                return True
            else:
                return False

    def turn(self, direction):
        self.__facing = direction

    """
    internals
    """

    def _is_facing(self, direction):
        return self.__facing == direction

    def _can_move(self, maze, translation):
        target_y = self.__location.y + translation.y
        target_x = self.__location.x + translation.x
        return maze[target_y][target_x].get_type() in self.valid_move_targets

    def _perform_move(self, maze, translation):
        target_y = self.__location.y + translation.y
        target_x = self.__location.x + translation.x
        self.__location = Point(target_x, target_y)

    def _can_push(self, maze, translation):
        return False

    def _perform_push(self, maze, translation):
        pass
