#!/usr/bin/env python3
import os
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Seperate by newline, and make into an int.
    """
    tmp = open(filepath).read().split('\n')
    return [int(x) for x in tmp]


# Save cache here to do some simple dynamic programming for the recursion
CACHE = {}


def tribonacci_seq(dist):
    """Get the tribonacci sequence."""
    if dist in CACHE:
        return CACHE[dist]
    paths = 0
    for x in range(1, 4):

        if dist - x <= 0:
            paths += 1
            break
        paths += tribonacci_seq(dist - x)
    CACHE[dist] = paths
    return paths

#########################Main functions############################


def solver_1star(d):
    """
    Simply solve by counting the occurrences of 3 sets and 1 set, and add a last tree set
    for the computer itself.
    Sort it to easily calculate the diff.
    """
    lst = sorted(d + [0])
    ones = 0
    threes = 0
    for a, b in zip(lst, lst[1:]):
        res = b - a
        if res == 1:
            ones += 1
        if res == 3:
            threes += 1
    return ones * (threes + 1)


def solver_2star(d):
    """
    Sort the list, and then count the occupance of 3 split.
    This inicates that the combinatorial graph cannot split there, and can
    be used as a stopping point.
    We then use the tribonacci sequence to calculate the amount of jumps for a
    sequence of one increment graph. We sprinkle it with some cache, if the
    input of ones in a row becomes too big.

    Note:
    It is not specifically written down that all inputs differ by 1 and 3.
    It it possible to solve this problem with a simple graph traversal counter
    with cache. But i found this solution more novel, and possibly also
    computationally faster.
    """
    lst = sorted(d + [0])
    lst.append(lst[-1] + 3)

    last_time = 0
    total_combinations = 1

    for a, b in zip(lst, lst[1:]):
        # Break when we see 3, and calculate the combinatorial
        if b-a == 3:
            total_combinations *= tribonacci_seq(last_time)
            last_time = 0
        else:
            last_time += 1

    return total_combinations

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
