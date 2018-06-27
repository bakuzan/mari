from .point import Point

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'

translations = {
    'up': Point(0, -1),
    'left': Point(-1, 0),
    'down': Point(0, 1),
    'right': Point(1, 0)
}

hammer = 'h'
troll = 'T'
character = {
    'up': '^',
    'left': '<',
    'down': 'v',
    'right': '>'
}

""" WASD """
""" arrow keys """
movement_keys = {
    119: 'up',
    97: 'left',
    115: 'down',
    100: 'right',
    72: 'up',
    75: 'left',
    80: 'down',
    77: 'right',
}
quit_key = 27

key_press = {
    'w': 'up',
    'a': 'left',
    's': 'down',
    'd': 'right',
    'up': 'up',
    'left': 'left',
    'down': 'down',
    'right': 'right'
}
key_press_action = {
    'h': 'sledgehammer'
}

maze_point_empty = ' '
maze_point_wall = '#'
maze_point_exit = 'X'

maze_tile_passage = 'passage'
maze_tile_wall = 'wall'
maze_tile_exit = 'exit'