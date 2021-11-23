#!/usr/bin/env python3
import os
import sys
import re

#######################Helping functions###########################


def data_parser(filepath):
    """
    Split up in 3 groups of double newline, then parse accordingly
    """
    tmp = open(filepath).read().split('\n\n')

    # Parse the ranges
    range_dict = {}
    for line in tmp[0].split('\n'):
        match = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line)
        range_dict[match.group(1)] = [(int(match.group(2)), int(match.group(3))),
                                      (int(match.group(4)), int(match.group(5)))]

    def parse_ticket_block(block):
        tmp = block.split('\n')
        ret = []
        for line in tmp[1:]:
            ret.append([int(x) for x in line.split(',')])
        return ret
    # Parse own ticket
    own_ticket = parse_ticket_block(tmp[1])[0]
    other_tickets = parse_ticket_block(tmp[2])
    return {'range': range_dict, 'own': own_ticket, 'other': other_tickets}


#########################Main functions############################


def solver_1star(d):
    """
    Create a big hashmap with the viable values, and test the values
    that does not fit.
    """
    # Generate the set of good values
    good_values = set()
    for restrictions in d['range'].values():
        for min_l, max_l in restrictions:
            good_values.update(range(min_l, max_l+1))

    ret = 0
    for value in [item for sublist in d['other'] for item in sublist]:
        if value not in good_values:
            ret += value

    return ret


def solver_2star(d):
    """
    Sort away bad tickets like star1, and then do the same,
    but with a set per range. Detect what mapping fits on each range,
    and test each mapping set if it is size 1 (Must be the only viable value)
    do this until all mappings are applied.
    """

    # First we discard the bad elements
    good_values = set()
    for restrictions in d['range'].values():
        for min_l, max_l in restrictions:
            good_values.update(range(min_l, max_l+1))

    good_tickets = []
    for ticket in d['other']:
        good = True
        for value in ticket:
            if value not in good_values:
                good = False
                break
        if good:
            good_tickets.append(ticket)

    # Then we recreate each class to have a set instread of range
    # so we easier can find the good groups
    good_range = {}
    for key, ((va, vb), (vc, vd)) in d['range'].items():
        s = set()
        s.update(range(va, vb+1))
        s.update(range(vc, vd+1))
        good_range[key] = s

    # Go over each value (inlcuding our own)
    # and find the correct cadegory
    all_tickets = good_tickets
    all_tickets.append(d['own'])
    detection = {}
    for index, values in enumerate(zip(*all_tickets)):
        for group, restraint in good_range.items():
            if all([value in restraint for value in values]):
                if group not in detection:
                    detection[group] = set()
                detection[group].add(index)

    # We iterate over the detection dict, and find all elements we
    # Are sure are correct (set size 1)
    mapping = {}
    while True:
        singles = []
        for key, values in detection.items():
            if len(values) == 1:
                mapping[key] = list(values)[0]
                singles.append(list(values)[0])
        # Remove singles elements
        for single in singles:
            for key, values in detection.items():
                if single in values:
                    values.remove(single)
        if len(mapping) == len(detection):
            break

    # Find the correct values we look at, and generate the final return
    ret = 1
    for key, value in mapping.items():
        if key.startswith('departure'):
            ret *= d['own'][value]

    return ret

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
