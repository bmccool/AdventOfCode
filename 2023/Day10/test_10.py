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
        """ Get the point directly above this one """
        return self + Point(0, -1)

    def down(self) -> Self:
        """ Get the point directly below this one """
        return self + Point(0, 1)

    def left(self) -> Self:
        """ Get the point directly left of this one """
        return self + Point(-1, 0)

    def right(self) -> Self:
        """ Get the point directly right of this one """
        return self + Point(1, 0)

class Pipe():
    """ A pipe, with a label and a point"""
    def __init__(self, label: str, point: Point):
        # Ugh use pattern matching lol
        if label == '|':
            self.label = '┃'
        elif label == '-':
            self.label = '━'
        elif label == 'L':
            self.label = '┗'
        elif label == 'J':
            self.label = '┛'
        elif label == '7':
            self.label = '┓'
        elif label == 'F':
            self.label = '┏'
        elif label == 'S':
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
    """ Sketch of a 2D grid of pipes """
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
                    if char != ' ' and char != '\n' and char != '.':
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
                    if datapoint != ' ':
                        if datapoint.distance is None:
                            datapoint = ' '
                    row += str(datapoint)
            log_func(row)

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

    def replace_starting_pipe(self) -> None:
        """ Replace the starting pipe (S) with a normal pipe (used for painting purposes)"""
        pipes_to_start = [pipe.prev for pipe in self.get_starting_pipes()]
        if "down" in pipes_to_start and "up" in pipes_to_start:
            self.data[self.start].label = '┃'
        if "left" in pipes_to_start and "right" in pipes_to_start:
            self.data[self.start].label = '━'
        if "down" in pipes_to_start and "right" in pipes_to_start:
            self.data[self.start].label = '┛'
        if "down" in pipes_to_start and "left" in pipes_to_start:
            self.data[self.start].label = '┗'
        if "up" in pipes_to_start and "right" in pipes_to_start:
            self.data[self.start].label = '┓'
        if "up" in pipes_to_start and "left" in pipes_to_start:
            self.data[self.start].label = '┏'

    def paint_pipes(self) -> None:
        """ Paint the pipes """
        # From top to bottom, left to right, Count pipes passed and paint odd numbered locations
        inside_locations = 0

        for y in range(self.max.y + 1):
            inside = False
            inside_dir = None
            row = ""
            for x in range(self.max.x + 1):
                if Point(x,y) in self.data:
                    pipe = self.data[Point(x,y)]
                    if pipe.distance is not None:
                        #logger.info("This is a pipe can't paint")
                        match (inside, inside_dir, self.data[Point(x,y)].label):
                            case (_, _, '┃'):
                                inside = not inside
                                inside_dir = 'in' if inside else 'left'
                            case (_, _, '━'):
                                logger.debug("Do nothing?")
                            case (_, _, '┏'):
                                inside_dir = 'up' if inside else 'down'
                            case (_, _, '┗'):
                                inside_dir = 'down' if inside else 'up'
                            case (_, _, '┓'):
                                inside = True if inside_dir == 'up' else False
                                inside_dir = 'in' if inside else 'down'
                            case (_, _, '┛'):
                                inside = True if inside_dir == 'down' else False
                                inside_dir = 'in' if inside else 'up'

                        row += self.data[Point(x,y)].label
                        continue
                if inside:
                    row += 'I'
                    inside_locations += 1
                else:
                    row += 'O'
            logger.info(row)
        return inside_locations


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
    sketch.replace_starting_pipe()
    locations = sketch.paint_pipes()
    logger.info(f"Locations: {locations}")
    assert locations == 4

def test_sample_3():
    """Test part 3"""
    logger.info("")
    sketch = Sketch(WORKING_DIR + 'input_sample3.txt')
    sketch.render()
    starting_pipes = sketch.get_starting_pipes()
    longest = sketch.walk_pipes(starting_pipes)
    sketch.render(show_complete=True)
    logger.info(f"Longest: {longest}")
    sketch.replace_starting_pipe()
    locations = sketch.paint_pipes()
    logger.info(f"Locations: {locations}")
    assert locations == 8


def test_part_2():
    """Test part 2"""
    logger.info("")
    sketch = Sketch(WORKING_DIR + 'input.txt')
    sketch.render()
    starting_pipes = sketch.get_starting_pipes()
    longest = sketch.walk_pipes(starting_pipes)
    sketch.render(show_complete=True)
    logger.info(f"Longest: {longest}")
    sketch.replace_starting_pipe()
    locations = sketch.paint_pipes()
    logger.info(f"Locations: {locations}")
    assert locations == 445
