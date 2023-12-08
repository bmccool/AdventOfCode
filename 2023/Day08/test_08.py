""" Advent of Code 2023 Day 05 """
from typing import Dict
from dataclasses import dataclass
from math import lcm

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day08/'

@dataclass
class Fork:
    """ Choice Class represents a fork in the desert, with a left and right path """
    location: str
    left: str
    right: str

    def __str__(self) -> str:
        return f"{self.location} -> ({self.left}, {self.right})"

@dataclass
class LoopPoint:
    """ Loop Point Class """
    location: Fork
    steps: int
    direction_index: int

@dataclass
class Ghost:
    """ Ghost Class """
    location: str
    steps: int

    def __str__(self) -> str:
        return f"{self.location}, {self.steps}"

class DesertGuidanceSystem:
    """ Desert Guidance System """
    def __init__(self, filename: str):
        self.filename = filename
        self.desert: Dict[str, Fork] = {}
        self.parse()

    def parse(self) -> None:
        """ Parse the input file """
        with open(self.filename, 'r', encoding="utf-8") as file:
            for line in file:
                if ("=" not in line) and ("L" in line or "R" in line):
                    # Line is the directions
                    self.directions = line.strip()
                if "=" in line:
                    # Line is a desert location/choice
                    location = line.split("=")[0].strip()
                    left = line.split("=")[1].split(",")[0].split('(')[1].strip()
                    right = line.split("=")[1].split(",")[1].split(')')[0].strip()
                    self.desert[location] = Fork(location=location, left=left, right=right)

    def walk(self) -> int:
        """ Walk the desert and return number of steps taken"""
        current_location: str = "AAA"
        direction_index = 0
        steps_taken = 0
        while current_location != "ZZZ":
            if self.directions[direction_index] == "L":
                current_location = self.desert[current_location].left
            else:
                current_location = self.desert[current_location].right

            direction_index += 1
            steps_taken += 1
            direction_index = direction_index % len(self.directions)

        return steps_taken

    def haunt(self) -> int:
        """ Haunt the desert and return number of steps taken """
        # Ghosts start at all locations ending with A
        ghosts = [Ghost(location=location.location, steps=0)
                  for location in self.desert.values()
                  if location.location[-1] == "A"]

        for ghost in ghosts:
            ghost.steps = self.find_loop(starting_location=ghost.location)
            logger.info(f"Ghost: {ghost}")

        meeting_steps = lcm(*[ghost.steps for ghost in ghosts])
        logger.info(f"Meeting Steps: {meeting_steps}")
        return meeting_steps

    def find_loop(self, starting_location: str) -> int:
        """ 
        Find the loop for a given starting location
        Return -1 if dead end "ZZZ" found
        """
        current_location: str = starting_location
        direction_index = 0
        steps_taken = 0
        potential_loop_point: LoopPoint = None
        while True:
            if self.directions[direction_index] == "L":
                current_location = self.desert[current_location].left
            else:
                current_location = self.desert[current_location].right

            direction_index += 1
            steps_taken += 1
            direction_index = direction_index % len(self.directions)

            if current_location[-1] == "Z":
                if potential_loop_point:
                    if potential_loop_point.location == self.desert[current_location]:
                        return potential_loop_point.steps
                potential_loop_point = LoopPoint(location=self.desert[current_location],
                                                 steps=steps_taken,
                                                 direction_index=direction_index)

def test_sanity():
    """Sanity check """
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    cgs = DesertGuidanceSystem(WORKING_DIR + 'input_sample.txt')
    steps = cgs.walk()
    assert steps == 6

def test_part_1():
    """Test part 1"""
    logger.info("")
    cgs = DesertGuidanceSystem(WORKING_DIR + 'input.txt')
    steps = cgs.walk()
    logger.info(f"Answer: {steps}")
    assert steps == 13301

def test_sample_2():
    """Test part 2"""
    logger.info("")
    dgs = DesertGuidanceSystem(WORKING_DIR + 'input_sample2.txt')
    steps = dgs.haunt()
    logger.info(f"Answer: {steps}")

def test_part_2():
    """Test part 2"""
    logger.info("")
    dgs = DesertGuidanceSystem(WORKING_DIR + 'input.txt')
    steps = dgs.haunt()
    logger.info(f"Answer: {steps}")
    # 155520416281
