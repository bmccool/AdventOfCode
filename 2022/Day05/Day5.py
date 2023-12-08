from collections import deque 



class Stack:
    """ 0-index is top of stack, n-index is bottom """
    def __init__(self):
        self.contents = deque()

    def build(self, item: str):
        self.contents.append(item)

    def top(self):
        return self.contents[-1]

    def pop(self):
        return self.contents.pop()

    def drop(self, item: str):
        self.contents.append(item)

    def __len__(self):
        return len(self.contents)

    def __getitem__(self, item):
        return self.contents[item]

    def push(self, item: str):
        self.contents.appendleft(item)

class Pile:
    def __init__(self):
        self.map_complete = False
        self.stacks = []

    def render(self):
        max_len = 0
        for stack in self.stacks:
            if len(stack) > max_len:
                max_len = len(stack)
        for level in range(max_len, 0, -1):
            for stack in self.stacks:
                if level > len(stack):
                    print("    ", end="")
                else:
                    print(f"[{stack[level-1]}] ", end="")
            print("")

    def read_map_line(self, line :str):
        """
                                [R] [J] [W]
                    [R] [N]     [T] [T] [C]
        [R]         [P] [G]     [J] [P] [T]
        [Q]     [C] [M] [V]     [F] [F] [H]
        [G] [P] [M] [S] [Z]     [Z] [C] [Q]
        [P] [C] [P] [Q] [J] [J] [P] [H] [Z]
        [C] [T] [H] [T] [H] [P] [G] [L] [V]
        [F] [W] [B] [L] [P] [D] [L] [N] [G]
        1   2   3   4   5   6   7   8   9
        """
        if "1   2" in line:
            return
        if line.strip() == "":
            for stack in self.stacks:
                stack.contents.reverse()
            self.map_complete = True
            return
        line = line.strip('\n')
        num_stacks = int((len(line) + 1) / 4)
        while len(self.stacks) != num_stacks:
            self.stacks.append(Stack())
        for stack in range(num_stacks):
            #print(f"Checking stack {stack} with line {line}")
            if line[0:4] != "    ":
                #print(line)
                #print(f"Stacks[{stack}] = {line[1]}")
                self.stacks[stack].build((line[1]))
            line = line[4:]

    def execute_move(self, move :str):
        """ Crates are moved one at a time! """
        """move 3 from 1 to 3"""
        move = move.strip().split()
        num_to_move = int(move[1])
        origin_stack = int(move[3]) - 1 # 1 -> 0 Indexed
        target_stack = int(move[5]) - 1 # 1 -> 0 Indexed
        while num_to_move > 0:
            crate = self.stacks[origin_stack].pop()
            self.stacks[target_stack].drop(crate)
            num_to_move -= 1

    def execute_move_multiple(self, move :str):
        """ Crates are moved all at once! """
        """move 3 from 1 to 3"""
        move = move.strip().split()
        num_to_move = int(move[1])
        origin_stack = int(move[3]) - 1 # 1 -> 0 Indexed
        target_stack = int(move[5]) - 1 # 1 -> 0 Indexed
        crane = deque()
        for _ in range(num_to_move):
            crane.append(self.stacks[origin_stack].pop())

        for _ in range(num_to_move):
            self.stacks[target_stack].drop(crane.pop())




print("Part 1:")
pile = Pile()
with open("Day5Data.txt", "r") as datafile:
    for line in datafile:
        if not pile.map_complete:
            pile.read_map_line(line)
        else:
            pile.execute_move(line)

for stack in pile.stacks:
    print(stack.top(), end="")
print()
pile.render()

print("Part 2:")
pile = Pile()
with open("Day5Data.txt", "r") as datafile:
    for line in datafile:
        if not pile.map_complete:
            pile.read_map_line(line)
        else:
            pile.execute_move_multiple(line)

for stack in pile.stacks:
    print(stack.top(), end="")
print()
pile.render()