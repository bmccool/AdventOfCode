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


class Field:
    def __init__(self):
        # Smallest containing rectangle
        self.left = None
        self.right = None

        self.top = None
        self.bottom = None

        self.lines_consumed = 0

        self.elves = set()

    def place_elf(self, coordinates):
        # Deal with first input
        if self.bottom == None:
            self.left = coordinates[0]
            self.right = coordinates[0]
            self.top = coordinates[0]
            self.bottom = coordinates[0]


        self.elves.add(coordinates)
        self.left = min(self.left, coordinates[0])
        self.right = max(self.right, coordinates[0])
        self.top = min(self.top, coordinates[1])
        self.bottom = max(self.bottom, coordinates[1])
        print(f"Inserted elf at ({coordinates}), LR, TB = {self.left}, {self.right}, {self.top}, {self.bottom}")

    def consume(self, line):
        for i, marker in enumerate(line):
            if marker == "#":
                self.place_elf((i, self.lines_consumed))
        self.lines_consumed += 1


    def render(self):
        for j in range(self.top, self.bottom + 1):
            for i in range(self.left, self.right + 1):
                if ((i, j) in self.elves):
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def test_part_demo():
    print("Part DEMO")
    print("BEGIN")
    f = Field()
    with open("Day23/Day23DemoData.txt", "r") as datafile:
        for line in datafile:
            f.consume(line.strip())

    f.render()
