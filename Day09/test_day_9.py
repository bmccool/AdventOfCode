from Day09.Day9 import Rope, Ropes

def test_part_1():
    print()
    print("Part 1: How many unique positions did the tail of the rope visit?")
    rope = Rope()
    with open("Day09/Day9Data.txt", "r") as datafile:
        for line in datafile:
            rope.multi_move(line.strip())

    print(len(rope.tail_map))
    assert len(rope.tail_map) == 6023

def test_part_2():
    print()
    print("Part 1: How many unique positions did the tail of the rope visit?")
    rope = Ropes(10)
    with open("Day09/Day9Data.txt", "r") as datafile:
        for line in datafile:
            rope.multi_move(line.strip())

    print(len(rope.ropes[8].tail_map))
    assert len(rope.ropes[8].tail_map) == 2533