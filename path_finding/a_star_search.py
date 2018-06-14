import math
from path_finding.priority_queue import PriorityQueue
from path_finding.maze_grid import MazeGridWeighted


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, start, target):
    current = target
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
    path.append(start)
    path.reverse()
    return path


def a_star_search(graph, start, target):
    edge = PriorityQueue()
    edge.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not edge.is_empty():
        current = edge.get()

        if current == target:
            break

        for next in graph.neighbours(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if new_cost < cost_so_far.get(next, math.inf):
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(target, next)
                edge.put(next, priority)
                came_from[next] = current

    path = reconstruct_path(came_from, start, target)
    return came_from, path


def perform_search(layout, start, target):
    graph = MazeGridWeighted(layout, target)
    _, path = a_star_search(graph, start, target)
    return path
