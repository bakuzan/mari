from random import randrange
from maze import constants
from maze.point import Point
from maze.character.character import Character
from path_finding import a_star_search


class Troll(Character):

    """
    Enemy character
    """

    valid_move_targets = Character.valid_move_targets[:] + \
        [maze_point for k, maze_point in list(constants.character.items())]

    def __init__(self, id, starting_point):
        super().__init__(id, starting_point, constants.troll)

    def render(self, factory):
        return factory.render_entity(self.get_location(), self)

    def move(self, maze, player_location):
        location = self.get_location()
        path = a_star_search.perform_search(
            maze, location, player_location)
        # path[0] == self.__location
        target_point = path[1] if len(
            path) > 1 else path[0]
        direction = self._get_moving_direction(
            location, target_point) or self.get_facing()

        super().move(maze, direction)

    """
    internals
    """

    def _get_moving_direction(self, current_point, target_point):
        c_x, c_y = current_point
        t_x, t_y = target_point
        translation = Point(t_x - c_x, t_y - c_y)
        d_list = [facing for facing, point in list(
            self.translations.items()) if point == translation]
        return d_list[0] if len(d_list) == 1 else None
