""" Advent of Code 2023 Day 04 """
from typing import Dict

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day04/'

class ScratchCard:
    """ A Scratch Card """
    def __init__(self, line: str):
        self.input = line
        self.id = None
        self.numbers = []
        self.winning_numbers = []
        self.score = 0
        self.copies = 1
        self.matches = 0
        self.parse_input()
        self.get_score()

    def __repr__(self) -> str:
        return f"ScratchCard(id={self.id}, numbers={self.numbers}, "\
            "winning_numbers={self.winning_numbers}, score={self.score})"

    def increase_score(self) -> None:
        """ Increase the score """
        if self.score == 0:
            self.score += 1
        else:
            self.score *= 2

    def get_score(self) -> None:
        """ Get the score """
        for number in self.numbers:
            if number in self.winning_numbers:
                self.increase_score()
                self.matches += 1

    def parse_input(self) -> None:
        """ Parse the input """
        self.id = int(self.input.split(":")[0].strip("Card "))
        self.numbers = [int(x) for x in self.input.split(":")[1].split("|")[0].strip().split()]
        self.winning_numbers = [
            int(x) for x in self.input.split(":")[1].split("|")[1].strip().split()]

class ScratchCards:
    """ A dictionary of scratch cards """
    def __init__(self, infile: str):
        self.infile = infile
        self.cards: Dict[int, ScratchCard] = {}
        self.parse_input()

    def parse_input(self) -> None:
        """ Parse the input """
        with open(self.infile, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                card = ScratchCard(line)
                self.cards[card.id] = card

    def get_score_total(self) -> int:
        """ Get the total score """
        total = 0
        for card in self.cards.values():
            total += card.score
        return total

    def get_total_scratch_cards(self) -> int:
        """ Get the total number of scratch cards """
        total_copies = 0
        logger.info(f"Processing {len(self.cards)} cards")
        for card in self.cards.values():
            for x in range(1, card.matches + 1):
                self.cards[card.id + x].copies += card.copies
            total_copies += card.copies
        return total_copies


def test_sanity():
    """Sanity check """
    assert True

def test_scratch_card():
    """ Test the scratch card """
    logger.info("Test Scratch Card")
    scratch_card = ScratchCard("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    logger.pretty(logger.INFO, scratch_card)
    assert True

def test_sample_1():
    """ Test Sample 1"""
    logger.info("Sample 1")
    scratch_cards = ScratchCards(WORKING_DIR + "input_sample.txt")
    #logger.pretty(logger.INFO, scratch_cards.cards)
    assert scratch_cards.get_score_total() == 13

def test_part_1():
    """Test part 1"""
    logger.info("Part 1")
    scratch_cards = ScratchCards(WORKING_DIR + "input.txt")
    total = scratch_cards.get_score_total()
    logger.info(f"Total score: {total}")

def test_sample_2():
    """Test part 2"""
    logger.info("Sample 2")
    scratch_cards = ScratchCards(WORKING_DIR + "input_sample.txt")
    assert scratch_cards.get_total_scratch_cards() == 30

def test_part_2():
    """Test part 2"""
    logger.info("Part 2")
    scratch_cards = ScratchCards(WORKING_DIR + "input.txt")
    total = scratch_cards.get_total_scratch_cards()
    logger.info(f"Total Cards: {total}")
