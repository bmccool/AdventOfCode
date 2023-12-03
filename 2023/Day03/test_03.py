""" Advent of Code 2023 Day 03 """
from dataclasses import dataclass
from typing import List, Dict, Self, Optional
import re

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023.03",
))

WORKING_DIR = '2023/Day03/'

@dataclass
class Point:
    """ A point on the grid """
    x: int
    y: int

    def is_close_to(self, other: Self) -> bool:
        """
        Is this point close to another point?
        Retruns True if the other point is within 1 (including diagonals) of this point
        """
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


@dataclass
class Symbol:
    """ A symbol on the schematic """
    symbol: str
    location: Point

    def __hash__(self) -> int:
        return int(str(self.location.x) + str(self.location.y))



@dataclass
class Number:
    """ A number on the schematic """
    number: int
    location: Point

    def get_part(self, symbols: List[Symbol]) -> Optional['Part']:
        """ Is this number a part? """
        # Check each digit in this number against each symbol with a y value within 1 of this number
        # TODO, lazy, not filtering the symbols by y value
        for x in range(self.location.x, self.location.x + len(str(self.number))):
            ref_point = Point(x, self.location.y)
            for symbol in symbols:
                if ref_point.is_close_to(symbol.location):
                    return Part(number=self, symbol=symbol)
        return None

@dataclass
class Part:
    """ Part of a schematic """
    number: Number
    symbol: Symbol


class Schematic:
    """ Class to eat schematics from a file """
    def __init__(self, filename):
        self.filename: str = filename
        self.numbers: List[Number] = []
        self.symbols: List[Symbol] = []
        self.parts: List[Part] = []

    def eat(self):
        """ Run through the file and eat all the schematics """
        line_number = 0
        with open(self.filename, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                self.numbers += [Number(int(m.group()), Point(m.start(), line_number))
                                 for m in re.finditer(r'(\d+)', line)]
                chars = re.escape(",/;'[]\)<>?:\"\{\}|`~!@#$%^&*()_+-=")
                self.symbols += [Symbol(m.group(), Point(m.start(), line_number))
                                 for m in re.finditer(f'([{chars}])', line)]
                line_number += 1

    def get_parts(self):
        """ Get the parts of the schematic """
        logger.debug(f"Getting parts for {len(self.numbers)} numbers")
        for number in self.numbers:
            part = number.get_part(self.symbols)
            if part:
                self.parts.append(part)


    def sum_parts(self):
        """ Sum the parts """
        ret_val = 0
        for part in self.parts:
            ret_val += part.number.number
        return ret_val

    def find_gears(self) -> int:
        """
        Find the gears
        A gear is any * symbol that is adjacent to exactly two part numbers. 
        Its gear ratio is the result of multiplying those two numbers together.
        Return the sum of all gear ratios.
        """
        # First build a dict of all the symbols == "*" mapping each symbol to its parts
        symbol_parts: Dict[Symbol, List[Part]] = {}
        for part in self.parts:
            if part.symbol.symbol != "*":
                continue
            if part.symbol not in symbol_parts:
                symbol_parts[part.symbol] = []
            symbol_parts[part.symbol].append(part)

        # Remove symbols which do not have exactly two parts
        gears: Dict[Symbol, List[Part]] = {symbol: parts for symbol, parts in
                                           symbol_parts.items() if len(parts) == 2}

        logger.pretty(logger.DEBUG, gears)

        # Now calculate the gear ratios
        ret_val = 0
        for symbol, parts in gears.items():
            ret_val += parts[0].number.number * parts[1].number.number
        return ret_val


def test_sanity():
    """Sanity check """
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("Test Sample 1")
    s = Schematic(WORKING_DIR + "input_sample.txt")
    s.eat()
    s.get_parts()
    logger.pretty(logger.DEBUG, s.parts)
    logger.info(f"Sum of parts: {s.sum_parts()}")
    assert s.sum_parts() == 4361

def test_part_1():
    """Test part 1"""
    logger.info("Part 1")
    s = Schematic(WORKING_DIR + "input.txt")
    s.eat()
    s.get_parts()
    logger.pretty(logger.DEBUG, s.parts)
    logger.info(f"Sum of parts: {s.sum_parts()}")

def test_sample_2():
    """Test part 2"""
    logger.info("Test Sample 2")
    s = Schematic(WORKING_DIR + "input_sample.txt")
    s.eat()
    s.get_parts()
    logger.pretty(logger.DEBUG, s.parts)
    ratios = s.find_gears()
    logger.info(f"Sum of ratios: {ratios}")
    assert ratios == 467835

def test_part_2():
    """Test part 2"""
    logger.info("Part 2")
    s = Schematic(WORKING_DIR + "input.txt")
    s.eat()
    s.get_parts()
    logger.pretty(logger.DEBUG, s.parts)
    ratios = s.find_gears()
    logger.info(f"Sum of ratios: {ratios}")
    assert ratios == 81997870
