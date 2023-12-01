""" Advent of Code 2023 Day 01 """
from dataclasses import dataclass
from typing import List
from rich import print # pylint: disable=redefined-builtin

WORKING_DIR = '2023/Day01/'

@dataclass
class Calibration:
    """ Calibration value and the position found in the line """
    value: int
    position: int

class CalibrationEater:
    """ Class to eat calibrations from a file """
    def __init__(self, filename):
        self.filename = filename

    def get_calibration_sum(self):
        """ Find all calibrations in the file and return the sum with part 1 rules. """
        calibration_sum = 0
        with open(self.filename, 'r', encoding="utf-8") as f:
            calibration_sum = \
                sum([int(self.get_calibration_from_line(line)) for line in f.readlines()])
        return calibration_sum

    def get_calibration_sum_2(self):
        """ Find all calibrations in the file and return the sum with part 1 rules. """
        calibration_sum = 0
        with open(self.filename, 'r', encoding="utf-8") as f:
            calibration_sum = \
                sum([int(self.get_calibration_from_line_2(line)) for line in f.readlines()])
        return calibration_sum

    def get_calibration_from_line(self, line: str) -> int:
        """
        Find the calibration in the line with Part1 rules.
        Use the first and last digits found concatenated as the calibration.
        Ignore written numbers.
        """
        digit_string = '0123456789'
        calibration = []
        for char in line:
            if char in digit_string:
                calibration.append(char)

        # Combine first and last digit
        first = calibration[0]
        last = calibration[-1]

        return int(''.join([first, last]))

    def get_calibration_from_line_2(self, line: str) -> int:
        """
        Find the calibration in the line with Part2 rules.
        Use the first and last digits found concatenated as the calibration.
        Consider written numbers.
        """
        line = line.lower()
        digit_list = ["0","1", "2", "3", "4", "5", "6", "7", "8", "9",
                  "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        found: List[Calibration] = []
        for digit in digit_list:
            start_index = 0
            while True:
                if line.find(digit, start_index) == -1:
                    break
                value = digit_list.index(digit)
                index = line.find(digit, start_index)
                if value > 9:
                    value = value - 10
                found.append(Calibration(value, index))
                start_index = line.find(digit, start_index) + 1

        found.sort(key=lambda x: x.position)
        return int(''.join([str(found[0].value), str(found[-1].value)]))

def test_sanity():
    """Sanity check """
    assert True

def test_get_calibration_from_line():
    """Test get_calibration_from_line"""
    ce = CalibrationEater('dummy.txt')
    assert ce.get_calibration_from_line('1abc2') == 12
    assert ce.get_calibration_from_line('pqr3stu8vwx') == 38
    assert ce.get_calibration_from_line('a1b2c3d4e5f') == 15
    assert ce.get_calibration_from_line('treb7uchet') == 77

def test_sample():
    """Test sample data"""
    ce = CalibrationEater(WORKING_DIR + 'input_sample.txt')
    assert ce.get_calibration_sum() == 142

def test_part_1():
    """Test part 1"""
    ce = CalibrationEater(WORKING_DIR + 'input.txt')
    answer = ce.get_calibration_sum()
    print(answer)
    assert answer == 55130

def test_sample_2():
    """Test part 2"""
    ce = CalibrationEater(WORKING_DIR + 'input_sample_2.txt')
    assert ce.get_calibration_sum_2() == 281

def test_part_2():
    """Test part 2"""
    ce = CalibrationEater(WORKING_DIR + 'input.txt')
    answer = ce.get_calibration_sum_2()
    print(answer)
    assert answer == 54985
