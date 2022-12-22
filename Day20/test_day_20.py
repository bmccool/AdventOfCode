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

    def mix(self):
        to_mix = [element for element in self.elements]
        to_mix.reverse() # The first elements to be mixed are at the end and poppable
        while(len(to_mix) > 0):
            element = to_mix.pop()
            self.mix_single(element)
             

    def mix_single(self, element):
        #print(f"Mixing element {element}")
        #self.render()
        if element.value == 0:
            element.mix_count += 1
            return

        old_index = self.elements.index(element)
        self.elements.remove(element)
        self.elements.insert(old_index, "X")
        #self.render()
        element.mix_count += 1
        if element.value < 0:
            new_index = old_index + (element.value % (-len(self.elements) + 0))
            # TODO This is how the example behaves, but why?
            #if new_index == 0:
            #    new_index = len(self.elements)
            #print(new_index)
            while(new_index < 0):
                new_index += (len(self.elements) + 1)
            #print(new_index)
        else:
            #print(f"Old Index + value + 1 = \n{old_index} + {element.value} + 1 \n All with Mod {len(self.elements)}")
            if False: #(old_index + element.value + 1) >= (len(self.elements) * 2):
                additional_value = -1
            else:
                additional_value = 0
            new_index = (old_index + (element.value % (len(self.elements) + 0))+ additional_value + 1) % (len(self.elements) + 1)

        #print(f"Inserting {element.value} into index {new_index}")
        self.elements.insert(new_index, element)
        #self.render()
        self.elements.remove("X")
        self.render()

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
    def __init__(self):
        self.ee = ElfEncryptor()

    def consume(self, line: str):
        self.ee.append(int(line))
        

    def render(self):
        self.ee.render()

    def mix(self):
        self.ee.mix()



def test_part_1():
    print("Part 1")
    print("BEGIN")
    day20 = Day20Tester()
    with open("Day20/Day20Data.txt", "r") as datafile:
        for line in datafile:
            day20.consume(line.strip())

    day20.ee.contains_duplicates()
    day20.render()
    day20.mix()
    #day20.render()
    coordinates = day20.ee.find_coordinates()
    print(f"Coordinates: {coordinates}")
    assert coordinates == 3

def test_positive_mixe_1():
    print("Positive Mix 1")
    ee = ElfEncryptor()
    ee.append(3)
    ee.append(1)
    ee.append(1)
    ee.append(1)

    ee.mix_single(ee.elements[0])
    ee.render()

    assert ee.elements[3].value == 3

def test_positive_mixe_2():
    print("Positive Mix 2")
    ee = ElfEncryptor()
    ee.append(4)
    ee.append(1)
    ee.append(1)
    ee.append(1)

    ee.mix_single(ee.elements[0])
    ee.render()

    assert ee.elements[0].value == 4

def test_positive_mixe_3():
    print("Positive Mix 3")
    ee = ElfEncryptor()
    ee.append(5)
    ee.append(1)
    ee.append(1)
    ee.append(1)

    ee.mix_single(ee.elements[0])
    ee.render()

    assert ee.elements[1].value == 5

def test_positive_mixe_6():
    print("Positive Mix 6")
    ee = ElfEncryptor()
    ee.append(6)
    ee.append(1)
    ee.append(1)
    ee.append(1)

    ee.mix_single(ee.elements[0])
    ee.render()

    assert ee.elements[2].value == 6

def test_positive_mixe_7():
    print("Positive Mix 7")
    ee = ElfEncryptor()
    ee.append(7)
    ee.append(1)
    ee.append(1)
    ee.append(1)

    ee.mix_single(ee.elements[0])
    ee.render()

    assert ee.elements[3].value == 7

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

def test_positive_n3():
    print("Positive Mix -3")
    ee = ElfEncryptor()
    for e in [1, -3, 2, 3, -2, 0, 4]:
        ee.append(e)

    ee.render()
    ee.mix_single(ee.elements[1])
    ee.render()

    assert ee.elements[3].value == -2
    assert ee.elements[4].value == -3
    assert ee.elements[5].value == 0