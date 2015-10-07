#!/usr/bin/python

import enum
import re
import sys

import vi.grid

class Vehicle(object):
    class Orientation(enum.Enum):
        horizontal = 0
        vertical   = 1

    @staticmethod
    def from_string(text):
        parts = map(int, list(x for x in re.split('[(,)]', text.strip()) if x))
        return Vehicle(
            Vehicle.Orientation(parts[0]),
            vi.grid.Coordinate(parts[1], parts[2]),
            parts[3])

    def __init__(self, orientation, coordinate, size):
        self.orientation = orientation
        self.coordinate  = coordinate
        self.size        = size

    def __str__(self):
        return 'Vehicle(orientation={0},coordinate={1},size={2}'.format(
            self.orientation, self.coordinate, self.size)
    
    def distance_from_coordinate(self, coordinate):
        if self.orientation is self.Orientation.horizontal:
            diff_y = abs(self.coordinate.y - coordinate.y)
            diff_x = min(abs(self.coordinate.x - coordinate.x),
                         abs(self.coordinate.x + self.size - 1 - coordinate.x))
        elif self.orientation is self.Orientation.vertical:
            diff_x = abs(self.coordinate.x - coordinate.x)
            diff_y = min(abs(self.coordinate.y - coordinate.y),
                         abs(self.coordinate.y + self.size - 1 - coordinate.y))

        return diff_y + diff_x
    
    def intersects_coordinate(self, coordinate):
        if self.orientation is self.Orientation.horizontal:
            return (self.coordinate.y == coordinate.y) and \
                   (self.coordinate.x <= coordinate.x) and \
                   (coordinate.x < self.coordinate.x + self.size)
        else:
            return (self.coordinate.x == coordinate.x) and \
                   (self.coordinate.y <= coordinate.y) and \
                   (coordinate.y < self.coordinate.y + self.size)

class Problem(object):
    def __init__(self, vehicles, goal):
        self.vehicles = vehicles
        self.goal     = goal

    def goal_test(self, state):
        return self.vehicles[0].intersects(self.goal)

    def heuristic(self, state):
        # Use Manhattan heuristic:
        return abs(self.goal.x - state.x) + abs(self.goal.y - state.y)

    def initial_node(self):
        return Node(self.start)

    def is_blocked(self, position):
        return position.x < 0 or \
               position.x >= self.grid.width or \
               position.y < 0 or \
               position.y >= self.grid.height or \
               self.grid.values[position.y][position.x] == vi.grid.obstructed

    def successors(self, node):
        for action in Action:
            if action == Action.move_up:
                successor_state = node.state.up()
            elif action == Action.move_down:
                successor_state = node.state.down()
            elif action == Action.move_left:
                successor_state = node.state.left()
            elif action == Action.move_right:
                successor_state = node.state.right()

            if not self.is_blocked(successor_state):
                yield Successor(self, node, successor_state, action, 1)

with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        print(Vehicle.from_string(line))

