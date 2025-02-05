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
import csv

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
    def __init__(self, data):
        self.id = data["id"]
        self.question = data["question"]
        self.difficulty = data["difficulty"]
        self.children = []
        
        if self.id == 0:
            self.is_root = True
        else:
            self.is_root = False

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

    def to_dict(self):
        '''
        Convert object to dictionary.
        Used with flask's jsonify
        '''
        return {
            "id" : self.id,
            "question" : self.question,
            "difficulty" : self.difficulty,
            "children_arr" : self.children,
            "is_root" : self.is_root
        }


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
    return open(file, mode, encoding="utf-8")


def populate_tree(file_path):
    '''
    Main:
    Construct tree from csv
    '''
    nodes = []
    # CSV to Dictionary
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    
    for element in data:
        # Set root
        if element["id"] == '0':
            node = Tree({
                "id" : 0,
                "question" : element["question"],
                "difficulty" : element["difficulty"]})
        else:
            node = Tree({
                "id" : int(element["id"]),
                "question" : element["question"],
                "difficulty" : element["difficulty"]})
        
        # Add children
        if element["easy_id"] != "n/a":
            node.add_child(int(element["easy_id"]))
        if element["harder_id"] != "n/a":
            node.add_child(int(element["harder_id"]))
        
        nodes.append(node)
        
    return nodes
