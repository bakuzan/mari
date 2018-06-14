import random

NOT_VISITED = 0
VISITED_PASSAGE = ' '
N, S, E, W = 1, 2, 4, 8
compass_directions = [N, S, E, W]
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}


def carve_passages_from(x, y, grid):
    directions = random.sample(compass_directions, len(compass_directions))
    for d in directions:
        next_x, next_y = x + DX[d], y + DY[d]

        if not next_y < 0 and next_y < len(grid) - 1 and not next_x < 0 and next_x < len(grid[next_y]) - 1 and grid[next_y][next_x] == NOT_VISITED:
            grid[y][x] = d
            grid[next_y][next_x] = OPPOSITE[d]
            carve_passages_from(next_x, next_y, grid)

    return grid


def generate(width, height):
    grid = [[NOT_VISITED for c in range(width)] for r in range(height)]
    maze = carve_passages_from(1, 21, grid)
    display = []
    for r, _ in enumerate(maze):
        for c, _ in enumerate(maze[r]):
            display.append(str(maze[r][c]))
        display.append('\n')
    print("".join(display))


if __name__ == "__main__":
    generate(37, 23)
