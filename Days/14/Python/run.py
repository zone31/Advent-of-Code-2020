#!/usr/bin/env python3
import os
import sys
from collections import namedtuple
import re
import itertools

#######################Helping functions###########################

State = namedtuple('State', 'mem mask')
Inst = namedtuple('Inst', 'inst arg1 arg2')


def data_parser(filepath):
    """
    Split by newline, and parse into instruction tuple
    """
    tmp = open(filepath).read().split('\n')
    ret = []
    for x in tmp:
        if x.startswith("mask"):
            mask = map(lambda x: int(x) if x != 'X' else -1, list(x[7:]))
            inst = Inst("mask", list(mask), None)
            ret.append(inst)
        if x.startswith("mem"):
            m = re.search(r'mem\[(.*)\] = (.*)', x)
            inst = Inst("mem", int(m.group(1)), int(m.group(2)))
            ret.append(inst)
    return ret


def mem_float(s, i):
    """
    Memory function from second assignment
    """
    b = [int(x) for x in f'{i.arg1:036b}']
    new_addr = []
    magic_index = []
    for index, (val, mask) in enumerate(zip(b, s.mask)):
        if mask == 0:
            new_addr.append(val)
        elif mask == -1:
            new_addr.append(mask)
            magic_index.append(index)
        else:
            new_addr.append(mask)

    # Calculate all the new adresses we need to save the value into

    for perm in itertools.product([1, 0], repeat=new_addr.count(-1)):
        tmp_addr = list(new_addr)
        for p, index in zip(perm, magic_index):
            tmp_addr[index] = p

        s.mem[int(''.join(map(str, tmp_addr)), 2)] = i.arg2
    return s


def mem_mask(s, i):
    """
    Memory function from first assignment
    """
    b = [int(x) for x in f'{i.arg2:036b}']
    ret = []
    for val, mask in zip(b, s.mask):
        if mask == -1:
            ret.append(val)
        else:
            ret.append(mask)
    s.mem[i.arg1] = int(''.join(map(str, ret)), 2)
    return s


def step(state, instruction, mem_func):
    """
    Translate each instrustion into a state change.
    """
    table = {
        'mem': mem_func,
        'mask': lambda s, i: State(s.mem, i.arg1),
    }
    return table[instruction.inst](state, instruction)


#########################Main functions############################


def solver_1star(d):
    """
    Go over the instructions step by step, and sum the memory values afterwards
    """
    default_mask = [-1 for _ in range(36)]
    default_mem = {}
    state = State(default_mem, default_mask)
    for inst in d:
        state = step(state, inst, mem_mask)
    # Take the sum of the memory values
    return sum(state.mem.values())


def solver_2star(d):
    """
    Same as star 1, but use other memory model
    """
    # Notice that the memory contains a different format than star 1
    default_mask = [-1 for _ in range(36)]
    default_mem = {}
    state = State(default_mem, default_mask)
    for inst in d:
        state = step(state, inst, mem_float)
    # Take the sum of the memory values
    return sum(state.mem.values())

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
