import os
import sys
import msvcrt
from maze import constants
from maze.maze import Maze
from maze.point import Point
from path_finding.maze_grid import MazeGridWeighted
from path_finding.a_star_search import a_star_search


def load_maze():
    with open("./layouts/narrow.txt", "r") as layout:
        return layout.readlines()


if __name__ == "__main__":
    layout = load_maze()
    graph = MazeGridWeighted(layout)
    start, goal = Point(21, 9), Point(1, 22)
    _, path = a_star_search(graph, start, goal)

    display = []
    for row_i, row in enumerate(graph.grid):
        for col_i, col in enumerate(row):
            current_point = Point(col_i, row_i)
            if current_point == start:
                display.append("S")
            elif current_point == goal:
                display.append("X")
            else:
                cha = "!" if current_point in path else col
                display.append(cha)
    print("".join(display))
