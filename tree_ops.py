# Code inspired by this website:
# https://www.tutorialspoint.com/python/python_binary_tree.htm


class BinaryTreeNode:
    # Allows for a root node to be added to the tree, not required
    def __init__(self, pixel_id=None):
        self.data = pixel_id
        self.left = None
        self.right = None

    def insert_node(self, pixel_data):
        # Check if the node being inserted is the root node
        if self.data is None:
            self.data = pixel_data

        # The node being inserted will not be the root and will lie in one of the branches of the tree
        else:
            if pixel_data < self.data:
                if self.left is None:
                    self.left = BinaryTreeNode(pixel_data)
                else:
                    self.left.insert_node(pixel_data)
            elif pixel_data > self.data:
                if self.right is None:
                    self.right = BinaryTreeNode(pixel_data)
                else:
                    self.right.insert_node(pixel_data)

    # Debugging purposes
    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print(self.data)
        if self.right:
            self.right.print_tree()
