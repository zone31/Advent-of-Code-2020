#!/usr/bin/env python3
import os
import sys

#######################Helping functions###########################


def data_parser(filepath):
    """
    Split up line by line
    """
    tmp = open(filepath).read().split('\n')
    return tmp


def tree_precedence(tree):
    """
    We find each occurrence of the plus operator, and
    modify the tree so it is calculated first.
    """
    new_tree = []

    # Run on all nested values
    for value in tree:
        v = value
        if type(value) == list:
            v = tree_precedence(value)
        new_tree.append(v)

    # Find each plus, and modify the list
    while True:
        if '+' not in new_tree:
            break
        pos = new_tree.index('+')

        # modify the list with the new part
        part = [new_tree[pos-1], new_tree[pos], new_tree[pos+1]]
        new_tree = new_tree[:pos-1] + [part] + new_tree[pos+2:]

    return new_tree


def generate_tree(question):
    """
    Spits out a tree of operations that wa can calculate
    We could use a parser library, but that would be cheating, right?
    This is an extremely bad implementation, and very ugly
    """
    gobble = ""
    par_count = 0
    ret = []

    for char in question:
        if char == '(':
            par_count += 1
        if char == ')':
            par_count -= 1

        gobble += char
        if par_count == 0:
            if gobble.startswith("("):
                ret.append(generate_tree(gobble[1:-1]))
            else:
                if char != ' ':
                    if char in [f"{x}" for x in range(0, 10)]:
                        ret.append(int(char))
                    else:
                        ret.append(char)
            # reset gobble
            gobble = ""
    return ret


def calculate(tree):
    """
    Calculate the tree, with no nowledge of precedence.
    """
    value = None
    op = None
    for element in tree:
        if type(element) == int:
            if value is None:
                value = element
            else:
                value = op(value, element)
        if type(element) == str:
            if element == '*':
                def op(a, b): return a*b
            if element == '+':
                def op(a, b): return a+b
        if type(element) == list:
            tmp = calculate(element)
            if value is None:
                value = tmp
            else:
                value = op(value, tmp)
    return value


#########################Main functions############################


def solver_1star(d):
    """
    Parse each line in a tree, and then calculate the nested tree.
    """
    ret = 0
    for question in d:
        tree = generate_tree(question)
        value = calculate(tree)
        ret += value
    return ret


def solver_2star(d):
    """
    same as star 1, but we first add new precedence for the operators,
    then calculate it.
    """
    ret = 0
    for question in d:
        tree = generate_tree(question)
        new_tree = tree_precedence(tree)
        value = calculate(new_tree)
        ret += value
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
