#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque
from enum import Enum

test_input="""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

real_input = list(fileinput.input())

class Direction(Enum):
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)

class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self, direction, dist=1):
        return Point(self.x + direction.value[0] * dist, self.y + direction.value[1] * dist)
    
    def __repr__(self):
        return repr((self.x, self.y))
    
    def __eq__(self, o):
        return (self.x, self.y) == (o.x, o.y)

def shoelace_formula(vectices):
    l = len(vectices)
    return sum(vectices[i].x * vectices[(i+1)%l].y - vectices[(i+1)%l].x * vectices[i].y for i in range(len(vectices))) // 2

def build_vectices(sequences):
    vectices = []
    p = Point(0, 0)
    # vectices.append(p) # NOPE.

    for i in range(len(sequences)):
        seq = sequences[i]
        next_seq = sequences[(i+1)%len(sequences)]
        direction, steps = seq
        next_direction = next_seq[0]
        p = p.move(direction, steps)
        
        # the overly tricky part...
        # made me cry a little
        if (direction == Direction.UP and next_direction == Direction.RIGHT) or \
            (direction == Direction.RIGHT and next_direction == Direction.UP):
            tp = p
        if (direction == Direction.RIGHT and next_direction == Direction.DOWN) or \
            (direction == Direction.DOWN and next_direction == Direction.RIGHT):
            tp = p.move(Direction.RIGHT)
        if (direction == Direction.DOWN and next_direction == Direction.LEFT) or \
            (direction == Direction.LEFT and next_direction == Direction.DOWN):
            tp = p.move(Direction.RIGHT).move(Direction.DOWN)
        if (direction == Direction.LEFT and next_direction == Direction.UP) or \
            (direction == Direction.UP and next_direction == Direction.LEFT):
            tp = p.move(Direction.DOWN)
        
        vectices.append(tp)

    return vectices

def work_p1(inputs):
    dir_to_offset = {
        'U' : Direction.UP,
        'D' : Direction.DOWN,
        'L' : Direction.LEFT,
        'R' : Direction.RIGHT
    }

    sequences = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        direction, steps, color = line.split(" ")
        direction = dir_to_offset[direction]
        steps = int(steps)
        sequences.append((direction, steps))
    
    vectices = build_vectices(sequences)
    return shoelace_formula(vectices)

    

def work_p2(inputs):
    dir_to_offset = {
        3 : Direction.UP,
        1 : Direction.DOWN,
        2 : Direction.LEFT,
        0 : Direction.RIGHT
    }

    sequences = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        instrs = int(line.split(" ")[2][2:-1], 16)
        direction = dir_to_offset[instrs & 0b1111]
        steps = instrs >> 4
        sequences.append((direction, steps))
    
    vectices = build_vectices(sequences)
    # for vect in vectices:
    #     print(f"({vect.x}, {vect.y})")
    return shoelace_formula(vectices)
        
def test_p1():
    assert(work_p1(test_input) == 62)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 952408144115)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
