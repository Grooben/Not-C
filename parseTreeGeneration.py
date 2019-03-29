#Author: PeterMaltby
#Created: 18/03/2019

#translation table, sorry if this is dirty

assignment = "assignment"
variable = "variable"
operator = "operator"

from semantics import Node

GeneratedTrees = []

nodeBuffer = [];##temp  buffer holds all code from a line.
def addNode(catagory, tokenType, val = None):
    nodeBuffer.append(Node(catagory, tokenType, val))


#-------------------------------------------------------------

def EvalBuffer():
    None

