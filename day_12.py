#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import functools

# test_input="""#.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1
# """.splitlines()

test_input="""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

# for part 1, first a tester, returns True if the record matches the groups
def is_valid(record, groups):
    counts = []
    n = 0
    for c in record:
        if c == '#':
            n += 1
        else:
            if n != 0:
                counts.append(n)
            n = 0
    if n != 0:
        counts.append(n)
    
    return groups == counts

# for part 2, need a recursive, cached build of the groups
@functools.cache
def rec_build_from_partial_record(partial_record, groups):
    if len(partial_record) == 0:
        if len(groups) == 0:
            return 1
        return 0

    c = partial_record[0]
    if c == '#':
        # empty group, but more springs
        if len(groups) == 0:
            return 0
        
        # current group is larger than what we have
        if len(partial_record) < groups[0] or "." in partial_record[0:groups[0]]:
            return 0
        
        # there is no . in the groups[0] following chars
        # and len(partial_record) >= groups[0]
        
        if len(partial_record) > groups[0]:
            # current group is shorter than what we have
            if partial_record[groups[0]] == '#':
                return 0
            # accept this group and count the following '?' as '.'
            if partial_record[groups[0]] == '?':
                return rec_build_from_partial_record(partial_record[groups[0] + 1:], groups[1:])
        
        # accept this group
        return rec_build_from_partial_record(partial_record[groups[0]:], groups[1:])
    
    elif c == '.':
        # remove all leading '.'
        s = partial_record.lstrip('.')
        return rec_build_from_partial_record(s, groups)
    elif c == '?':
        return rec_build_from_partial_record('#' + partial_record[1:], groups) + rec_build_from_partial_record('.' + partial_record[1:], groups)

# part1 is a light bruteforce over all the possible replacements for the placeholders
def work_p1(inputs):
    ret = 0

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        #### bruteforce ####

        # record, groups = line.split(" ")
        # record = list(record)
        # groups = list(map(int, groups.split(",")))

        # unknown_positions = []
        # for i in range(len(record)):
        #     if record[i] == '?':
        #         unknown_positions.append(i)
        
        # n_unknowns = len(unknown_positions)

        # for N in range(1<<n_unknowns):
        #     for b in range(n_unknowns):
        #         record[unknown_positions[b]] = '#' if ((N >> b) & 1) else '.'
        #     ret += is_valid(record, groups)

        #### recursive ####

        record, groups = line.split(" ")
        groups = tuple(map(int, groups.split(",")))

        ret += rec_build_from_partial_record(record, groups)
    
    return ret

def work_p2(inputs):
    ret = 0

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        record, groups = line.split(" ")
        groups = tuple(map(int, groups.split(",")))

        record = record + '?' + record + '?' + record + '?' + record + '?' + record
        groups = groups + groups + groups + groups + groups

        ret += rec_build_from_partial_record(record, groups)
    return ret

def test_p1():
    assert(work_p1(test_input) == 21)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 525152)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
