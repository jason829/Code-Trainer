import logging
logger = logging.getLogger(__name__)

''' TREE DEFINITION
Attribute: 
    data - CSV of question plus answer,
    isRoot - Boolean,
Methods:
    addChild - Add child to parent,
Info:
    Currently just using this to create a static tree of 
    set questions. thinking this can be used as a guide
    for a model to follow this defined structure. Not
    sure yet still early days.
'''
class Tree:
    def __init__(self, data, isRoot):
        self.data = data
        self.children = []
        self.isRoot = isRoot
    def addChild(self, node):
        self.children.append(node)

'''
Function - Deletes target node
    Parameters: 
        root - Root node
        target - target node for deletion
    Info: N/A
'''
def deleteNode(root, target):
    logger.info("*****Deleting node, ", target, " *****")
    if root is None:
        logger.info("Root is undefined")
        return None
    root.children = [child for child in root.children if child.data != target]
    for child in root.children:
        deleteNode(child, target)

'''
Function - Adds target node
    Parameters: 
        root - Root node
        target - target node for deletion
    Info: N/A
'''
def insert_node(root, node):
    if root is None:
        root = node
    else:
        root.add_child(node)

'''
Function - returns opened file
    Parameters: 
        file - File Path
        mode - open mode
    Info: N/A
'''
def readFile(file, mode):
    if mode == "w":
        logger.error("Write mode... Killing to keep file safe")
    else:
        logger.info("Opening file...")
        return open(file, mode)

'''
Main:
Populate tree with questions read from csv file
'''
def main():
    file = readFile("questionInit/staticQuestions.csv", "r")
    