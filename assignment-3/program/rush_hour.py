#!/usr/bin/python

import copy
import enum
import re
import sys

from vi.search.graph import BestFirst, Node, Successor
from vi.search.grid import Action
from vi.grid import Coordinate, Rectangle

class Vehicle(Rectangle):
    class Orientation(enum.Enum):
        horizontal = 0
        vertical   = 1

    @staticmethod
    def from_string(text):
        parts = map(int, list(x for x in re.split('[(,)]', text.strip()) if x))
        return Vehicle(
            Vehicle.Orientation(parts[0]),
            Coordinate(parts[1], parts[2]),
            parts[3])

    def __init__(self, orientation, coordinate, size):
        super(Vehicle, self).__init__(
            coordinate.x,
            coordinate.y,
            size if orientation is Vehicle.Orientation.horizontal else 1,
            size if orientation is Vehicle.Orientation.vertical else 1)

        self.orientation = orientation

    def __str__(self):
        return 'Vehicle({0},orientation={1})'.format(
            super(Vehicle, self).__str__(),
            self.orientation)

class Problem(object):
    def __init__(self, vehicles, dimensions, goal):
        self.vehicles   = vehicles
        self.dimensions = dimensions
        self.goal       = goal

    def goal_test(self, state):
        return state[0].intersects_coordinate(self.goal)

    def heuristic(self, state):
        h = 0
        for vehicle in state[1:]:
            if vehicle.orientation is Vehicle.Orientation.vertical and \
               vehicle.x >= state[0].x and \
               vehicle.intersects_coordinate(Coordinate(vehicle.x, state[0].y)):
                h = h + min(state[0].y - vehicle.y, \
                            vehicle.y + vehicle.height - state[0].y)

        #return h + sum(self.vehicles[0].distance_to_coordinate(self.goal))
        return sum(self.vehicles[0].distance_to_coordinate(self.goal))

    def initial_node(self):
        return Node(self.vehicles)

    def successors(self, node):
        def build_successor(action, vehicle_id, diff_x, diff_y):
            successor_state     = copy.deepcopy(node.state)

            successor_vehicle   = successor_state[vehicle_id]
            successor_vehicle.x = successor_vehicle.x + diff_x
            successor_vehicle.y = successor_vehicle.y + diff_y

            return Successor(
                self, node, successor_state, (action, vehicle_id, 1), 1)

        for vehicle_id, vehicle in enumerate(node.state):
            if vehicle.orientation is Vehicle.Orientation.horizontal:
                if vehicle.x > 0 and \
                   not any(other.intersects_coordinate(
                               Coordinate(vehicle.x - 1, vehicle.y)) \
                           for other in node.state \
                           if other is not vehicle):

                    yield build_successor(Action.move_left, vehicle_id, -1, 0)

                if vehicle.x + vehicle.width < self.dimensions.x and \
                   not any(other.intersects_coordinate( \
                               Coordinate(vehicle.x + vehicle.width, vehicle.y)) \
                           for other in node.state \
                           if other is not vehicle):

                    yield build_successor(Action.move_right, vehicle_id, +1, 0)

            elif vehicle.orientation is Vehicle.Orientation.vertical:
                if vehicle.y > 0 and \
                   not any(other.intersects_coordinate( \
                               Coordinate(vehicle.x, vehicle.y - 1)) \
                           for other in node.state \
                           if other is not vehicle):

                    yield build_successor(Action.move_up, vehicle_id, 0, -1)

                if vehicle.y + vehicle.height < self.dimensions.y and \
                   not any(other.intersects_coordinate( \
                               Coordinate(vehicle.x, vehicle.y + vehicle.height)) \
                           for other in node.state \
                           if other is not vehicle):

                    yield build_successor(Action.move_down, vehicle_id, 0, +1)

def print_solution(solution):
    i = 1
    while i < len(solution.path):
        action, state = solution.path[i]
        num_moves = action[2]

        j = i + 1
        while j < len(solution.path):
            if action[0] == solution.path[j][0][0] and \
               action[1] == solution.path[j][0][1]:
                num_moves = num_moves + 1
                j = j + 1
            else:
                break
        i = j

        print('Move Vehicle#{0} {1} {2} step{3}'.format(
            action[1],
            str(action[0]).split('_')[1],
            num_moves,
            's' if num_moves > 1 else ''))

with open(sys.argv[1]) as f:
    vehicles = tuple(Vehicle.from_string(line) for line in f.readlines())

problem = Problem(vehicles, Coordinate(6, 6), Coordinate(5, 2))
search  = BestFirst(problem, BestFirst.Strategy.astar)
solution = search.search()

print("heuristic 1")
print(search.state)
print("open = {0} closed = {1} total = {2}".format(
    len(list(search.open_list())),
    len(list(search.closed_list())),
    len(list(search.open_list())) + len(list(search.closed_list()))))

print_solution(solution)


