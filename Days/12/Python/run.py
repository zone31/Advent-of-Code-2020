#!/usr/bin/env python3
import os
import sys
from collections import namedtuple
from math import sin, cos, radians

#######################Helping functions###########################


Action = namedtuple('Operation', 'inst value')
StateShip = namedtuple('State', 'x y degree')
StateWaypoint = namedtuple('State', 'x_s y_s x_w y_w')


def data_parser(filepath):
    """
    Split by line, an make into a state tuple
    """
    tmp = open(filepath).read().split('\n')
    return [Action(x[0], float(x[1:])) for x in tmp]


def step_waypoint(state, action):
    """
    Translate each instrustion into a state change.
    """
    inst = {
        'N': lambda s, a: StateWaypoint(s.x_s, s.y_s, s.x_w, s.y_w + a.value),
        'S': lambda s, a: StateWaypoint(s.x_s, s.y_s, s.x_w, s.y_w - a.value),
        'E': lambda s, a: StateWaypoint(s.x_s, s.y_s, s.x_w + a.value, s.y_w),
        'W': lambda s, a: StateWaypoint(s.x_s, s.y_s, s.x_w - a.value, s.y_w),
        'L': lambda s, a: StateWaypoint(s.x_s, s.y_s,
                                        s.x_w * cos(radians(a.value)) -
                                        s.y_w * sin(radians(a.value)),
                                        s.y_w * cos(radians(a.value)) +
                                        s.x_w * sin(radians(a.value))),
        'R': lambda s, a: StateWaypoint(s.x_s, s.y_s,
                                        s.x_w * cos(radians(-1.0*a.value)) -
                                        s.y_w * sin(radians(-1.0*a.value)),
                                        s.y_w * cos(radians(-1.0*a.value)) +
                                        s.x_w * sin(radians(-1.0*a.value))),
        'F': lambda s, a: StateWaypoint(s.x_s + s.x_w * a.value,
                                        s.y_s + s.y_w * a.value,
                                        s.x_w, s.y_w),
    }
    return inst[action.inst](state, action)


def step_ship(state, action):
    """
    Translate each instrustion into a state change.
    """
    inst = {
        'N': lambda s, a: StateShip(s.x, s.y + a.value, s.degree),
        'S': lambda s, a: StateShip(s.x, s.y - a.value, s.degree),
        'E': lambda s, a: StateShip(s.x + a.value, s.y, s.degree),
        'W': lambda s, a: StateShip(s.x - a.value, s.y, s.degree),
        'L': lambda s, a: StateShip(s.x, s.y, s.degree - a.value),
        'R': lambda s, a: StateShip(s.x, s.y, s.degree + a.value),
        'F': lambda s, a: StateShip(s.x + a.value * sin(radians(s.degree)),
                                    s.y + a.value * cos(radians(s.degree)),
                                    s.degree),
    }
    return inst[action.inst](state, action)

#########################Main functions############################


def solver_1star(d):
    """
    Set an initial state, and move the system each instruction, then take
    the manhatten distance of the state.
    """
    state = StateShip(0, 0, 90)
    for inst in d:
        state = step_ship(state, inst)

    return round(abs(state.x) + abs(state.y))


def solver_2star(d):
    """
    Set an initial state, and move the system each instruction, then take
    the manhatten distance of the state.
    """
    state = StateWaypoint(0, 0, 10, 1)
    for inst in d:
        state = step_waypoint(state, inst)

    return round(abs(state.x_s) + abs(state.y_s))

##############################MAIN#################################


def main():
    """Run the program by itself, return a tuple of star1 and star2."""
    dirname = os.path.dirname(__file__)
    input_source = os.path.join(dirname, '..', 'input1.txt')
    # Make list, since the generator has to be used multiple times
    d = data_parser(input_source)
    return (solver_1star(d), solver_2star(d))


def day_name():
    """Get the date name from the folder."""
    file_path = os.path.dirname(__file__)
    day_path = os.path.normpath(os.path.join(file_path, '..'))
    return os.path.basename(day_path)


if __name__ == "__main__":
    star1, star2 = main()
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == '1':
            print(star1)
        elif arg == '2':
            print(star2)
    else:
        day = day_name()
        print(f"Day {day} first star:")
        print(star1)
        print(f"Day {day} second star:")
        print(star2)
