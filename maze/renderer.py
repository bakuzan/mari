import math
from maze.constants import translations, maze_point_wall, UP, LEFT, DOWN, RIGHT

ALL_DIRECTIONS = 4

DARK_SHADE = u'\u2593'
BOX_SQUARE = u'\u25A1'

BOX_TOP_LEFT = u'\u2554'
BOX_TOP_RIGHT = u'\u2557'
BOX_BOTTOM_LEFT = u'\u255a'
BOX_BOTTOM_RIGHT = u'\u255d'

BOX_HORIZONTAL = u'\u2550'
BOX_VERTICAL = u'\u2551'

BOX_CROSS = u'\u256c'
BOX_VERTICAL_RIGHT = u'\u2560'
BOX_VERTICAL_LEFT = u'\u2563'
BOX_HORIZONTAL_UP = u'\u2569'
BOX_HORIZONTAL_DOWN = u'\u2566'

BOX_CAP_TOP = u'\u2565'
BOX_CAP_BOTTOM = u'\u2568'
BOX_CAP_LEFT = u'\u2552'
BOX_CAP_RIGHT = u'\u2555'


class Renderer:
    """
    Class that works out what to render in a given square
    """

    def __init__(self, maze, player_location, fog_of_war):
        self.__fog_of_war = fog_of_war
        self.__maze = maze
        self.__h_sight_range = math.floor(len(maze) / 5)
        self.__w_sight_range = math.floor(len(maze[0]) / 5)
        self.__player_location = player_location

    def render_square(self, current, sq):
        if self.__fog_of_war and not self._is_within_line_of_sight(current):
            return DARK_SHADE

        if sq != maze_point_wall:
            return sq

        directions = self._get_neighbouring_wall_directions(current)
        if len(directions) == ALL_DIRECTIONS:
            return BOX_CROSS
        elif set([UP, DOWN, RIGHT]) == directions:
            return BOX_VERTICAL_RIGHT
        elif set([UP, DOWN, LEFT]) == directions:
            return BOX_VERTICAL_LEFT
        elif set([UP, LEFT, RIGHT]) == directions:
            return BOX_HORIZONTAL_UP
        elif set([DOWN, LEFT, RIGHT]) == directions:
            return BOX_HORIZONTAL_DOWN
        elif set([UP, DOWN]) == directions:
            return BOX_VERTICAL
        elif set([LEFT, RIGHT]) == directions:
            return BOX_HORIZONTAL
        elif set([DOWN, RIGHT]) == directions:
            return BOX_TOP_LEFT
        elif set([UP, RIGHT]) == directions:
            return BOX_BOTTOM_LEFT
        elif set([DOWN, LEFT]) == directions:
            return BOX_TOP_RIGHT
        elif set([UP, LEFT]) == directions:
            return BOX_BOTTOM_RIGHT
        elif set([UP]) == directions:
            return BOX_CAP_BOTTOM
        elif set([DOWN]) == directions:
            return BOX_CAP_TOP
        elif set([LEFT]) == directions:
            return BOX_CAP_RIGHT
        elif set([RIGHT]) == directions:
            return BOX_CAP_LEFT
        else:
            return BOX_SQUARE

    """
    internals
    """

    def _is_within_line_of_sight(self, current):
        px, py = self.__player_location
        cx, cy = current
        return abs(cx-px) <= self.__w_sight_range and abs(cy-py) <= self.__h_sight_range

    def _get_neighbouring_wall_directions(self, current):
        neighbour_directions = set()
        h = len(self.__maze) - 1
        w = len(self.__maze[0]) - 1
        cx, cy = current

        for k, (tx, ty) in translations.items():
            nx = cx + tx
            ny = cy + ty
            if nx >= 0 and nx <= w and ny >= 0 and ny <= h:
                if self.__maze[ny][nx] == maze_point_wall:
                    neighbour_directions.add(k)
        return neighbour_directions
