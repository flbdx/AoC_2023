#!/usr/bin/python3
#encoding: UTF-8

import sys

test_input1="""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test_input2="""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

test_input1 = test_input1.strip()
test_input2 = test_input2.strip()
real_input = open(sys.argv[1], encoding="UTF-8").read().strip()

def work_p1(s):
    r = 0
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        l = [int(c) for c in line if c.isnumeric()]
        r += int(l[0] * 10 + l[-1])
    return r

def work_p2(s):
    r = 0
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9,
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "0": 0}
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        l = []
        while len(line) != 0:
            for w, v in words.items():
                if line.startswith(w):
                    l.append(v)
                    break
            line = line[1:]
        r += int(l[0] * 10 + l[-1])
    return r

def test_p1():
    assert(work_p1(test_input1) == 142)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input2) == 281)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
