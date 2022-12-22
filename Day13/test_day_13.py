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


class Day13Tester:
    def __init__(self):
        self.left = None
        self.right = None
        self.tests_done = 1
        self.sum_indicies = 0

    def test(self):
        result = self.compare(eval(self.left), eval(self.right))
        print(f"Pair {self.tests_done} result: {result}\nLeft : {self.left}\nRight: {self.right} with result")
        if result == 1:
            self.sum_indicies += self.tests_done
        self.tests_done += 1

    @staticmethod
    def compare(left, right) -> bool:
        # If both are not list, compare directly
        #print(f"Comparing {left} ||| {right}")
        if (not isinstance(left, list)) and (not isinstance(right, list)):
            if int(left) < int(right):
                #print(" - Success!")
                return 1
            elif int(left) == int(right):
                #print(" - Undetermined...")
                return 0
            else:
                #print(" - Failure!")
                return -1

        # Otherwise, if one side is an int and the other is a list, make sure both are lists
        if not isinstance(left, list):
            left = [left]
        if not isinstance(right, list):
            right = [right]

        # And compare elementwise
        for i, e in enumerate(right):
            try:
                new_left = left[i]
            except IndexError:
                # Left ranout first!
                #print(" - Success!")
                return 1

            result = Day13Tester.compare(left[i], right[i])
            if result > 0:
                # Items were in right order!
                return 1
            elif result < 0:
                return -1
        if len(left) > len(right):
            return -1
        return 0
             

    def consume(self, line: str):
        if line != "":
            if self.left == None:
                self.left = line

            elif self.right == None:
                self.right = line

        if self.left and self.right :
            self.test()
            self.left = None
            self.right = None

import functools
#key=functools.cmp_to_key(compare)
class Day13TesterPart2(Day13Tester):
    def __init__(self):
        super().__init__()
        self.packet_list = [[[2]], [[6]]]

    def consume(self, line: str):
       if line != "":
        self.packet_list.append(eval(line))

    def sort(self):
        print("SORTING")
        self.packet_list.sort(key=functools.cmp_to_key(Day13TesterPart2.compare), reverse=True)

    def analyze(self):
        product = 1
        for i, packet in enumerate(self.packet_list):
            print(packet)
            if (packet == [[2]] ) or (packet ==[[6]]):
                product = product * (i + 1)
        return product


   


def test_part_1():
    print("Part 1")
    day13 = Day13Tester()
    with open("Day13/Day13Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip()
            day13.consume(line)
    print(f"Sum of indicies is {day13.sum_indicies}")

def test_part_2():
    print("Part 2")
    day13 = Day13TesterPart2()
    with open("Day13/Day13Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip()
            day13.consume(line)
    day13.sort()
    result = day13.analyze()
    print(f"Result of part2 is {result}")