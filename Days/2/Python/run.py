#!/usr/bin/env python3
import os
import re
import sys
from collections import namedtuple

#######################Helping functions###########################

Entry = namedtuple('Entry', 'min max target data')


def data_parser(filepath):
    """Parse the data by splitting each line, and doing a regular expression."""
    pattern = r'(.*)-(.*) (.): (.*)'
    prog = re.compile(pattern)

    d = [prog.match(line) for line in open(filepath)]

    return [Entry(int(s.group(1)), int(s.group(2)), s.group(3), s.group(4)) for s in d]


#########################Main functions############################


def solver_1star(d):
    """Simply count the amount of elements, and mark them valid if min <= x <= max."""
    valid_count = 0
    for entry in d:
        if entry.min <= entry.data.count(entry.target) <= entry.max:
            valid_count += 1

    return valid_count


def solver_2star(d):
    """Find the index of the elements, and compare them with xor to the target letter."""
    valid_count = 0
    for entry in d:
        a = entry.data[entry.min - 1]
        b = entry.data[entry.max - 1]
        if (a == entry.target) ^ (b == entry.target):
            valid_count += 1

    return valid_count

##############################MAIN#################################


def main():
    """Run the program by itself, return a tuple of star1 and star2."""
    dirname = os.path.dirname(__file__)
    input_source = os.path.join(dirname, '..', 'input1.txt')
    # Make list, since the generator has to be used multiple times
    d = data_parser(input_source)
    return (solver_1star(d), solver_2star(d))


if __name__ == "__main__":
    star1, star2 = main()
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == '1':
            print(star1)
        elif arg == '2':
            print(star2)
    else:
        print("Day 1 first star:")
        print(star1)
        print("Day 1 second star:")
        print(star2)
