#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

real_input = list(fileinput.input())

def read_grid(inputs):
    grid = {}
    starting_point = None
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            y -= 1
            break
        for x, c in enumerate(line):
            if c == "S":
                starting_point = (x, y)
                grid[(x, y)] = '.'
            else:
                grid[(x, y)] = c
    
    return grid, x+1, y+1, starting_point

def work_p1(inputs, steps):
    grid, size_x, size_y, S = read_grid(inputs)

    q = set()
    q.add(S)

    for step in range(steps):
        nq = set()

        for p in q:
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                np = (p[0] + d[0], p[1] + d[1])
                if grid.get(np, None) == '.':
                    nq.add(np)
        q = nq
    
    return len(q)


def work_p2(inputs):
    grid, size_x, size_y, S = read_grid(inputs)

    q = set()
    q.add(S)

    W = size_x
    target = 26501365
    div, rem = divmod(target, W)
    total_steps = 0

    # by oberving the values after rem + N*div steps, we can see that it's quadratic
    # we need to keep the first 3 values to have the first and 2nd derivatives

    def run_n(n):
        nonlocal q, W, total_steps
        total_steps += n
        for step in range(n):
            nq = set()
            for p in q:
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    np = (p[0] + d[0], p[1] + d[1])
                    npmod = (np[0] % W, np[1] % W)
                    if grid.get(npmod, None) == '.':
                        nq.add(np)
            q = nq

    # values = {0: 3947, 1: 35153, 2: 97459}    
            
    values = {}
    run_n(rem)
    values[0] = len(q)

    for period in range(1, 3):
        run_n(W)
        values[period] = len(q)

    derivatives_1 = [values[i+1] - values[i] for i in range(len(values) - 1)]
    derivatives_2 = [derivatives_1[i+1] - derivatives_1[i] for i in range(len(derivatives_1) - 1)]
    # print(derivatives_1, derivatives_2)

    # we can count. or we can use a nice formula. let's count.
    d1 = derivatives_1[0]
    d2 = derivatives_2[0]
    ret = values[0]
    for period in range(div):
        ret = ret + d1
        d1 += d2
    return ret

def test_p1():
    assert(work_p1(test_input, 6) == 16)

    # check some properties of the input garden
    grid, size_x, size_y, S = read_grid(real_input)
    # it's a square
    assert size_x == size_y
    # with odd sizes
    assert size_x & 1 == 1
    for i in range(size_x):
        # borders are clear
        assert grid[(i, 0)] == '.'
        assert grid[(i, size_y -1)] == '.'
        assert grid[(0, i)] == '.'
        assert grid[(size_x - 1, i)] == '.'
        # we also have some clear segments between the border's middle points
        assert grid[(i, size_x//2)] == '.'
        assert grid[(size_x//2, i)] == '.'

test_p1()

def p1():
    print(work_p1(real_input, 64))
p1()

def test_p2():
    assert(work_p2(test_input) == None)
# test_p2()

def p2():
    print(work_p2(real_input))
p2()
