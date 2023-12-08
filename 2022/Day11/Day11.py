from __future__ import annotations
from collections import deque
from typing import List, Callable
import time





class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def calm(self):
        self.worry_level = int(int(self.worry_level) // 3)

    def __add__(self, other):
        try:
            return self.worry_level + other.worry_level
        except AttributeError:
            return self.worry_level + other

    def __sub__(self, other: Item):
        try:
            return self.worry_level - other.worry_level
        except AttributeError:
            return self.worry_level - other

    def __mul__(self, other: Item):
        try:
            return self.worry_level * other.worry_level
        except AttributeError:
            return self.worry_level * other

class Monkey:
    def __init__(self, starting_items: deque[Item]=[], operation: Callable=None, test: Callable=None, next_monkies: List[Monkey]=None):
        self.items = deque(starting_items)
        self.operation = operation
        self.test = test
        self.divisor = None
        self.next_monkies = next_monkies or [-1, -1]
        self.inspections = 0
        self.big_mod = None

    def set_operation_from_args(self, args: List[str]):
        "Assume args is of the form old * old + 6, but as a WS separated list of strings"
        "Assign a lambda to self.operation that captures old and utilizes <args> as the body"
        arg_string = " ".join(args)
        #print(arg_string)
        #assert arg_string != "old * old"
        if arg_string == "old * old":
            self.operation = lambda old: ((old % self.big_mod) * (old % self.big_mod) % self.big_mod)
            return

        # Lol, this is clunky.  Could probably fix Item class to allow operators, or just make it a int and get rid of fancypants class
        #arg_string.replace("old", "old.worry_level")
        #print(arg_string)
        self.operation = lambda old: eval(arg_string)

    def set_test_from_int(self, val: int):
        "Assume the test is just return True if divisible by val"
        self.test = lambda v: True if ((v % val) == 0) else False
        self.divisor = val

    def __repr__(self):
        return f"{self.inspections} insepctions.  Item List: {[i.worry_level for i in self.items]}"

    def inspect(self):
        self.items[0].worry_level = self.operation(self.items[0].worry_level)
        self.inspections += 1

    def get_bored(self):
        self.items[0].calm()

    def throw_to(self) -> int:
        #print(self)
        if self.test(int(self.items[0].worry_level)):
            next_monkey = self.next_monkies[0]
        else:
            next_monkey = self.next_monkies[1]
        #print(f"Throwing to Monkey: {next_monkey}")
        return next_monkey

    def catch(self, item: Item):
        self.items.append(item)


def round(monkies: List[Monkey], stressed: bool=False):
    for monkey in monkies:
        #print("=" * 10 + "MONKEY" + "=" * 10)
        #print(monkey)
        while len(monkey.items) > 0:
            #print(f"Monkey inspects an item with worry level {monkey.items[0].worry_level}")
            monkey.inspect()
            #print(f"Worry level is multiplied to {monkey.items[0].worry_level}")
            if not stressed:
                monkey.get_bored()
            #print(f"Monkey gets bored with item.  Worry level is divided by 3 to {monkey.items[0].worry_level}")
            next_monkey = monkey.throw_to()
            monkies[next_monkey].catch(monkey.items.popleft())


def calculate_monkey_business(monkies: List[Monkey]) -> int:
    shenanigans = sorted([monkey.inspections for monkey in monkies])
    return shenanigans.pop() * shenanigans.pop()


def set_big_mod(monkies: List[Monkey]):
    big_mod = 1
    for monkey in monkies:
        print(f"Monkey Divisor: {monkey.divisor}")
        big_mod = big_mod * monkey.divisor

    for monkey in monkies:
        monkey.big_mod = big_mod


if __name__ == "main":

    print("Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?")
    monkies = []
    with open("Day11Data.txt", "r") as datafile:
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

    for _ in range(20):
        round(monkies)
        #for monkey in monkies:
        #    print(monkey)

    print(f"Monkey Business Total: {calculate_monkey_business(monkies)}")




    print("Part 1: what is the level of monkey business after 10000 rounds of stuff-slinging simian shenanigans? - NO WORRY REDUCTION")
    monkies = []
    with open("Day11Data.txt", "r") as datafile:
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

    for r in range(10000):
        start_time = time.time()
        round(monkies, stressed=True)
        end_time = time.time()
        print(f"Finished round {r} in {(end_time - start_time):.2f}s")
        #for monkey in monkies:
        #    print(monkey)

    print(f"Monkey Business Total: {calculate_monkey_business(monkies)}")