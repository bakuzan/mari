import constants
from point import Point
from character import Character


class Mari(Character):

    def __init__(self, maze, starting_point):
        super().__init__(maze, starting_point)

    def render(self):
        return constants.character[self.facing]

    def move(self, translation):
        did_action = super().move(translation)
        if not did_action:
            print("Mari can't do that!")

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
        return self.maze[beyond_y][beyond_x] != constants.maze_point_wall

    def _perform_push(self, translation):
        maze = self.maze[:]
        lx, ly = self.location
        tx, ty = translation
        x, y = Point(lx + tx, ly + ty)
        ux, uy = Point(x + tx, y + ty)
        maze[uy][ux], maze[y][x] = maze[y][x], maze[uy][ux]
        self.location = Point(x, y)
        self.maze = maze
