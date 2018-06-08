import constants
from maze import Maze


def load_maze():
    with open("./layouts/narrow.txt", "r") as layout:
        return layout.readlines()


if __name__ == "__main__":
    lines = load_maze()
    maze = Maze(lines)

    print("Help Mari escape the maze!")
    while not maze.is_escaped():
        maze.render()
        move = input('Use the WASD keys to move Mari\n')
        while move not in constants.movement_keys:
            move = input('Press W,A,S, or D to move Mari\n')

        maze.move(move)
    print("Mari escaped!")
