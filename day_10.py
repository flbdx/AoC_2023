#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum

test_input="""..F7.
.FJ|.
SJ.L7
|F--J
LJ...

""".splitlines()

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

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

# coordinates in the grid are complex numbers
def read_grid(inputs):
    grid = {}
    max_x = 0
    max_y = 0
    start_pos = None
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            max_y = y - 1
            break
        for x, c in enumerate(line):
            grid[x + y*1j] = c
            if c == "S":
                start_pos = (x + y*1j)
        max_x = x
    
    return grid, start_pos, max_x + 1, max_y + 1

# walk the loop and return a path
def walk_loop(grid, start_pos, start_direction):
    direction = start_direction
    pos = start_pos
    path = []

    # print(pos, direction)
    while True:
        path.append(pos)
        pos = direction.move(pos)

        tile = grid[pos]
        if tile == "7":
            if direction == Direction.RIGHT:
                direction = direction.turn_right()
            elif direction == Direction.UP:
                direction = direction.turn_left()
        elif tile == "J":
            if direction == Direction.RIGHT:
                direction = direction.turn_left()
            elif direction == Direction.DOWN:
                direction = direction.turn_right()
        elif tile == "F":
            if direction == Direction.LEFT:
                direction = direction.turn_left()
            elif direction == Direction.UP:
                direction = direction.turn_right()
        elif tile == "L":
            if direction == Direction.LEFT:
                direction = direction.turn_right()
            elif direction == direction.DOWN:
                direction = direction.turn_left()

        # print(pos, tile, direction, distance)
        if pos == start_pos:
            break
    return path

def display_grid(grid):
    y = 0
    while (0 + y*1j) in grid:
        x = 0
        s = ""
        while True:
            c = grid.get((x + y*1j), None)
            if c is None:
                break
            s += c.replace("7", "┐").replace("F", "┌").replace("L", "└").replace("J", "┘").replace("-", "─").replace("|", "│")
            x += 1
        print(s)
        y += 1

def work_p1(inputs):
    grid, start_pos, max_x, max_y = read_grid(inputs)
    
    # let's decide in which direction we will travel along the path
    def search_start_direction():
        if grid.get(Direction.UP.move(start_pos), None) in "7F":
            return Direction.UP
        if grid.get(Direction.RIGHT.move(start_pos), None) in "7J":
            return Direction.RIGHT
        if grid.get(Direction.DOWN.move(start_pos), None) in "JL":
            return Direction.DOWN
        if grid.get(Direction.LEFT.move(start_pos), None) in "FL":
            return Direction.LEFT
    
    direction = search_start_direction()
    path = walk_loop(grid, start_pos, direction)

    return len(path) // 2


def work_p2(inputs):
    grid, start_pos, max_x, max_y = read_grid(inputs)
    
    def search_start_direction():
        if grid.get(Direction.UP.move(start_pos), None) in "7F":
            return Direction.UP
        if grid.get(Direction.RIGHT.move(start_pos), None) in "7J":
            return Direction.RIGHT
        if grid.get(Direction.DOWN.move(start_pos), None) in "JL":
            return Direction.DOWN
        if grid.get(Direction.LEFT.move(start_pos), None) in "FL":
            return Direction.LEFT
    
    direction = search_start_direction()
    path = walk_loop(grid, start_pos, direction)

    # let's clean-up the place
    spath = set(path)
    for p in grid:
        if not p in spath:
            grid[p] = "."
    
    # and replace 'S' by a nice tile
    if grid.get(Direction.UP.move(start_pos), None) in "7JLF|-" and grid.get(Direction.RIGHT.move(start_pos), None) in "7JLF|-":
        grid[start_pos] = 'L'
    if grid.get(Direction.UP.move(start_pos), None) in "7JLF|-" and grid.get(Direction.LEFT.move(start_pos), None) in "7JLF|-":
        grid[start_pos] = 'J'
    if grid.get(Direction.DOWN.move(start_pos), None) in "7JLF|-" and grid.get(Direction.RIGHT.move(start_pos), None) in "7JLF|-":
        grid[start_pos] = 'F'
    if grid.get(Direction.DOWN.move(start_pos), None) in "7JLF" and grid.get(Direction.LEFT.move(start_pos), None) in "7JLF":
        grid[start_pos] = '7'


    # display_grid(grid)

    # we will walk the loop again
    # let's start with any | tile
    start_pos
    for p, v in grid.items():
        if v == '|':
            start_pos = p
            break

    # we will go up
    direction = Direction.UP
    # and mark our "left" tiles with a l, and the "right" tiles with a 'r'
    dir_set_l = direction.LEFT
    dir_set_r = direction.RIGHT

    pos = start_pos
    while True:
        # copypasta world
        # print(pos, direction)
        v = grid[pos]
        if v == '|' or v == '-':
            test_p_l = dir_set_l.move(pos)
            test_v_l = grid.get(test_p_l, None)
            test_p_r = dir_set_r.move(pos)
            test_v_r = grid.get(test_p_r, None)
            if test_v_l == '.':
                grid[test_p_l] = 'l'
            if test_v_r == '.':
                grid[test_p_r] = 'r'
            
            #pos = direction.move(pos)

        elif v == '7': # ┐
            if direction == Direction.RIGHT:
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
                direction = direction.turn_right()
                dir_set_l = dir_set_l.turn_right()
                dir_set_r = dir_set_r.turn_right()
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
            elif direction == Direction.UP:
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
                direction = direction.turn_left()
                dir_set_l = dir_set_l.turn_left()
                dir_set_r = dir_set_r.turn_left()
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
        elif v == 'F': # ┌
            if direction == Direction.LEFT:
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
                direction = direction.turn_left()
                dir_set_l = dir_set_l.turn_left()
                dir_set_r = dir_set_r.turn_left()
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
            elif direction == Direction.UP:
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
                direction = direction.turn_right()
                dir_set_l = dir_set_l.turn_right()
                dir_set_r = dir_set_r.turn_right()
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
        elif v == 'J': # ┘
            if direction == Direction.RIGHT:
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
                direction = direction.turn_left()
                dir_set_l = dir_set_l.turn_left()
                dir_set_r = dir_set_r.turn_left()
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
            elif direction == Direction.DOWN:
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
                direction = direction.turn_right()
                dir_set_l = dir_set_l.turn_right()
                dir_set_r = dir_set_r.turn_right()
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
        elif v == 'L': # └
            if direction == Direction.LEFT:
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
                direction = direction.turn_right()
                dir_set_l = dir_set_l.turn_right()
                dir_set_r = dir_set_r.turn_right()
                test_p_l = dir_set_l.move(pos)
                test_v_l = grid.get(test_p_l, None)
                if test_v_l == '.':
                    grid[test_p_l] = 'l'
            elif direction == Direction.DOWN:
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
                direction = direction.turn_left()
                dir_set_l = dir_set_l.turn_left()
                dir_set_r = dir_set_r.turn_left()
                test_p_r = dir_set_r.move(pos)
                test_v_r = grid.get(test_p_r, None)
                if test_v_r == '.':
                    grid[test_p_r] = 'r'
        
        pos = direction.move(pos)
        if pos == start_pos:
            break
    
    # display_grid(grid)

    # now we will expand our 'r' and 'l' areas
    def expand(mark):
        todo = set(p for p in grid if grid[p] == mark)
        while len(todo) > 0:
            pos = todo.pop()
            tp = Direction.UP.move(pos)
            if grid.get(tp, None) == '.':
                todo.add(tp)
                grid[tp] = mark
            tp = Direction.DOWN.move(pos)
            if grid.get(tp, None) == '.':
                todo.add(tp)
                grid[tp] = mark
            tp = Direction.LEFT.move(pos)
            if grid.get(tp, None) == '.':
                todo.add(tp)
                grid[tp] = mark
            tp = Direction.RIGHT.move(pos)
            if grid.get(tp, None) == '.':
                todo.add(tp)
                grid[tp] = mark

    expand('l')
    expand('r')
    # display_grid(grid)
    count_l = sum(1 for p in grid if grid[p] == 'l')
    count_r = sum(1 for p in grid if grid[p] == 'r')

    # surely the inner area is the smaller one, right?
    return min(count_l, count_r)

def test_p1():
    assert(work_p1(test_input) == 8)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 1)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
