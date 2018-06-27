from maze import constants


class Hammer:
    """
    Hammer item player can find in the maze
    Can destroy walls
    """

    def __init__(self, starting_point):
        self.id = 'sledgehammer'
        self.__location = starting_point
        self.__is_carried = False

    def render(self, factory):
        return factory.render_entity(self.__location, constants.hammer)

    def get_location(self):
        return self.__location

    def pick_up(self):
        self.__is_carried = True
        self.__location = None

    def is_carried(self):
        return self.__is_carried
