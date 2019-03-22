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
root.lhn = Node("variable", "c")
root.rhn = Node("operator", "-")
root.rhn.rhn = Node("variable", "x")
root.rhn.lhn = Node("variable", "y")

root.PrintTree()
