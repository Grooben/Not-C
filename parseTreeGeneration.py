#Author: PeterMaltby
#Created: 18/03/2019

#translation table, sorry if this is dirty

assignment = "assignment"
variable = "variable"
operator = "operator"

from semantics import Node

ParseTrees = []

token = []       #test data
token.append(Node(variable, "c"))
token.append(Node(assignment,'='))
token.append(Node(variable, "x"))
token.append(Node(operator, "-"))
token.append(Node(variable, "y"))



def nodeIndex(tokens, criteria):
    i = 0
    for Node in tokens:
        if Node.nodetype == criteria: return i
        i +=1
    return None

#assignment sorting:------------------------------------------
    
def treeGen(tokens):

    if nodeIndex(tokens,assignment) != None :
        root = tokens[nodeIndex(tokens,assignment)]
        del tokens[nodeIndex(tokens,assignment)]

        root.lhn = tokens[nodeIndex(tokens,variable)]
        del tokens[nodeIndex(tokens,variable)] 


    root.PrintTree()


treeGen(token)

#-------------------------------------------------------------





