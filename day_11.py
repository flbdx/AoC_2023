#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

test_input="""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

def read_picture(inputs):
    grid = set()
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            if c != '.':
                grid.add((x, y))
        max_x = x
    max_y = y

    return grid, max_x + 1, max_y + 1

# expansion_size is added to the coordinates
# so for part 1 (doubling the empty space), we need to add +1
# and for part 2 (*1000000), we need to add +999999
def work(inputs, expansion_size=1):
    grid, size_x, size_y = read_picture(inputs)

    class Galaxy(object):
        def __init__(self, pos):
            self.x = pos[0]
            self.y = pos[1]
        def __repr__(self):
            return f"{(self.x,self.y)}"
        def __eq__(self, o):
            return self.x == o.x and self.y == o.y
        def __hash__(self):
            return hash((self.x,self.y))
    galaxies = {Galaxy(p) for p in grid}

    # for y in range(size_y):
    #     s = ""
    #     for x in range(size_x):
    #         s += "#" if (x,y) in grid else "."
    #     print(s)
    
    def expand_y():
        nonlocal galaxies, size_y
        left = galaxies
        right = set()
        for y in range(size_y - 1, -1, -1):
            col = {g for g in left if g.y == y}
            # print((y, col, left, right))
            if len(col) == 0:
                for g in right:
                    g.y += expansion_size
                size_y += expansion_size
            else:
                for g in col:
                    right.add(g)
                    left.remove(g)
        galaxies = {g for g in right}
    expand_y()
    
    def expand_x():
        nonlocal galaxies, size_x
        top = galaxies
        bottom = set()
        for x in range(size_x - 1, -1, -1):
            row = {g for g in top if g.x == x}
            # print((x, row, top, bottom))
            if len(row) == 0:
                for g in bottom:
                    g.x += expansion_size
                size_x += expansion_size
            else:
                for g in row:
                    bottom.add(g)
                    top.remove(g)
        galaxies = {g for g in bottom}
    expand_x()

    
    # for y in range(size_y):
    #     s = ""
    #     for x in range(size_x):
    #         s += "#" if Galaxy((x,y)) in galaxies else "."
    #     print(s)
    
    ret = 0
    for g1, g2 in itertools.combinations(galaxies, r=2):
        sp = abs(g2.x - g1.x) + abs(g2.y - g1.y)
        # print(g1, g2, sp)
        ret += sp
    
    # print(ret, size_x, size_y)
    return ret

def work_p1(inputs):
    return work(inputs, expansion_size=1)

def work_p2(inputs, expansion_size):
    return work(inputs, expansion_size)

def test_p1():
    assert(work_p1(test_input) == 374)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input, 10-1) == 1030)
    assert(work_p2(test_input, 100-1) == 8410)
test_p2()

def p2():
    print(work_p2(fileinput.input(), 1000000-1))
p2()
