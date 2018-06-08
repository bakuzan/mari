import os
import sys
import msvcrt
import constants
from maze import Maze


def load_maze():
    with open("./layouts/narrow.txt", "r") as layout:
        return layout.readlines()


def check_if_quit(key):
    if key == constants.quit_key:
        sys.exit()


if __name__ == "__main__":
    lines = load_maze()
    maze = Maze(lines)
    os.system('cls')
    print("Help Mari escape the maze!")
    while not maze.is_escaped():
        maze.render()
        move = None
        while move not in constants.movement_keys:
            print('Use the WASD or the arrow keys to move Mari\n')
            move = ord(msvcrt.getch())
            check_if_quit(move)
        os.system('cls')
        maze.move(move)
    print("Mari escaped!")
