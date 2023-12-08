#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import math

test_input_1="""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

test_input_2="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

test_input_3="""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

def parse_inputs(inputs):
    it = iter(inputs)
    instructions = next(it).strip()
    transitions = {}

    for line in it:
        line = line.strip()
        if len(line) == 0:
            continue
        state, rem = line.split(" = ")
        left, right = rem[1:-1].split(", ")
        transitions[state] = (left, right)
    
    return instructions, transitions

def work_p1(inputs):
    instructions, transitions = parse_inputs(inputs)

    st = "AAA"
    n = 0
    n_instructions = len(instructions)
    while st != "ZZZ":
        i = instructions[n % n_instructions]
        st = transitions[st][0] if i == "L" else transitions[st][1]
        n += 1
    
    return n

def work_p2(inputs):
    instructions, transitions = parse_inputs(inputs)

    start_nodes = {k for k in transitions if k[-1] == "A"}
    end_nodes = {k for k in transitions if k[-1] == "Z"}
    
    n_instructions = len(instructions)

    # here the inputs are quite simple. Don't need the Chinese Reminder Theorem
    ret = 1
    for node in start_nodes:
        n = 0
        while not node in end_nodes:
            i = instructions[n % n_instructions]
            node = transitions[node][0] if i == "L" else transitions[node][1]
            n += 1
        # offset = n
        # end = node
        # while True:
        #     i = instructions[n % n_instructions]
        #     node = transitions[node][0] if i == "L" else transitions[node][1]
        #     n += 1
        #     if node == end:
        #         break
        # cycle = n - offset
        ret = math.lcm(ret, n)
    return ret

def test_p1():
    assert(work_p1(test_input_1) == 2)
    assert(work_p1(test_input_2) == 6)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input_3) == 6)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
