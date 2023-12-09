#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

def get_history_stack(sequence):
    stack = [sequence]
    
    while True:
        if all((e == 0 for e in stack[-1])):
            break
        stack.append([stack[-1][i+1] - stack[-1][i] for i in range(len(stack[-1]) - 1)])
    
    return stack

def work_p1(inputs):
    ret = 0
    re_int = re.compile("[-]?[0-9]+")
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        sequence = list(map(int, re_int.findall(line)))
        stack = get_history_stack(sequence)
        
        v = 0
        d = len(stack) - 1
        while d >= 0:
            v = stack[d][-1] + v
            d -= 1
        ret += v
    return ret


def work_p2(inputs):
    ret = 0
    re_int = re.compile("[-]?[0-9]+")
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        sequence = list(map(int, re_int.findall(line)))
        stack = get_history_stack(sequence)
        
        v = 0
        d = len(stack) - 1
        while d >= 0:
            v = stack[d][0] - v
            d -= 1
        ret += v
    return ret
def test_p1():
    assert(work_p1(test_input) == 114)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 2)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
