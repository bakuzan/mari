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

        if not next_y < 0 and next_y < len(grid) and not next_x < 0 and next_x < len(grid[next_y]) and grid[next_y][next_x] == NOT_VISITED:
            grid[y][x] = d
            grid[next_y][next_x] = OPPOSITE[d]
            carve_passages_from(next_x, next_y, grid)

    return grid


def loop_carve_passages_from(x, y, grid):
    height = len(grid) - 1
    width = len(grid[0]) - 1
    directions = random.sample(compass_directions, len(compass_directions))
    stack = [(x, y, directions[:])]
    while len(stack) != 0:
        print(stack)
        cx, cy, c_directions = stack.pop()
        while len(c_directions) != 0:
            d = c_directions.pop(0)
            nx, ny = x + DX[d], y + DY[d]
            if nx >= 0 and ny >= 0 and nx <= width and ny <= height and grid[ny][nx] == NOT_VISITED:
                grid[cy][cx] = d
                grid[ny][nx] = OPPOSITE[d]
                stack.append((nx, ny, directions[:]))
        stack.pop(0)
    return grid


def generate(width, height):
    grid = [[NOT_VISITED for c in range(width)] for r in range(height)]
    maze = carve_passages_from(1, 22, grid)
    display = []  # ["_" for _ in maze[0]]
    for y, _ in enumerate(maze):
        display.append("|")
        for x, _ in enumerate(maze[y]):
            display.append(" " if (grid[y][x] & S != 0) else "_")
            if grid[y][x] & E != 0:
                display.append(
                    " " if ((grid[y][x] | grid[y][x+1]) & S != 0) else "_")
            else:
                display.append("|")
        display.append('\n')
    print("".join(display))


if __name__ == "__main__":
    generate(37, 23)
