from Day9.Day9 import Rope
print("Part 1: How many unique positions did t")
rope = Rope()
with open("Day9/Day9Data.txt", "r") as datafile:
    for line in datafile:
        rope.multi_move(line.strip())

print(len(rope.tail_map))