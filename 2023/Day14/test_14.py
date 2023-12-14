""" Advent of Code 2023 Day 12 """
from typing import List, Tuple, Dict
from sortedcontainers import SortedSet
from functools import lru_cache
import re
from pymccool.math import Point

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day14/'

class HashableSortedSet(SortedSet):
    def __hash__(self):
        return hash(str(self))

class RockPattern:
    """ An observation of rock and ash patterns """
    def __init__(self):
        self.round_rocks: HashableSortedSet[Point] = HashableSortedSet()
        self.cube_rocks: HashableSortedSet[Point] = HashableSortedSet()
        self.max: Point = Point(-1, -1)
        self.map_str: str = ""



    def __hash__(self):
        """ Hash the pattern """
        return hash(self.map_str)

    def parse_line(self, line: str):
        """ Parse a line of the input file """
        line = line.strip()
        self.max = Point(max(self.max.x, len(line)), self.max.y + 1)
        for i, char in enumerate(line):
            if char == 'O':
                self.round_rocks.add(Point(i, self.max.y))
            elif char == '#':
                self.cube_rocks.add(Point(i, self.max.y))

    def get_point(self, point: Point) -> str:
        """ Get the character at a point """
        if point in self.round_rocks:
            return 'O'
        if point in self.cube_rocks:
            return '#'
        return '.'
    
    @staticmethod
    def sort_string(sort_string: str, reverse=False) -> str:
        """ Sort a string """
        parts = []
        index = 0
        for cube_rock_chunk in re.finditer(r"#+", sort_string):
            parts.append(sort_string[index:cube_rock_chunk.span()[0]])
            parts.append(cube_rock_chunk[0])
            index = cube_rock_chunk.span()[1]
        if index < len(sort_string):
            parts.append(sort_string[index:])

        assert len(sort_string) == len("".join(parts))
        ret_val = ""
        for part in parts:
            ret_val += "".join(sorted(part, reverse=reverse))
        return ret_val
    
    @lru_cache
    def tilt_north(self, round_rocks: SortedSet[Point], cube_rocks: SortedSet[Point]):
        """ Tilt the pattern north """
        for column in range(self.max.x):
            column_str: str = ""
            for row in range(self.max.y + 1):
                column_str += self.get_point(Point(column, row))
            column_str = self.sort_string(column_str, reverse=True)

            # This column should match column string.  Pop everything out of this column, and readd as per column_str
            for row in range(self.max.y + 1):
                if column_str[row] == self.get_point(Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not column_str[row] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not column_str[row] == '#':
                            cube_rocks.remove(Point(column, row))
                    if column_str[row] == 'O':
                        round_rocks.add(Point(column, row))
                    elif column_str[row] == '#':
                        cube_rocks.add(Point(column, row))

    @lru_cache
    def tilt_south(self, round_rocks: SortedSet[Point], cube_rocks: SortedSet[Point]):
        """ Tilt the pattern south """
        for column in range(self.max.x):
            column_str: str = ""
            for row in range(self.max.y + 1):
                column_str += self.get_point(Point(column, row))
            column_str = self.sort_string(column_str, reverse=False)

            # This column should match column string.  Pop everything out of this column, and readd as per column_str
            for row in range(self.max.y + 1):
                if column_str[row] == self.get_point(Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not column_str[row] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not column_str[row] == '#':
                            cube_rocks.remove(Point(column, row))
                    if column_str[row] == 'O':
                        round_rocks.add(Point(column, row))
                    elif column_str[row] == '#':
                        cube_rocks.add(Point(column, row))

    @lru_cache
    def tilt_west(self, round_rocks: SortedSet[Point], cube_rocks: SortedSet[Point]):
        """ Tilt the pattern west """
        for row in range(self.max.y + 1):
            row_str: str = ""
            for column in range(self.max.x):
                row_str += self.get_point(Point(column, row))
            row_str = self.sort_string(row_str, reverse=True)

            # This row should match row string.  Pop everything out of this row, and readd as per row_str
            for column in range(self.max.x):
                if row_str[column] == self.get_point(Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not row_str[column] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not row_str[column] == '#':
                            cube_rocks.remove(Point(column, row))
                    if row_str[column] == 'O':
                        round_rocks.add(Point(column, row))
                    elif row_str[column] == '#':
                        cube_rocks.add(Point(column, row))
    @lru_cache
    def tilt_east(self, round_rocks: SortedSet[Point], cube_rocks: SortedSet[Point]):
        """ Tilt the pattern east """
        for row in range(self.max.y + 1):
            row_str: str = ""
            for column in range(self.max.x):
                row_str += self.get_point(Point(column, row))
            row_str = self.sort_string(row_str, reverse=False)

            # This row should match row string.  Pop everything out of this row, and readd as per row_str
            for column in range(self.max.x):
                if row_str[column] == self.get_point(Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not row_str[column] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not row_str[column] == '#':
                            cube_rocks.remove(Point(column, row))
                    if row_str[column] == 'O':
                        round_rocks.add(Point(column, row))
                    elif row_str[column] == '#':
                        cube_rocks.add(Point(column, row))



    def render(self):
        logger.info("Rendering pattern")
        for row in range(self.max.y + 1):
            row_str: str = ""
            for col in range(self.max.x):
                point = Point(col, row)
                row_str += self.get_point(point)
            logger.info(row_str)

    def calculate_load(self) -> int:
        """ Calculate the load of this pattern """
        total_load = 0
        for rock in self.round_rocks:
            total_load += (self.max.y + 1 - rock.y)

        return total_load

    def cycle(self) -> None:
        """ Cycle the pattern """
        self.tilt_north(self.round_rocks, self.cube_rocks)
        self.tilt_west(self.round_rocks, self.cube_rocks)
        self.tilt_south(self.round_rocks, self.cube_rocks)
        self.tilt_east(self.round_rocks, self.cube_rocks)

class PatternEater:
    """ Class to parse multiple rock patterns from a file input """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.pattern: RockPattern = RockPattern()
        self.parse_data()

    def parse_data(self):
        """ Read the input data and fill the data dict """
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.pattern.parse_line(line.strip())


def test_sanity():
    """Sanity check """
    assert True

def test_sort_string():
    logger.info("")
    assert RockPattern.sort_string("OO.O.O..##", reverse=True) == "OOOO....##"
    assert RockPattern.sort_string("O..O.#O.O", reverse=True) == "OO...#OO."
    assert RockPattern.sort_string("O..O.###O.O", reverse=True) == "OO...###OO."
    

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input_sample.txt')
    pattern_eater.pattern.render()
    pattern_eater.pattern.tilt_north(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    pattern_eater.pattern.render()
    load = pattern_eater.pattern.calculate_load()
    logger.info(f"Load is {load}")

def test_part_1():
    """Test part 1"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input.txt')
    #pattern_eater.pattern.render()
    pattern_eater.pattern.tilt_north(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    #pattern_eater.pattern.render()
    load = pattern_eater.pattern.calculate_load()
    logger.info(f"Load is {load}")
    assert load == 108_955


def test_profile_this():
    """Test part 2"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input_sample.txt')
    pattern_eater.pattern.render()
    #logger.info("Tilting North")
    #pattern_eater.pattern.tilt_north(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    #pattern_eater.pattern.render()
    #logger.info("Tilting West")
    #pattern_eater.pattern.tilt_west(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    #pattern_eater.pattern.render()
    #logger.info("Tilting South")
    #pattern_eater.pattern.tilt_south(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    #pattern_eater.pattern.render()
    #logger.info("Tilting East")
    #pattern_eater.pattern.tilt_east(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks)
    #pattern_eater.pattern.render()
    for _ in range(1_000_000_000):
        pattern_eater.pattern.cycle()
        #pattern_eater.pattern.render()
        if _ % 10_000 == 0:
            logger.info(f"Cycle: {_}.  {100 * _ / 1_000_000_000:2}% done")

    load = pattern_eater.pattern.calculate_load()
    logger.info(f"Load is {load}")

def test_part_2():
    """Test part 2"""
    logger.info("")
