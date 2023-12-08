
""" FTree should implement a file tree in which a particular node records the space of all files at this level and all it's children """

class FTreeNode:
    def __init__(self, name: str, parent=None):
        self.usage = 0
        self.children = {}
        self.files = {}
        self.name = name
        self.parent = parent



class FTree:
    def __init__(self):
        self.root = FTreeNode("/")
        self.current_node = self.root
        self.accumulator = 0
        self.smallest_node = self.root #TODO this is a lazy way of tracking smallest deletable node.  Probably a better way to do this.

    def cd(self, dest: str):
        if dest == "/":
            self.current_node = self.root
        elif dest == "..":
            self.current_node = self.current_node.parent
        else:
            self.current_node = self.current_node.children[dest]

    def dir(self, dest: str):
        """ Create node at dest and make current node it's parent """
        if dest not in self.current_node.children:
            self.current_node.children[dest] = FTreeNode(dest, self.current_node)
    
    def get_usage(self):
        return self.depth_first_sum(self.root)

    def depth_first_sum(self, node: FTreeNode):
        # 1. Get usage of all children
        for child in node.children:
            node.usage += self.depth_first_sum(node.children[child])

        # 2. Get usage of all files
        node.usage += sum(node.files.values())

        # 3. Return node.usage
        return node.usage

    def get_cumulative_usage_under(self, node: FTreeNode, threshold: int=100_000):
        # 1. Check all children first
        # 2. If this node's sum matches, accumulate it
        # 3. Return
        for child in node.children:
            self.get_cumulative_usage_under(node.children[child], threshold=threshold)

        # 2. If this node's sum matches, accumulate it
        if node.usage < threshold:
            #print(f"{node.usage} is less than {threshold}, so adding it to accumulator!")
            self.accumulator += node.usage

        # 3. Return node.usage
        return node.usage

    def get_smallest_dir_more_than(self, node: FTreeNode, threshold: int):
        for child in node.children:
            self.get_smallest_dir_more_than(node.children[child], threshold=threshold)
        if (node.usage >= threshold) and (node.usage < self.smallest_node.usage):
            self.smallest_node = node

    def render(self, node: FTreeNode, level=0):
        # 1. Print directory usage under level tab
        print(("  " * level) + f"- {node.name} node uses {node.usage}")
        # 2. print file usage under level + 1 tab
        for file in node.files:
            print(("  " * (level + 1)) + f"- {file} file uses {node.files[file]}")
        # 3. print directory under level + 1 tab
        for child in node.children:
            self.render(node.children[child], level + 1)




print("Part 1:")
tree = FTree()
with open("Day7Data.txt", "r") as datafile:
    for line in datafile:
        match (line.strip().split()):
            case ["$", "cd", path]:
                tree.cd(path)
            case ["$", "ls"]:
                pass
            case ["dir", path]:
                tree.dir(path)
            case [size, filename]:
                tree.current_node.files[filename] = int(size)

full_usage = tree.get_usage()
print(full_usage)

tree.get_cumulative_usage_under(tree.root)
print(tree.accumulator)
           

print("Part 2: Find the smallest directory to delete such that unused space is at least 30_000_000, Total disk size is 70_000_000")
needed_space = 30_000_000
total_size = 70_000_000
total_usage = tree.root.usage
smallest_deletion = total_usage - (total_size - needed_space)
print(f"Smallest allowable deletion is: {smallest_deletion}")
tree.get_smallest_dir_more_than(tree.root, smallest_deletion)
print(tree.smallest_node.usage)


#tree.render(tree.root)