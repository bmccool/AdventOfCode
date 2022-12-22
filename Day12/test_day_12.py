from __future__ import annotations
from collections import deque
from typing import List, Callable
import random
import pytest
import math
import copy
from functools import partial

from termcolor import colored
#colored(tree.height, 'red')


class Node:
    def __init__(self, height: str, index: Index=None):
        self.estimated_total_score = None
        self.height = height
        self.local_score = 1_000_000_000 # higher is worse
        self.previous = None
        self.index = copy.deepcopy(index)
        self.touched = False

    def __repr__(self):
        return f"{self.height}@({self.index.x},{self.index.y}):={self.local_score}"

class Index:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def _set_p(self, i):
        self.x = i[0]
        self.y = i[1]
    
    def _get_p(self):
        return (self.x, self.y)
        
    def _del_p(self):
        del self.x
        del self.y

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    xy = property(
        fget = _get_p,
        fset = _set_p,
        fdel = _del_p
    )

    def __repr__(self):
        return f"{self.xy}"

class Mappy:
    def __init__(self):
        self.nodes = []

    def consume_line(self, line: str):
        row = len(self.nodes)
        self.nodes.append([])
        for n in line.strip():
            column = len(self.nodes[-1])
            self.nodes[-1].append(Node(n, Index(x=column, y=row)))

    def a_star(self, start: Index, end: Index, hueristic: Callable):

        pass

    def get_node(self, index: Index) -> Node:
        return self.nodes[index.y][index.x]

    def contains(self, index) -> bool:
        if index.x < 0:
            return False
        if index.y < 0:
            return False
        if index.x > len(self.nodes[0]) - 1:
            return False
        if index.y > len(self.nodes) - 1:
            return False
        return True

    def reconstruct(self):
        openset = set()
        node = self.end
        steps = 0
        while node.previous:
            node = node.previous
            openset.add(node)
            steps += 1
        return steps, openset

def index_distance(a: Index, b: Index) -> float:
   return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))

def node_distance(a: Node, b: Node) -> float:
   return math.sqrt(((a.index.x - b.index.x) ** 2) + ((a.index.y - b.index.y) ** 2))

def node_a_rel_to_b(a: Node, b: Node) -> str:
    if a.index.x == b.index.x:
        if a.index.y > b.index.y:
            return "^"
        elif a.index.y < b.index.y:
            return "v"
        else:
            return "."
    elif a.index.y == b.index.y:
        if a.index.x > b.index.x:
            return "<"
        elif a.index.x < b.index.x:
            return ">"
        else:
            return "."
    return "."

class AStar:
    def __init__(self, start: Node, end: Node, get_node: Callable, get_neighbors: Callable, part2=False):
        self.open_set = set()
        self.start = start
        self.end = end
        self.heuristic = partial(node_distance, self.end)
        self.get_node = get_node #get_node by index
        self.get_neighbors = get_neighbors #get_neighbors of Node
        self.part2 = part2

        # Opening Step
        self.open_set.add(self.start)
        self.start.local_score = 0
        self.estimated_total_score = self.heuristic(self.start)
        



    def step(self):
        #print("Step")
        #print(self.open_set)
        if len(self.open_set) == 0:
            print("Set was empty, returning")
            return False
        
        node = self.open_set.pop()
        if node.index.xy == self.end.index.xy:
            self.end.previous = node
            self.end.local_score = node.local_score + 1
            print(f"Done, found end with score {self.end.local_score}")
            #TODO should return False here yeah?

        for neighbor in self.get_neighbors(node):

            tentative_local_score = node.local_score + 1
            #print(f"Checking neighbor: {neighbor} with tentative score {tentative_local_score}")
            if (neighbor.height == "a") and (self.part2):
                if neighbor.local_score > 0:
                    neighbor.local_score = 0
                    neighbor.previous = None
                    neighbor.estimated_total_score = self.heuristic(neighbor)
                    self.open_set.add(neighbor)
            elif tentative_local_score < neighbor.local_score:
                neighbor.previous = node
                neighbor.local_score = tentative_local_score
                neighbor.estimated_total_score = tentative_local_score + self.heuristic(neighbor)
                #print(f"Updated score: {neighbor}")
                if neighbor not in self.open_set:
                    #print(f"Adding {neighbor} to openset")
                    self.open_set.add(neighbor)

        #print(self.open_set)
        return True
    
def render(map: Mappy, astr: AStar):
    #print(astr.open_set)
    index = Index()
    #print(f"Highlighting nodes in set: {astr.open_set}")
    for line in map.nodes:
        for node in line:
            highlight = False
            if False: #node.previous != None:
                highlight = True
            else:
                for open_node in astr.open_set:
                    if open_node.index.xy == index.xy:
                        highlight = True
                        break
            if False: #node.previous != None and (node.index.xy != map.start.index.xy) and (node.index.xy != map.end.index.xy):
                print(colored(node_a_rel_to_b(node, node.previous), 'cyan', on_color='on_white'), end="")
            else:
                match (node.height):
                    case "S":
                        if not highlight:
                            print(colored(node.height, 'green'), end="")
                        else:
                            print(colored(node.height, 'green', on_color='on_white'), end="")
                    case "E":
                        if not highlight:
                            print(colored(node.height, 'red'), end="")
                        else:
                            print(colored(node.height, 'red', on_color='on_white'), end="")
                    case _:
                        
                        if not highlight:
                            print(colored(node.height, 'white'), end="")
                        else:
                            print(colored(node.height, 'blue', on_color='on_white'), end="")

            index.right()
        index.down()
        index.x = 0
        print()



def get_neighbors(map: Mappy, node: Node, legal: bool=True):
    neighbors = []

    if node.height == "S":
        legal = False # Anything is legal from starting position
    #TODO will need to handle END condition as well

    def is_doable(map: Mappy, current_node: Node, destination: Index, legal: bool=True) -> bool:
        if not map.contains(destination):
            return False

        current_height = ord(current_node.height)
        destination_height = ord(map.get_node(destination).height)

        if ((destination_height - current_height) > 1) and legal:
            return False
        return True

    # UP
    index = copy.deepcopy(node.index)
    index.up()
    if is_doable(map, node, index, legal):
        neighbors.append(map.get_node(index))
    
    # LEFT
    index = copy.deepcopy(node.index)
    index.left()
    if is_doable(map, node, index, legal):
        neighbors.append(map.get_node(index))

    # DOWN
    index = copy.deepcopy(node.index)
    index.down()
    if is_doable(map, node, index, legal):
        neighbors.append(map.get_node(index))

    # RIGHT
    index = copy.deepcopy(node.index)
    index.right()
    if is_doable(map, node, index, legal):
        neighbors.append(map.get_node(index))
    
    return neighbors

def test_part_1():
    print("Part 1")
    _map = Mappy()
    with open("Day12/Day12Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip()
            _map.consume_line(line)

    index = Index()
    for line in _map.nodes:
        for node in line:
            match (node.height):
                case "S":
                    _map.start = copy.deepcopy(_map.get_node(index))
                case "E":
                    _map.end = copy.deepcopy(_map.get_node(index))
                case _:
                    pass
            index.right()
        index.down()
        index.x = 0

    print(_map.start.height)
    print(_map.end.height)

    import time
    astar = AStar(_map.start, _map.end, _map.get_node, partial(get_neighbors, _map))
    while astar.step():
        continue

    steps, openset = _map.reconstruct()
    steps -= 1 #TODO WHY?  Off by one somewhere
    astar.open_set = openset
    render(_map, astar)
    print(steps)
    assert steps == 350

def test_part_2():
    print("Part 2")
    _map = Mappy()
    with open("Day12/Day12Data.txt", "r") as datafile:
        for line in datafile:
            line = line.strip()
            _map.consume_line(line)

    index = Index()
    for line in _map.nodes:
        for node in line:
            match (node.height):
                case "S":
                    _map.start = copy.deepcopy(_map.get_node(index))
                case "E":
                    _map.end = copy.deepcopy(_map.get_node(index))
                case _:
                    pass
            index.right()
        index.down()
        index.x = 0

    print(_map.start.height)
    print(_map.end.height)

    import time
    astar = AStar(_map.start, _map.end, _map.get_node, partial(get_neighbors, _map), True)
    while astar.step():
        continue

    steps, openset = _map.reconstruct()
    steps -= 1 #TODO WHY?  Off by one somewhere
    astar.open_set = openset
    render(_map, astar)
    print(steps)
    assert steps == 349