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

def snafuint(snafu_digit: str) -> int:
    match snafu_digit:
        case "0":
            return 0
        case "1":
            return 1
        case "2":
            return 2
        case "-":
            return -1
        case "=":
            return -2
        case _:
            print(f"Don't know what digit that is! {snafu_digit}")
    return False

def sanfu2dec(snafu: str) -> int:

    reversed = (list(snafu))
    reversed.reverse()

    sum = 0
    for i, e in enumerate(reversed):
        digit = (snafuint(e))
        multiplier = pow(5, i)
        number = digit * multiplier
        print(f"SNAFU({e}: {digit} at place {i}, with multiplier {multiplier}adding {number} to sum: {sum}")
        sum = sum + number
    return sum

def dec2snafu(int) -> str:
    represented = 0
    place = 1


def test_dec2snafu():
    print("TEST SNAFU")
    assert dec2snafu(1) == "1"
    assert dec2snafu(2) == "2"
    assert dec2snafu(3) == "1="
    assert dec2snafu(4) == "1-" 
    

def test_sanfu2dec():
    print("TEST SNAFU")
    assert sanfu2dec("1") == 1
    assert sanfu2dec("2") == 2
    assert sanfu2dec("1=") == 3
    assert sanfu2dec("1-") == 4
    assert sanfu2dec("10") == 5
    assert sanfu2dec("11") == 6
    assert sanfu2dec("12") == 7
    assert sanfu2dec("2=") == 8
    assert sanfu2dec("2-") == 9
    assert sanfu2dec("20") == 10
    assert sanfu2dec("1=0") == 15
    assert sanfu2dec("1-0") == 20
    assert sanfu2dec("1=11-2") == 2022
    assert sanfu2dec("1-0---0") == 12345
    assert sanfu2dec("1121-1110-1=0") == 314159265


def test_part_demo():
    print("Part DEMO")
    print("BEGIN")
    with open("Day25/Day25DemoData.txt", "r") as datafile:
        sum = 0
        for line in datafile:
            sum = sum + sanfu2dec(line.strip())
            #f.consume(line.strip())

    print(sum)