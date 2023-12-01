""" DAY 15 of ADVENT OF CODE """
from __future__ import annotations
from typing import List
import pytest

from pymccool.logging import Logger, LoggerKwargs
logger = Logger(LoggerKwargs(app_name="AOC2022"))

class MyRange:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __len__(self):
        return self.high - self.low

    def __repr__(self):
        return f"R:[{self.low:,}, {self.high:,}]"

def manhatten_distance(p1: Point, p2: Point) -> int:
    return (abs(p1.x - p2.x) + abs(p1.y - p2.y)) 

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"Point: ({self.x}, {self.y})"

    def coordinates(self) -> tuple:
        return (self.x, self.y)

class Sensor(Point):
    def __init__(self, x, y, beacon: Point):
        super().__init__(x, y)
        self.beacon = beacon
        self.distance = manhatten_distance(self, self.beacon)
        self.cover_set = set()

    def fill_cover_set(self):
        for x in range(self.x - self.distance, self.x + self.distance + 1):
            for y in range(self.y - (self.distance - abs(x - self.x)), self.y + (self.distance - abs(x - self.x)) + 1):
                p = Point(x, y)
                #print(f"Adding point {p}")
                self.cover_set.add(p.coordinates())

    def get_cover_range_at_line(self, line_no: int) -> MyRange:
        distance = self.distance - abs(line_no - self.y)
        if distance < 0:
            return None

        return MyRange(self.x - distance, self.x + distance)

    def __repr__(self):
        return f"Sensor: ({self.x}, {self.y}), Closest Beacon {self.beacon}, at distance {self.distance})"

class Field:
    def __init__(self):
        self.x_min = None
        self.y_min = None
        self.x_max = None
        self.y_max = None

        self.sensors = []
        self.beacon_locations = set()

    def add_sensor(self, sensor: Sensor):
        if self.x_min == None:
            self.x_min = sensor.x
            self.y_min = sensor.y
            self.x_max = sensor.x
            self.y_max = sensor.y

        self.x_min = min(self.x_min, sensor.x, sensor.beacon.x)
        self.x_max = max(self.x_max, sensor.x, sensor.beacon.x)
        self.y_min = min(self.y_min, sensor.y, sensor.beacon.y)
        self.y_max = max(self.y_max, sensor.y, sensor.beacon.y)
        self.sensors.append(sensor)
        self.beacon_locations.add(sensor.beacon.coordinates())

    def consume_sensor_pair(self, line: str):
        line = line.strip()
        line = line.split()
        junk = "xy=,:"
        beacon = Point(line[8].strip(junk), line[9].strip(junk))
        sensor = Sensor(line[2].strip(junk), line[3].strip(junk), beacon)
        self.add_sensor(sensor)

    def __repr__(self):
        return f"({self.x_min} - {self.x_max}, {self.y_min} - {self.y_max})"

    def get_checked_spots_at_line(self, line_no: int):
        #Strategy:
        # 1. Check all sensors to see which ones could POSSIBLY check this line
            # If the sensor line number (y) is within its distance from the line_no in question,
            # then it is a candidate
        # 2. For all sensors from (#1), fill the cover set (optionally with a filter on this line_no)
        # 3. For all sensors from (#1), find all in the cover set that are also on this line
        # 4. Union #4 and count
        line_set = set()
        #print("ALL SENSORS")
        #for sensor in self.sensors:
        #    print(sensor)

        ranges = []
        for sensor in self.sensors:
            r = sensor.get_cover_range_at_line(line_no)
            if r:
                combine_ranges(ranges, r)


        print(ranges)

        #for i, e in enumerate(line_set):
        #    print(f"{i + 1}: {e}")

        #for i, e in enumerate(self.beacon_locations):
        #    print(f"{i + 1}: {e}")

        sum = 0
        for r in ranges:
            sum += len(r)



        logger.info(sum)
        return sum

    def get_possible_beacons(self, line_no: int, r: MyRange) -> List[Point]:
        logger.verbose(f"Getting Beacons at line {line_no} and range {r}")
        ranges = [r]
        for sensor in self.sensors:
            r = sensor.get_cover_range_at_line(line_no)
            if r:
                subtract_ranges(ranges, r)

        if ranges == []:
            return None

        possible_beacons = set()
        for r in ranges:
            for x in range(r.low, r.high + 1):
                possible_beacons.add(Point(x, line_no))

        return possible_beacons

        

def subtract_ranges(list_of_ranges: List[MyRange], new_range: MyRange):
    logger.verbose(f"Subtracting {new_range} from {list_of_ranges}")
    while True:
        modified = False
        for r in list_of_ranges:
            if (r.low <= new_range.low <= r.high) and (r.low <= new_range.high <= r.high):
                list_of_ranges.append(MyRange(new_range.high + 1, r.high))
                r.high = new_range.low - 1
            elif (new_range.low <= r.low <= new_range.high) and (new_range.low <= r.high <= new_range.high):
                list_of_ranges.remove(r)
                modified = True
                break
            elif r.low <= new_range.low <= r.high:
                r.high = new_range.low - 1
            elif r.low <= new_range.high <= r.high:
                r.low = new_range.high + 1
        if not modified:
            break


    logger.verbose(f"Result: {list_of_ranges}")

            

def combine_ranges(list_of_ranges: List[MyRange], new_range: MyRange):
    # Add the range
    logger.debug(f"Adding {new_range} to {list_of_ranges}")
    added = False
    for r in list_of_ranges:
        if (r.low == new_range.low) and (r.high == new_range.high):
            return

        elif r.low <= new_range.low <= r.high:
            r.high = max(new_range.high, r.high)
            added = True

        elif r.low <= new_range.high <= r.high:
            r.low = min(new_range.low, r.low)
            added = True

        elif (new_range.low <= r.low <= new_range.high) and (new_range.low <= r.high <= new_range.high):
            r.low = min(new_range.low, r.low)
            r.high = max(new_range.high, r.high)
            added = True


    
    if not added:
        list_of_ranges.append(new_range)

    logger.debug(f"Intermediate Step: {list_of_ranges}")

    # Combine any new ranges
    while True:
        combined = False
        for r in list_of_ranges:
            for s in list_of_ranges:
                if r == s:
                    continue
                if r.low < s.low < r.high:
                    s.low = r.low
                    list_of_ranges.remove(r)
                    combined = True
                    break

                if r.low < s.high < r.high:
                    s.high = r.high
                    list_of_ranges.remove(r)
                    combined = True
                    break
            if combined:
                 break # out of nested loop
        if not combined:
            break # out of true loop

    logger.debug(f"Result: {list_of_ranges}")

def test_cover_set():
    print()
    #f = Field()
    s = Sensor(0, 0, Point(1, 0))
    s.fill_cover_set()
    assert (-1, 0) in s.cover_set
    assert (0, -1) in s.cover_set
    assert (0,  0) in s.cover_set
    assert (0 , 1) in s.cover_set
    assert (1 , 0) in s.cover_set
    assert (-2, 0) not in s.cover_set
    assert (2, 0) not in s.cover_set
    assert (0, 2) not in s.cover_set
    assert (0, -2) not in s.cover_set

def test_part_demo():
    print()
    logger.info("Part DEMO")
    logger.info("BEGIN")
    f = Field()
    with open("2022/Day15/Day15DemoData.txt", "r") as datafile:
        for line in datafile:
            f.consume_sensor_pair(line)

    assert f.x_min == -2
    assert f.x_max == 25
    assert f.y_min ==  0
    assert f.y_max == 22

    assert f.get_checked_spots_at_line(10) == 26

def test_part_1():
    print("Part 1")
    print("BEGIN")
    f = Field()
    with open("2022/Day15/Day15Data.txt", "r") as datafile:
        for line in datafile:
            #TODO distances are massive.  Use ranges instead of walking over each spot in cover_set
            f.consume_sensor_pair(line)


    assert f.get_checked_spots_at_line(2000000) == 6124805

def test_part_2_demo():
    print()
    logger.info("Part 2 DEMO")
    logger.info("BEGIN")
    f = Field()
    with open("2022/Day15/Day15DemoData.txt", "r") as datafile:
        for line in datafile:
            f.consume_sensor_pair(line)

    assert f.x_min == -2
    assert f.x_max == 25
    assert f.y_min ==  0
    assert f.y_max == 22

    possible_beacons = set()

    for line_no in range(0, 20 + 1):
        try:
            possible_beacons = possible_beacons.union(f.get_possible_beacons(line_no, MyRange(0, 20)))
        except TypeError:
            continue

    logger.info(f"Possible Beacons: {possible_beacons}")
    assert len(possible_beacons) == 1
    beacon = possible_beacons.pop()
    tuning_frequency = (beacon.x * 4_000_000) + beacon.y
    logger.info(f"Tuning frequency of {beacon} is {tuning_frequency}")
    assert tuning_frequency == 56000011

@pytest.mark.skip(reason="Too Slow!")
def test_part_2():
    print()
    logger.info("Part 2")
    logger.info("BEGIN")
    f = Field()
    with open("2022/Day15/Day15Data.txt", "r") as datafile:
        for line in datafile:
            f.consume_sensor_pair(line)

    possible_beacons = set()

    for line_no in range(0, 4_000_000 + 1):
    #for line_no in range(3138880, 4_000_000 + 1):
    #for line_no in range(2723728, 2723728 + 1):
        if (line_no % 1_000) == 0:
            percent = (line_no / 4_000_000) * 100
            logger.info(f"Before Scanning LineNo {line_no}, Possible Beacons: {possible_beacons}, percent complete: {percent:.2f}")
        try:
            possible_beacons = possible_beacons.union(f.get_possible_beacons(line_no, MyRange(0, 4_000_000)))
        except TypeError:
            continue



    logger.info(f"Possible Beacons: {possible_beacons}")
    assert len(possible_beacons) == 1
    beacon = possible_beacons.pop()
    tuning_frequency = (beacon.x * 4_000_000) + beacon.y
    logger.info(f"Tuning frequency of {beacon} is {tuning_frequency}")
    assert tuning_frequency == 12555527364986
