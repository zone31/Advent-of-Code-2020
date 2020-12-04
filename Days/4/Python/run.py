#!/usr/bin/env python3
import os
import re
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Seperate by double new line, then by newline or space, and then make
    into a dict by splitting at '.'
    """
    blocks = open(filepath).read().split('\n\n')
    reg = re.compile("\n| ")
    data = [{x.split(":")[0]:x.split(":")[1]
             for x in reg.split(y)} for y in blocks]
    return data


#########################Main functions############################


def solver_1star(d):
    """
    Check if the dict for each element have the valid keys
    """
    valid = ['eyr', 'iyr', 'byr', 'ecl', 'pid', 'hcl', 'hgt']
    count = 0
    for element in d:
        if all([(x in element.keys()) for x in valid]):
            count += 1

    return count


def solver_2star(d):
    """
    Check if all valid keys is there, and then test each attribute with a simple lambda.
    """
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #   If cm, the number must be at least 150 and at most 193.
    #   If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.
    valid = ['eyr', 'iyr', 'byr', 'ecl', 'pid', 'hcl', 'hgt']
    eye_color = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    func = {
        'byr': lambda x: 1920 <= int(x) <= 2002,
        'iyr': lambda x: 2010 <= int(x) <= 2020,
        'eyr': lambda x: 2020 <= int(x) <= 2030,
        'hgt': lambda x: (x[-2:] == "cm" and 150 <= int(x[:-2]) <= 193) or (x[-2:] == "in" and 59 <= int(x[:-2]) <= 76),
        'hcl': lambda x: bool(re.match(r"^#[a-f0-9]{6}$", x)),
        'ecl': lambda x: x in eye_color,
        'pid': lambda x: len(x) == 9 and type(int(x)) == int,
        'cid': lambda x: True,
    }
    count = 0
    for element in d:
        if all([(x in element.keys()) for x in valid]):
            if all([func[key](value) for key, value in element.items()]):
                count += 1
    return count

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
