from time import sleep
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
        self.__inventory = set()
        self.__busy = False

    def render(self):
        return constants.character[self.facing]

    def move(self, direction):
        did_action = super().move(direction)
        if did_action:
            if self.location == self.game.hammer.get_location():
                self._pick_up(self.game.hammer)
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

    def do(self, action):
        if self._has_item(action) and self._can_destroy_wall():
            viewer = self.game.get_viewer()
            viewer.set_alert("Hammering...")
            self._perform_destroy_wall()
            return ""
        else:
            return "Mari can't do that!"

    """
    internals
    """

    def _has_item(self, key):
        return key in self.__inventory

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

    def _pick_up(self, item):
        item.pick_up()
        self.__inventory.add(item.id)
        viewer = self.game.get_viewer()
        viewer.set_alert("Picked up {}".format(item.id))
        sleep(1)
        viewer.set_alert("")

    def _can_destroy_wall(self):
        lx, ly = self.location
        tx, ty = constants.translations[self.facing]
        x, y = Point(lx + tx, ly + ty)
        return y != 0 and y != len(self.maze) - 1 and x != 0 and x != len(self.maze[0]) - 1

    def _perform_destroy_wall(self):
        sleep(1)
        maze = self.maze[:]
        lx, ly = self.location
        tx, ty = constants.translations[self.facing]
        x, y = Point(lx + tx, ly + ty)
        maze[y][x] = constants.maze_point_empty
        self.maze = maze
