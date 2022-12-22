from Day11.Day11 import Monkey, Item, round, calculate_monkey_business, set_big_mod
from collections import deque
from typing import List
import random
import pytest

def test_day_11_part_1():

    print("Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?")
    monkies = []
    with open("Day11/Day11Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip().strip(',')
            match(line.split()):
                case ["Monkey", *args]:
                    monkies.append(Monkey())
                case ["Starting", "items:", *args]:
                    args = ("".join(args)).split(',')
                    args = [Item(int(arg)) for arg in args]
                    monkies[-1].items = deque(args)
                case ["Operation:", "new", "=", *args]:
                    monkies[-1].set_operation_from_args(args)
                case ["Test:", "divisible", "by", val]:
                    monkies[-1].set_test_from_int(int(val))
                case ["If", "true:", "throw", "to", "monkey", m]:
                    monkies[-1].next_monkies[0] = int(m)
                case ["If", "false:", "throw", "to", "monkey", m]:
                    monkies[-1].next_monkies[1] = int(m)
                case _:
                    print(f"This line didn't match: {line}")
                    pass

    for monkey in monkies:
        print(monkey)

    set_big_mod(monkies)

    for _ in range(20):
        round(monkies)

    monkey_business_total = calculate_monkey_business(monkies)
    print(f"Monkey Business Total: {monkey_business_total}")
    assert monkey_business_total == 111210

def long_multiply_mod(a, b, mod):
    return ((a % mod) * (b % mod) % mod)

def test_long_multiply():
    monkey_mods = [2, 3, 5, 7, 10]
    big_mod = 1
    for mod in monkey_mods:
        big_mod = big_mod * mod
    accumulator = 6
    magic = accumulator

    tests = 0

    while(accumulator < 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000):
        accumlatand = random.randint(2,accumulator)
        magic_accumlatand = accumlatand % big_mod

        for mod in monkey_mods:
            assert (long_multiply_mod(magic, magic_accumlatand, big_mod) % mod) == ((accumulator * accumlatand) % mod)
        accumulator = accumulator * accumlatand
        magic = (magic * accumlatand) % big_mod
        tests += 1

    print(f"Tested {tests} times")
    print(accumulator)

def test_day_11_part_2():

    print("Part 1: What is the level of monkey business after 10000 rounds of stuff-slinging simian shenanigans? - NO WORRY REDUCTION")
    monkies = []
    with open("Day11/Day11Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip().strip(',')
            match(line.split()):
                case ["Monkey", *args]:
                    monkies.append(Monkey())
                case ["Starting", "items:", *args]:
                    args = ("".join(args)).split(',')
                    args = [Item(int(arg)) for arg in args]
                    monkies[-1].items = deque(args)
                case ["Operation:", "new", "=", *args]:
                    monkies[-1].set_operation_from_args(args)
                case ["Test:", "divisible", "by", val]:
                    monkies[-1].set_test_from_int(int(val))
                case ["If", "true:", "throw", "to", "monkey", m]:
                    monkies[-1].next_monkies[0] = int(m)
                case ["If", "false:", "throw", "to", "monkey", m]:
                    monkies[-1].next_monkies[1] = int(m)
                case _:
                    print(f"This line didn't match: {line}")
                    pass

    set_big_mod(monkies)

    for monkey in monkies:
        print(monkey)

    for _ in range(10000):
        round(monkies, stressed=True)

    monkey_business_total = calculate_monkey_business(monkies)
    print(f"Monkey Business Total: {monkey_business_total}")
    assert monkey_business_total == 15447387620