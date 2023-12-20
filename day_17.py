#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
import heapq

test_input="""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".splitlines()

test_input_2="""111111111111
999999999991
999999999991
999999999991
999999999991
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

def parse_inputs(inputs):
    nodes = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            y -= 1
            break
        for x, c in enumerate(line):
            nodes[(x, y)] = int(c)
    
    return nodes, x+1, y+1

class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])
    
    def turn_left(self):
        return Direction((self.value + 1) % 4)
    def turn_right(self):
        return Direction((self.value - 1) % 4)

class State(object):
    def __init__(self, pos, dir, steps=0, weight=0):
        self.pos, self.dir, self.steps, self.weight = pos, dir, steps, weight
    
    # will be used with heapq, which sort by lowest priority
    def __lt__(self, o) -> bool:
        return self.weight < o.weight
    
    # don't hash or compare on the total weight...
    def __eq__(self, o) -> bool:
        return (self.pos, self.dir, self.steps) == (o.pos, o.dir, o.steps)
    def __hash__(self) -> int:
        return hash((self.pos, self.dir, self.steps))
    
    def __repr__(self) -> str:
        return repr((self.pos, self.dir, self.steps, self.weight))

def work(nodes, start_point, end_point, limit_min=1, limit_max=3):
    # note that we do not count the weight of the first node
    # so we can act as if the weight of each node is the weight of an edge
    q = []
    visited = set()

    heapq.heappush(q, State(start_point, Direction.RIGHT))
    heapq.heappush(q, State(start_point, Direction.DOWN))

    while len(q) > 0:
        state = heapq.heappop(q)

        if state in visited:
            continue
        visited.add(state)

        if state.pos == end_point and state.steps >= (limit_min - 1):
            return state.weight
        
        if state.steps < (limit_max - 1):
            next_dir = state.dir
            next_pos = next_dir.next(state.pos)
            if next_pos in nodes:
                next_state = State(next_pos, next_dir, state.steps+1, state.weight + nodes[next_pos])
                heapq.heappush(q, next_state)
        
        if state.steps >= limit_min - 1:
            next_dir = state.dir.turn_left()
            next_pos = next_dir.next(state.pos)
            if next_pos in nodes:
                next_state = State(next_pos, next_dir, 0, state.weight + nodes[next_pos])
                heapq.heappush(q, next_state)
        
        if state.steps >= limit_min - 1:
            next_dir = state.dir.turn_right()
            next_pos = next_dir.next(state.pos)
            if next_pos in nodes:
                next_state = State(next_pos, next_dir, 0, state.weight + nodes[next_pos])
                heapq.heappush(q, next_state)

def work_p1(inputs):
    nodes, size_x, size_y = parse_inputs(inputs)
    
    start_point = (0, 0)
    end_point = (size_x - 1, size_y - 1)

    return work(nodes, start_point, end_point, 1, 3)

def work_p2(inputs):
    nodes, size_x, size_y = parse_inputs(inputs)
    
    start_point = (0, 0)
    end_point = (size_x - 1, size_y - 1)

    return work(nodes, start_point, end_point, 4, 10)

def test_p1():
    assert(work_p1(test_input) == 102)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 94)
    assert(work_p2(test_input_2) == 71)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
