from maze.constants import maze_point_wall, maze_tile_wall
from maze.tile.tile import Tile


class Wall(Tile):
    """
    Represents a maze wall tile.
    """

    def __init__(self):
        super().__init__(maze_tile_wall, maze_point_wall)

    def render(self, factory, location):
        return factory.render_tile(location, self)
