from random import randrange
from maze import constants
from maze.character.character import Character
from path_finding import a_star_search


def get_facing_direction(translation):
    [facing] = [facing for facing, point in list(
        Character.translations.items()) if point == translation]
    return facing


class Troll(Character):

    """
    Enemy character
    """

    valid_move_targets = Character.valid_move_targets + \
        [maze_point for k, maze_point in list(constants.character.items())]

    def __init__(self, maze, starting_point):
        super().__init__(maze, starting_point)

    def render(self):
        return "T"

    def move(self, player_location):
        path = a_star_search.perform_search(
            self.maze, self.location, player_location)
        move = path[1] # path[0] == self.location
        return super().move(move)

    def turn(self, translation):
        self.facing = get_facing_direction(translation)

    """
    internals
    """

    def _is_facing(self, translation):
        print(translation)
        return self.facing == get_facing_direction(translation)
