#!/usr/bin/env python3
import os
import re
import sys
from collections import namedtuple

#######################Helping functions###########################
Operation = namedtuple('Operation', 'instruction arg1')
State = namedtuple('State', 'program_counter accum')


def data_parser(filepath):
    """
    Load each operation line by line, and then split the operation name and the arg into
    a named tuple.
    """
    tmp = [Operation(x.split(" ")[0], int(x.split(" ")[1]))
           for x in open(filepath).read().split('\n')]
    return tmp


def run(operation_list, state):
    """
    Run a step in the program, by taking in a state of the machine, and
    returning a new state of the machine.
    """
    if(state.program_counter > len(operation_list) - 1):
        # We hit the end, set the program counter to -1
        return State(-1, state.accum)
    inst = {
        'nop': lambda op, s: State(s.program_counter + 1, s.accum),
        'acc': lambda op, s: State(s.program_counter + 1, s.accum + op.arg1),
        'jmp': lambda op, s: State(s.program_counter + op.arg1, s.accum)
    }
    cur_op = operation_list[state.program_counter]

    return inst[cur_op.instruction](cur_op, state)

#########################Main functions############################


def solver_1star(d):
    """
    Set the state to the initial conditions, and go over each program counter seen.
    break when we hit one for the second time.
    """
    state = State(0, 0)
    seen = []

    while True:
        if state.program_counter in seen:
            return state.accum
        seen.append(state.program_counter)
        state = run(d, state)


def solver_2star(d):
    """
    Like star1, but return the accum when the program counter is -1 (Program has ended).
    Go over all instructions, and modify them one at a time, and test if the program terminates.

    """
    # We try to swap each jump to a nop, or nop to a jump on each instruction, and run the code

    convert = {
        'nop': lambda op: Operation('jmp', op.arg1),
        'acc': lambda op: Operation('acc', op.arg1),
        'jmp': lambda op: Operation('nop', op.arg1),
    }

    for index in range(len(d)):
        inst_list = list(d)

        inst_list[index] = convert[inst_list[index].instruction](
            inst_list[index])

        state = State(0, 0)
        seen = []
        while True:
            if state.program_counter == -1:
                return state.accum
            if state.program_counter in seen:
                break
            seen.append(state.program_counter)
            state = run(inst_list, state)


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
