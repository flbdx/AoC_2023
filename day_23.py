#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
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

    graph = {}
    graph[src_point] = []
    graph[dst_point] = []

    queue = deque()
    queue.append(src_point)
    visited = set()
    visited.add(src_point)

    while len(queue) > 0:
        node = queue.pop()
        queue2 = deque()
        queue2.append((node, node, 0))

        while len(queue2) > 0:
            n, prev, s = queue2.pop()

            if n != prev and n in (src_point, dst_point):
                graph.setdefault(node, []).append((n, s))
                if not n in visited:
                    visited.add(n)
                    queue.append(n)
                continue

            neighboors = []
            for d in ((1,0),(-1,0),(0,1),(0,-1)):
                np = (n[0] + d[0], n[1] + d[1])
                if np[0] < 0 or np[0] >= size_x or np[1] < 0 or np[1] >= size_y or grid[np] == '#':
                    continue
                neighboors.append(np)
            
            if (n != prev and len(neighboors) >= 3):
                graph.setdefault(node, []).append((n, s))
                if not n in visited:
                    visited.add(n)
                    queue.append(n)
            else:
                for neigh in neighboors:
                    if neigh != prev:
                        queue2.append((neigh, n, s+1))

    # for n, neighboors in graph.items():
    #     print(f"{n}:")
    #     for ngh,s in neighboors:
    #         print(f"  {ngh} : {s}")
    # print(len(graph))

    point_to_bit = lambda p: 1<<(p[1]*size_x + p[0])
    best = 0
    queue = deque()
    queue.append((src_point, 0, point_to_bit(src_point)))

    while len(queue) > 0:
        p, s, visited = queue.pop()

        if p == dst_point:
            if s > best:
                best = s
            continue

        for neigh, dist in graph.get(p, []):
            b = point_to_bit(neigh)
            if (b & visited) != 0:
                continue
            queue.append((neigh, s + dist, visited | b))
    
    return best

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
