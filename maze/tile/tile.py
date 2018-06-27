

class Tile:
    """
    Represents a point within the maze
    """

    def __init__(self, tile_type, render_value):
        self.__type = tile_type
        self.__render = render_value

    def get_type(self):
        return self.__type

    def render_value(self):
        return self.__render

    def render(self):
        pass
