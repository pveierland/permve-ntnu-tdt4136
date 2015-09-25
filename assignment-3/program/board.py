from PyQt5 import QtCore, QtGui, QtSvg, QtWidgets
import sys

import vi.grid
import vi.search.graph
import vi.search.grid

binary_board_values = {
    '.': 1, '#': -1
}

binary_board_symbols = {
    1: '.', -1: '#'
}

fancy_board_values = {
    'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1, '.': 1, '#': -1
}

fancy_board_symbols = {
    100: 'w', 50: 'm', 10: 'f', 5: 'g', 1: 'r'
}

def load_board_file(filename, value_mapping):
    with open(filename, 'r') as f:
        map_data = [ line.strip() for line in f.readlines() if line.strip() ]

        grid = vi.grid.Grid(width = len(map_data[0]), height = len(map_data))

        start = None
        goal  = None

        # x, y is indexed with (0, 0) at bottom left of map:
        for y, line in enumerate(reversed(map_data)):
            for x, value in enumerate(line):
                if value == 'A':
                    start = vi.grid.Coordinate(x, y)
                elif value == 'B':
                    goal = vi.grid.Coordinate(x, y)
                else:
                    grid.values[y][x] = value_mapping[value]

        if not start:
            raise ValueError("{0}: no start location found".format(filename))

        if not goal:
            raise ValueError("{0}: no goal location found".format(filename))

        return vi.search.grid.Problem(grid, start, goal)

def load_binary_board_file(filename):
    return load_board_file(filename, binary_board_values)

def load_fancy_board_file(filename):
    return load_board_file(filename, fancy_board_values)

def render_problem(problem, painter, size, line_color, colors):
    def draw_square(x, y, color):
        painter.fillRect(size * x, size * (problem.grid.height - y - 1), size, size, color)

    def draw_text(x, y, text):
        painter.drawText(QtCore.QRectF(size * x, size * (problem.grid.height - y - 1), size, size),
                         QtCore.Qt.AlignCenter,
                         text)

    for y in range(problem.grid.height):
        for x in range(problem.grid.width):
            draw_square(x, y, colors[problem.grid.values[y][x]])

    painter.setPen(QtGui.QPen(QtGui.QBrush(line_color), size / 25))
    painter.setFont(QtGui.QFont('Arial', 11))

    astar = vi.search.graph.AStar(problem)
    solution = astar.search()

    for closed_state, closed_node in astar.closed_hash_table.iteritems():
        draw_square(closed_state.x, closed_state.y, QtGui.QColor(175, 238, 238))
        draw_text(closed_state.x, closed_state.y, 'g={0}\nh={1:.1f}'.format(closed_node.path_cost, closed_node.heuristic_value))

    for open_state, open_node in astar.open_hash_table.iteritems():
        draw_square(open_state.x, open_state.y, QtGui.QColor(152, 251, 152))
        draw_text(open_state.x, open_state.y, 'g={0}\nh={1:.1f}'.format(open_node.path_cost, open_node.heuristic_value))

    draw_square(problem.start.x, problem.start.y, QtGui.QColor(0, 221, 0))
    draw_text(problem.start.x, problem.start.y, 'START')
    draw_square(problem.goal.x, problem.goal.y, QtGui.QColor(238, 68, 0))
    draw_text(problem.goal.x, problem.goal.y, 'GOAL')

    for y in range(problem.grid.height + 1):
        painter.drawLine(0, size * (problem.grid.height - y), size * problem.grid.width, size * (problem.grid.height - y))

    for x in range(problem.grid.width + 1):
        painter.drawLine(size * x, 0, size * x, size * problem.grid.height)

app = QtWidgets.QApplication([ '-platform', 'offscreen'])

problem = load_binary_board_file(
    '/home/pveierland/permve-ntnu-tdt4136/assignment-3/problem/boards/board-1-3.txt')

grid_cell_size = 50
margin_wtf = 5

generator = QtSvg.QSvgGenerator()
generator.setFileName('wat.svg')

output_width = 2 * margin_wtf + grid_cell_size * problem.grid.width
output_height = 2 * margin_wtf + grid_cell_size * problem.grid.height

generator.setSize(QtCore.QSize(output_width, output_height))
generator.setViewBox(QtCore.QRect(0, 0, output_width, output_height))
#generator.setViewBox(QtCore.QRect(0, 0, margin_wtf + 2 * grid_cell_size * problem.grid.width, 2 * margin_wtf + grid_cell_size * problem.grid.height))
generator.setTitle("SVG Generator Example Drawing")
generator.setDescription("wuwu description")

painter = QtGui.QPainter(generator)
painter.translate(margin_wtf, margin_wtf)
render_problem(problem, painter, grid_cell_size, QtGui.QColor(51, 51, 51), { 1: QtGui.QColor(0, 0, 0, 0), -1: QtGui.QColor(51, 51, 51) })
painter.end()

