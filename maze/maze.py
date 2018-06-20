import random
from threading import Thread
from time import sleep

from maze import constants
from maze.point import Point
from maze.character.mari import Mari
from maze.character.troll import Troll
from maze.generator import MazeGenerator
from path_finding import a_star_search
from viewer.viewer import Viewer


class Maze:
    """
    Holds all the information about the current maze
    Provides method to interact with the game. 
    """

    def __init__(self, w, h, troll_count=3):
        self.layout = None
        self.player = None
        self.trolls = []
        self.message = ""

        self.__window = Viewer(on_play=self.start_game,
                               on_user_input=self.take_turn)
        self.__factory = MazeGenerator(w, h, window=self.__window)

        t = Thread(target=self.__factory.generate, args=(True,))
        t.daemon = True
        t.start()

        self.__window.start()

    def is_ready(self):
        if not self.layout:
            return False
        return True

    def start_game(self):
        self.layout = self.__factory.grid()
        self._place_entities()
        self.render()

        t = Thread(target=self._start_trolls)
        t.daemon = True
        t.start()

    def render(self):
        player_location = self.player.get_location()
        display = []
        for row_i, row in enumerate(self.layout):
            for col_i, col in enumerate(row):
                current_point = Point(col_i, row_i)
                if current_point == player_location:
                    display.append(self.player.render())
                elif current_point in [t.get_location() for t in self.trolls] and col != constants.maze_point_wall:
                    trolls = [
                        t for t in self.trolls if current_point == t.get_location()]
                    troll = trolls[0]
                    display.append(troll.render())
                else:
                    display.append(col)
            display.append('\n')

        self.__window.update("".join(display))
        self.__window.set_alert(self.message)
        self.game_is_playable()

    def take_turn(self, key):
        if not self.is_ready() or not self.game_is_playable():
            return

        key = str(key).lower()
        direction = constants.key_press.get(key)
        if direction and self.is_ready():
            self.message = self.player.move(direction)
            self.render()

    def is_escaped(self):
        if self.player:
            x, y = self.player.get_location()
            return self.layout[y][x] == constants.maze_point_exit
        else:
            return False

    def is_solvable(self):
        player_location = self.player.get_location()
        exit_point = next(Point(row.index(constants.maze_point_exit), y)
                          for y, row in enumerate(self.layout) if constants.maze_point_exit in row)
        path = a_star_search.perform_search(
            self.layout, player_location, exit_point)
        if len(path) > 1 and self.player.can_move(path[1]):
            return True
        else:
            print('blocked!', path)
            # TODO
            # check if moving a block will make solvable.
            return True

    def game_is_playable(self):
        is_playable = (
            not self.is_escaped() and
            (not self.player or not self.player.is_caught()) and
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
        elif self.player.is_caught():
            self.__window.set_alert("Mari was caught!\nYou lose!")
        elif not self.is_solvable():
            self.__window.set_alert("Mari is trapped!\nYou lose!")
        else:
            self.__window.set_alert("Game ended.")

    def _place_entities(self):
        if not self.player:
            self.player = Mari(self, self._get_random_point(True))
            self.trolls = [Troll(i, self.layout, self._get_random_point())
                           for i in range(0, 3)]

    def _get_random_point(self, is_player=False):
        height = len(self.layout)
        width = len(self.layout[0])

        p = Point(random.randrange(width), random.randrange(height))
        while self._point_not_acceptable(p, is_player):
            p = Point(random.randrange(width), random.randrange(height))

        return p

    def _point_not_acceptable(self, p, is_player):
        if not self.layout[p.y][p.x] == constants.maze_point_empty or self.layout[p.y][p.x] in [t.get_location() for t in self.trolls]:
            return True
        elif not is_player and len(a_star_search.perform_search(self.layout, p, self.player.get_location())) < 10:
            return True
        else:
            return False

    def _perform_trolls_turn(self):
        player_location = self.player.get_location()
        for troll in self.trolls:
            t_x, t_y = troll.get_location()
            if not self.layout[t_y][t_x] == constants.maze_point_wall:
                troll.move(player_location)
            else:
                self.trolls = [t for t in self.trolls if t.id != troll.id]
        self.render()
        self._start_trolls()

    def _start_trolls(self):
        sleep(1)
        if self.trolls and len(self.trolls) > 0 and self.game_is_playable():
            self._perform_trolls_turn()
