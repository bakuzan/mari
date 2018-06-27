from threading import Thread
from time import sleep
from maze import constants
from maze.point import Point
from maze.character.character import Character
from maze.tile.passage import Passage

class Mari(Character):

    """
    Player character 
    """

    valid_move_targets = Character.valid_move_targets[:] + \
        [constants.maze_tile_exit]

    def __init__(self, starting_point):
        super().__init__('mari', starting_point)
        self.__inventory = set()
        self.__busy = False

    def render(self):
        return constants.character[self.get_facing()]

    def move(self, maze, direction, **kwargs):
        send_message = kwargs.pop('send_message')
        did_action = super().move(maze, direction)

        if did_action:
            hammer = kwargs.pop('hammer')
            if not self.get_location() == hammer.get_location():
                send_message("")
            else:
                t = Thread(target=self._pick_up, args=(hammer,), kwargs={
                           'send_message': send_message}, daemon=True)
                t.start()
        else:
            send_message("Mari can't do that!")

    def can_move(self, maze, target_point):
        c_x, c_y = self.get_location()
        t_x, t_y = target_point
        translation = Point(t_x - c_x, t_y - c_y)
        if translation in [p for _, p in list(self.translations.items())]:
            return super()._can_move(maze, translation)
        else:
            return False

    def is_caught(self, trolls):
        return self.get_location() in [troll.get_location() for troll in trolls]

    def is_busy(self):
        return self.__busy

    def do(self, maze, action, **kwargs):
        send_message = kwargs.pop('send_message')
        if self._has_item(action) and self._can_destroy_wall(maze):
            t = Thread(target=self._perform_destroy_wall,
                       args=(maze,), kwargs={'send_message': send_message}, daemon=True)
            t.start()

        else:
            send_message("Mari can't do that!")

    """
    internals
    """

    def _has_item(self, key):
        return key in self.__inventory

    def _can_push(self, maze, translation):
        x, y = translation
        lx, ly = self.get_location()
        beyond_target = Point(x + x, y + y)
        beyond_y = ly + beyond_target.y
        beyond_x = lx + beyond_target.x
        if (beyond_y <= 0 or beyond_y >= len(maze) - 1):
            return False
        if (beyond_x <= 0 or beyond_x >= len(maze[beyond_y]) - 1):
            return False
        return maze[beyond_y][beyond_x].get_type() == constants.maze_tile_passage

    def _perform_push(self, maze, translation):
        lx, ly = self.get_location()
        tx, ty = translation
        x, y = Point(lx + tx, ly + ty)
        ux, uy = Point(x + tx, y + ty)
        maze[uy][ux], maze[y][x] = maze[y][x], maze[uy][ux]
        self.set_location(Point(x, y))

    def _pick_up(self, item, **kwargs):
        send_message = kwargs.pop('send_message')
        item.pick_up()
        self.__inventory.add(item.id)
        send_message("Picked up {}".format(item.id))
        sleep(2)
        send_message("")

    def _can_destroy_wall(self, maze):
        lx, ly = self.get_location()
        tx, ty = self.translations[self.get_facing()]
        x, y = Point(lx + tx, ly + ty)
        return y != 0 and y != len(maze) - 1 and x != 0 and x != len(maze[0]) - 1

    def _perform_destroy_wall(self, maze, **kwargs):
        send_message = kwargs.pop('send_message')
        send_message("Hammering...")
        self.__busy = True
        sleep(1)
        lx, ly = self.get_location()
        tx, ty = self.translations[self.get_facing()]
        x, y = Point(lx + tx, ly + ty)
        maze[y][x] = Passage()
        self.__busy = False
        send_message("")
