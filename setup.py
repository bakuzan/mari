from maze import Maze


def load_maze():
    with open("./layouts/narrow.txt", "r") as layout:
        return layout.read()


if __name__ == "__main__":
    layout = load_maze()
    maze = Maze(layout)
    maze.render()
