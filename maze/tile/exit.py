from maze.constants import maze_point_exit, maze_tile_exit
from maze.tile.tile import Tile


class Exit(Tile):
    """
    Represents a maze exit tile.
    """

    def __init__(self):
        super().__init__(maze_tile_exit, maze_point_exit)

    def render(self, factory, location):
        return factory.render_tile(location, self)
