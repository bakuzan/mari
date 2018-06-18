from maze import constants
from maze.point import Point
from maze.character.character import Character


class Mari(Character):

    """
    Player character 
    """

    valid_move_targets = Character.valid_move_targets[:] + \
        [constants.maze_point_exit]

    def __init__(self, maze, starting_point):
        super().__init__('mari', maze.layout, starting_point)
        self.game = maze

    def render(self):
        return constants.character[self.facing]

    def move(self, direction):
        did_action = super().move(direction)
        if did_action:
            return ""
        else:
            return "Mari can't do that!"

    def can_move(self, target_point):
        c_x, c_y = self.location
        t_x, t_y = target_point
        translation = Point(t_x - c_x, t_y - c_y)
        if translation in [p for _, p in list(self.translations.items())]:
            return super()._can_move(translation)
        else:
            return False

    def is_caught(self):
        return self.location in [troll.get_location() for troll in self.game.trolls]

    """
    internals
    """

    def _can_push(self, translation):
        x, y = translation
        beyond_target = Point(x + x, y + y)
        beyond_y = self.location.y + beyond_target.y
        beyond_x = self.location.x + beyond_target.x
        if (beyond_y <= 0 or beyond_y >= len(self.maze) - 1):
            return False
        if (beyond_x <= 0 or beyond_x >= len(self.maze[beyond_y]) - 1):
            return False
        return self.maze[beyond_y][beyond_x] == constants.maze_point_empty

    def _perform_push(self, translation):
        maze = self.maze[:]
        lx, ly = self.location
        tx, ty = translation
        x, y = Point(lx + tx, ly + ty)
        ux, uy = Point(x + tx, y + ty)
        maze[uy][ux], maze[y][x] = maze[y][x], maze[uy][ux]
        self.location = Point(x, y)
        self.maze = maze
