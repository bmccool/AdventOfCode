""" Advent of Code 2023 Day 12 """
from itertools import combinations
from typing import Callable, List
import pytest

from pymccool.logging import Logger, LoggerKwargs
from pymccool.math import Point

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day12/'

class Record():
    """ A record of springs, damaged (#) and undamaged (.) """
    def __init__(self, record: str):
        self.record: str = record.strip()
        self.map = record.split()[0]
        self.broken_record = record.split()[1]

    def unfold(self):
        """ Unfold the record """
        self.map += "?"
        self.map *= 5
        self.broken_record = ((self.broken_record + ',') * 5).strip(',')
        self.record = self.map + " " + self.broken_record


    def get_unknowns(self) -> List[int]:
        """ Get the indices of the unknowns """
        return [i for i, char in enumerate(self.map) if char == '?']
        
    def matches(self, other: str, partial=False) -> bool:
        """ Check if a given string matches this record """
        # Check that the lengths match
        if (not partial) and (len(other) != len(self.map)):
            return False
        
        for i, char in enumerate(other):
            # Check that charcters match which were not unknown before
            if self.map[i] != '?' and self.map[i] != char:
                return False
            # Check that all characters are in [., #, ?]
            if char not in ['.', '#', '?']:
                return False
            
        if not partial:
            broken_strings = ",".join([str(len(block)) for block in other.split(".") if block])
            if broken_strings != self.broken_record:
                return False
        else:
            broken_strings = ",".join([str(len(block)) for block in other.split("?", maxsplit=1)[0].split(".") if block])
            if not self.broken_record.startswith(broken_strings):
                return False
        
        return True

    def count_ways(self) -> int:
        """ Count the number of ways to fill in the unknowns (faster) """

    def count_ways_slow(self, test_record: str = None) -> int:
        """ Count the number of ways to fill in the unknowns """

        test_record = test_record or ""
        
        # If the length is the same as the original map, we're done
        if len(test_record) == len(self.map):
            if self.matches(test_record):
                return 1
            else:
                return 0
        
        count = 0
        if self.map[len(test_record)] == '?':
            count += self.count_ways_slow(test_record + '.')
            count += self.count_ways_slow(test_record + '#')
        else:
            count += self.count_ways_slow(test_record + self.map[len(test_record)])

        return count

".??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##." "1,1,3,1,1,3,1,1,3,1,1,3,1,1,3"
def test_sanity():
    """Sanity check """
    assert True

def test_matches():
    """ test Record.matches """
    logger.info("")
    assert not Record("???.### 1,1,3").matches("...###") # Lenths don't match
    assert not Record("???.### 1,1,3").matches("....###") # Broken records don't match
    assert not Record("???.### 1,1,3").matches("....#.#") # Given characters don't match
    assert not Record("???.### 1,1,3").matches("..,.###") # Weird Character
    assert Record("???.### 1,1,3").matches("#.#.###")

def test_matches_partial():
    """ test Record.matches """
    logger.info("")
    assert Record("???.### 1,1,3").matches("#.", partial=True)
    assert Record("???.### 1,1,3").matches("#.#", partial=True)
    assert not Record("???.### 1,1,3").matches("##.", partial=True)


def test_count_ways():
    """Test count_ways """
    logger.info("")
    assert Record("???.### 1,1,3").count_ways_slow() == 1
    assert Record(".??..??...?##. 1,1,3").count_ways_slow() == 4
    assert Record("?###???????? 3,2,1").count_ways_slow() == 10

@pytest.mark.skip(reason="Too slow")
def test_count_ways_folded():
    logger.info("")
    record = Record(".??..??...?##. 1,1,3")
    record.unfold()
    assert record.count_ways_slow() == 16384


def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    with open(WORKING_DIR + "input_sample.txt", "r", encoding="utf-8") as file:
        answer = sum([Record(line).count_ways_slow() for line in file.readlines()])
    logger.info(f"Answer: {answer}")

def test_part_1():
    """Test part 1"""
    logger.info("")
    with open(WORKING_DIR + "input.txt", "r", encoding="utf-8") as file:
        answer = sum([Record(line).count_ways_slow() for line in file.readlines()])
    logger.info(f"Answer: {answer}")

def test_sample_2():
    """Test part 2"""
    logger.info("")

def test_part_2():
    """Test part 2"""
    logger.info("")
