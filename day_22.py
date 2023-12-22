#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

real_input = list(fileinput.input())

class Brick(object):
    def __init__(self, spec: str, global_grid: set):
        first, last = spec.split("~")
        first = list(int(s) for s in first.split(","))
        last = list(int(s) for s in last.split(","))
        self.spec = spec
        self.global_grid = global_grid
        self.blocks = []
        if first[0] != last[0]:
            for t in range(first[0], last[0] + 1):
                self.blocks.append((t, first[1], first[2]))
        elif first[1] != last[1]:
            for t in range(first[1], last[1] + 1):
                self.blocks.append((first[0], t, first[2]))
        else:
            for t in range(first[2], last[2] + 1):
                self.blocks.append((first[0], first[1], t))
        
        self.z_index = min(blk[2] for blk in self.blocks)
        for blk in self.blocks:
            self.global_grid.add(blk)
        
        self.save_position()
        
    def __repr__(self):
        return repr(self.spec) + ": " + repr(self.blocks) + f" [{self.z_index}]"
    
    def get_min_z(self):
        return self.z_index
    
    def __fall(self, n):
        self.disintegrate()
        self.blocks = [(blk[0], blk[1], blk[2] - n) for blk in self.blocks]
        self.z_index -= n
        self.rebuild()
    
    def can_fall(self):
        bottom = [blk for blk in self.blocks if blk[2] == self.z_index]
        to_fall = 0
        can_fall = True
        while can_fall:
            for blk in bottom:
                z = blk[2] - to_fall - 1
                if z <= 0:
                    can_fall = False
                    break
                sblk = (blk[0], blk[1], z)
                can_fall &= (sblk not in self.global_grid) 
            if can_fall:
                to_fall += 1
        return to_fall

    def fall(self):
        to_fall = self.can_fall()
        if to_fall > 0:
            self.__fall(to_fall)
        return to_fall
    
    def disintegrate(self):
        for blk in self.blocks:
            self.global_grid.discard(blk)
    def rebuild(self):
        for blk in self.blocks:
            self.global_grid.add(blk)
    
    def save_position(self):
        self.saved_position = self.blocks.copy()
        self.saved_z_index = self.z_index

    def restore_position(self):
        self.blocks = self.saved_position.copy()
        self.z_index = self.saved_z_index


def work_p1(inputs):
    bricks = []
    world = set()
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        bricks.append(Brick(line, world))
    
    bricks = list(sorted(bricks, key=lambda b: b.get_min_z()))

    for brick in bricks:
        brick.fall()
    
    bricks = list(sorted(bricks, key=lambda b: b.get_min_z()))

    safe_bricks = 0
    for i in range(len(bricks)):
        brick = bricks[i]
        brick.disintegrate()
        safe = True
        for j in range(i+1, len(bricks)):
            other_brick = bricks[j]
            if other_brick.can_fall() > 0:
                safe = False
                break
        brick.rebuild()
        safe_bricks += 1 if safe else 0
    
    return safe_bricks

def work_p2(inputs):
    bricks = []
    world = set()
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        bricks.append(Brick(line, world))
    
    bricks = list(sorted(bricks, key=lambda b: b.get_min_z()))

    for brick in bricks:
        brick.fall()
        brick.save_position()
    
    bricks = list(sorted(bricks, key=lambda b: b.get_min_z()))
    
    ret = 0
    for i in range(len(bricks)):
        brick = bricks[i]
        brick.disintegrate()
        fallen = []
        for j in range(i+1, len(bricks)):
            other_brick = bricks[j]
            if other_brick.fall() > 0:
                fallen.append(other_brick)
        ret += len(fallen)

        for b in fallen:
            b.disintegrate()
        for b in fallen:
            b.restore_position()
            b.rebuild()
        brick.rebuild()
    
    return ret


def test_p1():
    assert(work_p1(test_input) == 5)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 7)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
