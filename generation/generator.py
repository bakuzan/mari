from random import randrange, sample

NOT_VISITED = 0
VISITED_PASSAGE = ' '
N, S, E, W = 1, 2, 4, 8
compass_directions = [N, S, E, W]
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}


def carve_passages_from(x, y, grid):
    directions = sample(compass_directions, len(compass_directions))
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
    directions = sample(compass_directions, len(compass_directions))
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


class MazeGenerator:
    """
    Generator object for maze
    """
    PASSAGE = 0
    WALL = 1

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.hMax = (2 * h) + 1
        self.wMax = (2 * w) + 1

    def generate(self):
        g = [[self.WALL for c in range(self.wMax)] for r in range(self.hMax)]
        grid = g

        # random starting co-ords from 1 to index, multiples of 2
        c_row = randrange(1, self.hMax, 2)
        c_col = randrange(1, self.wMax, 2)
        stack = [(c_row, c_col)]
        grid[c_row][c_col] = self.PASSAGE

        while grid:
            (c_row, c_col) = stack[-1]
            neighbours = self._get_neighbours(c_row, c_col, grid)

            if len(neighbours) == 0:
                # drop the current item from the stack
                stack = stack[:-1]
            else:
                # carve passage in neighbour
                n_row, n_col = neighbours[0]
                grid[n_row][n_col] = self.PASSAGE
                grid[(n_row + c_row) // 2][(n_col + c_col) // 2] = self.PASSAGE
                stack += [(n_row, n_col)]
        
        return grid

    """
    internals
    """

    def _get_neighbours(self, x, y, grid):
        """
        get 'neighbouring' cells in a random order
        """
        n_list = []

        if x > 1 and grid[x - 2][y] == self.WALL:
            n_list.append((x - 2, y))
        if x < self.hMax - 2 and grid[x + 2][y] == self.WALL:
            n_list.append((x + 2, y))
        if y > 1 and grid[x][y - 2] == self.WALL:
            n_list.append((x, y - 2))
        if y < self.wMax - 2 and grid[x][y + 2] == self.WALL:
            n_list.append((x, y + 2))

        return sample(n_list, len(n_list))



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
    # generate(37, 23)
    m = MazeGenerator(37,23)
    maze = m.generate()
    display = []
    for y, _ in enumerate(maze):
        for x, _ in enumerate(maze[y]):
            display.append("#" if maze[y][x] == True else ' ')
        display.append('\n')
    print("".join(display))
