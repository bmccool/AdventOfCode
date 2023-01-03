from typing import Tuple
from collections import deque 
from termcolor import colored


class Rope:
    def __init__(self):
        # Assume it always starts at (0, 0)
        self.H = (0,0) # Head
        self.T = (0,0) # Tail
        self.S = (0,0) # Start
        self.tail_map = set()

    def move(self, direction: str):
        match(direction.upper()):
            case "L":
                self.H = (self.H[0] - 1, self.H[1])
            case "R":
                self.H = (self.H[0] + 1, self.H[1])
            case "D":
                self.H = (self.H[0],     self.H[1] - 1)
            case "U":
                self.H = (self.H[0],     self.H[1] + 1)
        self.follow()
        #print(f"H:{self.H} T:{self.T}")
        self.tail_map.add((self.T))
        #print(self.tail_map)

    def multi_move(self, move: str):
        move = move.split()
        for _ in range(int(move[1])):
            self.move(move[0])

    def follow(self):
        move = None
        if self.H == self.T:
            return
        if (abs(self.H[0] - self.T[0]) > 1):
            move = "X"
            self.T = (self.T[0] + (1 if ((self.H[0] - self.T[0]) > 0) else -1), self.T[1])
        elif (abs(self.H[1] - self.T[1]) > 1):
            move = "Y"
            self.T = (self.T[0], self.T[1] + (1 if ((self.H[1] - self.T[1]) > 0) else -1))

        if move == "X":
            if (abs(self.H[1] - self.T[1]) > 0):
                self.T = (self.T[0], self.T[1] + (1 if ((self.H[1] - self.T[1]) > 0) else -1))
        if move == "Y":
            if (abs(self.H[0] - self.T[0]) > 0):
                self.T = (self.T[0] + (1 if ((self.H[0] - self.T[0]) > 0) else -1), self.T[1])
