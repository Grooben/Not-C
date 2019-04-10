# Optimiser v2 - electric bugaloo
# Author: Oliver Grooby

import LexicalAnalysis as lex
import parseTreeGeneration as pT

class Operations:
    # Perform a sanity check if needed!
    def test(Buffer):
        print("Buffer access check:\n")
        for Node in Buffer.GeneratedTrees:
            print ("\nLine: ",Node.line)
            Node.PrintTree()
    
    # Removes a node that is superfluous to us by using the python inbuilt
    # del function, that allows me to safely remove a node in the node tree,
    # this works well as the tree is built in a horizontal linear fashion.
    def remove_node(Buffer, node):
        print("Going to delete node ", node)
        print(type(Buffer.GeneratedTrees))
        del Buffer.GeneratedTrees[node]

class Optimisations:
    # Check for redundant Assignments
    def check_redundant_assign(Buffer, currNode):
        print(currNode)
        print("TEST AGAIN: ", Buffer.GeneratedTrees[currNode].type)
        if Buffer.GeneratedTrees[currNode].type == "Oassign":
            print("Will check assignment to see if it is redundant...")
            # Check to see if the left hand node and the right hand node are both identifiers
            if Buffer.GeneratedTrees[currNode].lhn.type and Buffer.GeneratedTrees[currNode].rhn.type == "Identifier":
                print("Redundant identifier detected!")
                Operations.remove_node(Buffer, currNode)
        
def icOptimise(Buffer):
    currNode = 0
    for Node in Buffer.GeneratedTrees:
        Optimisations.check_redundant_assign(Buffer, currNode)
        currNode+=1