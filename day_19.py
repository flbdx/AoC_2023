#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import namedtuple, deque
import re
import operator

test_input="""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_19"]

real_input = list(fileinput.input())

Part = namedtuple("Part", list("xmas"))

def work_p1(inputs):
    workflows = {}

    rule_re = re.compile("([a-z]+)([<>])([0-9]+):([a-zAR]+)")
    part_re = re.compile("([0-9]+)")

    it = iter(inputs)
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        label, raw_rules = line.split('{')
        raw_rules = raw_rules[:-1].split(",")
        
        rules = []
        for rule in raw_rules:
            if rule == "A":
                rules.append(lambda part: True)
            elif rule == "R":
                rules.append(lambda part: False)
            elif ":" in rule:
                m = rule_re.match(rule)
                var, ope, n, target = m.groups()
                if target == "A":
                    target = True
                elif target == "R":
                    target = False
                n = int(n)
                ope = operator.lt if ope == "<" else operator.gt

                def get_lambda(var, ope, n, target):
                    return lambda part: target if ope(getattr(part, var), n) else None
                rules.append(get_lambda(var, ope, n, target))
            else:
                def get_lambda(target):
                    return lambda part: target
                rules.append(get_lambda(rule))
            
        workflows[label] = rules
    
    parts = []
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        ints = tuple(int(g) for g in part_re.findall(line))
        parts.append(Part(*ints))
    
    ret = 0
    for part in parts:
        # print(part)
        label = "in"
        finished = False
        accepted = False
        while not finished:
            # print(label)
            for rule in workflows[label]:
                res = rule(part)
                if res == True:
                    finished = True
                    accepted = True
                    break
                elif res == False:
                    finished = True
                    accepted = False
                    break
                elif res == None:
                    continue
                else:
                    label = res
                    break
        
        if accepted:
            ret += part.x + part.m + part.a + part.s
    return ret

class State(object):
    def __init__(self, empty=False):
        if empty:
            self.x = []
            self.m = []
            self.a = []
            self.s = []
        else:
            self.x = list(range(1, 4001))
            self.m = list(range(1, 4001))
            self.a = list(range(1, 4001))
            self.s = list(range(1, 4001))
    
    def split(self, var, ope, n):
        o1 = State(empty=True)
        o2 = State(empty=True)

        for v in "xmas":
            if v == var:
                for i in getattr(self, v):
                    (getattr(o1, v) if ope(i, n) else getattr(o2, v)).append(i)
            else:
                setattr(o1, v, getattr(self, v).copy())
                setattr(o2, v, getattr(self, v).copy())

        return o1, o2

    
    def __repr__(self):
        return f"{{x:{len(self.x)},m:{len(self.m)},a:{len(self.a)},s:{len(self.s)}}}"

    def card(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

def work_p2(inputs):
    workflows = {}

    rule_re = re.compile("([a-z]+)([<>])([0-9]+):([a-zAR]+)")

    it = iter(inputs)
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        label, raw_rules = line.split('{')
        raw_rules = raw_rules[:-1].split(",")
        
        rules = []
        for rule in raw_rules:
            if rule == "A":
                rules.append(True)
            elif rule == "R":
                rules.append(False)
            elif ":" in rule:
                m = rule_re.match(rule)
                var, ope, n, target = m.groups()
                if target == "A":
                    target = True
                elif target == "R":
                    target = False
                n = int(n)
                ope = operator.lt if ope == "<" else operator.gt

                rules.append((var, ope, n, target))
            else:
                rules.append(rule)
            
        workflows[label] = rules

    accepted = []

    q = deque()
    q.append((State(), "in", 0))

    while len(q) > 0:
        state, label, rule_nb = q.popleft()
        if rule_nb > len(workflows[label]):
            continue

        rule = workflows[label][rule_nb]
        if rule == True:
            accepted.append(state)
        elif rule == False:
            pass
        elif type(rule) == str:
            q.append((state, rule, 0))
        else:
            var, ope, n, next_label = rule
            s1, s2 = state.split(var, ope, n)
            if next_label == True:
                accepted.append(s1)
            elif next_label == False:
                pass
            else:
                q.append((s1, next_label, 0))
            q.append((s2, label, rule_nb + 1))

    return sum(s.card() for s in accepted)
        
def test_p1():
    assert(work_p1(test_input) == 19114)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 167409079868000)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
