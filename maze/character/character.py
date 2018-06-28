from maze import constants
from maze.point import Point


class Character:

    """
    Base class for maze entities 
    """

    translations = constants.translations.copy()

    valid_move_targets = [
        constants.maze_tile_passage,
        constants.maze_tile_tunnel,
        constants.hammer
    ]

    def __init__(self, id, starting_point):
        self.id = id
        self.__facing = 'up'
        self.__location = starting_point

    def render(self):
        pass

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_facing(self):
        return self.__facing

    def move(self, maze, direction):
        if not self._is_facing(direction):
            self.turn(direction)
            return True
        else:
            translation = Character.translations[self.__facing]
            if self._can_move(maze, translation):
                self._perform_move(maze, translation)
                return True
            elif self._can_push(maze, translation):
                self._perform_push(maze, translation)
                return True
            else:
                return False

    def turn(self, direction):
        self.__facing = direction

    """
    internals
    """

    def _is_facing(self, direction):
        return self.__facing == direction

    def _can_move(self, maze, translation):
        target_y = self.__location.y + translation.y
        target_x = self.__location.x + translation.x
        return maze[target_y][target_x].get_type() in self.valid_move_targets

    def _perform_move(self, maze, translation):
        target_y = self.__location.y + translation.y
        target_x = self.__location.x + translation.x
        location = Point(target_x, target_y)
        tile = maze[target_y][target_x]
        if tile.get_type() != constants.maze_tile_tunnel:
            self.__location = location
        else:
            self.__location = self._travel_tunnel(maze, tile)

    def _travel_tunnel(self, maze, tunnel_entrance_tile):
        tunnel_num = tunnel_entrance_tile.get_tunnel_number()
        entrance_id = tunnel_entrance_tile.get_tunnel_identifier()

        exit_x, exit_y = next(Point(x, y) for y, row in enumerate(maze) for x, tile in enumerate(maze[y])
                              if tile.get_type() == constants.maze_tile_tunnel and
                              tile.get_tunnel_number() == tunnel_num and
                              tile.get_tunnel_identifier() != entrance_id)

        return Point(exit_x, exit_y)

    def _can_push(self, maze, translation):
        return False

    def _perform_push(self, maze, translation):
        pass
