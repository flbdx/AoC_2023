#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

test_input="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

real_input = list(fileinput.input())

class Card(object):
    def __init__(self, v, part2=False):
        self.face = v
        if not part2:
            self.value = 14 if v == 'A' else 13 if v == 'K' else 12 if v == 'Q' else 11 if v == 'J' \
            else 10 if v == 'T' else 9 if v == '9' else 8 if v == '8' else 7 if v == '7' else 6 if v == '6' \
            else 5 if v == '5' else 4 if v == '4' else 3 if v == '3' else 2
        else:
            self.value = 14 if v == 'A' else 13 if v == 'K' else 12 if v == 'Q' else  1 if v == 'J' \
            else 10 if v == 'T' else 9 if v == '9' else 8 if v == '8' else 7 if v == '7' else 6 if v == '6' \
            else 5 if v == '5' else 4 if v == '4' else 3 if v == '3' else 2
    
    def __gt__(self, o):
        return self.value > o.value
    def __lt__(self, o):
        return self.value < o.value
    def __eq__(self, o):
        return self.value == o.value
    def __ne__(self, o):
        return self.value != o.value
    def __ge__(self, o):
        return self.value >= o.value
    def __le__(self, o):
        return self.value <= o.value
    def __hash__(self):
        return hash(self.face)
    
    def __repr__(self):
        return f"[{self.face}]"

class Hand(object):
    def __init__(self, hand, bid, part2=False):
        self.hand = [Card(c, part2=part2) for c in hand]
        self.bid = bid

        if not part2:
            self.__setup_part1()
        else:
            self.__setup_part2()

    def __hand_value(hand):
        counts = {}
        for c in hand:
            counts[c] = counts.get(c, 0) + 1

        if len(counts) == 1:
            return 7                            # Five of a kind
        elif len(counts) == 2:
            l = list(sorted(counts.values()))
            if l[0] == 1 and l[1] == 4:
                return 6                        # Four of a kind
            elif l[0] == 2 and l[1] == 3:
                return 5                        # Full house
        elif len(counts) == 3:
            l = list(sorted(counts.values()))
            if l[0] == 1 and l[1] == 1 and l[2] == 3:
                return 4                        # Three of a kind
            elif l[0] == 1 and l[1] == 2 and l[2] == 2:
                return 3                        # Two pair
        elif len(counts) == 4:
            return 2                            # One pair
        else:
            return 1                            # High card

    def __setup_part1(self):
        self.type_value = Hand.__hand_value(self.hand)
        
        
    def __setup_part2(self):
        n_jokers = sum((1 for c in self.hand if c.face == 'J'))
        other_cards = [Card(c, part2=True) for c in "23456789TQKA"]

        if n_jokers == 0:
            self.type_value = Hand.__hand_value(self.hand)
            return

        self.type_value = 0

        for replacements in itertools.product(other_cards, repeat=n_jokers):
            nhand = []
            j = 0
            for i in range(5):
                if self.hand[i].face != 'J':
                    nhand.append(self.hand[i])
                else:
                    nhand.append(replacements[j])
                    j += 1
            v = Hand.__hand_value(nhand)
            self.type_value = max(v, self.type_value)
        
    
    def __cmp(self, o):
        if self.type_value > o.type_value:
            return 1
        elif self.type_value < o.type_value:
            return -1
        else:
            for i in range(5):
                if self.hand[i] > o.hand[i]:
                    return 1
                elif self.hand[i] < o.hand[i]:
                    return -1
            return 0
    def __gt__(self, o):
        return self.__cmp(o) > 0
    def __lt__(self, o):
        return self.__cmp(o) < 0
    def __eq__(self, o):
        return self.__cmp(o) == 0
    def __ne__(self, o):
        return self.__cmp(o) != 0
    def __ge__(self, o):
        return self.__cmp(o) >= 0
    def __le__(self, o):
        return self.__cmp(o) <= 0

    def __repr__(self):
        return "[" + "".join(c.face for c in self.hand) + f"]{(self.bid, self.type_value)}"

def work_p1(inputs):
    hands = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        hand, bid = line.split(" ")
        hand = Hand(hand, int(bid))
        hands.append(hand)
    hands = list(sorted(hands, reverse=False))
    
    ret = sum(hands[i].bid * (i+1) for i in range(len(hands)))
    return ret

def work_p2(inputs):
    hands = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        hand, bid = line.split(" ")
        hand = Hand(hand, int(bid), part2=True)
        hands.append(hand)
    hands = list(sorted(hands, reverse=False))
    
    ret = sum(hands[i].bid * (i+1) for i in range(len(hands)))
    return ret

def test_p1():
    assert(work_p1(test_input) == 6440)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 5905)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
