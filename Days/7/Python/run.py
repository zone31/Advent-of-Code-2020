#!/usr/bin/env python3
import os
import re
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    We parse each line , and create a dict with the base case, and
    then a list containing the amount of suitcases in that case.
    """
    tmp = open(filepath).read().split('\n')
    ret = {}
    for element in tmp:
        name, others = element.split(' bags contain ')
        parsed_values = {}
        for value in [re.sub(r' bags?.?', '', x) for x in others.split(', ')]:
            if value == 'no other':
                continue
            parsed_values[value.split(' ', 1)[1]] = int(value.split(' ')[0])
        ret[name] = parsed_values

    return ret


def inverse_graph(g):
    """
    Inverse a acrylic suitcase graph.
    """
    ret = {}
    for name, elements in g.items():
        if name not in ret:
            ret[name] = {}
        for element, value in elements.items():
            if element not in ret:
                ret[element] = {}
            ret[element][name] = value

    return ret


def node_visits_unique(g, node_name):
    """
    Recursively get the unique nodes we hit, when traversing the suit
    case graph at node 'node_name'
    """
    node = g[node_name]
    vals = set(node.keys())
    for new_node in node.keys():
        vals |= node_visits_unique(g, new_node)

    return vals


def node_visits_count(g, node_name):
    """
    Like the recursive function, but return the amount of suitcases seen from
    that node.
    """
    node = g[node_name]
    vals = 1
    for new_node, value in node.items():
        vals += value * node_visits_count(g, new_node)

    return vals


#########################Main functions############################


def solver_1star(d):
    """
    Inverse the suitcase graph, and get the unique node visits.
    """
    inv_g = inverse_graph(d)
    visits = node_visits_unique(inv_g, 'shiny gold')
    return len(visits)


def solver_2star(d):
    """
    Count all the notes visited from the shiny gold suitcase.
    """
    return node_visits_count(d, 'shiny gold') - 1


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
