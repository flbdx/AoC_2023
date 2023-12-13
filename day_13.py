#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

def read_inputs(inputs):
    grids = []
    grid = {}
    y = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            if len(grid) != 0:
                grids.append((grid.copy(), x+1, y))
                grid = {}
            y = 0
        else:
            for x, c in enumerate(line):
                grid[(x,y)] = c
            y += 1
    
    if len(grid) != 0:
        grids.append((grid.copy(), x+1, y))
    
    return grids

def work(inputs, difference=0):
    ret = 0
    grids = read_inputs(inputs)
    for grid, size_x, size_y in grids:
        for test_col in range(1, size_x):
            test_width = min(test_col, size_x - test_col)
            ok = False
            matching = 0
            total = 0
            for col in range(test_width):
                total += size_y
                matching += sum(1 if grid[(test_col-col-1, y)] == grid[(test_col+col, y)] else 0 for y in range(size_y))
                if total-matching > difference:
                    break
            
            if total - matching == difference:
                ok = True
                ret += test_col
                break
        
        if ok == True:
            continue

        for test_row in range(1, size_y):
            test_width = min(test_row, size_y - test_row)
            matching = 0
            total = 0
            for row in range(test_width):
                total += size_x
                matching += sum(1 if grid[(x, test_row-row-1)] == grid[(x, test_row+row)] else 0 for x in range(size_x))
                if total-matching > difference:
                    break

            if total - matching == difference: 
                ret += test_row * 100
                break
    
    return ret

def work_p1(inputs):
    return work(inputs, 0)

def work_p2(inputs):
    return work(inputs, 1)


def test_p1():
    assert(work_p1(test_input) == 405)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 400)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
