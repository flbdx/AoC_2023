#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
# import networkx as nx
from collections import deque

test_input="""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            y -= 1
            break
        for x, c in enumerate(line):
            grid[(x,y)] = c
    size_x = x + 1
    size_y = y + 1
    src_point = [(x, 0) for x in range(size_x) if grid[(x,0)] == '.'][0]
    dst_point = [(x, size_y - 1) for x in range(size_x) if grid[(x,size_y - 1)] == '.'][0]

    return grid, size_x, size_y, src_point, dst_point


def work_p1(inputs):
    grid, size_x, size_y, src_point, dst_point = read_inputs(inputs)

    point_to_bit = lambda p: 1<<(p[1]*size_x + p[0])

    queue = deque()
    queue.append((src_point, point_to_bit(src_point)))

    best = 0

    while len(queue) > 0:
        p, visited = queue.pop()

        if p == dst_point:
            l = int(visited).bit_count()
            if l > best:
                best = l
            continue

        c = grid[p]
        if c == '#':
            continue
        if c == '.':
            dirs = ((1,0),(-1,0),(0,1),(0,-1))
        elif c == '>':
            dirs = ((1,0),)
        elif c == '<':
            dirs = ((-1,0),)
        elif c == 'v':
            dirs = ((0,1),)
        elif c == '^':
            dirs = ((0,-1),)
        else:
            assert False
        
        for d in dirs:
            np = (p[0] + d[0], p[1] + d[1])
            
            if grid.get(np, '#') != '#':
                b = point_to_bit(np)
                if (visited & b) == 0:
                    queue.append((np, visited | b))

    return best - 1

def work_p2(inputs):
    grid, size_x, size_y, src_point, dst_point = read_inputs(inputs)

    point_to_bit = lambda p: 1<<(p[1]*size_x + p[0])

    walls = 0
    for p, c in grid.items():
        if c == '#':
            walls |= point_to_bit(p)

    queue = deque()
    queue.append((src_point, point_to_bit(src_point)))

    best = 0

    while len(queue) > 0:
        p, visited = queue.pop()

        if p == dst_point:
            l = int(visited).bit_count()
            if l > best:
                best = l
                print(best-1)
            continue


        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            np = (p[0] + d[0], p[1] + d[1])
            if np[0] < 0 or np[1] < 0 or np[0] >= size_x or np[1] >= size_y:
                continue
            npb = point_to_bit(np)
            if (npb & walls != 0) or (npb & visited != 0):
                continue
            queue.append((np, visited | npb))

    return best - 1

def test_p1():
    assert(work_p1(test_input) == 94)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 154)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
