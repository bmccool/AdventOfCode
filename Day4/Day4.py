from typing import Tuple

#RangePair = namedtuple('RangePair', ['a', 'b'])

def is_redundant(a: range, b: range) -> bool:
    if len(a) > len(b):
        # A is bigger
        if (a.start <= b.start) and (a.stop >= b.stop):
            return True
    else:
        # B is bigger
        if (b.start <= a.start) and (b.stop >= a.stop):
            return True
    return False

def is_overlap(a: range, b: range) -> bool:
    if (a.start <= b.start <= a.stop) or (b.start <= a.start <= b.stop):
        return True
    return False

def parse_assignment_pair(line: str) -> Tuple[range, range]:
    "20-45,13-44"
    line = line.strip()
    range_strings = line.split(",")
    range_a = range(int(range_strings[0].split("-")[0]), int(range_strings[0].split("-")[1]))
    range_b = range(int(range_strings[1].split("-")[0]), int(range_strings[1].split("-")[1]))
    return (range_a, range_b)

print("Part 1:")
redundant_pairs = 0
with open("Day4Data.txt", "r") as datafile:
    for line in datafile:
        range_a, range_b = parse_assignment_pair(line)
        if is_redundant(range_a, range_b):
            redundant_pairs += 1

print(f"Redundant pairs: {redundant_pairs}")


print("Part 1:")
overlapping_pairs = 0
with open("Day4Data.txt", "r") as datafile:
    for line in datafile:
        range_a, range_b = parse_assignment_pair(line)
        if is_overlap(range_a, range_b):
            overlapping_pairs += 1

print(f"Overlapping pairs: {overlapping_pairs}")
