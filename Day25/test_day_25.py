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
        #print(f"SNAFU({e}: {digit} at place {i}, with multiplier {multiplier}adding {number} to sum: {sum}")
        sum = sum + number
    return sum

def biggest_at_digit(digit: int) -> int:
    """ Return the biggest integer that can be represented with this many digits """
    number = 0
    while digit > 0:
        number = number + (pow(5, digit - 1) * 2)
        digit -= 1

    return number


def dec2snafu(number) -> str:
    snafu = ""
    represented = 0
    place = 1
    digits = 1
    while True:
        if biggest_at_digit(digits) >= number:
            break
        digits += 1

    
    for digit in range(digits, 0, -1):
        #Use the digit that brings us closest to the 
        best = None
        best_abs = None
        for multiplier in [1, 2, 0, -1, -2]:
            this_abs = abs(((multiplier * pow(5, digit - 1)) + represented) - number)
            #print(f"for digit {digit} and multiplier {multiplier}, this_abs = {this_abs}, best is {best_abs}")
            if (best is None) or (this_abs < best_abs):
                best = multiplier
                best_abs = this_abs

        match best:
            case -2:
                sigit = "="
            case -1:
                sigit = "-"
            case 0:
                sigit = "0"
            case 1:
                sigit = "1"
            case 2:
                sigit = "2"

        #print(f"Chose {sigit}")
        snafu = snafu + sigit
        represented = represented + (best * pow(5, digit - 1))
    return snafu



def test_biggest_at_digit():
    sum  = 0
    assert biggest_at_digit(0) == sum
    sum += 2
    assert biggest_at_digit(1) == sum
    sum += 10
    assert biggest_at_digit(2) == sum
    sum += 50
    assert biggest_at_digit(3) == sum
    sum += 250 
    assert biggest_at_digit(4) == sum
    sum += 1250
    assert biggest_at_digit(5) == sum
    sum += 6250
    assert biggest_at_digit(6) == sum

def test_dec2snafu():
    print("TEST SNAFU")
    assert dec2snafu(0) == "0"
    assert dec2snafu(1) == "1"
    assert dec2snafu(2) == "2"
    assert dec2snafu(3) == "1="
    assert dec2snafu(4) == "1-" 
    assert dec2snafu(15) == "1=0"
    assert dec2snafu(314159265) == "1121-1110-1=0"
    

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
    assert sum == 4890
    assert dec2snafu(sum) == "2=-1=0"

def test_part_1():
    print("Part 1")
    print("BEGIN")
    with open("Day25/Day25Data.txt", "r") as datafile:
        sum = 0
        for line in datafile:
            sum = sum + sanfu2dec(line.strip())
            #f.consume(line.strip())

    print(sum)
    assert sum == 36966761092496
    print(dec2snafu(sum))
    assert dec2snafu(sum) == "20=212=1-12=200=00-1"