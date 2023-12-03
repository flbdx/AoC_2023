#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import namedtuple

test_input="""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

Number = namedtuple("Number", ["value", "coords"])

def work_p1(inputs):
    numbers = set()
    symbols = {}

    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            continue
        
        v = None
        start = None

        for x, c in enumerate(line):
            if c.isnumeric():
                if start is None:
                    start = (x, y)
                    v = int(c)
                else:
                    v = v * 10 + int(c)
            else:
                if start is not None:
                    n = Number(v, ((start[0], x-1), y))
                    numbers.add(n)
                    start = None
                    v = None
                if c != '.':
                    symbols[(x, y)] = c
        if start is not None:
            n = Number(v, ((start[0], x), y))
            numbers.add(n)

    ret = 0
    for number in numbers:
        value, (x_range, y) = number
        def tst():
            for x in range(x_range[0]-1, x_range[1]+2):
                if symbols.get((x, y-1), None) != None:
                    return value
                if symbols.get((x, y+1), None) != None:
                    return value
            if symbols.get((x_range[0] - 1, y), None) != None:
                return value
            if symbols.get((x_range[1] + 1, y), None) != None:
                return value
            return 0
        ret += tst()
    return ret

def work_p2(inputs):
    numbers = set()
    symbols = {}

    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            continue
        
        v = None
        start = None

        for x, c in enumerate(line):
            if c.isnumeric():
                if start is None:
                    start = (x, y)
                    v = int(c)
                else:
                    v = v * 10 + int(c)
            else:
                if start is not None:
                    n = Number(v, ((start[0], x-1), y))
                    numbers.add(n)
                    start = None
                    v = None
                if c == '*':
                    symbols[(x, y)] = []
        if start is not None:
            n = Number(v, ((start[0], x), y))
            numbers.add(n)
    
    for number in numbers:
        value, (x_range, y) = number
        adjacents = set()
        for x in range(x_range[0]-1, x_range[1]+2):
            adjacents.add((x, y-1))
            adjacents.add((x, y+1))
        adjacents.add((x_range[0] - 1, y))
        adjacents.add((x_range[1] + 1, y))
        for p in adjacents:
            g = symbols.get(p, None)
            if g is not None:
                symbols[p].append(value)

    ret = 0
    for l in symbols.values():
        if len(l) == 2:
            ret += l[0] * l[1]
    return ret

def test_p1():
    assert(work_p1(test_input) == 4361)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 467835)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
