#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import namedtuple

test_input="""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

def work_p1(inputs):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        p1, p2 = line.split(": ")
        p2, p3 = p2.split(" | ")
        card_id = int(p1.split(" ")[-1])
        winning_numbers = set(int(s) for s in p2.split(" ") if len(s) > 0)
        numbers = set(int(s) for s in p3.split(" ") if len(s) > 0)
        in_common = len(winning_numbers & numbers)
        ret += 1 << (in_common - 1) if in_common > 0 else 0

    return ret

def work_p2(inputs):
    Card = namedtuple('Card', ('winning', 'have'))

    cards = {}
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        p1, p2 = line.split(": ")
        p2, p3 = p2.split(" | ")
        card_id = int(p1.split(" ")[-1])
        winning_numbers = set(int(s) for s in p2.split(" ") if len(s) > 0)
        numbers = set(int(s) for s in p3.split(" ") if len(s) > 0)
        cards[card_id] = Card(winning_numbers, numbers)

    possessed_cards = {cid: 1 for cid in cards}
    current_card = 1
    ret = 0
    while len(possessed_cards) != 0:
        count = possessed_cards[current_card]
        ret += count
        card = cards[current_card]
        common = len(card.winning & card.have)
        for i in range(common):
            possessed_cards[current_card + i + 1] = possessed_cards.get(current_card + i + 1, 0) + count
        del possessed_cards[current_card]
        current_card += 1
    
    return ret

def test_p1():
    assert(work_p1(test_input) == 13)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 30)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
