from .character import Character


class Troll(Character):

    """
    Enemy character 
    """

    def __init__(self, maze, starting_point):
        super().__init__(maze, starting_point)

    def render(self):
        return "T"
