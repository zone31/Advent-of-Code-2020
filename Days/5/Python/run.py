#!/usr/bin/env python3
import os
import re
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Split each ticket by newline.
    """
    data = open(filepath).read().split('\n')
    return data


def bording_pass_parse(value):
    """
    The values seating are represented binary, where the first 7 are
    the row values, and the last 3 are the column.
    """
    row = int(value[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(value[7:].replace('L', '0').replace('R', '1'), 2)
    id = row * 8 + col
    return {'row': row, 'col': col, 'id': id}


#########################Main functions############################


def solver_1star(d):
    """
    Go over all the id's, and find the higest.
    """
    highest_id = 0
    for x in d:
        this_id = bording_pass_parse(x)['id']
        if this_id > highest_id:
            highest_id = this_id

    return highest_id


def solver_2star(d):
    """
    Use the rule (((n**2) / 2) + n/2) to find the sum of total id's.
    Iterate over the already seen id's, and sum them together.
    The missing id must therefore be the max minus the total
    """
    accum = 0
    highest_id = 0
    for x in d:
        this_id = bording_pass_parse(x)['id']
        accum += this_id
        if this_id > highest_id:
            highest_id = this_id

    # Add the first rows
    accum += sum(range(0, 6))

    # Find the sum of id's, if they where all taken
    total = ((highest_id**2) / 2) + highest_id/2

    # Subtract it from eachother, returning our id
    res = total - accum

    return int(res)


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
