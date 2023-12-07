""" Advent of Code 2023 Day 05 """
from typing import Dict, List
from dataclasses import dataclass

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day06/'

@dataclass
class Race:
    time: int
    distance: int

class Boat:
    """ Boat Class """
    def __init__(self):
        self.speed_rate_ms = 1

    def get_race_distance(self, button_press_ms: int, race: Race) -> int:
        """ Get distance travelled """
        elapsed_ms: int = button_press_ms
        speed: int = button_press_ms * self.speed_rate_ms
        time_to_race_ms: int = race.time - elapsed_ms
        distance: int = time_to_race_ms * speed

        return distance
    
    def is_race_won(self, button_press_ms: int, race: Race) -> bool:
        """ 
        """
        return self.get_race_distance(button_press_ms=button_press_ms, race=race) > race.distance
    
    def get_winning_race_ways(self, race: Race) -> int:
        """ Get the number of ways to win a race """
        num_ways: int = 0
        for button_press_duration in range(1, race.time):
            if self.is_race_won(button_press_ms=button_press_duration, race=race):
                num_ways += 1

        return num_ways




class Races:
    """ Class for parsing Races """
    def __init__(self, filename: str):
        self.filename = filename
        self.races: List[Race] = []
        self.big_race: Race = None
        self.parse()
    
    def parse(self) -> None:
        """ Parse the input file """
        with open(self.filename, 'r') as file:
            for line in file:
                if "Time" in line:
                    times = line.split(":")[1].strip().split()
                if "Distance" in line:
                    distances = line.split(":")[1].strip().split()

        for time, distance in zip(times, distances):
            self.races.append(Race(int(time), int(distance)))

        self.big_race = Race(time=int("".join(times)), distance=int("".join(distances)))
        



def test_sanity():
    """Sanity check """
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    r = Races(WORKING_DIR + 'input_sample.txt')
    boat = Boat()
    logger.pretty(logger.INFO, r.races)
    all_possibilities = [boat.get_winning_race_ways(race=race) for race in r.races]
    logger.info(f"All Possibilities: {all_possibilities}")
    answer = 1
    for possibilities in all_possibilities:
        answer *= possibilities
    logger.info(f"Answer: {answer}")



def test_part_1():
    """Test part 1"""
    r = Races(WORKING_DIR + 'input.txt')
    boat = Boat()
    logger.pretty(logger.INFO, r.races)
    all_possibilities = [boat.get_winning_race_ways(race=race) for race in r.races]
    logger.info(f"All Possibilities: {all_possibilities}")
    answer = 1
    for possibilities in all_possibilities:
        answer *= possibilities
    logger.info(f"Answer: {answer}")

def test_sample_2():
    """Test part 2"""
    logger.info("")
    r = Races(WORKING_DIR + 'input_sample.txt')
    boat = Boat()
    num_ways = boat.get_winning_race_ways(race=r.big_race)
    logger.info(f"Answer: {num_ways}")
    

def test_part_2():
    """Test part 2"""
    r = Races(WORKING_DIR + 'input.txt')
    boat = Boat()
    num_ways = boat.get_winning_race_ways(race=r.big_race)
    logger.info(f"Answer: {num_ways}")