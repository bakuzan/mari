import random
from threading import Thread
from time import sleep

from maze import constants
from maze.point import Point
from maze.character.mari import Mari
from maze.character.troll import Troll
from maze.item.hammer import Hammer
from maze.generator import MazeGenerator
from maze.renderer import Renderer
from path_finding import a_star_search
from viewer.viewer import Viewer


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game. 
    """

    def __init__(self, w, h, troll_count=3):
        self.__w = w
        self.__h = h
        self.__troll_count = troll_count

        self.__window = Viewer(
            dimensions=(w, h),
            on_play=self.start_game,
            on_user_input=self.take_turn,
            on_reset=self.reset_maze)
        self.__factory = MazeGenerator(
            self.__w,
            self.__h,
            window=self.__window)

        self.reset_maze()
        self.__window.start()

    def is_ready(self):
        if not self.layout:
            return False
        return True

    def start_game(self):
        self.layout = self.__factory.grid()
        self._place_entities()
        self.render()

        t = Thread(target=self._start_trolls, daemon=True)
        t.start()

    def reset_maze(self):
        self.layout = None
        self.player = None
        self.trolls = []
        self.hammer = None
        self.message = ""

        t = Thread(target=self.__factory.generate, args=(True,), daemon=True)
        t.start()

    def get_viewer(self):
        return self.__window

    def render(self):
        player_location = self.player.get_location()
        hammer_location = self.hammer.get_location()
        in_progress = self.game_is_playable()
        display = []
        render_factory = Renderer(self.layout, player_location, in_progress)

        for row_i, row in enumerate(self.layout):
            for col_i, tile in enumerate(row):
                current_point = Point(col_i, row_i)

                if current_point == player_location:
                    display.append(self.player.render())

                elif current_point in [t.get_location() for t in self.trolls]:
                    trolls = [
                        t for t in self.trolls if current_point == t.get_location()]
                    troll = trolls[0]

                    if tile.get_type() != constants.maze_tile_wall:
                        display.append(troll.render(render_factory))
                    else:
                        display.append(tile.render(render_factory, current_point))
                        self.trolls = [
                            t for t in self.trolls if t.id != troll.id]

                elif not self.hammer.is_carried() and current_point == hammer_location:
                    display.append(self.hammer.render(render_factory))

                else:
                    display.append(tile.render(render_factory, current_point))

            display.append('\n')

        self.__window.update("".join(display))
        self.__window.set_alert(self.message)
        self.game_is_playable()

    def take_turn(self, key):
        if not self.is_ready() or not self.game_is_playable():
            return

        key = str(key).lower()
        direction = constants.key_press.get(key)
        action = constants.key_press_action.get(key)
        if self.is_ready() and not self.player.is_busy():
            if direction:
                self.player.move(
                    self.layout, direction, hammer=self.hammer, send_message=self._update_window_message)
                self.render()
            elif action:
                self.player.do(
                    self.layout, action, send_message=self._update_window_message)
                self.render()

    def is_escaped(self):
        if self.player:
            x, y = self.player.get_location()
            return self.layout[y][x].get_type() == constants.maze_tile_exit
        else:
            return False

    def is_solvable(self):
        player_location = self.player.get_location()
        exit_point = next(
            Point([c.get_type() for c in row].index(
                constants.maze_tile_exit), y)
            for y, row in enumerate(self.layout) if constants.maze_tile_exit in [c.get_type() for c in row])

        path = a_star_search.can_find_path(
            self.layout, player_location, exit_point)

        if len(path) > 1 and self.player.can_move(self.layout, path[1]):
            return True
        else:
            # TODO
            # detect if a you can actually move blocks to escape
            if not self.message:
                self.message = "You are blocked from the exit.\nTry pushing walls or find the hammer!"

            return True

    def game_is_playable(self):
        is_playable = (
            not self.is_escaped() and
            (not self.player or not self.player.is_caught(self.trolls)) and
            (not self.player or self.is_solvable())
        )

        if not is_playable:
            self._display_game_ended_message()

        return is_playable

    """
    internals 
    """

    def _display_game_ended_message(self):
        if self.is_escaped():
            self.__window.set_alert("Mari escaped!\nYou win!")
        elif self.player.is_caught(self.trolls):
            self.__window.set_alert("Mari was caught!\nYou lose!")
        elif not self.is_solvable():
            self.__window.set_alert("Mari is trapped!\nYou lose!")
        else:
            self.__window.set_alert("Game ended.")

        self.__window.enable_new_game()

    def _update_window_message(self, message):
        self.message = message
        self.__window.set_alert(self.message)

    def _place_entities(self):
        if not self.player:
            self.player = Mari(self._get_random_point(True))
            self.trolls = [Troll(i, self._get_random_point())
                           for i in range(0, self.__troll_count)]
            self.hammer = Hammer(self._get_random_point())

    def _get_random_point(self, is_player=False):
        height = len(self.layout)
        width = len(self.layout[0])

        p = Point(random.randrange(width), random.randrange(height))
        while self._point_not_acceptable(p, is_player):
            p = Point(random.randrange(width), random.randrange(height))

        return p

    def _point_not_acceptable(self, p, is_player):
        tile_type = self.layout[p.y][p.x].get_type()
        if not tile_type == constants.maze_tile_passage or Point(p.y, p.x) in [t.get_location() for t in self.trolls]:
            return True
        elif not is_player and len(a_star_search.perform_search(self.layout, p, self.player.get_location())) < 10:
            return True
        else:
            return False

    def _perform_trolls_turn(self):
        player_location = self.player.get_location()
        for troll in self.trolls:
            t_x, t_y = troll.get_location()
            if not self.layout[t_y][t_x].get_type() == constants.maze_tile_wall:
                troll.move(self.layout, player_location)
            else:
                self.trolls = [t for t in self.trolls if t.id != troll.id]
        self.render()
        self._start_trolls()

    def _start_trolls(self):
        sleep(0.55)
        if self.trolls and len(self.trolls) > 0 and self.game_is_playable():
            self._perform_trolls_turn()
