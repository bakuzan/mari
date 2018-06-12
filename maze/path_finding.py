import collections
from maze import constants
from .point import Point
from .path_step import PathStep

direction_list = [point for name, point in list(
    constants.translations.items())]


def get_neighbour_points(point):
    x, y = point
    return [Point(x + d.x, y + d.y) for d in direction_list]


def get_next_possible_step(path_step):
    x, y, w = path_step
    return [PathStep(x + p.x, y + p.y, w + 1) for p in get_neighbour_points(Point(x, y))]


def is_point_a_wall(maze, path_step):
    x, y = path_step
    return maze[y][x] == constants.maze_point_wall


def is_point_in_queue(queue, path_step):
    return path_step in queue


def find_path(maze, start, end):
    queue = [PathStep(end.x, end.y, 0)]
    step = 0
    while step < len(queue):
        current = queue[step]
        next_step = get_next_possible_step(current)
        next_step = [p for p in next_step if not is_point_a_wall(
            maze, p) and not is_point_in_queue(queue, p)]
        queue.extend(next_step)
        step += 1
    return queue


def find_next_move(maze, current, target):
    path = find_path(maze, current, target)
    neighbours = get_neighbour_points(current)
    options = [ps for ps in path if ps in neighbours]
    min_step = min(options, key=lambda x: x[2])
    [move] = [Point(x, y) for x, y, w in options if w == min_step]
    return move


if __name__ == "__main__":
    lines = []
    with open("./layouts/narrow.txt", "r") as layout:
        lines = layout.readlines()

    maze = [list(line) for line in lines]
    start = (17, 10)
    end = (1, 22)
    path = find_path(maze, start, end)
    display = []
    for row_i, row in enumerate(maze):
        for col_i, col in enumerate(row):
            current_point = Point(col_i, row_i)
            if current_point == start:
                display.append("S")
            elif current_point == end:
                display.append("E")
            elif current_point in [Point(x, y) for x, y in path]:
                [weight] = [ps.w for ps in path if current_point ==
                            Point(ps.x, ps.y)]
                display.append(weight)
            else:
                display.append(col)
    print("".join(display))
