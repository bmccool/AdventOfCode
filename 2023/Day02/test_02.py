""" Advent of Code 2023 Day 01 """
from dataclasses import dataclass, field
from typing import List, Dict
from rich import print # pylint: disable=redefined-builtin

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day02/'


@dataclass
class Round:
    """ How many of each color ball are pulled from the bag """
    red: int = 0
    green: int = 0
    blue: int = 0

@dataclass
class Game:
    """ Calibration value and the position found in the line """
    id: int
    rounds: List[Round]
    known_totals: Round = field(default_factory=Round)


class GameEater:
    def __init__(self, filename):
        self.filename = filename
        self.games: Dict[int, Game] = {}

    def get_game_from_line(self, line: str) -> Game:
        line = line.lower()
        rounds: List[Round] = []
        game_number = int(line.split(":")[0].strip("game "))
        for string_round in line.split(":")[1].strip().split(";"):
            string_round = string_round.strip()
            round = Round()
            for entry in string_round.split(","):
                entry = entry.strip()
                if "red" in entry:
                    round.red = int(entry.split(" ")[0])
                elif "green" in entry:
                    round.green = int(entry.split(" ")[0])
                elif "blue" in entry:
                    round.blue = int(entry.split(" ")[0])
            rounds.append(round)
        return Game(game_number, rounds)

    def eat_games(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                game = self.get_game_from_line(line)
                self.games[game.id] = game

    @staticmethod
    def is_game_possible(max_round: Round, game: Game) -> bool:
        ret_val = True
        for round in game.rounds:
            if round.red > max_round.red:
                ret_val = False
            if round.green > max_round.green:
                ret_val = False
            if round.blue > max_round.blue:
                ret_val = False
        #logger.info(f"Game {game.id} is possible: {ret_val}")
        return ret_val

    def find_possible_games(self, max_round: Round) -> List[int]:
        possible_rounds: List[int] = []
        for game in self.games.values():
            if not self.is_game_possible(max_round, game):
                continue
            possible_rounds.append(game.id)
        return possible_rounds
    
    def calculate_known_totals(self):
        for game in self.games.values():
            for round in game.rounds:
                game.known_totals.red = max(game.known_totals.red, round.red)
                game.known_totals.green = max(game.known_totals.green, round.green)
                game.known_totals.blue = max(game.known_totals.blue, round.blue)

def test_sanity():
    """Sanity check """
    assert True

def test_get_game_from_line():
    ge = GameEater(WORKING_DIR + "Day01Data.txt")
    game = ge.get_game_from_line("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red")
    test_game = Game(4, [Round(3, 1, 6), Round(6, 3, 0), Round(14, 3, 15)])
    assert game == test_game

def test_sample_1():
    """Test sample data"""
    logger.info("Starting Sample 1")
    ge = GameEater(WORKING_DIR + 'input_sample_1.txt')
    ge.eat_games()
    logger.info(ge.find_possible_games(Round(12, 13, 14)))
    logger.info(f"Sum of possible game IDs: {sum(ge.find_possible_games(Round(12, 13, 14)))}")

def test_part_1():
    """Test part 1"""
    logger.info("Starting part 1")
    ge = GameEater(WORKING_DIR + 'input.txt')
    ge.eat_games()
    logger.info(ge.find_possible_games(Round(12, 13, 14)))
    logger.info(f"Sum of possible game IDs: {sum(ge.find_possible_games(Round(12, 13, 14)))}")

def test_sample_2():
    """Test part 2"""
    logger.info("Starting sample 2")
    ge = GameEater(WORKING_DIR + 'input_sample_1.txt')
    ge.eat_games()
    ge.calculate_known_totals()
    logger.pretty(logger.INFO, ge.games[1])

def test_part_2():
    """Test part 2"""
    logger.info("Starting part 2")
    ge = GameEater(WORKING_DIR + 'input.txt')
    ge.eat_games()
    ge.calculate_known_totals()
    s  = sum([(game.known_totals.red * game.known_totals.green * game.known_totals.blue) for game in ge.games.values()])
    logger.info(f"Sum of all game powers: {s}")
