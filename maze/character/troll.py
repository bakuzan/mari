from random import randrange
from maze import constants
from maze.point import Point
from maze.character.character import Character
from path_finding import a_star_search


def get_moving_direction(current_point, target_point):
    c_x, c_y = current_point
    t_x, t_y = target_point
    translation = Point(c_x - t_x, c_y - t_y)
    [facing] = [facing for facing, point in list(
        Character.translations.items()) if point == translation]
    return facing


class Troll(Character):

    """
    Enemy character
    """

    valid_move_targets = Character.valid_move_targets[:] + \
        [maze_point for k, maze_point in list(constants.character.items())]

    def __init__(self, maze, id, starting_point):
        super().__init__(maze, starting_point)
        self.id = id

    def render(self):
        return "T"

    def move(self, player_location):
        path = a_star_search.perform_search(
            self.maze, self.location, player_location)
        target_point = path[1]  # path[0] == self.location
        direction = get_moving_direction(self.location, target_point)
        return super().move(direction)

    """
    internals
    """
