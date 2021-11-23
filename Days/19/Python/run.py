#!/usr/bin/env python3
import os
import sys
import re

#######################Helping functions###########################


def data_parser(filepath):
    """
    Parse the rules, then the lines.
    """
    tmp = open(filepath).read().split('\n\n')
    # parse the rules
    rules = {}
    for line in tmp[0].split('\n'):
        parts = line.split(':')
        segments = parts[1][1:].split(' | ')
        paths = []
        for segment in segments:
            seg_ret = []
            for val in segment.split(' '):
                if val.startswith('"'):
                    seg_ret = val[1]
                    break
                else:
                    seg_ret.append(int(val))
            paths.append(seg_ret)
        rules[int(parts[0])] = paths

    lines = []
    for line in tmp[1].split('\n'):
        lines.append(line)

    return {'rules': rules, 'lines': lines}


# Cache for regular expression expansion
CACHE = {}


def regular_expression_expand(rules, rule_id):
    if rule_id in CACHE:
        return CACHE[rule_id]
    rule = rules[rule_id]
    if type(rule[0]) == str:
        return f'{rule[0]}'
    ret = "("
    for segments in rule:
        for segment in segments:
            ret += regular_expression_expand(rules, segment)
        ret += '|'
    ret = ret[:-1] + ')'
    CACHE[rule_id] = ret
    return ret


def match_rule(rules, current_str, stack):
    """
    Do back propergation , and test each combination of rules until we find something correct.
    """
    # If the stack is too big, we cant possibly find a result, since all rules does
    # atleast produce one letter
    if len(stack) > len(current_str):
        return False

    # if the stack is empty, or the string is empty, we test if they both are.
    # If they are , the result must have been satisfactory
    if len(stack) == 0 or len(current_str) == 0:
        return len(stack) == 0 and len(current_str) == 0

    c = stack.pop()

    # If the stack contains a string ,it is a latter, and we can see if
    # the current string matches that up
    if isinstance(c, str):
        if current_str[0] == c:
            return match_rule(rules, current_str[1:], stack.copy())
    else:
        # Go over all rules, if one of them are true, return
        for rule in rules[c]:
            if match_rule(rules, current_str, stack + list(reversed(rule))):
                return True
    return False

#########################Main functions############################


def solver_1star(d):
    """
    Make the rules into a regular expression, and test that on the
    elements.
    """
    regular_string = regular_expression_expand(d['rules'], 0)
    reg = re.compile('^' + regular_string + '$')
    matches = 0
    for line in d['lines']:

        res = reg.match(line)
        if res:
            matches += 1
    return matches


def solver_2star(d):
    """
    """
    new_rules = dict(d['rules'])
    # 8: 42 | 42 8
    new_rules[8] = [[42], [42, 8]]
    # 11: 42 31 | 42 11 31
    new_rules[11] = [[42, 31], [42, 11, 31]]

    matches = 0

    for line in d['lines']:
        if match_rule(new_rules, line, list(reversed(new_rules[0][0]))):
            matches += 1
    return matches

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
