from typing import List

class Elf:
    def __init__(self):
        self.inventory = []

    def add(self, item: int):
        self.inventory.append(item)

    def get_total(self):
        total = 0
        for item in self.inventory:
            total += item

        return total

def sorting_func(elf: Elf):
    return elf.get_total()

def keep_heaviest_elves(elves: List[Elf], new_elf: Elf, num_to_keep: int=3):
    # elves is a sorted list, lightest elf at p0, heaviest at pN
    if new_elf.get_total() > elves[0].get_total(): # Heavier than the lightest fat elf
        elves[0] = new_elf
        elves[0].inventory = new_elf.inventory
        elves.sort(key=sorting_func)


elf_list = [Elf(), Elf(), Elf()]

heaviest_elf = Elf()
this_elf = Elf()
with open("Day1Data.txt", "r") as datafile:
    for line in datafile:
        if line.strip():
            this_elf.add(int(line))
        else: # Empty line, do elf comparisons
            keep_heaviest_elves(elf_list, this_elf, 3)
            #if this_elf.get_total() > heaviest_elf.get_total():
            #    heaviest_elf = this_elf
            this_elf = Elf()

print("Heaviest Elves are:")
sum = 0
for elf in elf_list:
    #print(elf.inventory)
    print(elf.get_total())
    sum += elf.get_total()
print(f"Total sum is: {sum}")
print(f"Elves in list is {len(elf_list)}")