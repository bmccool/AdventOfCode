from typing import Set




class Rucksack:
    def __init__(self, contents: str):
        self.contents = contents.strip()
        halfsize = int(len(contents) / 2)
        self.compartment1 = contents[:halfsize]
        self.compartment2 = contents[halfsize:]

        print(contents)
        print(f"{self.compartment1} | {self.compartment2} ----> {self.get_common_items()}")

    def get_common_items(self) -> Set[str]:
        " Return a Set of all items (letters) present in both compartments. "
        common_items = set()
        for item in self.compartment1:
            if item in self.compartment2:
                common_items.update(item)

        return common_items

class SafetyGroup:
    def __init__(self, max_size=3):
        self.elves = []
        self.max_size = max_size

    def add(self, rucksack: Rucksack):
        if self.is_full():
            print("Can't add to full safetygroup!")
            return
        
        self.elves.append(rucksack)


    def is_full(self):
        if len(self.elves) == self.max_size:
            return True
        return False

    def find_badge(self):
        """ Find the common item among all elves in this group """
        for item in self.elves[0].contents:
            for elf in self.elves:
                if item not in elf.contents:
                    break
            else:
                return item

def score_items(items: Set[str]) -> int:
    score = 0
    for item in items:
        if item.isupper():
            score += (ord(item) - ord("A") + 27)
        else:
            score += (ord(item) - ord("a") + 1)
    return score





print("Part 1:")
common_items = set()
running_score = 0
with open("Day3Data.txt", "r") as datafile:
    for line in datafile:
        rucksack = Rucksack(line)
        running_score += score_items(rucksack.get_common_items())
        common_items.update(rucksack.get_common_items())
print(common_items)
print(score_items(common_items))
print(running_score)


print("Part 2:")
common_items = set()
running_score = 0
safety_group = SafetyGroup()
with open("Day3Data.txt", "r") as datafile:
    for line in datafile:
        rucksack = Rucksack(line)
        safety_group.add(rucksack)
        if safety_group.is_full():
            badge = safety_group.find_badge()
            running_score += score_items(set(badge))
            safety_group = SafetyGroup()
            common_items.update(set(badge))
print(common_items)
print(score_items(common_items))
print(running_score)