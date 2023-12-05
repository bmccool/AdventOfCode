""" Advent of Code 2023 Day 05 """
from typing import Dict, List, Optional
from dataclasses import dataclass

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day05/'

@dataclass
class Interval:
    """ An INCLUSIVE interval """
    start: int
    stop: int

    def __contains__(self, item: int) -> bool:
        """ Check if an item is in the interval """
        return item >= self.start and item < self.stop

    def __repr__(self) -> str:
        """ String representation of the interval """
        return f"[{self.start}, {self.stop}]"

    def __len__(self) -> int:
        """ Length of the interval """
        return self.stop - self.start

class Section:
    """ A section of a map (mapping from one range to another)"""
    def __init__(self, line: str):
        parts = [int(part) for part in line.strip().split()]
        self.source_range: range = range(parts[1], parts[1] + parts[2])
        self.destination_range: range = range(parts[0], parts[0] + parts[2])

    def __repr__(self) -> str:
        return f"{self.source_range} -> {self.destination_range}"

class IntervalSection:
    """ A section made out of intervals instead of ranges """
    def __init__(self, section: Section):
        self.source_range: Interval = Interval(section.source_range.start,
                                               section.source_range.stop - 1)
        self.destination_range: Interval = Interval(section.destination_range.start,
                                                    section.destination_range.stop - 1)

    def __repr__(self) -> str:
        return f"{self.source_range} -> {self.destination_range}"

class Map:
    """ A Map """
    def __init__(self):
        self.sections: List[Section] = []

    def __repr__(self) -> str:
        """ String representation of the map """
        return "\n" + "\n".join([s.__repr__() for s in self.sections])

    def get_destination(self, source: int) -> int:
        """ Get the destination of a source """
        for section in self.sections:
            if source in section.source_range:
                return source + (section.destination_range.start - section.source_range.start)
        return source

class Almanac:
    """ An almanac representing seeds/seed ranges, and mappings between seed and location """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.seeds: List[int] = []
        self.maps: Dict[str, Map] = {}
        self.last_map: str = None
        self.parse_input()

    def parse_input(self) -> None:
        """ Parse the input """
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "seeds" in line:
                    self.seeds = [int(seed) for seed in line.strip("seeds: ").split()]
                elif "map" in line:
                    self.create_map(line)
                elif line != "":
                    self.add_to_map(line)

    def create_map(self, line: str) -> None:
        """ Add a line to the map """
        mapping = line.strip(" map:")
        self.maps[mapping] = Map()
        self.last_map = mapping

    def add_to_map(self, line: str) -> None:
        """ Add a line to the map """
        if self.last_map is None:
            raise ValueError("No map to add line to")
        self.maps[self.last_map].sections.append(Section(line))

    def map_seed(self, seed: int) -> int:
        """ Map a seed """
        location: int = seed
        location = self.maps["seed-to-soil"].get_destination(location)
        location = self.maps["soil-to-fertilizer"].get_destination(location)
        location = self.maps["fertilizer-to-water"].get_destination(location)
        location = self.maps["water-to-light"].get_destination(location)
        location = self.maps["light-to-temperature"].get_destination(location)
        location = self.maps["temperature-to-humidity"].get_destination(location)
        location = self.maps["humidity-to-location"].get_destination(location)
        #logger.info(f"Seed {seed} -> {location}")
        return location

    def map_seeds(self) -> Dict[int, int]:
        """ Map seeds to locations """
        ret_val: Dict[int, int] = {}
        for seed in self.seeds:
            location: int = self.map_seed(seed)
            ret_val[seed] = location

        return ret_val

    def map_seeds_ranges(self) -> int:
        """ Map seeds to locations using seed input as ranges instead of individual seeds """
        next_intervals: List[Interval] = \
            [Interval(self.seeds[i], self.seeds[i] + self.seeds[i + 1] - 1)
             for i in range(0, len(self.seeds), 2)]
        intervals = []
        for plant_map in self.maps.values():
            intervals.extend(next_intervals)
            next_intervals = []
            for section in plant_map.sections:
                section_interval = IntervalSection(section)
                remaining_intervals: List[Interval] = []
                while intervals:
                    interval = intervals.pop(0)
                    next_interval, remaining = get_overlapped_interval(interval, section_interval)
                    if next_interval:
                        next_intervals.append(next_interval)
                    remaining_intervals.extend(remaining)
                intervals = remaining_intervals

        intervals.extend(next_intervals)
        return min([i.start for i in intervals])

def get_overlapped_interval(source: Interval, mapping: IntervalSection) \
    -> (Optional[Interval], List[Interval]):
    """
    Given an interval, and a mapping, return a discrete interval,
    and any intervals that aren't mapped.

    This can only ever return zero or one mapped interval, and zero to two remaining intervals.

    :param source: The source interval
    :param mapping: The interval mapping
    :return:
    """
    overlap_min = max(source.start, mapping.source_range.start)
    overlap_max = min(source.stop, mapping.source_range.stop)
    remaining = []
    if overlap_min <= overlap_max:
        # There is an overlap between source interval and mapping interval
        if source.start < overlap_min:
            remaining.append(Interval(source.start, overlap_min - 1))
        if source.stop > overlap_max:
            remaining.append(Interval(overlap_max + 1, source.stop))
        mapped_interval = Interval(
            overlap_min + mapping.destination_range.start - mapping.source_range.start,
            overlap_max + mapping.destination_range.start - mapping.source_range.start)
        return mapped_interval, remaining
    return None, [source]


def test_sanity():
    """Sanity check """
    assert True

def test_almanac():
    """ Test the almanac """
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input_sample.txt")
    logger.info(f"Seeds: {almanac.seeds}")
    logger.pretty(logger.INFO, almanac.maps)

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input_sample.txt")
    locations = almanac.map_seeds().values()
    assert min(locations) == 35

def test_part_1():
    """Test part 1"""
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input.txt")
    locations = almanac.map_seeds().values()
    logger.info(min(locations))

def test_sample_2():
    """Test part 2"""
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input_sample.txt")
    result = almanac.map_seeds_ranges()
    logger.info(result)

def test_part_2():
    """Test part 2"""
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input.txt")
    result = almanac.map_seeds_ranges()
    assert result == 79004094
