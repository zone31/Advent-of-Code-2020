#!/usr/bin/env python3
import os
import re
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Split up each double newline in a list, then split up each person by single newline
    """
    tmp = open(filepath).read().split('\n\n')
    return [x.split('\n') for x in tmp]


#########################Main functions############################


def solver_1star(d):
    """
    Iterate over each group, then person, then answer, and keep a set
    on the seen answers in the group. Take the length of all seen answers per group
    """
    total = 0
    for group in d:
        seen = set()
        for person in group:
            for answer in person:
                if answer not in seen:
                    seen.add(answer)
        total += len(seen)

    return total


def solver_2star(d):
    """
    Like star 1, but keep a dict of the seen answers in the group. Count the occupance last,
    and if it is the same size as the group, all persons must have the answer. Add this to the total.
    """
    total = 0
    for group in d:
        seen = {}
        for person in group:
            for answer in person:
                if answer not in seen:
                    seen[answer] = 0
                seen[answer] += 1

        for answer, count in seen.items():
            if count == len(group):
                total += 1

    return total

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
