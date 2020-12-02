#!/usr/bin/env python3
import sys
import os

#######################Helping functions###########################


def data_parser(filepath):
    """Parse the data by splitting each line into a number."""
    d = [int(line) for line in open(filepath)]
    return d


#########################Main functions############################


def solver_1star(d):
    """
    Iterate over all combinations, and add them together. Could be optimized if the
    list was sorted, and binary search where done to find the closest element.
    The elements could also be mate in to a hashset, and we would be able to find
    the target value by y=2020-x
    """
    target = 2020
    for index, a in enumerate(d):
        for b in d[index:]:
            if a + b == target:
                return a * b


def solver_2star(d):
    """
    Same as first star, but with another number
    """
    target = 2020
    for index_a, a in enumerate(d):
        for index_b, b in enumerate(d[index_a:]):
            for c in d[index_a+index_b:]:
                if a + b + c == target:
                    return a * b * c

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
