#!/usr/bin/python

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *

import vi.grid
import vi.qt.grid
import vi.search.graph
import vi.search.grid

binary_board_values = {
    '.': 1, '#': -1
}

binary_board_symbols = {
    1: '.', -1: '#'
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

def render(painter, colors, sizes, problem, solution):
    vi.qt.grid.draw_grid(painter, colors['cells'], problem.grid, sizes['cell'])

    vi.qt.grid.draw_cell(painter, colors['start'], problem.grid, sizes['cell'], problem.start)
    vi.qt.grid.draw_cell(painter, colors['goal'], problem.grid, sizes['cell'], problem.goal)

    painter.setPen(QPen(colors['line'], 0))
    vi.qt.grid.draw_grid_lines(painter, problem.grid, sizes['cell'])

    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(colors['text']))
    painter.setFont(QFont('Arial', sizes['symbol']))

    for action, state in solution.path:
        vi.qt.grid.draw_cell_text(
            painter, problem.grid, sizes['cell'], state, u'\u2022')

app = QApplication([ '-platform', 'offscreen'])

input_file_name  = sys.argv[1]
output_file_name = '{0}.svg'.format(
    os.path.splitext(os.path.basename(input_file_name))[0])

problem  = load_binary_board_file(input_file_name)
search   = vi.search.graph.BestFirst(problem, vi.search.graph.BestFirst.Strategy.astar)
solution = search.search()

cell_size     = 50
text_size     = 10
symbol_size   = 25
margin_size   = 5
output_width  = 2 * margin_size + cell_size * problem.grid.width
output_height = 2 * margin_size + cell_size * problem.grid.height

generator = QSvgGenerator()
generator.setFileName(output_file_name)

generator.setSize(QSize(output_width, output_height))
generator.setViewBox(QRect(0, 0, output_width, output_height))
generator.setTitle("permve-ntnu-tdt4136-assignment-3: {0}".format(output_file_name))
generator.setDescription("AI Intro Search Visualization")

painter = QPainter(generator)
painter.translate(margin_size, margin_size)

colors = {
    'start': QColor(0, 221, 0),
    'goal':  QColor(238, 68, 0),
    'line':  QColor(51, 51, 51),
    'text':  QColor(51, 51, 51),
    'cells': {
        -1: QColor(51, 51, 51),
         1: QColor(255, 255, 255)
    }
}

sizes = {
    'cell':   cell_size,
    'symbol': symbol_size,
    'text':   text_size
}

render(painter, colors, sizes, problem, solution)
painter.end()

