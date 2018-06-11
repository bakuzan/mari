from maze import constants
from maze.point import Point
from .character import Character


class Mari(Character):

    """
    Player character 
    """

    valid_move_targets = Character.valid_move_targets.extend([
        constants.maze_point_exit
    ])

    def __init__(self, maze, starting_point):
        super().__init__(maze.layout, starting_point)
        self.game = maze

    def render(self):
        return constants.character[self.facing]

    def move(self, translation):
        did_action = super().move(translation)
        if not did_action:
            print("Mari can't do that!")

    def turn(self, move):
        self.facing = constants.movement_keys[move]

    def is_caught(self):
        return self.location in [troll.get_location() for troll in self.game.trolls]

    """
    internals
    """

    def _is_facing(self, move):
        return self.facing == constants.movement_keys[move]

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
