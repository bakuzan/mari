from maze.constants import maze_point_empty, maze_tile_passage
from maze.tile.tile import Tile


class Passage(Tile):
    """
    Represents a maze passage tile.
    """

    def __init__(self):
        super().__init__(maze_tile_passage, maze_point_empty)

    def render(self, factory, location):
        return factory.render_tile(location, self)
