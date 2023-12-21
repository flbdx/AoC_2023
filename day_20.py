#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from collections import deque
import math

test_input_1=r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".splitlines()

test_input_2=r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

real_input = list(fileinput.input())

class Pulse(Enum):
    LOW = 0
    HIGH = 1

class Module(object):
    def __init__(self, label : str, send_queue : deque):
        self.label = label
        self.inputs = []
        self.outputs = []
        self.send_queue = send_queue
    
    def add_input(self, input):
        self.inputs.append(input)
    
    def add_output(self, output):
        self.outputs.append(output)
    
    def enqueue_pulse(self, pulse):
        for output in self.outputs:
            self.send_queue.append((self, output, pulse))
    
    def __repr__(self):
        ins = ",".join(i.label for i in self.inputs)
        outs = ",".join(i.label for i in self.outputs)
        return f"{type(self).__name__} : {ins} <> {outs}"

class FlipFlop(Module):
    def __init__(self, label : str, send_queue : deque):
        super().__init__(label, send_queue)
        self.is_on = False
    
    def receive(self, from_input, pulse):
        if pulse == Pulse.HIGH:
            return
        
        self.is_on = not self.is_on
        if self.is_on:
            self.enqueue_pulse(Pulse.HIGH)
        else:
            self.enqueue_pulse(Pulse.LOW)
        

class Conjunction(Module):
    def __init__(self, label : str, send_queue : deque):
        super().__init__(label, send_queue)
        self.memory = {}
    
    def receive(self, from_input, pulse):
        self.memory[from_input] = pulse
        all_high = True
        for input in self.inputs:
            all_high &= (self.memory.get(input, Pulse.LOW) == Pulse.HIGH)
        if all_high:
            self.enqueue_pulse(Pulse.LOW)
        else:
            self.enqueue_pulse(Pulse.HIGH)

class Broadcast(Module):
    def __init__(self, label : str, send_queue : deque):
        super().__init__(label, send_queue)
    
    def receive(self, from_input, pulse):
        self.enqueue_pulse(pulse)

class Rx(Module):
    def __init__(self, label : str, send_queue : deque):
        super().__init__(label, send_queue)
        self.flag = False
    
    def receive(self, from_inputs, pulse):
        self.flag |= (pulse == Pulse.LOW)

class Null(Module):
    def __init__(self, label : str, send_queue : deque):
        super().__init__(label, send_queue)
    
    def receive(self, from_inputs, pulse):
        pass

def setup(inputs):
    send_queue = deque()

    modules = {}
    lines = list(inputs)
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            break
        src, dests = line.split(" -> ")
        dests = dests.split(", ")

        if src == "broadcaster":
            label = "broadcaster"
            obj = Broadcast(label, send_queue)
        elif src[0] == "%":
            label = src[1:]
            obj = FlipFlop(label, send_queue)
        else:
            label = src[1:]
            obj = Conjunction(label, send_queue)
        
        modules[label] = (obj, dests)
    
    modules["rx"] = (Rx("rx", send_queue), [])

    for label, module_data in modules.items():
        obj, dests = module_data
        for dst in dests:
            other = modules[dst][0]
            obj.add_output(other)
            other.add_input(obj)
    for label, module_data in modules.items():
        modules[label] = module_data[0]
    
    return send_queue, modules

def work_p1(inputs):
    send_queue, modules = setup(inputs)
    
    count_low = 0
    count_high = 0
    for i in range(1000):
        send_queue.appendleft((Null("button", send_queue), modules["broadcaster"], Pulse.LOW))
        while len(send_queue) > 0:
            mod_from, mod_to, pulse = send_queue.popleft()
            if pulse == Pulse.HIGH:
                count_high += 1
            else:
                count_low += 1
            mod_to.receive(mod_from, pulse)

    return count_low * count_high

# for my inputs :
# &hp -> rx
# &sr -> hp
# &sn -> hp
# &rf -> hp
# &vq -> hp
#
# I will spy for a single low pulse incoming on sr, sn rf and vq
# This low pulse means a high pulse incoming on hp
# 
def work_p2(inputs):
    send_queue, modules = setup(inputs)

    n_presses = 0
    cycles = {}
    while len(cycles) != 4:
        n_presses += 1
        send_queue.appendleft((Null("button", send_queue), modules["broadcaster"], Pulse.LOW))
        while len(send_queue) > 0:
            mod_from, mod_to, pulse = send_queue.popleft()
            mod_to.receive(mod_from, pulse)

            if pulse == Pulse.LOW and mod_to.label in ("sr", "sn", "rf", "vq"):
                cycles[mod_to.label] = n_presses
                print(cycles)

    return math.lcm(cycles["vq"], math.lcm(cycles["sr"], math.lcm(cycles["sn"], cycles["rf"])))

def test_p1():
    assert(work_p1(test_input_1) == 32000000)
    assert(work_p1(test_input_2) == 11687500)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    # assert(work_p2(test_input_1) == None)
    pass
test_p2()

def p2():
    print(work_p2(real_input))
p2()
