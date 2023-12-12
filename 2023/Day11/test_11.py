""" Advent of Code 2023 Day 05 """
from itertools import combinations
from typing import Callable, List

from pymccool.logging import Logger, LoggerKwargs
from pymccool.math import Point

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day11/'

class Galaxy():
    """ A pipe, with a label and a point"""
    def __init__(self, number: int, point: Point):
        self.number: int = number
        self.point: Point = point

    def __str__(self):
        return f"({self.number} @ {self.point})"

    def __repr__(self):
        return self.__str__()


class Observation():
    """ Sketch of a 2D grid of pipes """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.galaxies: List[Galaxy] = []
        self.max: Point = Point(0, 0)
        self.parse_data()

    def parse_data(self):
        """ Read the input data and fill the data dict """
        with open(self.filename, 'r', encoding='utf-8') as f:
            for y, line in enumerate(f.readlines()):
                for x, char in enumerate(line.strip()):
                    if y > self.max.y:
                        self.max.y = y
                    if x > self.max.x:
                        self.max.x = x
                    if char == '#':
                        self.galaxies.append(Galaxy(len(self.galaxies) + 1, Point(x, y)))

    def render(self, log_func: Callable=logger.info):
        """ Render the sketch"""
        galaxy_dict = {galaxy.point: galaxy.number for galaxy in self.galaxies}
        for y in range(self.max.y + 1):
            row = ""
            for x in range(self.max.x + 1):
                row += str(galaxy_dict.get(Point(x, y), '.'))
            log_func(row)


    def expand_rows(self, expansion_size: int=2):
        """ For each row that has no galxies, add a second blank row."""
        # Algorithm ADDS rows, but problem statement REPLACES rows.  We already have 1 row.
        expansion_size = expansion_size - 1
        index = 0
        while True:
            if not any([galaxy.point.y == index for galaxy in self.galaxies]):
                logger.info(f"Expanding Galaxies at row {index}, max: {self.max.y}")
                for galaxy in self.galaxies:
                    if galaxy.point.y > index:
                        galaxy.point.y += expansion_size
                self.max.y += expansion_size
                index += expansion_size + 1
            else:
                index += 1
            if index > self.max.y:
                break

    def expand_columns(self, expansion_size: int=2):
        """ For each column that has no galxies, add a second blank column."""
        # Algorithm ADDS rows, but problem statement REPLACES cols.  We already have 1 cols.
        expansion_size = expansion_size - 1
        index = 0
        while True:
            if not any([galaxy.point.x == index for galaxy in self.galaxies]):
                logger.info(f"Expanding Galaxies at column {index}, max: {self.max.x}")
                for galaxy in self.galaxies:
                    if galaxy.point.x > index:
                        galaxy.point.x += expansion_size
                self.max.x += expansion_size
                index += expansion_size + 1
            else:
                index += 1
            if index > self.max.x:
                break

    def expand(self, expansion_size: int=2):
        """
        For each row that has no galxies, add a second blank row (or more).
        Likewise for columns
        """
        self.expand_rows(expansion_size=expansion_size)
        self.expand_columns(expansion_size=expansion_size)

    def get_sum_distances(self) -> int:
        """ Get all combinations of galaxies """
        total_distance = 0
        combos = list(map(list, combinations(set(self.galaxies), 2)))
        logger.info(len(combos))
        for combo in combos:
            total_distance += combo[0].point.manhatten(combo[1].point)
        return total_distance


def test_sanity():
    """Sanity check """
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    observation = Observation(WORKING_DIR + 'input_sample.txt')
    logger.pretty(logger.INFO, observation.galaxies)
    observation.render()
    observation.expand()
    observation.render()
    sum_distances = observation.get_sum_distances()
    logger.info(sum_distances)
    assert sum_distances == 374

def test_part_1():
    """Test part 1"""
    logger.info("")
    observation = Observation(WORKING_DIR + 'input.txt')
    observation.expand()
    sum_distances = observation.get_sum_distances()
    logger.info(sum_distances)
    assert sum_distances == 9639160

def test_sample_2():
    """Test part 2"""
    logger.info("")
    observation = Observation(WORKING_DIR + 'input_sample.txt')
    observation.expand(expansion_size=10)
    sum_distances = observation.get_sum_distances()
    logger.info(sum_distances)
    assert sum_distances == 1030

def test_part_2():
    """Test part 2"""
    logger.info("")
    observation = Observation(WORKING_DIR + 'input.txt')
    observation.expand(expansion_size=1_000_000)
    sum_distances = observation.get_sum_distances()
    logger.info(sum_distances)
    assert sum_distances == 752_936_133_304
