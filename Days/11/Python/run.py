#!/usr/bin/env python3
import os
import sys
import copy
from pprint import pprint

#######################Helping functions###########################


def data_parser(filepath):
    """
    """
    tmp = open(filepath).read().split('\n')
    return [list(x) for x in tmp]


def clamp(min_n, n, max_n):
    """
    Clamp an integer between 2 values
    """
    return max(min(max_n, n), min_n)


def adjacent(floorplan, x, y):
    """
    Count the occupation around a point on the floor
    """
    len_x = len(floorplan)
    len_y = len(floorplan[0])
    min_x = clamp(0, x-1, len_x - 1)
    max_x = clamp(0, x+2, len_x)
    min_y = clamp(0, y-1, len_y - 1)
    max_y = clamp(0, y+2, len_y)
    seen = 0
    for x_delta in range(min_x, max_x):
        for y_delta in range(min_y, max_y):
            if (x_delta, y_delta) == (x, y):
                continue
            if floorplan[x_delta][y_delta] == '#':
                seen += 1
    return seen


def adjacent_air(floorplan, x, y):
    """
    Count the occupation around a point, and check if all 8
    dirrections are clear.
    """
    looks_dirs = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),  (1, 0),
                  (-1, 1), (0, 1), (1, 1)]

    seen = 0
    for looks_dir in looks_dirs:
        x_d = x
        y_d = y
        while True:
            x_d = x_d + looks_dir[0]
            y_d = y_d + looks_dir[1]
            if x_d < 0 or y_d < 0:
                break
            try:
                if floorplan[x_d][y_d] == 'L':
                    break
                if floorplan[x_d][y_d] == '#':
                    seen += 1
                    break
            except:
                break
    return seen


def simulate_step(floorplan, adjacent_func, threshhold):
    """
    Simulate an evolutionary step
    """
    f = copy.deepcopy(floorplan)

    for x in range(len(floorplan)):
        for y in range(len(floorplan[0])):
            if floorplan[x][y] == 'L' and adjacent_func(floorplan, x, y) == 0:
                f[x][y] = '#'
            if floorplan[x][y] == '#' and adjacent_func(floorplan, x, y) >= threshhold:
                f[x][y] = 'L'
    return f


def bprint(floorplan):
    for l in floorplan:
        print("".join(l))

#########################Main functions############################


def solver_1star(d):
    """
    Go over each evolution step by step. And break out when
    the step does not change anything. Then count the seats.
    """
    f = copy.deepcopy(d)
    while True:
        f_next = simulate_step(f, adjacent, 4)
        if f_next == f:
            break
        f = f_next

    # Test how many are occupied
    occupied = 0
    for x in range(len(f)):
        for y in range(len(f[0])):
            if f[x][y] == '#':
                occupied += 1

    return occupied


def solver_2star(d):
    """
    Go over each evolution step by step. And break out when
    the step does not change anything. Then count the seats.
    """
    f = copy.deepcopy(d)
    c = 0
    while True:
        f_next = simulate_step(f, adjacent_air, 5)
        if f_next == f:
            break
        f = f_next

    # Test how many are occupied
    occupied = 0
    for x in range(len(f)):
        for y in range(len(f[0])):
            if f[x][y] == '#':
                occupied += 1

    return occupied

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
