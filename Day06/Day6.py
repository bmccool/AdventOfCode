from typing import Tuple
from collections import deque 



class Window:
    def __init__(self, length: int=4):
        self.contents = deque()
        self.length = length
        self.index = 0

    def feed(self, character: str):
        if len(self.contents) == self.length:
            self.contents.popleft()
        elif len(self.contents) > self.length:
            print("TODO this shouldn't happen, handle this error case")

        self.contents.append(character)
        self.index += 1

    def is_start_marker(self):
        if len(self.contents) != self.length:
            return False
        unique_chars = set()
        for c in range(self.length):
            if self.contents[c] in unique_chars:
                return False
            else:
                unique_chars.add(self.contents[c])
        return True



print("Part 1:")
window = Window()
with open("Day6Data.txt", "r") as datafile:
    for line in datafile:
        for character in line:
            window.feed(character)
            if window.is_start_marker():
                print(window.index)
                print(window.contents)
                break

print("Part 2:")
window = Window(length=14)
with open("Day6Data.txt", "r") as datafile:
    for line in datafile:
        for character in line:
            window.feed(character)
            if window.is_start_marker():
                print(window.index)
                print(window.contents)
                break

