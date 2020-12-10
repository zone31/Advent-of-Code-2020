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


def list_validate_number(lst, target):
    """
    Generate a set of the list, and find if there exist
    a candidate for a+b = x by doing x-a = b. If it is there, return true
    or else false.
    """
    elements = set(lst)
    for element in elements:
        if target - element in elements:
            return True
    return False


def list_sum_range_finder(lst, target):
    """
    Go over all the possible list lengths we want to iterate over,
    then iterate over the list by that size, and compare the sum to the target.
    If found, add together max and min vals of the sublist.
    """
    for n in range(2, len(lst)):
        for sublist in zip(*[lst[x:] for x in range(n)]):
            if sum(sublist) == target:
                return min(sublist) + max(sublist)


#########################Main functions############################


def solver_1star(d):
    """
    Set the amount of numbers we want to "preallocate", and then iterate over
    all indexes of the list, beginning from preallocate+1. If we cant find a
    match, return that value.
    """
    amount = 25
    for x in range(amount, len(d)):
        if not list_validate_number(d[x-amount:x], d[x]):
            return d[x]


def solver_2star(d):
    """
    Get the solution from star 1, and use the function to find the result.
    """
    target = solver_1star(d)
    return list_sum_range_finder(d, target)


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
