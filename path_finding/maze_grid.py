import sys
sys.path.append("../maze/")

from maze import constants
from maze.point import Point

accessible_points = [constants.maze_tile_passage, constants.maze_tile_exit]

direction_list = [point for name, point in list(
    constants.translations.items())]


def load_maze():
    with open("./assets/narrow.txt", "r") as layout:
        return layout.readlines()


class MazeGrid:
    def __init__(self, layout, target):
        self.target = target
        self.grid = [list(line) for line in layout]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def is_accessible(self, item):
        x, y = item
        return self.grid[y][x].get_type() in accessible_points or item == self.target

    def is_in_bounds(self, item):
        x, y = item
        if y < 0 or y >= self.height:
            return False
        if x < 0 or x >= self.width:
            return False
        return True

    def neighbours(self, item):
        x, y = item
        neighbours = [Point(x + d.x, y + d.y) for d in direction_list]
        neighbours = [n for n in neighbours if self.is_in_bounds(n)]
        neighbours = [n for n in neighbours if self.is_accessible(n)]
        return neighbours


class MazeGridWeighted(MazeGrid):
    def __init__(self, layout, target):
        super().__init__(layout, target)
        self.weights = {}

    def cost(self, from_point, to_point):
        return self.weights.get(to_point, 1)


if __name__ == "__main__":
    layout = load_maze()
    target = Point(1, 22)
    test = MazeGridWeighted(layout, target)
    for row_i, row in enumerate(test.grid):
        for col_i, col in enumerate(row):
            k = (row_i, col_i)
            v = test.neighbours(k)
            print("{0}: {1}".format(k, v))
