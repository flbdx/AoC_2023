#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import concurrent.futures

test_input="""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

class State(object):
    def __init__(self):
        self.seeds = []
        self.maps = []
    
    def parse(self, inputs):
        re_int = re.compile("[0-9]+")

        it = iter(inputs)
        self.seeds= list(map(int, re_int.findall(next(it))))

        while True:
            try:
                line = next(it)
            except:
                break
            line = line.strip()
            if len(line) == 0:
                continue

            if "map" in line:
                self.maps.append(list())
            else:
                dst, src, nb = list(map(int, re_int.findall(line)))
                self.maps[-1].append((src, src+nb, dst))
                self.maps[-1] = list(sorted(self.maps[-1], key=lambda e: e[0]))
        
    def traverse_one(self, seed):
        for mapping in self.maps:
            for mpg in mapping:
                if seed < mpg[0]:
                    break
                if seed >= mpg[0] and seed < mpg[1]:
                    seed = mpg[2] + seed - mpg[0]
                    break
        return seed
    
    def traverse_iter(self, it):
        ret = None
        for s in it:
            v = self.traverse_one(s)
            if ret is None or v < ret:
                ret = v
        return ret

    def translate_range(self, rng):
        ranges = [rng]
        for mapping in self.maps:
            translated_ranges = []
            for mpg in mapping:
                untouched_ranges = []
                for r in ranges:
                    l = r + (mpg[0], mpg[1])
                    l = list(sorted(l))
                    # print(rng, ranges, r, mpg, l)
                    for npart in range(3):
                        part = (l[npart], l[npart + 1])
                        if part[0] == part[1]:
                            continue
                        if part[0] >= r[0] and part[1] <= r[1]:
                            if part[0] >= mpg[0] and part[1] <= mpg[1]:
                                translated_ranges.append((part[0] + mpg[2] - mpg[0], part[1] + mpg[2] - mpg[0]))
                                # print(f"... {part} -> {translated_ranges[-1]}")
                            else:
                                untouched_ranges.append(part)
                                # print(f"... {part} -> {untouched_ranges[-1]}")
                ranges = untouched_ranges
            ranges += translated_ranges
        return ranges


def work_p1(inputs):
    state = State()
    state.parse(inputs)
    return state.traverse_iter(state.seeds)

def work_p2(inputs):
    state = State()
    state.parse(inputs)
    ranges = [(state.seeds[2*i], state.seeds[2*i] + state.seeds[2*i+1]) for i in range(len(state.seeds) // 2)]
    def work_range(rng):
        nrng = state.translate_range(rng)
        return min(r[0] for r in nrng)
    return min(map(work_range, ranges))

def test_p1():
    assert(work_p1(test_input) == 35)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 46)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
