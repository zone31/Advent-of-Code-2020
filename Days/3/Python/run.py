#!/usr/bin/env python3
import os
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """Line by line, and remove newline symbol."""

    d = [list(line)[:-1] for line in open(filepath)]

    return d


def tree_count(x_d, y_d, data):
    """Jump the desired delta amount, and loop for the y height of the data."""
    x = 0
    y = 0
    count = 0
    for _ in range(len(data)):
        x += x_d
        y += y_d
        if y > len(data) - 1:
            break

        if data[y][x % len(data[0])] == "#":
            count += 1

    return count


#########################Main functions############################


def solver_1star(d):
    """Call the helper function."""
    return tree_count(3, 1, d)


def solver_2star(data):
    """Call the helper function, and multiply the counts together."""
    a = tree_count(1, 1, data)
    b = tree_count(3, 1, data)
    c = tree_count(5, 1, data)
    d = tree_count(7, 1, data)
    e = tree_count(1, 2, data)
    return a*b*c*d*e


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
