#!/usr/bin/python3
#encoding: UTF-8

import sys
from functools import reduce

test_input1="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

test_input1 = test_input1.strip()
real_input = open(sys.argv[1], encoding="UTF-8").read().strip()

def work_p1(s):
    ret = 0
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        
        colors = {}
        gid, draws = line.split(": ")
        gid = int(gid.split(" ")[1])
        for draw in draws.split("; "):
            draw = draw.split(", ")
            for cpl in draw:
                cubes, color = cpl.split(" ")
                colors[color] = max(colors.get(color, 0), int(cubes))
        
        if colors.get("red", 0) <= 12 and colors.get("green", 0) <= 13 and colors.get("blue", 0) <= 14:
            ret += gid
    return ret

def work_p2(s):
    ret = 0
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        
        colors = {}
        gid, draws = line.split(": ")
        gid = int(gid.split(" ")[1])
        for draw in draws.split("; "):
            draw = draw.split(", ")
            for cpl in draw:
                cubes, color = cpl.split(" ")
                colors[color] = max(colors.get(color, 0), int(cubes))
        
        ret += reduce(lambda a, b: a*b, colors.values(), 1)
    return ret
def test_p1():
    assert(work_p1(test_input1) == 8)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input1) == 2286)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
