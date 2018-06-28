from uuid import uuid4
from maze.constants import maze_point_tunnel, maze_tile_tunnel
from maze.tile.tile import Tile


class Tunnel(Tile):
    """
    Represents a maze tunnel tile.
    """

    def __init__(self, tunnel_number):
        super().__init__(maze_tile_tunnel, maze_point_tunnel)
        self.__tunnel_number = tunnel_number
        self.__tunnel_id = uuid4()

    def render(self, factory, location):
        return factory.render_tile(location, self)

    def get_tunnel_number(self):
        return self.__tunnel_number

    def get_tunnel_identifier(self):
        return self.__tunnel_id
