class Round:
    def __init__(self, opponent_move: str, suggested_move: str, part2: bool = False):
        if opponent_move not in ["A", "B", "C"] or suggested_move not in ["X", "Y", "Z"]:
            print(f"INVALID INPUT: {opponent_move}, {suggested_move}")

        if part2:
            match (opponent_move, suggested_move):
                case ("A", "X"):
                    suggested_move = "Z"
                case ("A", "Y"):
                    suggested_move = "X"
                case ("A", "Z"):
                    suggested_move = "Y"
                case ("B", "X"):
                    suggested_move = "X"
                case ("B", "Y"):
                    suggested_move = "Y"
                case ("B", "Z"):
                    suggested_move = "Z"
                case ("C", "X"):
                    suggested_move = "Y"
                case ("C", "Y"):
                    suggested_move = "Z"
                case ("C", "Z"):
                    suggested_move = "X"
                case _:
                    print("Code not found")

        self.opponent_move = opponent_move
        self.suggested_move = suggested_move

    def score(self):
        match (self.opponent_move, self.suggested_move):
            case ("A", "X"):
                ret_val = 1 + 3
            case ("A", "Y"):
                ret_val = 2 + 6
            case ("A", "Z"):
                ret_val = 3 + 0
            case ("B", "X"):
                ret_val = 1 + 0
            case ("B", "Y"):
                ret_val = 2 + 3
            case ("B", "Z"):
                ret_val = 3 + 6
            case ("C", "X"):
                ret_val = 1 + 6
            case ("C", "Y"):
                ret_val = 2 + 0
            case ("C", "Z"):
                ret_val = 3 + 3
            case _:
                print("Code not found")
        return ret_val

print("Part 1:")
total_score = 0
with open("Day2Data.txt", "r") as datafile:
    for line in datafile:
        col1, col2 = line.split()
        total_score += Round(col1, col2).score()
print(total_score)

print("Part 2:")
total_score = 0
with open("Day2Data.txt", "r") as datafile:
    for line in datafile:
        col1, col2 = line.split()
        total_score += Round(col1, col2, part2=True).score()
print(total_score)