""" Advent of Code 2023 Day 12 """
import pytest

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day15/'

def holiday_ascii_string_helper(s: str) -> int:
    """
    The HASH algorithm is a way to turn any string of characters into a single 
    number in the range 0 to 255. 
    To run the HASH algorithm on a string, start with a current value of 0. 
    Then, for each character in the string starting from the beginning:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    ret_val = 0
    for char in s:
        ret_val += ord(char)
        ret_val *= 17
        ret_val %= 256

    return ret_val


def test_sanity():
    """Sanity check """
    assert True

@pytest.mark.parametrize("input_str, expected", [
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
])
def test_hash(input_str, expected):
    """ Test the holiday_ascii_string_helper function """
    assert holiday_ascii_string_helper(input_str) == expected

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    with open(WORKING_DIR + "input_sample.txt", encoding="utf-8") as f:
        answer  = sum([holiday_ascii_string_helper(step) 
                       for line in f.readlines() 
                       for step in line.split(",")])
    logger.info(answer)
    assert answer == 1_320

def test_part_1():
    """Test part 1"""
    logger.info("")
    with open(WORKING_DIR + "input.txt", encoding="utf-8") as f:
        answer  = sum([holiday_ascii_string_helper(step)
                       for line in f.readlines()
                       for step in line.split(",")])
    logger.info(answer)
    assert answer == 517_965

def test_sample_2():
    """Test part 2"""
    logger.info("")

def test_part_2():
    """Test part 2"""
    logger.info("")
