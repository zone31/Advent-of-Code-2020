#!/usr/bin/env python3
import os
import sys
from collections import namedtuple
import itertools

#######################Helping functions###########################


Coord = namedtuple('State', 'x y z')
Coord4 = namedtuple('State', 'x y z w')


def data_parser(filepath):
    """
    Go over each coordinate, and return it as a nested list.
    """
    tmp = open(filepath).read().split('\n')
    return [list(x) for x in tmp]


def iteration(space, coord_class):
    """
    Take a space, and a classification of the coord class.
    Generate all values we must focus on (Local around all active
    values in the input space) and return a new set with new values
    """
    new_space = set()

    # Generate list of neighbors we have to theck
    scope = set()
    for coord in space:
        r = [range(x-1, x+2) for x in coord]
        for d in itertools.product(*r):
            scope.add(coord_class(*d))

    for coord in scope:
        # get the coords local space, and test how many we have in the set
        r = [range(x-1, x+2) for x in coord]
        seen = 0
        for d in itertools.product(*r):
            if coord_class(*d) in space:
                seen += 1
        if coord in space:
            seen -= 1  # We have seen ourself, subtract
            if 2 <= seen <= 3:
                new_space.add(coord)
        else:
            if seen == 3:
                new_space.add(coord)

    return new_space


#########################Main functions############################


def solver_1star(d):
    """
    Use a set for all values, and then iterate over each step 6 times.
    """
    # Convert 2d plane into a set of 3d coords
    space = set()
    for x, r in enumerate(d):
        for y, value in enumerate(r):
            if value == '#':
                space.add(Coord(x, y, 0))

    for _ in range(6):
        space = iteration(space, Coord)
    return len(space)


def solver_2star(d):
    """
    Do the same as star1, but use 4d coords instead.
    """
    # Convert 2d plane into a set of 4d coords
    space = set()
    for x, r in enumerate(d):
        for y, value in enumerate(r):
            if value == '#':
                space.add(Coord4(x, y, 0, 0))

    for _ in range(6):
        space = iteration(space, Coord4)
    return len(space)

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
