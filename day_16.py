#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque
from enum import Enum

test_input=r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

def read_inputs(inputs):
    cave = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            y -= 1
            break
        for x, c in enumerate(line):
            cave[x + y * 1j] = c
    
    return cave, x+1, y+1

# A "complex" helper for directions
class Direction(Enum):
    UP = (0-1j)
    DOWN = (0+1j)
    RIGHT = (1+0j)
    LEFT = (-1+0j)

    def turn_left(self):
        return Direction(self.value * -1j)
    def turn_right(self):
        return Direction(self.value * 1j)
    
    def move(self, point):
        return point + self.value

def work(cave, starting_pos, starting_direction):
    energized = set()
    loop_breaker = set()
    stack = deque()

    stack.append((starting_pos, starting_direction))

    while len(stack) > 0:
        pos, direction = stack.popleft()

        if (pos, direction) in loop_breaker:
            continue
        c = cave.get(pos, None)
        if c is None:
            continue
        loop_breaker.add((pos, direction))
        energized.add(pos)

        if c == '.' or \
            (c == '-' and (direction == Direction.RIGHT or direction== Direction.LEFT)) or \
            (c == '|' and (direction == Direction.UP or direction== Direction.DOWN)):
            stack.appendleft((direction.move(pos), direction))
        elif c == '-':
            d = direction.turn_right()
            stack.appendleft((d.move(pos), d))
            d = direction.turn_left()
            stack.append((d.move(pos), d))
        elif c == '|':
            d = direction.turn_right()
            stack.appendleft((d.move(pos), d))
            d = direction.turn_left()
            stack.append((d.move(pos), d))
        elif c == '/' and (direction == Direction.UP or direction== Direction.DOWN) or \
            c == '\\' and (direction == Direction.RIGHT or direction== Direction.LEFT):
            d = direction.turn_right()
            stack.appendleft((d.move(pos), d))
        else:
            d = direction.turn_left()
            stack.appendleft((d.move(pos), d))
    
    return len(energized)

def work_p1(inputs):
    cave, size_x, size_y = read_inputs(inputs)
    return work(cave, 0+0j, Direction.RIGHT)

def work_p2(inputs):
    cave, size_x, size_y = read_inputs(inputs)
    
    ret = 0
    to_check = []
    for x in range(size_x):
        to_check.append((x + 0j, Direction.DOWN))
        to_check.append((x + (size_y-1)*1j, Direction.UP))
    for y in range(size_y):
        to_check.append((0 + y*1j, Direction.RIGHT))
        to_check.append((size_x - 1 + y*1j, Direction.LEFT))
    for pos, direction in to_check:
        ret = max(ret, work(cave, pos, direction))
    
    return ret

def test_p1():
    assert(work_p1(test_input) == 46)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 51)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
