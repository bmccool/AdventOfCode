""" Advent of Code 2023 Day 12 """
from typing import List, Tuple
from functools import lru_cache
import re
from pymccool.math import Point

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day13/'



class RockPattern:
    """ An observation of rock and ash patterns """
    def __init__(self):
        self.rocks: List[Point] = []
        self.ash: List[Point] = []
        self.max: Point = Point(-1, -1)

    def parse_line(self, line: str):
        """ Parse a line of the input file """
        line = line.strip()
        logger.info(line)
        self.max = Point(max(self.max.x, len(line)), self.max.y + 1)
        for i, char in enumerate(line):
            if char == '#':
                self.rocks.append(Point(i, self.max.y))
            elif char == '.':
                self.ash.append(Point(i, self.max.y))

    def get_point(self, point: Point) -> str:
        """ Get the character at a point """
        if point in self.rocks:
            return 'rock'
        elif point in self.ash:
            return 'ash'
        raise ValueError(f"Point {point} not found in rocks or ash")

    def is_horizontal_reflection(self, before_column: int) -> bool:
        """ Check if this pattern is a horizontal reflection of another """
        for row in range(self.max.y):
            for i, col in enumerate(range(before_column, self.max.x)):
                p1 = Point(col - (i * 2) - 1, row)
                if p1.x < 0:
                    break
                p2 = Point(col, row)
                if (not (p1 in self.rocks and p2 in self.rocks)) and (
                    not (p1 in self.ash and p2 in self.ash)):
                    logger.info(f"Failed at {p1} and {p2}")
                    logger.info(f"{p1} is {self.get_point(p1)}")
                    logger.info(f"{p2} is {self.get_point(p2)}")
                    return False
        return True

    def get_horizontal_reflection(self) -> int:
        """
        Get the horizontal reflections of this pattern 
        Assume only one line of reflection
        """
        
        return [self]

class PatternEater:
    """ Class to parse multiple rock patterns from a file input """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.patterns: List[RockPattern] = []
        self.parse_data()

    def parse_data(self):
        """ Read the input data and fill the data dict """
        self.patterns.append(RockPattern())
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.strip() == "":
                    self.patterns.append(RockPattern())
                else:
                    self.patterns[-1].parse_line(line.strip())


def test_sanity():
    """Sanity check """
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input_sample.txt')
    logger.pretty(logger.INFO, pattern_eater.patterns)
    assert pattern_eater.patterns[0].is_horizontal_reflection(5)

def test_part_1():
    """Test part 1"""
    logger.info("")

def test_sample_2():
    """Test part 2"""
    logger.info("")

def test_part_2():
    """Test part 2"""
    logger.info("")
