# Optimiser v2 - electric bugaloo
# Author: Oliver Grooby

import LexicalAnalysis as lex
import parseTreeGeneration as pT

class Operations:
    # Perform a sanity check if needed!
    def test(Buffer):
        print("NEW TREE:\n")
        for Node in Buffer.GeneratedTrees:
            print ("\nLine: ",Node.line)
            Node.PrintTree()
    
    # Removes a node that is superfluous to us
    def remove_node(Buffer, node):
        print("Yeet")
        print(type(Buffer.GeneratedTrees))
        del Buffer.GeneratedTrees[node] # This doesn't work quite yet

class Optimisations:
    # Check for redundant Assignments
    def check_redundant_assign(Buffer, currNode):
        print(currNode)
        print("TEST AGAIN: ", Buffer.GeneratedTrees[currNode].type)
        if Buffer.GeneratedTrees[currNode].type == "Oassign":
            print("Will check assignment!")
            print("Left hand: ", Buffer.GeneratedTrees[currNode].lhn.type, " Right hand: ", Buffer.GeneratedTrees[currNode].rhn.type)
            if Buffer.GeneratedTrees[currNode].lhn.type and Buffer.GeneratedTrees[currNode].rhn.type == "Identifier":
                print("Redundant identifier detected!")
                Operations.remove_node(Buffer, currNode)

    # Check for if statements that always eval as true

    #def check_always_true():
        

def icOptimise(Buffer):
    currNode = 0
    for Node in Buffer.GeneratedTrees:
        Optimisations.check_redundant_assign(Buffer, currNode)
        currNode+=1