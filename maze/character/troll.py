from random import randrange
from maze import constants
from maze import path_finding
from .character import Character


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
        # self.last_movement = None

    def render(self):
        return "T"

    def move(self, player_location):
        move = path_finding.find_next_move(
            self.maze, self.location, player_location)
        return super().move(move)
        # did_move = False
        # potential_moves = [point for name, point in list(
        #     Character.translations.items())]
        # potential_moves_count = len(potential_moves)
        # index = randrange(potential_moves_count)
        # move = self.last_movement if self.last_movement else potential_moves[index]
        # while not did_move:
        #     did_move = super().move(move)
        #     if did_move:
        #         self.last_movement = move
        #     else:
        #         [i] = [i for i, p_m in enumerate(
        #             potential_moves) if p_m == move]
        #         target_index = i + 1
        #         move = potential_moves[0] if target_index == potential_moves_count else potential_moves[target_index]
        # return did_move

    def turn(self, translation):
        self.facing = get_facing_direction(translation)

    """
    internals
    """

    def _is_facing(self, translation):
        return self.facing == get_facing_direction(translation)
