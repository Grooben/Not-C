#Author: PeterMaltby
#Created: 18/03/2019

from semantics import Node

class Buffer:  ##Buffer class contains all manipulation code.
    data=[]
    root

    def __init__(self):
        None

    def append(catagory, tokenType, val = None):
        data.append(Node(catagory, tokenType, val))
    
    def Eval():##sets root node and sends program to recursivly gen tree.

        return root

    def Eval( parent, lhn, i = []): ##recursive eval function
        None



GeneratedTrees = []

nodeBuffer = Buffer();
def addNode(catagory, tokenType, val = None):
    nodeBuffer.append(catagory, tokenType, val)
    if catagory == "EOL": GeneratedTrees.append(nodeBuffer.Eval())


#-------------------------------------------------------------