#Author: PeterMaltby
#Created: 18/03/2019

#translation table, sorry if this is dirty

assignment = "assignment"
variable = "variable"
operator = "operator"

class Node: 
    def __init__(self, type, value, lhn = None, rhn = None):
        self.type = type
        self.value = value 
        self.lhn = lhn
        self.rhn = rhn

ParseTrees = []

token = []       #test data
token.append(Node(variable, "c"))
token.append(Node(assignment,'='))
token.append(Node(variable, "x"))
token.append(Node(operator, "-"))
token.append(Node(variable, "y"))
token.append(Node(operator, "+"))
token.append(Node(variable, "z"))



def nodeIndex(tokens, criteria):
    i = 0
    for Node in tokens:
        if Node.nodetype == criteria: return i
        i +=1
    return None



#assignment sorting:------------------------------------------
    
def treeGen(tokens):

    if nodeIndex(tokens,assignment) != None :#checks if list contains assignment operator
        root = tokens[nodeIndex(tokens,assignment)]
        del tokens[nodeIndex(tokens,assignment)]#sets assignment as root.

        root.lhn = tokens[nodeIndex(tokens,variable)]
        del tokens[nodeIndex(tokens,variable)] 

        temp = root#tree save point for recursive programs.
        while nodeIndex(tokens,operator) != None :#recursivly builds right of tree.
            temp.rhn=tokens[nodeIndex(tokens,operator)]
            del tokens[nodeIndex(tokens,operator)]
            
            temp= temp.rhn#rebase temp for recursion using object refrence.
            temp.lhn=tokens[nodeIndex(tokens,variable)]
            del tokens[nodeIndex(tokens,variable)]

        temp.rhn=tokens[nodeIndex(tokens,variable)]
        del tokens[nodeIndex(tokens,variable)]

        if tokens:
            print("list not empty")#todo update to proper error handeling.

    root.PrintTree()#prints completed tree.


treeGen(token)

#-------------------------------------------------------------

def PrintTree(self,i = 0): #tree print function
    print(i* "  ",self.nodetype , " - \'" , self.value, "\'")
    if self.lhn != None : self.lhn.PrintTree(i+1)
    if self.rhn != None : self.rhn.PrintTree(i+1)