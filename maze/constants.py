from point import Point

translations = {
    'up': Point(0, -1),
    'left': Point(-1, 0),
    'down': Point(0, 1),
    'right': Point(1, 0)
}

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

maze_point_empty = ' '
maze_point_wall = '#'
maze_point_exit = 'X'
