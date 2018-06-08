import sys
import msvcrt
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
        print('Use the WASD or the arrow keys to move Mari\n')
        move = ord(msvcrt.getch())
        while move not in constants.movement_keys:
            print('Press W,A,S, or D to move Mari\n')
            move = ord(msvcrt.getch())
            if move == constants.quit_key:
                sys.exit()
        maze.move(move)
    print("Mari escaped!")
