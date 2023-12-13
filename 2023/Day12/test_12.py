""" Advent of Code 2023 Day 12 """
from typing import List, Tuple
from functools import lru_cache
import re

from pymccool.logging import Logger, LoggerKwargs

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
        self.map = self.map[:-1]
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

    @lru_cache
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

    def get_hashable_maps(self) -> Tuple[str, ...]:
        """ Get the hashable maps """
        return tuple(elem for elem in self.map.split(".") if elem)
    
    def get_hashable_nums(self) -> Tuple[int, ...]:
        """ Get the hashable nums """
        return tuple(int(elem) for elem in self.broken_record.split(",") if elem)
    
    @lru_cache
    def count_ways_fast(self, spring_map: Tuple[str, ...], sizes: Tuple[int, ...]) -> int:
        """ Use memoization (lru_cache) and a few tricks to speed up the counting """
        # If there are no broken springs according to the "broken_record",
        # then we can only count this as 1 there are no broken springs in the map
        if not sizes:
            return 1 if all(spring.replace("?", "") == "" for spring in spring_map) else 0
        # If there is no spring map left, then we cant count any more
        if not spring_map:
            return 0

        first_spring = spring_map[0]
        # Check if there are any broken springs in the first group of springs
        if not first_spring:
            # If there's nothing in the first group (TODO is this possible?) then we can just skip it
            return self.count_ways_fast(spring_map[1:], sizes)

        # if the first spring in the group is broken, we can't change it.
        # Account for it and reapply the function with the subset which skips it.
        if first_spring[0] == "#":
            if is_possible(first_spring, sizes[0]):
                return self.count_ways_fast((first_spring[sizes[0] + 1 :],) + spring_map[1:], sizes[1:])
            else:
                return 0
        
        # The first character is a ?, reapply the function twice, once assuming it's empty and once assuming it's broken
        res_when_empty = self.count_ways_fast((first_spring[1:],) + spring_map[1:], sizes)
        res_when_broken = self.count_ways_fast((f"#{first_spring[1:]}",) + spring_map[1:], sizes)
        return res_when_empty + res_when_broken


@lru_cache
def is_possible(spring: str, size: int) -> bool:
    pattern = r"^[#|\?]{" + str(size) + "}" + r"(\?|$)"
    return re.match(pattern, spring) is not None



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

def test_count_ways_folded():
    logger.info("")
    record = Record(".??..??...?##. 1,1,3")
    record.unfold()
    assert record.count_ways_fast(record.get_hashable_maps(), record.get_hashable_nums()) == 16384


def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    with open(WORKING_DIR + "input_sample.txt", "r", encoding="utf-8") as file:
        records = [Record(line) for line in file.readlines()]
        answer = 0
        for record in records:
            c = record.count_ways_fast(record.get_hashable_maps(), record.get_hashable_nums())
            answer += c
    logger.info(f"Answer: {answer}")
    assert answer == 21

def test_part_1():
    """Test part 1"""
    logger.info("")
    with open(WORKING_DIR + "input.txt", "r", encoding="utf-8") as file:
        records = [Record(line) for line in file.readlines()]
        answer = 0
        for record in records:
            c = record.count_ways_fast(record.get_hashable_maps(), record.get_hashable_nums())
            answer += c
    logger.info(f"Answer: {answer}")
    assert answer == 7350

def test_sample_2():
    """Test part 2"""
    logger.info("")
    with open(WORKING_DIR + "input_sample.txt", "r", encoding="utf-8") as file:
        records = [Record(line) for line in file.readlines()]
        answer = 0
        for record in records:
            record.unfold()
            c = record.count_ways_fast(record.get_hashable_maps(), record.get_hashable_nums())
            logger.info(f"{record.map} {record.broken_record} {c}")
            answer += c
    logger.info(f"Answer: {answer}")

def test_part_2():
    """Test part 2"""
    logger.info("")
    with open(WORKING_DIR + "input.txt", "r", encoding="utf-8") as file:
        records = [Record(line) for line in file.readlines()]
        answer = 0
        for record in records:
            record.unfold()
            c = record.count_ways_fast(record.get_hashable_maps(), record.get_hashable_nums())
            answer += c
    logger.info(f"Answer: {answer}")
