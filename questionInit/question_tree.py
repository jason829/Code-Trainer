'''
Module for populating a tree structure.
Contains Tree class initilisation and tree operations.
HOW TO USE:
------------------------------------
populate_tree(file_path)
where file_path is the path of the csv file used

EXAMPLE:
questionInit/staticQuestions.csv
'''

class Tree:
    ''' TREE DEFINITION
    Attribute: 
        data - CSV of question plus answer,
        is_root - Boolean,
    Methods:
        add_child - Add child to parent,
    Info:
        Currently just using this to create a static tree of 
        set questions. thinking this can be used as a guide
        for a model to follow this defined structure. Not
        sure yet still early days.
    '''

    def __init__(self, data, is_root):
        self.data = data
        self.children = []
        self.is_root = is_root
    def add_child(self, node):
        '''
        Add child node to the list of children that the parent has
        '''
        self.children.append(node)
    def show_attributes(self):
        '''
        Return the objects attributes
        '''
        return self.data, self.children, self.is_root


def delete_node(root, target):
    '''
    Function - Deletes target node
        Parameters: 
            root - Root node
            target - target node for deletion
        Info: N/A
    '''

    if root is None:
        return
    root.children = [child for child in root.children if child.data != target]
    for child in root.children:
        delete_node(child, target)

def insert_node(root, node):
    '''
    Function - Adds target node
        Parameters: 
            root - Root node
            node - Insertion node 
        Info: N/A
    '''

    if root is None:
        root = node
    else:
        root.add_child(node)


def read_file(file, mode):
    '''
    Function - returns opened file
        Parameters: 
            file - File Path
            mode - open mode
        Info: N/A
    '''

    if mode == "w":
        return file.close(), "Write mode, killing to avoid destructive edits"
    return open(file, mode)


def populate_tree(file_path):
    '''
    Main:
    Populate tree with questions read from csv file
    '''

    list_of_all_nodes = []
    # Populate list with nodes from CSV
    try:
        file = read_file(file_path, "r")
        for line in file:
            split_lines = line.strip().split(",")
            # Skip the first line
            if split_lines[0] == 'id':
                continue
            # Root of tree is index 0
            if int(split_lines[0]) == 0:
                node = Tree(split_lines, True)
                list_of_all_nodes.append((0,node))
            else:
                node = Tree(split_lines, False)
                list_of_all_nodes.append((int(node.data[0]), node))
        file.close()
    except Exception as err:
        print("Error: ", err)
    # Create edges from parent to child
    for node in list_of_all_nodes:
        node_data = node[1]
        if node_data.data[3] == 'n/a' and node_data.data[4] == 'n/a':
            continue
        node_data.add_child(int(node_data.data[3]))
        node_data.add_child(int(node_data.data[4]))
