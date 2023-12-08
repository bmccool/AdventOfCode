from termcolor import colored

""" Implement a class Tree with a list "self.visible" which contains "FROM_LEFT, "FROM_UP", etc. """
""" Also, give it LRUD links to other trees or some constant for edgees """

class Tree:
    def __init__(self, height, left=None, right=None, up=None, down=None):
        self.height = int(height)
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.visible = []
        self.x = None # May not be needed, but allows coordinates of trees to be verified wrt the forest
        self.y = None

class Forest:
    """ Helper class to provide interface to instantiate and manipulate Trees """
    def __init__(self):
        self.lines_completed = 0
        self.trees_completed = 0
        self.origin = None
        self.previous_tree = None
        self.up_tree = None

    def add_tree_line(self, line: str):
        first_tree = True
        if self.trees_completed == 0:
            # Special case, first line
            for h in line:
                new_tree = Tree(h)
                if self.trees_completed == 0:
                    self.origin = new_tree
                else:
                    new_tree.left = self.previous_tree
                    self.previous_tree.right = new_tree
                self.previous_tree = new_tree
                self.trees_completed += 1

        else:
            # Get up tree (follower tree in previous row)
            up_tree = self.origin
            for _ in range(self.lines_completed - 1):
                up_tree = up_tree.down

            # Begin adding trees
            for h in line:
                new_tree = Tree(h)
                if not first_tree:
                    new_tree.left = self.previous_tree
                    self.previous_tree.right = new_tree
                up_tree.down = new_tree
                new_tree.up = up_tree
                self.previous_tree = new_tree
                up_tree = up_tree.right
                self.trees_completed += 1
                first_tree = False


        self.lines_completed += 1

    def render(self):
        tree = self.origin
        while True:
            if tree.visible:
                print(colored(tree.height, 'red'), end="")
            else:
                print(tree.height, end="")
            if tree.right is None:
                print("")
                if tree.down is None:
                    return
                else:
                    tree = tree.down
                    while tree.left:
                        tree = tree.left
            else:
                tree = tree.right

    def calculate_visible(self):
        """ From origin, calculate visibility down, then up.  Then move over one column.
        When we get to the end, beging calculating visibility left then right, then move
        down one row. Keep track of total number visible, and mark each tree with "FROM_X
        in its visible list """
        num_visible = 0
        tree = self.origin

        # VERTICAL,  L-> R
        while True:
            tallest = -1
            direction = "FROM_TOP"
            while True:
                if tree.height > tallest:
                    if not tree.visible:
                        num_visible += 1
                    tree.visible.append(direction)
                    tallest = tree.height
                if tree.down:
                    tree = tree.down
                else:
                    break

            direction = "FROM_BOTTOM"
            tallest = -1
            while True:
                if tree.height > tallest:
                    if not tree.visible:
                        num_visible += 1
                    tree.visible.append(direction)
                    tallest = tree.height
                if tree.up:
                    tree = tree.up
                else:
                    break
            if tree.right:
                tree = tree.right
            else:
                break
        
        # HORIZONTAL,  U -> D
        while True:
            tallest = -1
            direction = "FROM_RIGHT"
            while True:
                if tree.height > tallest:
                    if not tree.visible:
                        num_visible += 1
                    tree.visible.append(direction)
                    tallest = tree.height
                if tree.left:
                    tree = tree.left
                else:
                    break

            direction = "FROM_LEFT"
            tallest = -1
            while True:
                if tree.height > tallest:
                    if not tree.visible:
                        num_visible += 1
                    tree.visible.append(direction)
                    tallest = tree.height
                if tree.right:
                    tree = tree.right
                else:
                    break
            if tree.down:
                tree = tree.down
            else:
                break

        return num_visible


    def find_best_treehouse_naive(self):
        """Best treehouse is one in which product of view distance in cardinal directions is greatest """
        """ This is naive because we are simply going to score each tree and keep the highest one """
        """ Other potentially better solutions would understand that the best score is roughly the tallest
        tree in the center of the map, only check trees which have a chance of being best """
        tree = self.origin
        max_score = 0
        while True:
            score = self.score_tree(tree)
            if score > max_score:
                max_score = score
            if tree.right:
                tree = tree.right
            elif tree.down:
                tree = tree.down
                while tree.left:
                    tree = tree.left
            else:
                break
        return max_score
                
                    
            

    def score_tree(self, tree: Tree):
        base = tree
        left_score = 0
        while tree.left:
            left_score += 1
            if tree.left.height < base.height:
                tree = tree.left
            else:
                break

        tree = base
        right_score = 0
        while tree.right:
            right_score += 1
            if tree.right.height < base.height:
                tree = tree.right
            else:
                break

        tree = base
        up_score = 0
        while tree.up:
            up_score += 1
            if tree.up.height < base.height:
                tree = tree.up
            else:
                break

        tree = base
        down_score = 0
        while tree.down:
            down_score += 1
            if tree.down.height < base.height:
                tree = tree.down
            else:
                break


        return (up_score * down_score * left_score * right_score)


    




print("Part 1: How many trees are visible from outside the grid?")
forest = Forest()
with open("Day8Data.txt", "r") as datafile:
    for line in datafile:
        forest.add_tree_line(line.strip())

num_visible = forest.calculate_visible()
forest.render()
print(num_visible)


print("Part 2: What is the highest scenic score possible for any tree?")
max_score = forest.find_best_treehouse_naive()
print(max_score)
