#Author: PeterMaltby
#Created: 18/03/2019

#translation table, sorry if this is dirty

assignment = "assignment"
variable = "variable"
operator = "operator"


#parse tree generation.
#def __init__(self, nodetype, char, lhn = None, rhn = None):
from semantics import Node

root = Node(assignment,'=')
root.lhn = Node("variable", "x")
root.rhn = Node("operator", "-")


root.PrintTree()
