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
    logger.info("***** Deleting node, ", target, " *****")
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
        node - Insertion node 
    Info: N/A
'''
def insert_node(root, node):
    logger.info("***** Inserting node, ", node," *****")
    if root is None:
        logger.info("Root is undefined")
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
def populateTree(filePath):
    logger.info("*** Creating Tree with,", filePath, " ***")
    listOfAllNodes = []
    # Populate list with nodes from CSV
    try:
        file = readFile(filePath, "r")
        for line in file:
            splitLines = line.strip().split(",");
            # Skip the first line
            if splitLines[0] == 'id': 
                continue
            # Root of tree is index 0
            if int(splitLines[0]) == 0:
                node = Tree(splitLines, True)
                listOfAllNodes.append((0,node))
            else:
                node = Tree(splitLines, False)
                listOfAllNodes.append((int(node.data[0]), node))
        file.close()
    except Exception as err:
        logger.error("Error occurred: ", err)
    
    # Create edges from parent to child
    for node in listOfAllNodes:
        nodeData = node[1]
        if nodeData.data[3] == 'n/a' and nodeData.data[4] == 'n/a':
            continue
        nodeData.addChild(int(nodeData.data[3])); nodeData.addChild(int(nodeData.data[4]))

populateTree("questionInit/staticQuestions.csv")