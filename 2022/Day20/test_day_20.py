from __future__ import annotations
from collections import deque
from typing import List, Callable
import random
import pytest
import math
import copy
from functools import partial

from termcolor import colored
#colored(tree.height, 'red')

class ElfEncryptorElement:
    def __init__(self, value, position=None):
        self.mix_count = 0
        self.position = position
        self.value = value
        self.id = position

    def __repr__(self) -> str:
        return f"< {self.value}, Pos: {self.position}, mixed {self.mix_count} times >"

class ElfEncryptor:
    def __init__(self):
        self.elements = []

    def append(self, number):
        self.elements.append(ElfEncryptorElement(number, len(self.elements)))

    def render(self, verbose=False):
        if verbose:
            for element in self.elements:
                print(element)
        else:
            print("< ", end="")
            for element in self.elements:
                try:
                    print(f"{element.value} ", end="")
                except AttributeError: 
                    print(f"{element} ", end="")
            print(">")

    def mix(self, fast=True, iterations=1):
        to_mix = [element for element in self.elements]
        """
        to_mix.reverse() # The first elements to be mixed are at the end and poppable
        while(len(to_mix) > 0):
            element = to_mix.pop()
        """
        for _ in range(iterations):
            for element in to_mix:
                #print(f"Mixing element {element}, There are {len(to_mix)} elements to mix after this")
                if not fast:
                    self.mix_single_slow(element)
                else:
                    self.mix_single(element)
                

    def mix_single(self, element):
        #self.render()
        if element.value == 0:
            element.mix_count += 1
            return

        initial_index = self.elements.index(element)
        self.elements.pop(initial_index)
        if element.value > 0:
            dest_index = initial_index + element.value + 0
            dest_index = dest_index % len(self.elements)
        else:
            dest_index = initial_index + element.value + 0
            dest_index = dest_index % (-len(self.elements))

        self.elements.insert(dest_index, element)


    def mix_single_slow(self, element):
        #self.render()
        if element.value == 0:
            element.mix_count += 1
            return

        moves = element.value
        while moves > 0:
            self.swap(element, forward=True)
            moves -= 1
        while moves < 0:
            self.swap(element, forward=False)
            moves += 1        

    def swap(self, element: ElfEncryptorElement, forward: bool):
        item_index = self.elements.index(element)
        dest_index = None
        if forward:
            # Handle Wrap Case
            if item_index == (len(self.elements) - 1):
                dest_index = 0
            else:
                dest_index = item_index + 1
        else:
            # Handle Wrap Case
            if item_index == 0:
                dest_index = (len(self.elements) - 1)
            else:
                dest_index = item_index - 1
        
        # Swap dest/item with placeholder
        ele1 = self.elements[item_index]
        self.elements[item_index] = self.elements[dest_index]
        self.elements[dest_index] = ele1


        

    def find_coordinates(self):
        zero_index = self.elements.index([element for element in self.elements if element.value == 0][0])
        print(zero_index)
        a = (self.elements[(zero_index + 0 + 1000) % (len(self.elements) + 0)])
        b = (self.elements[(zero_index + 0 + 2000) % (len(self.elements) + 0)])
        c = (self.elements[(zero_index + 0 + 3000) % (len(self.elements) + 0)])
        print(a, b, c)
        return a.value + b.value + c.value

    def contains_duplicates(self):
        nums = [elemnt.value for elemnt in self.elements]
        for num in nums:
            if nums.count(num) > 1:
                print(num)
                print(nums.count(num))
                print("NOT COOL DUDE")



class Day20Tester:
    def __init__(self, encryption_key=1):
        self.ee = ElfEncryptor()
        self.encryption_key = encryption_key

    def consume(self, line: str):
        self.ee.append(int(line) * self.encryption_key)
        

    def render(self):
        self.ee.render()

    def mix(self, fast=True, iterations=1):
        self.ee.mix(fast, iterations)



def test_part_demo():
    print("Part DEMO")
    print("BEGIN")
    day20 = Day20Tester()
    with open("2022/Day20/Day20DemoData.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    day20.ee.contains_duplicates()
    day20.render()
    day20.mix()
    #day20.render()
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 3

@pytest.mark.skip(reason="Too Slow!")
def test_part_1():
    print("Part 1")
    print("BEGIN")
    day20 = Day20Tester()
    with open("2022/Day20/Day20Data.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    #day20.ee.contains_duplicates()
    day20.render()
    day20.mix(fast=False)
    #day20.render()
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 4066

def test_part_1_fast():
    print("Part 1")
    print("BEGIN")
    day20 = Day20Tester()
    with open("2022/Day20/Day20Data.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    #day20.ee.contains_duplicates()
    #day20.render()
    day20.mix(fast=True)
    #day20.render()
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 4066

def test_part_2():
    print("Part 2")
    print("BEGIN")
    day20 = Day20Tester(encryption_key=811589153)
    with open("2022/Day20/Day20Data.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    day20.mix(fast=True, iterations=10)
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 6704537992933

def test_part_2_demo():
    print("Part 2")
    print("BEGIN")
    day20 = Day20Tester(encryption_key=811589153)
    with open("2022/Day20/Day20DemoData.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    day20.mix(fast=True, iterations=10)
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 1623178306

@pytest.mark.xfail
def test_positive_mix_100():
    for i in range(1, 100):
        print(f"Testing {i}")
        ee = ElfEncryptor()
        ee.append(1)
        ee.append(i)
        ee.append(2)
        ee.append(3)
        ee.mix_single(ee.elements[1])
        ee.render()

        print(f"Checking elements[{(i + 1) % 4}] == {ee.elements[(i + 1) % 4].value} == {i}")
        assert ee.elements[(i + 1) % 4].value == i

@pytest.mark.xfail
def test_negative_mix_100():
    for i in range(-1, -100, -1):
        print(f"Testing {i}")
        ee = ElfEncryptor()
        ee.append(1)
        ee.append(i)
        ee.append(2)
        ee.append(3)
        ee.mix_single(ee.elements[1])
        ee.render()

        print(f"Checking elements[{(i + 1) % 4}] == {ee.elements[(i + 1) % 4].value} == {i}")
        assert ee.elements[(i + 1) % 4].value == i

