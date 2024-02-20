""" Advent of Code 2023 Day 12 """
from typing import List, Dict
from functools import lru_cache
import re
from sortedcontainers import SortedSet
from pymccool.math import Point

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day14/'

class HashableSortedSet(SortedSet):
    def __hash__(self):
        return hash(str(self))

class RockPattern:
    """ An observation of rock and ash patterns """
    def __init__(self):
        self.round_rocks: HashableSortedSet[Point] = HashableSortedSet()
        self.cube_rocks: HashableSortedSet[Point] = HashableSortedSet()
        self.max: Point = Point(-1, -1)
        self.map_str: str = ""
        self.hashes = set()


    def __hash__(self):
        """ Hash the pattern """
        return hash(self.map_str)

    def parse_line(self, line: str):
        """ Parse a line of the input file """
        line = line.strip()
        self.max = Point(max(self.max.x, len(line)), self.max.y + 1)
        for i, char in enumerate(line):
            if char == 'O':
                self.round_rocks.add(Point(i, self.max.y))
            elif char == '#':
                self.cube_rocks.add(Point(i, self.max.y))

    @staticmethod
    def get_point(round_rocks: HashableSortedSet, cube_rocks: HashableSortedSet, point: Point) -> str:
        """ Get the character at a point """
        if point in round_rocks:
            return 'O'
        if point in cube_rocks:
            return '#'
        return '.'
    
    @staticmethod
    def sort_string(sort_string: str, reverse=False) -> str:
        """ Sort a string """
        parts = []
        index = 0
        for cube_rock_chunk in re.finditer(r"#+", sort_string):
            parts.append(sort_string[index:cube_rock_chunk.span()[0]])
            parts.append(cube_rock_chunk[0])
            index = cube_rock_chunk.span()[1]
        if index < len(sort_string):
            parts.append(sort_string[index:])

        assert len(sort_string) == len("".join(parts))
        ret_val = ""
        for part in parts:
            ret_val += "".join(sorted(part, reverse=reverse))
        return ret_val
    
    @lru_cache
    @staticmethod
    def tilt_north(round_rocks: HashableSortedSet, cube_rocks: HashableSortedSet, max_point: Point):
        """ Tilt the pattern north """
        for column in range(max_point.x):
            column_str: str = ""
            for row in range(max_point.y + 1):
                column_str += RockPattern.get_point(round_rocks, cube_rocks, Point(column, row))
            column_str = RockPattern.sort_string(column_str, reverse=True)

            # This column should match column string.  Pop everything out of this column, and readd as per column_str
            for row in range(max_point.y + 1):
                if column_str[row] == RockPattern.get_point(round_rocks, cube_rocks, Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not column_str[row] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not column_str[row] == '#':
                            cube_rocks.remove(Point(column, row))
                    if column_str[row] == 'O':
                        round_rocks.add(Point(column, row))
                    elif column_str[row] == '#':
                        cube_rocks.add(Point(column, row))
        return (round_rocks, cube_rocks)

    @lru_cache
    @staticmethod
    def tilt_south(round_rocks: HashableSortedSet, cube_rocks: HashableSortedSet, max_point: Point):
        """ Tilt the pattern south """
        for column in range(max_point.x):
            column_str: str = ""
            for row in range(max_point.y + 1):
                column_str += RockPattern.get_point(round_rocks, cube_rocks, Point(column, row))
            column_str = RockPattern.sort_string(column_str, reverse=False)

            # This column should match column string.  Pop everything out of this column, and readd as per column_str
            for row in range(max_point.y + 1):
                if column_str[row] == RockPattern.get_point(round_rocks, cube_rocks, Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not column_str[row] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not column_str[row] == '#':
                            cube_rocks.remove(Point(column, row))
                    if column_str[row] == 'O':
                        round_rocks.add(Point(column, row))
                    elif column_str[row] == '#':
                        cube_rocks.add(Point(column, row))
        return (round_rocks, cube_rocks)

    @lru_cache
    @staticmethod
    def tilt_west(round_rocks: HashableSortedSet, cube_rocks: HashableSortedSet, max_point: Point) -> (HashableSortedSet, HashableSortedSet):
        """ Tilt the pattern west """
        for row in range(max_point.y + 1):
            row_str: str = ""
            for column in range(max_point.x):
                row_str += RockPattern.get_point(round_rocks, cube_rocks, Point(column, row))
            row_str = RockPattern.sort_string(row_str, reverse=True)

            # This row should match row string.  Pop everything out of this row, and readd as per row_str
            for column in range(max_point.x):
                if row_str[column] == RockPattern.get_point(round_rocks, cube_rocks, Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not row_str[column] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not row_str[column] == '#':
                            cube_rocks.remove(Point(column, row))
                    if row_str[column] == 'O':
                        round_rocks.add(Point(column, row))
                    elif row_str[column] == '#':
                        cube_rocks.add(Point(column, row))
        return (round_rocks, cube_rocks)
    
    @lru_cache
    @staticmethod
    def tilt_east(round_rocks: SortedSet[Point], cube_rocks: SortedSet[Point], max_point: Point):
        """ Tilt the pattern east """
        for row in range(max_point.y + 1):
            row_str: str = ""
            for column in range(max_point.x):
                row_str += RockPattern.get_point(round_rocks, cube_rocks, Point(column, row))
            row_str = RockPattern.sort_string(row_str, reverse=False)

            # This row should match row string.  Pop everything out of this row, and readd as per row_str
            for column in range(max_point.x):
                if row_str[column] == RockPattern.get_point(round_rocks, cube_rocks, Point(column, row)):
                    continue
                else:
                    if Point(column, row) in round_rocks:
                        if not row_str[column] == 'O':
                            round_rocks.remove(Point(column, row))
                    elif Point(column, row) in cube_rocks:
                        if not row_str[column] == '#':
                            cube_rocks.remove(Point(column, row))
                    if row_str[column] == 'O':
                        round_rocks.add(Point(column, row))
                    elif row_str[column] == '#':
                        cube_rocks.add(Point(column, row))
        return (round_rocks, cube_rocks)



    def render(self):
        logger.info("Rendering pattern")
        for row in range(self.max.y + 1):
            row_str: str = ""
            for col in range(self.max.x):
                point = Point(col, row)
                row_str += RockPattern.get_point(self.round_rocks, self.cube_rocks, point)
            logger.info(row_str)

    def calculate_load(self) -> int:
        """ Calculate the load of this pattern """
        total_load = 0
        for rock in self.round_rocks:
            total_load += (self.max.y + 1 - rock.y)

        return total_load

    @lru_cache
    @staticmethod
    def cycle(round_rocks: HashableSortedSet, cube_rocks: HashableSortedSet, max_point: Point) -> (HashableSortedSet, HashableSortedSet):
        """ Cycle the pattern """
        (round_rocks, cube_rocks) = RockPattern.tilt_north(round_rocks, cube_rocks, max_point)
        (round_rocks, cube_rocks) = RockPattern.tilt_west(round_rocks, cube_rocks, max_point)
        (round_rocks, cube_rocks) = RockPattern.tilt_south(round_rocks, cube_rocks, max_point)
        (round_rocks, cube_rocks) = RockPattern.tilt_east(round_rocks, cube_rocks, max_point)

        return round_rocks, cube_rocks

class PatternEater:
    """ Class to parse multiple rock patterns from a file input """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.pattern: RockPattern = RockPattern()
        self.parse_data()

    def parse_data(self):
        """ Read the input data and fill the data dict """
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.pattern.parse_line(line.strip())


def test_sanity():
    """Sanity check """
    assert True

def test_sort_string():
    logger.info("")
    assert RockPattern.sort_string("OO.O.O..##", reverse=True) == "OOOO....##"
    assert RockPattern.sort_string("O..O.#O.O", reverse=True) == "OO...#OO."
    assert RockPattern.sort_string("O..O.###O.O", reverse=True) == "OO...###OO."
    

def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input_sample.txt')
    pattern_eater.pattern.render()
    pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks = RockPattern.tilt_north(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks, pattern_eater.pattern.max)
    pattern_eater.pattern.render()
    load = pattern_eater.pattern.calculate_load()
    logger.info(f"Load is {load}")

def test_part_1():
    """Test part 1"""
    logger.info("")
    pattern_eater = PatternEater(WORKING_DIR + 'input.txt')
    #pattern_eater.pattern.render()
    pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks = RockPattern.tilt_north(pattern_eater.pattern.round_rocks, pattern_eater.pattern.cube_rocks, pattern_eater.pattern.max)
    #pattern_eater.pattern.render()
    load = pattern_eater.pattern.calculate_load()
    logger.info(f"Load is {load}")
    assert load == 108_955

        

def parse(filename = WORKING_DIR + 'input.txt') -> List[str]:
    """ Parse the input file """
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]
    
def render(board: List[str]):
    """ Render the board """
    for line in board:
        logger.info(line)

def rotate(board: List[str]) -> List[str]:
    """ Rotate the board 90 degrees clockwise (Facilitates N,W,S,E tilting in a cycle) """
    return ["".join(line) for line in zip(*board[::-1])]

def tilt_right(lines: List[str]) -> List[str]:
    """
    It's so much easier to tilt left or right, esp now that the board is a list of strings

    Split the lines by "#", remove the "O" from the left side of the chunks and add them to the right side."""
    return ["#".join([chunk.replace("O", "") + "O" * chunk.count("O") for chunk in line.split("#")]) for line in lines]


def calculate_load(lines: List[str]) -> int:
    """ Calculate the load of this pattern """
    return sum([(line.count("O") * (len(lines) - i)) for i, line in enumerate(lines)])
    
def test_part_1_fast():
    """
    Rewrite part 2 to be faster
    Things to do - 
    1. Keep the state of the board as a list of strings, not a set of points
    2. Keep track of the hashes of the board states
    3. When a hash is seen twice, we have a cycle
    4. Rotate the board instead of having four different tilt functions
    """
    logger.info("")
    board: List[str] = parse(filename=WORKING_DIR + 'input_sample.txt')
    logger.info("Starting board")
    render(board)
    board = rotate(board) # 1 Two wrongs don't make a right, but three lefts do...
    board = tilt_right(board)
    board = rotate(board) # 2
    board = rotate(board) # 3
    board = rotate(board) # 4
    logger.info("Done")
    render(board)
    load = calculate_load(board)
    logger.info(f"Load is {load}")
    assert load == 136

def test_part_2_fast():
    """
    Rewrite part 2 to be faster
    Things to do - 
    1. Keep the state of the board as a list of strings, not a set of points
    2. Keep track of the hashes of the board states
    3. When a hash is seen twice, we have a cycle
    4. Rotate the board instead of having four different tilt functions
    """
    logger.info("")
    board: List[str] = parse(filename=WORKING_DIR + 'input.txt')
    logger.info("Starting board")
    render(board)
    hashes: Dict[int, int] = {} # Store the hashes of the board states
    cycle_count = 0
    while cycle_count < 1_000_000_000:
        h = hash(tuple(board))
        if h in hashes:
            logger.info(f"Found a cycle at {cycle_count}, hash: {h}")
            loop_size = cycle_count - hashes[h] # Current cycle count - cycle count when this hash was seen
            remains = (1_000_000_000 - cycle_count) % loop_size # How many cycles remain after this cycle
            cycle_count = 1_000_000_000 - remains # Set the cycle count to the start of the loop
        board = rotate(board) # 1 Two wrongs don't make a right, but three lefts do...
        board = tilt_right(board) # Tilt North
        board = rotate(board) # 2 
        board = tilt_right(board) # Tilt West
        board = rotate(board) # 3
        board = tilt_right(board) # Tilt South
        board = rotate(board) # 4
        board = tilt_right(board) # Tilt East
        hashes[h] = cycle_count # Store the cycle count this hash was seen
        if cycle_count % 100_000 == 0:
            logger.info(f"Cycle: {cycle_count}.  {100 * cycle_count / 1_000_000_000:2}% done")
        cycle_count += 1
    logger.info("Done")
    render(board)
    load = calculate_load(board)
    logger.info(f"Load is {load}")
    assert load == 106_689
