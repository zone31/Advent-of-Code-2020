#!/usr/bin/env python3
import os
import sys
from pprint import pprint
#######################Helping functions###########################


def data_parser(filepath):
    """
    Split by commas.
    """
    tmp = open(filepath).read().split(',')
    return [int(x) for x in tmp]


#########################Main functions############################


def solver_1star(d):
    """
    Go over each value. detect if it has been seen in last iteration,
    and repeat until we hit 2020 numbers
    """
    seen = list(d)
    last_seen_index = len(seen) - 1
    for _ in range(len(seen), 2020):
        last_number = seen[-1]

        # Find values
        val = 0
        if last_seen_index + 1 != len(seen):
            val = len(seen) - 1 - last_seen_index

        # Test last seen
        last_seen_index = len(seen)
        if val in seen:
            last_seen_index = len(seen) - 1 - seen[::-1].index(val)
        seen.append(val)

    return seen[-1]


def solver_2star(d):
    """
    Rewrite into a dict of star 2, to optimize performance
    """
    seen_dict = {val: index for index, val in enumerate(d)}
    curr_number = d[-1]
    for index in range(len(d) - 1, 30000000 - 1):
        next_number = 0
        if curr_number in seen_dict and seen_dict[curr_number] != index:
            next_number = index - seen_dict[curr_number]

        # Update the current number index
        seen_dict[curr_number] = index
        curr_number = next_number
    return curr_number

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
