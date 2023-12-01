from __future__ import annotations
from collections import deque
from typing import List, Callable
import random
import pytest
import math
import copy

import functools
from functools import partial
from typing import Any, Callable
from opentelemetry.trace import Tracer

from pymccool.logging import Logger, LoggerKwargs
from pymccool.tracing import get_tracer, get_decorator
from uuid import uuid1
uuid = uuid1()
logger = Logger(LoggerKwargs(
    app_name="Day23",
    grafana_loki_endpoint="https://loki.capricorn.brendonmccool.com/loki/api/v1/push",
    uuid=uuid
    #500 "POST /loki/api/v1/push HTTP/1.1" 85 "-" "GrafanaAgent/" "-"
    #401 "POST /loki/api/v1/push HTTP/1.1" 10 "-" "python-requests/2.28.2" "192.168.8.113"
))

tracer = get_tracer(service_name="Day23",
                    endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                    uuid=uuid)

instrument = get_decorator(tracer)
        


class Field:
    @instrument
    def __init__(self):
        # Smallest containing rectangle
        self.left = None
        self.right = None

        self.top = None
        self.bottom = None

        self.lines_consumed = 0

        self.elves = set()

        self.compass = ["N", "S", "W", "E"]

    @instrument
    def round(self):
        # Get proposed moves for each elf and add it to a dictionary
        # the key is the coordinate destination and the value is the list of coordinate sources
        # (if multiple elves want the same spot)
        logger.info("High from ROUND")
        proposed_moves = {}
        elves_moved = 0
        for elf in self.elves:
            move = False
            proposed_coordinates = None
            proposed_direction = None
            x, y = elf
            for direction in self.compass:
                match(direction):
                    case "N":
                        if(((x-1, y-1) not in self.elves) and \
                           ((x,   y-1) not in self.elves) and \
                           ((x+1, y-1) not in self.elves)):
                           if not proposed_coordinates:
                                proposed_coordinates = (x, y-1)
                                proposed_direction = "N"
                        else:
                            move = True
                    case "E":
                        if(((x+1, y-1) not in self.elves) and \
                           ((x+1, y)   not in self.elves) and \
                           ((x+1, y+1) not in self.elves)):
                           if not proposed_coordinates:
                                proposed_coordinates = (x+1, y)
                                proposed_direction = "E"
                        else:
                            move = True
                    case "S":
                        if(((x-1, y+1) not in self.elves) and \
                           ((x,   y+1) not in self.elves) and \
                           ((x+1, y+1) not in self.elves)):
                           if not proposed_coordinates:
                                proposed_coordinates = (x, y+1)
                                proposed_direction = "S"
                        else:
                            move = True
                    case "W":
                        if(((x-1, y-1) not in self.elves) and \
                           ((x-1, y)   not in self.elves) and \
                           ((x-1, y+1) not in self.elves)):
                           if not proposed_coordinates:
                                proposed_coordinates = (x-1, y)
                                proposed_direction = "W"
                        else:
                            move = True
                    case _:
                        logger.info("SOMETHING WENT WRONG, THIS DIRECTION ISNT ON THE COMPASS")

            #self.show_point(elf, proposed_direction, move)
            if move and proposed_coordinates:
                try:
                    proposed_moves[(proposed_coordinates)].append(elf)
                except KeyError:
                    proposed_moves[(proposed_coordinates)] = [elf]

        # Iterate throught the proposed move list, and execute any moves that only want done
        # by one elf
        while len(proposed_moves) > 0:
            move = proposed_moves.popitem()
            if len(move[1]) == 1:
                #DO MOVE
                #logger.info(f"Moving from ({move[1][0]}) -> ({move[0]})")
                #self.show_point(move[1][0])
                self.elves.remove(move[1][0])
                self.place_elf(move[0])
                elves_moved += 1
            else:
                continue
                logger.info(f"Too many elves wanted to move to {move[0]}. ===== {move[1]}")

        # Update thd compass
        self.compass.append(self.compass.pop(0))
        return elves_moved
    
    @instrument
    def show_point(self, coordinates, direction=None, move=None):
        
        logger.info("SHOW POINT")
        x, y = coordinates
        line_no = 0
        line_to_print = ""
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i, j) in self.elves:
                    line_to_print += "#"
                else:
                    line_to_print += "."
            if (line_no == 0):
                line_to_print += f"   Compass = {self.compass}"
            elif (line_no == 1):
                line_to_print += f"   Move?: {move}"
            else:
                line_to_print += f"   Direction: {direction}"
            logger.info(line_to_print)
            line_no += 1

    #@tracer.start_as_current_span("Place Elf")
    def place_elf(self, coordinates):
        # Deal with first input
        if self.bottom == None:
            self.left = coordinates[0]
            self.right = coordinates[0]
            self.top = coordinates[0]
            self.bottom = coordinates[0]

        if coordinates in self.elves:
            logger.info("THIS SEATS TAKEN!")

        self.elves.add(coordinates)
        self.left = min(self.left, coordinates[0])
        self.right = max(self.right, coordinates[0])
        self.top = min(self.top, coordinates[1])
        self.bottom = max(self.bottom, coordinates[1])
        #logger.info(f"Inserted elf at ({coordinates}), LR, TB = {self.left}, {self.right}, {self.top}, {self.bottom}")

    #@tracer.start_as_current_span("Consume Line")
    def consume(self, line):
        for i, marker in enumerate(line):
            if marker == "#":
                self.place_elf((i, self.lines_consumed))
        self.lines_consumed += 1


    @instrument
    def render(self):
        for j in range(self.top, self.bottom + 1):
            for i in range(self.left, self.right + 1):
                if ((i, j) in self.elves):
                    logger.info("#", end="")
                else:
                    logger.info(".", end="")
            logger.info()

    @instrument
    def recalculate(self):
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        for elf in self.elves:
            if not self.top:
                self.top = elf[1]
            if not self.bottom:
                self.bottom = elf[1]
            if not self.left:
                self.left = elf[0]
            if not self.right:
                self.right = elf[0]
            self.top = min(self.top, elf[1])
            self.bottom = max(self.bottom, elf[1])
            self.left = min(self.left, elf[0])
            self.right = max(self.right, elf[0])

    @instrument
    def get_empty_spots(self):
        spots = 0
        for j in range(self.top, self.bottom + 1):
            for i in range(self.left, self.right + 1):
                if ((i, j) not in self.elves):
                    spots += 1
        return spots


@instrument
def test_part_demo():
    logger.info("Part DEMO")
    logger.info("BEGIN")
    f = Field()
    with open("Day23/Day23DemoData.txt", "r") as datafile:
        for line in datafile:
            f.consume(line.strip())

    f.render()
    for _ in range(10):
        logger.info(f.elves)
        f.round()
        f.render()

@instrument
def test_part_demo_2():
    logger.info("Part DEMO 2")
    logger.info("BEGIN")
    f = Field()
    with open("Day23/Day23DemoData2.txt", "r") as datafile:
        for line in datafile:
            f.consume(line.strip())

    #f.render()
    for _ in range(10):
        #logger.info(f.elves)
        f.round()
        #logger.info(f"END OF ROUND {_ + 1}")
        #f.render()

    spots = f.get_empty_spots()
    logger.info(spots)
    logger.info(f.top, f.bottom, f.left, f.right)
    assert spots == 110

def test_log():
    logger.info("Test Loki Message")
    assert True

@instrument
def test_part_1():
    logger.info("Part 1")
    logger.info("BEGIN")
    f = Field()
    with open("Day23/Day23Data.txt", "r") as datafile:
        for line in datafile:
            f.consume(line.strip())

    #f.render()
    for _ in range(10):
        #logger.info(f.elves)
        elves_moved = f.round()
        logger.info(f"END OF ROUND {_ + 1}, moved {elves_moved} elves")
        #f.render()

    
    f.recalculate()
    #f.render()
    spots = f.get_empty_spots()
    logger.info(spots)
    logger.info(f"{f.top},  {f.bottom}, {f.left}, {f.right}")
    assert spots == 4049
        
@instrument
def test_part_2():
    logger.info("Part 2")
    logger.info("BEGIN")
    f = Field()
    with open("Day23/Day23Data.txt", "r") as datafile:
        for line in datafile:
            f.consume(line.strip())

    #f.render()
    rounds = 0
    while True:
        #logger.info(f.elves)
        elves_moved = f.round()
        rounds += 1
        #logger.info(f"END OF ROUND {rounds}, moved {elves_moved} elves")
        if elves_moved == 0:
            break

    
    f.recalculate()
    logger.info(rounds)
    assert rounds == 1021