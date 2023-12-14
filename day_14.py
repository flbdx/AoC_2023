#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            y -= 1
            break
        for x, c in enumerate(line):
            grid[(x + y*1j)] = c
    
    return grid, x + 1, y + 1

def tilt_north(grid, size_x, size_y):
    for y in range(1, size_y):
        for x in range(size_x):
            p = x + y * 1j
            if grid.get(p, None) != 'O':
                continue
            move = p
            for yup in range(y-1, -1, -1):
                if grid.get(x + yup * 1j, None) == '.':
                    move -= 1j
                else:
                    break
            grid[move], grid[p] = grid[p], grid[move]

def tilt_west(grid, size_x, size_y):
    for x in range(1, size_x):
        for y in range(size_y):
            p = x + y * 1j
            if grid.get(p, None) != 'O':
                continue
            move = p
            for xlft in range(x-1, -1, -1):
                if grid.get(xlft + y * 1j, None) == '.':
                    move -= 1
                else:
                    break
            grid[move], grid[p] = grid[p], grid[move]

def tilt_south(grid, size_x, size_y):
    for y in range(size_y-2, -1, -1):
        for x in range(size_x):
            p = x + y * 1j
            if grid.get(p, None) != 'O':
                continue
            move = p
            for ydwn in range(y+1, size_y):
                if grid.get(x + ydwn * 1j, None) == '.':
                    move += 1j
                else:
                    break
            grid[move], grid[p] = grid[p], grid[move]

def tilt_east(grid, size_x, size_y):
    for x in range(size_x-2, -1, -1):
        for y in range(size_y):
            p = x + y * 1j
            if grid.get(p, None) != 'O':
                continue
            move = p
            for xrgt in range(x+1, size_x):
                if grid.get(xrgt + y * 1j, None) == '.':
                    move += 1
                else:
                    break
            grid[move], grid[p] = grid[p], grid[move]

def tilt_cycle(grid, size_x, size_y):
    tilt_north(grid, size_x, size_y)
    tilt_west(grid, size_x, size_y)
    tilt_south(grid, size_x, size_y)
    tilt_east(grid, size_x, size_y)

def weight(grid, size_x, size_y):
    ret = 0
    for p, c in grid.items():
        if c == 'O':
            ret += size_y - round(p.imag)
    return ret

def grid_to_string(grid, size_x, size_y):
    s = ""
    for y in range(size_y):
        if len(s):
            s += "\n"
        for x in range(size_x):
            s += grid[x + y * 1j]
    return s

def work_p1(inputs):
    grid, size_x, size_y = read_inputs(inputs)
    
    tilt_north(grid, size_x, size_y)
    return weight(grid, size_x, size_y)

def work_p2(inputs):   
    grid, size_x, size_y = read_inputs(inputs)

    cache = {grid_to_string(grid, size_x, size_y) : 0}
    target = 1000000000
    for n in range(target):
        n += 1
        tilt_cycle(grid, size_x, size_y)
        s = grid_to_string(grid, size_x, size_y)
        if s in cache:
            break
        else:
            cache[s] = n
    
    period = n - cache[s]
    rem = target - n
    rem %= period
    while rem != 0:
        tilt_cycle(grid, size_x, size_y)
        rem -= 1

    return weight(grid, size_x, size_y)

def test_p1():
    assert(work_p1(test_input) == 136)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 64)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
