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

class Optimisations:
    # Check for redundant Assignments
    def check_redundant_assign(Buffer, currNode):
        print(currNode)
        currNode = 4
        print("TEST AGAIN: ", type(Buffer.GeneratedTrees[currNode].lhn))

    # Check for if statements that always eval as true

    #def check_always_true():
        

def icOptimise(Buffer):
    currNode = 0
    for Node in Buffer.GeneratedTrees:
        Optimisations.check_redundant_assign(Buffer, currNode)
        currNode+=1



    
