#!/usr/bin/env python3
import os
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Split by newline, and take the first number, and split the rest by
    comma into a list.
    """
    tmp = open(filepath).read().split('\n')
    return (tmp[0], [x for x in tmp[1].split(',')])


def gcd(a, b):
    """
    Get the greatest common divisor between two numbers
    """
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    Get the least common multiple between two numbers
    """
    return a * b / gcd(a, b)

#########################Main functions############################


def solver_1star(d):
    """
    Do some simple arithmetic with modulo to find the correct time.
    """
    current = int(d[0])
    numbers = [int(x) for x in d[1] if x != 'x']
    next_time = [current + (x - current % x) for x in numbers]
    delta = min(next_time) - current
    id = numbers[next_time.index(min(next_time))]
    return delta * id


def solver_2star(d):
    """
    We know, that when we find the first correct value for the setup
    between two numbers (a,b), it will always repeat itself after lcm(a,b)
    time. We use this to our advantage, and find the correct pointer, and then
    search by a stepsize of the previous lcm(a,b).
    """
    values = []
    c = 0
    for val in d[1]:
        if val != 'x':
            values.append((int(val), c))
        c += 1

    block_point = 0
    block_size = 1
    for value, offset in values:

        while True:
            if (block_point + offset) % value == 0:
                break
            block_point += block_size

        block_size = int(lcm(block_size, value))
    return block_point

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
