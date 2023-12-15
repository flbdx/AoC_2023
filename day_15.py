#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import functools

test_input="""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

real_input = list(fileinput.input())

def hash(s):
    return functools.reduce(lambda v, c: ((v + ord(c)) * 17) & 0xFF, s, 0)

def work_p1(inputs):
    line = next(iter(inputs)).strip()
    return sum(hash(s) for s in line.split(","))

def work_p2(inputs):
    line = next(iter(inputs)).strip()
    hashmap = [list() for i in range(256)]

    for instr in line.split(","):
        if instr[-1] == '-':
            label, ope = instr[:-1], instr[-1]
        else:
            label, ope = instr[:-2], instr[-1]
        
        box = hash(label)
        if ope == '-':
            for i in range(len(hashmap[box])):
                if hashmap[box][i][0] == label:
                    hashmap[box] = hashmap[box][:i] + hashmap[box][i+1:]
                    break
        else:
            inserted = False
            for i in range(len(hashmap[box])):
                if hashmap[box][i][0] == label:
                    hashmap[box][i] = (label, ope)
                    inserted = True
                    break
            if not inserted:
                hashmap[box].append((label, ope))
    
    ret = 0
    for box in range(256):
        for l in range(len(hashmap[box])):
            ret += (box + 1) * (l + 1) * int(hashmap[box][l][1])
    return ret


def test_p1():
    assert(work_p1(test_input) == 1320)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 145)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
