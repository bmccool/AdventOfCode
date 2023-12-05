""" Advent of Code 2023 Day 05 """
from typing import Dict, List

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day05/'


class Section:
    def __init__(self, line: str):
        parts = [int(part) for part in line.strip().split()]
        self.source_range: range = range(parts[1], parts[1] + parts[2])
        self.destination_range: range = range(parts[0], parts[0] + parts[2])

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
    
    def get_destination_ranges_from_ranges(self, source_ranges: List[range]) -> List[range]:
        """ Get the destination ranges of a source range """
        starting_seeds = get_num_seeds_in_ranges(source_ranges)
        ret_val: List[range] = []
        for source_range in source_ranges:
            ret_val.extend(self.get_destination_ranges_from_range(source_range))
        logger.info(ret_val)
        assert get_num_seeds_in_ranges(ret_val) == starting_seeds
        return ret_val
    
    def get_destination_ranges_from_range(self, source: range) -> List[range]:
        """ Get the destination ranges of a source range """
        current_range = source
        ret_val: List[range] = []
        logger.info(f"Need to map {len(current_range)} seeds")
        while True:
            closest_section: Section = None
            for section in self.sections:
                movement = section.destination_range.start - section.source_range.start
                difference = current_range.start - section.source_range.start
                if not closest_section:
                    logger.info(f"Section: {section}, current_range: {current_range}")
                    if section.source_range.start > current_range.start:
                        closest_section = section
                elif (abs(difference) < abs(current_range.start - closest_section.source_range.start)) and \
                        (section.source_range.start > current_range.start):
                    closest_section = section

                if current_range.start in section.source_range:
                    logger.info(f"Section: {section}, current_range: {current_range}, Movement: {movement}")
                    if current_range.stop <= section.source_range.stop:
                        # This range is entirely in the section
                        ret_range = range(current_range.start + movement, current_range.stop + movement)
                        ret_val.append(ret_range)
                        logger.info(f"Adding dest range: {ret_range}, from {current_range}, with section {section}. Done with range.")
                        logger.info(f"Mapped {len(ret_range)} seeds, {0} seeds left")
                        return ret_val
                    else:
                        ret_range = range(current_range.start + movement, section.source_range.stop + movement)
                        ret_val.append(ret_range)
                        new_range = range(section.source_range.stop, current_range.stop)
                        logger.info(f"Adding dest range: {ret_range}, from {current_range}, with section {section}. -> new_range: {new_range}")
                        logger.info(f"Mapped {len(ret_range)} seeds, {len(new_range)} seeds left")
                        current_range = new_range
                        break
            else:
                if closest_section:
                    ret_range = range(current_range.start, closest_section.source_range.start)
                    ret_val.append(ret_range)
                    new_range = range(closest_section.source_range.start, current_range.stop)
                    logger.info(f"Closest Section {closest_section}")
                    logger.info(f"Adding dest range: {ret_range}, from {current_range}, with section {closest_section}. -> new_range: {new_range}")
                    logger.info(f"Mapped {len(ret_range)} seeds, {len(new_range)} seeds left")
                    current_range = new_range
                else:
                    ret_val.append(current_range)
                    logger.info(f"Adding dest range: {current_range}, from {current_range}. Done with range.")
                    logger.info(f"Mapped {len(current_range)} seeds, {0} seeds left")
                    return ret_val
            
def get_num_seeds_in_ranges(map_ranges: List[range]) -> int:
    """ Get the number of seeds in a range """
    ret_val: int = 0
    for map_range in map_ranges:
        ret_val += len(map_range)
    logger.info(f"{map_ranges} -> {ret_val} seeds")
    return ret_val

class Almanac:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.seeds: List[int] = []
        self.maps: Dict[str, Map] = {}
        self.last_map: str = None
        self.parse_input()

    
    def parse_input(self) -> None:
        """ Parse the input """
        with open(self.filename, "r") as file:
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
        map = line.strip(" map:")
        self.maps[map] = Map()
        self.last_map = map

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
        """ Map seeds to maps """
        ret_val: Dict[int, int] = {}
        for seed in self.seeds:
            location: int = self.map_seed(seed)
            ret_val[seed] = location

        return ret_val
    
    def map_seed_range(self, map_range: range) -> List[range]:
        """ Map a range of seeds """
        ret_val: List[range] = []
        for seed in map_range:
            location: int = self.map_seed(seed)
            ret_val.append(range(location, location + 1))
        return ret_val
    

    
    def map_range(self, seed_range: range) -> List[range]:
        """ Map a range of seeds """
        starting_seeds = get_num_seeds_in_ranges([seed_range])
        ret_val: List[range] = [seed_range]
        logger.info(f"Mapping seed-to-soil: {ret_val}")
        ret_val = self.maps["seed-to-soil"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping soil-to-fertilizer: {ret_val}")
        ret_val = self.maps["soil-to-fertilizer"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping fertilizer-to-water: {ret_val}")
        ret_val = self.maps["fertilizer-to-water"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping water-to-light: {ret_val}")
        ret_val = self.maps["water-to-light"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping light-to-temperature: {ret_val}")
        ret_val = self.maps["light-to-temperature"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping temperature-to-humidity: {ret_val}")
        ret_val = self.maps["temperature-to-humidity"].get_destination_ranges_from_ranges(ret_val)
        logger.info(f"Mapping humidity-to-location: {ret_val}")
        ret_val = self.maps["humidity-to-location"].get_destination_ranges_from_ranges(ret_val)

        ending_seeds = get_num_seeds_in_ranges(ret_val)
        assert starting_seeds == ending_seeds
        return ret_val
    
    def map_all_seeds(self) -> Dict[int, int]:
        """ Map seeds to maps """
        ret_val: Dict[int, int] = {}
        seed_ranges = [range(self.seeds[i], self.seeds[i] + self.seeds[i + 1]) for i in range(0, len(self.seeds), 2)]
        for seed_range in seed_ranges:
            logger.info(f"Seed Range: {seed_range}")
            for seed in seed_range:
                location: int = self.map_seed(seed)
                ret_val[seed] = location

        return ret_val
    
    def map_all_ranges(self) -> List[range]:
        """ Map seeds to locations using ranges """
        ret_val: List[range] = []
        seed_ranges = [range(self.seeds[i], self.seeds[i] + self.seeds[i + 1]) for i in range(0, len(self.seeds), 2)]
        for seed_range in seed_ranges:
            logger.info(f"Seed Range: {seed_range}")
            ret_val.extend(self.map_range(seed_range))

        return ret_val

def test_map_ranges():
    """ Test mapping ranges """
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input_sample.txt")
    locations = almanac.map_range(range(79, 93))



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
    locations = almanac.map_all_seeds().values()
    assert min(locations) == 46
    locations = almanac.map_all_ranges()
    logger.info(locations)
    min_locations = [min(location) for location in locations]
    assert (min(min_locations)) == 46
    

def test_part_2():
    """Test part 2"""
    logger.info("")
    almanac = Almanac(WORKING_DIR + "input.txt")
    locations = almanac.map_all_ranges()
    logger.info(locations)
    min_locations = [location.start for location in locations]
    logger.info(min(min_locations))