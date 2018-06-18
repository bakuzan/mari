import os
import sys
import msvcrt
from time import sleep
from maze import constants
from maze.maze import Maze


def check_if_quit(key):
    if key == constants.quit_key:
        sys.exit()


if __name__ == "__main__":
    os.system('cls')
    maze = Maze(9,9)
    while not maze.is_ready():
        sleep(0.5)
    print("Help Mari escape the maze!")
    while not maze.is_escaped() and (not maze.player or not maze.player.is_caught()):
        print('Use the WASD or the arrow keys to move Mari')
        maze.render()
        move = None
        while move not in constants.movement_keys:
            move = ord(msvcrt.getch())
            check_if_quit(move)
        maze.take_turn(move)

    if maze.is_escaped():
        print("Mari escaped!\nYou win!")
    elif maze.player.is_caught():
        print("Mari was caught!\nYou lose!")
    else:
        print("Game ended.")
