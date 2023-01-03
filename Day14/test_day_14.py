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


class Pit:
    def __init__(self):
        self.objects = dict()
        self.x_min = 500
        self.x_max = 500
        self.y_min = 0
        self.y_max = 0
        self.floor = 2
        self.insert((500, 0), "+")

    def in_bounds(self, x, y) -> bool:
        if not self.x_min <= x <= self.x_max:
            return False
        if not self.y_min <= y <= self.y_max:
            return False
        return True

    def insert(self, coordinates, label: str) -> bool:
        if coordinates in self.objects:
            return False # Seat's Taken

        self.objects[coordinates] = label
        self.x_min = min(self.x_min, coordinates[0])
        self.x_max = max(self.x_max, coordinates[0])
        self.y_min = min(self.y_min, coordinates[1])
        self.y_max = max(self.y_max, coordinates[1])

        if label == "#":
            #print(f"Checking for Floor with {coordinates} and y.max == {self.y_max}")
            if coordinates[1] > (self.y_max - 2):
                self.y_max = coordinates[1] + 2
        return True

    def render(self):
        #print("RENDERING PIT")
        #print(f"X[{self.x_min} - {self.x_max}]\nY[{self.y_min} - {self.y_max}]")
        for y in range(self.y_min, self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                if (x,y) in self.objects:
                    print(self.objects[(x,y)], end="")
                else:
                    print('.', end='')
            print()

    def add_sand(self, x=500, y=0) -> bool:
        #print(f"Checking {x}, {y}")
        if not self.in_bounds(x,y):
            return False
        
        if not (x, y+1) in self.objects:
            return self.add_sand(x, y+1)
        elif not (x - 1, y + 1) in self.objects:
            return self.add_sand(x - 1, y + 1)
        elif not (x + 1, y + 1) in self.objects:
            return self.add_sand(x + 1, y + 1)

        print(f"Sand insertion at {x}, {y}")
        if not self.insert((x,y), 'o'):
            print("OY IT DIDNT FIT")
        return True


class Pit2(Pit):
    def in_bounds(self, x, y) -> bool:
        if not self.y_min <= y <= self.y_max:
            return False
        return True

    def add_sand(self, x=500, y=0) -> bool:
        self.update_floor()
        #print(f"Checking {x}, {y}")
        if not self.in_bounds(x,y):
            return False
        
        if not (x, y+1) in self.objects:
            return self.add_sand(x, y+1)
        elif not (x - 1, y + 1) in self.objects:
            return self.add_sand(x - 1, y + 1)
        elif not (x + 1, y + 1) in self.objects:
            return self.add_sand(x + 1, y + 1)

        #print(f"Sand insertion at {x}, {y}")
        if not self.insert((x,y), 'o'):
            print("OY IT DIDNT FIT")
            return False
        return True


    def update_floor(self):
        for x in range(self.x_min - 2, self.x_max + 1+ 2):
            if not (x,self.y_max) in self.objects:
                self.objects[(x,self.y_max)] = "#"
                


class Day14Tester:
    def __init__(self):
        self.pit = Pit()

    

    def consume(self, line: str):
        rock_verticies = line.split(' -> ')
        print(rock_verticies)
        for index in range(1, len(rock_verticies)):
            self.add_rocks(rock_verticies[index - 1], rock_verticies[index])

    def add_rock(self, x: int, y: int):
        self.pit.insert((x,y), "#")

    def add_rocks(self, rock_a: str, rock_b: str):
        print(f"Adding rocks {rock_a} {rock_b}")
        rock_a_x, rock_a_y= rock_a.split(',')
        rock_b_x, rock_b_y= rock_b.split(',')
        rock_a_x = int(rock_a_x)
        rock_a_y = int(rock_a_y)
        rock_b_x = int(rock_b_x)
        rock_b_y = int(rock_b_y)
        # Either Xs or Ys must be equal
        if rock_a_x == rock_b_x:
            while True:
                self.add_rock(rock_a_x, rock_a_y)
                rock_a_y += 1 if (rock_b_y > rock_a_y) else -1
                if rock_a_y == rock_b_y:
                    self.add_rock(rock_a_x, rock_a_y)
                    break
        elif rock_a_y == rock_b_y:
            while True:
                self.add_rock(rock_a_x, rock_a_y)
                rock_a_x += 1 if (rock_b_x > rock_a_x) else -1
                if rock_a_x == rock_b_x:
                    self.add_rock(rock_a_x, rock_a_y)
                    break
        else:
            print("ERROR, ROCKS NOT ALIGNED")

    def render(self):
        self.pit.render()

    def add_sand(self):
        return self.pit.add_sand()


class Day14Tester2(Day14Tester):
    def __init__(self):
        super().__init__()
        self.pit = Pit2()

#@pytest.mark.skip
def test_part_1():
    print("Part 1")
    print("BEGIN")
    day14 = Day14Tester()
    with open("Day14/Day14Data.txt", "r") as datafile:
        for line in datafile:
            day14.consume(line.strip())
    units = 0
    while day14.add_sand():
        #day14.render()
        units += 1
    print(units)
    day14.render()
    assert units == 961 # 961 units of sand dropped into this structure

@pytest.mark.skip(reason="Takes 45 seconds")
def test_part_2():
    print("Part 1")
    print("BEGIN")
    day14 = Day14Tester2()
    with open("Day14/Day14Data.txt", "r") as datafile:
        for line in datafile:
            day14.consume(line.strip())
    units = 1 # Adding extra one because we can't (don't) cover up the spout
    while day14.add_sand():
        #day14.render()
        units += 1
    print(units)
    day14.render()