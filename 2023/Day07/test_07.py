""" Advent of Code 2023 Day 05 """
from typing import Dict, List, Self
from dataclasses import dataclass

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day07/'


CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J",  "Q", "K", "A"]

@dataclass
class Card:
    """ A card has a label and a value """
    label: str
    value: int = 0

    def __post_init__(self) -> None:
        self.label = self.label.upper()
        self.value = CARDS.index(self.label) + 2

    def __str__(self) -> str:
        return f"{self.label}"

@dataclass
class Hand:
    """ A hand consists of five cards and a bid """
    cards: List[Card]
    bid: int
    score: int = 0
    type: str = ""
    primary_score = 0
    secondary_score = 0

    def __str__(self) -> str:
        return f"{"".join([card.label for card in self.cards])}, ({self.type}: {self.score:_}), Bid: {self.bid}"
    
    def __repr__(self) -> str:
        return f"{self.__str__()}"
    
    def __post_init__(self) -> None:
        self.primary_score = self.get_primary_score_number()
        self.secondary_score = self.get_secondary_score_number()
        self.score = int(hex(self.primary_score) + hex(self.secondary_score).strip("0x"), 16)
        logger.info(f"Hand: {self.__str__()} Type: {self.type}, Score: {self.score}, Primary Score: {self.primary_score}, Secondary Score: {self.secondary_score}")

    def __lt__(self, other: Self) -> bool:
        logger.info(f"Comparing {self} and {other}")
        if self.primary_score < other.primary_score:
            return True
        logger.debug(f"Tiebreak check for {self} and {other}")
        for card_i in range(5):
            logger.info(f"Is {self.cards[card_i]} less than {other.cards[card_i]}?")
            if self.cards[card_i].value < other.cards[card_i].value:
                logger.info("YES")
                logger.info(f"Card {self.cards[card_i]} is less than {other.cards[card_i]}")
                return True
            elif self.cards[card_i].value > other.cards[card_i].value:
                logger.info("NO")
                return False
        return False
    
    def __le__(self, other: Self) -> bool:
        logger.info(f"Comparing {self} and {other}")
        if self.primary_score < other.primary_score:
            return True
        logger.debug(f"Tiebreak check for {self} and {other}")
        for card_i in range(5):
            if self.cards[card_i].value <= other.cards[card_i].value:
                return True
        return False

    def get_secondary_score_number(self) -> int:
        """ Get the tiebreaker score"""
        # Must be < 1000, the resolution of the primary score
        # Score each card and give weight to first cards
        secondary_score = int("0x" + "".join([hex(card.value).strip("0x") for card in self.cards]), 16)
        logger.info(f"Secondary Score: {secondary_score}")
        self.secondary_score = secondary_score
        return self.secondary_score
    
    def get_primary_score_number(self) -> int:
        """ Score the hand """
        TYPES = {"5oaK": 7,
                 "4oaK": 6, 
                 "FH": 5, 
                 "3oaK": 4, 
                 "2P": 3, 
                 "1P": 2, 
                 "HC": 1}
        
        # Put the hand in a dict for easy counting
        a = {}
        for card in self.cards:
            if card.label not in a:
                a[card.label] = 0
            a[card.label] += 1

        # Check for 5 of a kind
        if 5 in a.values():
            self.type = "5oaK"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]
        
        # Check for 4 of a kind
        if 4 in a.values():
            self.type = "4oaK"
            self.score += TYPES[self.type]
            return TYPES[self.type]
        
        # check for Full House
        if len(set([card.label for card in self.cards])) == 2:
            self.type = "FH"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]
        
        # Check for 3 of a kind
        if 3 in a.values():
            self.type = "3oaK"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]
        
        # Check for 2 pairs
        if len(a) == 3:
            self.type = "2P"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]
        
        # Check for 1 pair
        if len(a) == 4:
            self.type = "1P"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]
        
        # High Card
        if not self.type:
            self.type = "HC"
            self.primary_score = TYPES[self.type]
            return TYPES[self.type]






class Hands:
    """ Class for parsing Camel Cards Hands """
    def __init__(self, filename: str):
        self.filename = filename
        self.hands: List[Hand] = []
        self.parse()
    
    def parse(self) -> None:
        """ Parse the input file """
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                self.hands.append(Hand(cards=[Card(label=label) for label in parts[0]], bid=int(parts[-1])))

    def __repr__(self) -> str:
        return f"{self.hands}"
    
    def __str__(self) -> str:
        return f"{self.hands}"

def test_sanity():
    """Sanity check """
    assert True

def test_score():
    """ Test scoring """
    logger.info("")
    assert (Hand(cards=[Card(label="A"), Card(label="Q"), Card(label="A"), Card(label="Q"), Card(label="A")], bid=1).score <
            Hand(cards=[Card(label="2"), Card(label="2"), Card(label="2"), Card(label="2"), Card(label="7")], bid=1).score)
    
def test_hand():
    """ Test Hand """
    h1cards = "46646"
    h2cards = "38838"
    hand1 = Hand(cards=[Card(label=label) for label in h1cards], bid=1)
    hand2 = Hand(cards=[Card(label=label) for label in h2cards], bid=1)
    logger.info(f"Assert {hand1} > {hand2}")
    assert hand1 > hand2
    assert hand1.score > hand2.score

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    hands = Hands(WORKING_DIR + 'input_sample.txt')
    winnings = 0
    sorted_hands = sorted(hands.hands, key=lambda x: x.score, reverse=False)
    #sorted_hands = sorted(hands.hands, reverse=False)
    for rank, hand in enumerate(sorted_hands):
        winnings += hand.bid * (rank + 1)
        logger.info(f"Sorted Hand: {hand}, Rank: {rank + 1}, Total Winnings: {winnings:,}")
        try:
            assert sorted_hands[rank] < sorted_hands[rank + 1], f"Hand {sorted_hands[rank]} is not less than {sorted_hands[rank + 1]}"
        except IndexError:
            logger.info("No card to compare to")
        except AssertionError as e:
            logger.error(e)
    logger.info(f"Winnings: {winnings}")
    assert winnings == 6440



def test_part_1():
    """Test part 1"""
    hands = Hands(WORKING_DIR + 'input.txt')
    logger.info("")
    winnings = 0
    sorted_hands = sorted(hands.hands, key=lambda x: x.score, reverse=False)
    #sorted_hands = sorted(hands.hands, reverse=False)
    for rank, hand in enumerate(sorted_hands):
        winnings += hand.bid * (rank + 1)
        logger.info(f"Sorted Hand: {hand}, Rank: {rank + 1}, Total Winnings: {winnings:,}")
        try:
            assert sorted_hands[rank] < sorted_hands[rank + 1], f"Hand {sorted_hands[rank]} is not less than {sorted_hands[rank + 1]}"
        except IndexError:
            logger.info("No card to compare to")
        except AssertionError as e:
            logger.error(e)
    logger.info(f"Winnings: {winnings}")

def test_sample_2():
    """Test part 2"""
    logger.info("")
    

def test_part_2():
    """Test part 2"""
    logger.info("")