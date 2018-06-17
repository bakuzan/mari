from random import randrange, sample, shuffle
from time import sleep
from maze import constants

class MazeGenerator:
    """
    Generator object for maze
    """
    PASSAGE = 0
    WALL = 1
    EXIT = constants.maze_point_exit

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.hMax = (2 * h) + 1
        self.wMax = (2 * w) + 1

    def generate(self, animate = False):
        """
        create a maze layout
        """
        g = [[self.WALL for c in range(self.wMax)] for r in range(self.hMax)]
        grid = g

        # random starting co-ords from 1 to index, multiples of 2
        c_row = randrange(1, self.hMax, 2)
        c_col = randrange(1, self.wMax, 2)
        stack = [(c_row, c_col)]
        grid[c_row][c_col] = self.PASSAGE

        while stack:
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
            
            if animate:
                self._render(grid)
                sleep(0.10)
        
        grid = self._cut_exit(grid)
        if animate: 
            self._render(grid)
        
        for y, _ in enumerate(grid):
            for x, _ in enumerate(grid[y]):
                sq = grid[y][x]
                if sq == self.PASSAGE:
                    grid[y][x] = constants.maze_point_empty
                elif sq == self.WALL:
                    grid[y][x] = constants.maze_point_wall
                else:
                    grid[y][x] = sq
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

    def _cut_exit(self, grid):
        """
        removes 1 square at random from the outer wall
        """
        exit_options = []
        exit_point = None

        while not exit_point:
            exit_options = self._generate_exit_options(exit_options)
            shuffle(exit_options)
            c_x, c_y, (t_x, t_y) = exit_options.pop()

            # if this neighbour is empty, this is a valid exit
            if grid[c_x + t_x][c_y + t_y] == self.PASSAGE: 
                exit_point = (c_x, c_y)

        e_x, e_y = exit_point
        grid[e_y][e_x] = self.EXIT
        return grid
    
    def _generate_exit_options(self, options):
        """
        create randomised exit square list
        """
        if len(options) != 0:
            return options
        else:
            top_wall = (randrange(1, self.wMax, 2), 0, (0, 1))
            left_wall = (0, randrange(1, self.hMax, 2), (1, 0))
            bottom_wall = (randrange(1, self.wMax, 2), self.hMax, (0, -1))
            right_wall = (self.wMax, randrange(1, self.hMax, 2), (-1, 0))
            return [top_wall, left_wall, right_wall, bottom_wall]

    def _render(self, grid):
        display = []
        for y, _ in enumerate(grid):
            for x, _ in enumerate(grid[y]):
                sq = grid[y][x]
                if sq == self.PASSAGE:
                    display.append(constants.maze_point_empty)
                elif sq == self.WALL:
                    display.append(constants.maze_point_wall)
                else:
                    display.append(sq)
            display.append('\n')
        print("".join(display), end="\r", flush=True)

if __name__ == "__main__":
    m = MazeGenerator(10,10)
    maze = m.generate(True)
