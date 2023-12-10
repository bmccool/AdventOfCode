""" Advent of Code 2023 Day 05 """
from typing import List, Callable, Self, Dict
from dataclasses import dataclass

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))


WORKING_DIR = '2023/Day10/'


@dataclass
class Point:
    """ A point in 2D space """
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Self):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __sub__(self, other) -> Self:
        return Point(self.x - other.x, self.y - other.y)
    
    def up(self) -> Self:
        return self + Point(0, -1)
    
    def down(self) -> Self:
        return self + Point(0, 1)
    
    def left(self) -> Self:
        return self + Point(-1, 0)
    
    def right(self) -> Self:
        return self + Point(1, 0)

class Pipe():
    def __init__(self, label: str, point: Point):
        # Ugh use pattern matching lol
        if label is '|':
            self.label = '┃'
        elif label is '-':
            self.label = '━'
        elif label is 'L':
            self.label = '┗'
        elif label is 'J':
            self.label = '┛'
        elif label is '7':
            self.label = '┓'
        elif label is 'F':
            self.label = '┏'
        elif label is 'S':
            self.label = 'S'

        self.prev: str = None
        self.distance: int = None
        self.next: Self = None
        self.point = point

    def __str__(self):
        #return str(self.distance or self.label)
        return str(self.label)
    
    def __repr__(self):
        return self.__str__()


class Sketch:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.data: Dict[Point, Pipe] = {}
        self.start: Point = None
        self.max: Point = Point(0, 0)
        self.parse_data()

    def parse_data(self):
        """ Read the input data and fill the data dict """
        with open(self.filename, 'r', encoding='utf-8') as f:
            for y, line in enumerate(f.readlines()):
                for x, char in enumerate(line):
                    if y > self.max.y:
                        self.max.y = y
                    if x > self.max.x:
                        self.max.x = x
                    if char is not ' ' and char is not '\n' and char is not '.':
                        self.data[Point(x, y)] = Pipe(label=char, point=Point(x, y))
                        if char == 'S':
                            self.start = Point(x, y)
                            self.data[self.start].distance = 0

    def render(self, log_func: Callable=logger.info, show_complete: bool=False):
        """ Render the sketch"""
        for y in range(self.max.y + 1):
            row = ""
            for x in range(self.max.x + 1):
                if not show_complete:
                    row += str(self.data.get(Point(x, y), ' '))
                else:
                    datapoint = self.data.get(Point(x, y), ' ')
                    if datapoint is not ' ':
                        if datapoint.distance is None:
                            datapoint = ' '
                    row += str(datapoint)
            logger.info(row)

    def get_starting_pipes(self) -> List[Pipe]:
        """ Get the starting pipes next to the S pipe """
        starting_pipes = []
        try:
            pipe = self.data[self.start.up()]
            if pipe.label in ['┃', '┓', '┏']:
                pipe.prev = 'down'
                pipe.distance = 1
                starting_pipes.append(pipe)
        except KeyError:
            logger.debug("No pipe above S")
    
        try:
            pipe = self.data[self.start.down()]
            if pipe.label in ['┃', '┛', '┗']:
                pipe.prev = 'up'
                pipe.distance = 1
                starting_pipes.append(pipe)
        except KeyError:
            logger.debug("No pipe below S")

        try:
            pipe = self.data[self.start.left()]
            if pipe.label in ['━', '┏', '┗']:
                pipe.prev = 'right'
                pipe.distance = 1
                starting_pipes.append(pipe)
        except KeyError:
            logger.debug("No pipe left of S")

        try:
            pipe = self.data[self.start.right()]
            if pipe.label in ['━', '┓', '┛']:
                pipe.prev = 'left'
                pipe.distance = 1
                starting_pipes.append(pipe)
        except KeyError:
            logger.debug("No pipe right of S")

        return starting_pipes

    def get_next_pipe(self, pipe: Pipe) -> Pipe:
        """ Get the next pipe in the direction of the previous pipe """
        logger.debug(f"Getting next pipe for {pipe} @ {pipe.point}, Prev: {pipe.prev}")
        next_direction: str = None
        if pipe.prev == 'up':
            match pipe.label:
                case '┃':
                    next_direction = 'down'
                case '┛':
                    next_direction = 'left'
                case '┗':
                    next_direction = 'right'
        elif pipe.prev == 'down':
            match pipe.label:
                case '┃':
                    next_direction = 'up'
                case '┓':
                    next_direction = 'left'
                case '┏':
                    next_direction = 'right'
        elif pipe.prev == 'left':
            match pipe.label:
                case '━':
                    next_direction = 'right'
                case '┓':
                    next_direction = 'down'
                case '┛':
                    next_direction = 'up'
        elif pipe.prev == 'right':
            match pipe.label:
                case '━':
                    next_direction = 'left'
                case '┏':
                    next_direction = 'down'
                case '┗':
                    next_direction = 'up'
        else:
            raise ValueError("Invalid pipe")
        
        match next_direction:
            case 'up':
                pipe.next = self.data[pipe.point.up()]
                pipe.next.prev = 'down'
            case 'down':
                pipe.next = self.data[pipe.point.down()]
                pipe.next.prev = 'up'
            case 'left':
                pipe.next = self.data[pipe.point.left()]
                pipe.next.prev = 'right'
            case 'right':
                pipe.next = self.data[pipe.point.right()]
                pipe.next.prev = 'left'
            case _:
                raise ValueError("Invalid direction")
        pipe.next = self.data[getattr(pipe.point, next_direction)()]
        return pipe.next

    def walk_pipes(self, pipes: List[Pipe]) -> int:
        """ Walk the pipes """
        longest_distance = 0
        while len(pipes) > 0:
            pipe = pipes.pop(0)
            next_pipe = self.get_next_pipe(pipe)
            if next_pipe.distance is None:
                next_pipe.distance = pipe.distance + 1
                if next_pipe.distance > longest_distance:
                    longest_distance = next_pipe.distance
                pipes.append(next_pipe)
            
        return longest_distance
    

    def paint_pipes(self) -> None:
        """ Paint the pipes """
        # From top to bottom, left to right, Count pipes passed and paint odd numbered locations


def test_sanity():
    """Sanity check """
    assert True


def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    sketch = Sketch(WORKING_DIR + 'input_sample.txt')
    sketch.render()
    starting_pipes = sketch.get_starting_pipes()
    longest = sketch.walk_pipes(starting_pipes)
    sketch.render(show_complete=True)
    logger.info(f"Longest: {longest}")


def test_part_1():
    """Test part 1"""
    logger.info("")
    sketch = Sketch(WORKING_DIR + 'input.txt')
    sketch.render()
    starting_pipes = sketch.get_starting_pipes()
    longest = sketch.walk_pipes(starting_pipes)
    sketch.render(show_complete=True)
    logger.info(f"Longest: {longest}")


def test_sample_2():
    """Test part 2"""
    logger.info("")
    sketch = Sketch(WORKING_DIR + 'input_sample2.txt')
    sketch.render()
    starting_pipes = sketch.get_starting_pipes()
    longest = sketch.walk_pipes(starting_pipes)
    sketch.render(show_complete=True)
    logger.info(f"Longest: {longest}")


def test_part_2():
    """Test part 2"""
    logger.info("")
