#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import math

test_input="""Time:      7  15   30
Distance:  9  40  200
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

real_input = list(fileinput.input())

def work(races):
    ret = 1
    for race in races:
        t, r = race
        delta = t * t - 4 * r
        l1 = (t-math.sqrt(delta))/ 2
        l2 = (t+math.sqrt(delta))/ 2
        l1_ = math.ceil(l1)
        l2_ = math.floor(l2)
        if l1_ == l1:
            l1_ += 1
        if l2_ == l2:
            l2_ -= 1
        
        l1 = min(l1_, t)
        l2 = min(l2_, t)
        ret *= (l2 - l1 + 1)
    return ret

def work_p1(inputs):
    re_int = re.compile("[0-9]+")
    it = iter(inputs)
    durations = list(map(int, re_int.findall(next(it))))
    best_distances = list(map(int, re_int.findall(next(it))))
    races = [(a, b) for a, b in zip(durations, best_distances)]

    return work(races)


def work_p2(inputs):
    re_int = re.compile("[0-9]+")
    it = iter(inputs)
    durations = list(re_int.findall(next(it)))
    best_distances = list(re_int.findall(next(it)))
    duration = int("".join(durations))
    best_distance = int("".join(best_distances))
    
    return work([(duration, best_distance)])

    
def test_p1():
    assert(work_p1(test_input) == 288)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 71503)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
