# Optimiser v2
# Author: Oliver Grooby
# Description: A python script that optimises the parse tree before intemediate code generation.

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
        print("Going to delete node", node)
        del Buffer.GeneratedTrees[node]

class Optimisations:
    # Check for redundant Assignments
    def check_redundant_assign(Buffer, currNode):
        if Buffer.GeneratedTrees[currNode].type == "Oassign":
            print("Will check assignment to see if it is redundant...")
            # Check to see if the left hand node and the right hand node are both identifiers
            if Buffer.GeneratedTrees[currNode].lhn.type and Buffer.GeneratedTrees[currNode].rhn.type == "Identifier":
                # This statement checks to see if the assingment is truly redundant, the above statement checks
                # to see if both node types are Identifiers, thus meaninging something like x=a; would
                # be bypassed, when it shouldn't be...
                if Buffer.GeneratedTrees[currNode].lhn.value is Buffer.GeneratedTrees[currNode].rhn.value:
                    print("Redundant assignment detected!")
                    Operations.remove_node(Buffer, currNode)
    
    def check_zero_addition(Buffer, currNode):
        if Buffer.GeneratedTrees[currNode].type == "Oassign":
            # This long statement checks for a single line mathematical operation
            if Buffer.GeneratedTrees[currNode].rhn.rhn and Buffer.GeneratedTrees[currNode].rhn.lhn and not Buffer.GeneratedTrees[currNode].rhn.rhn.rhn:
                print("Single line addition detected!")
                if Buffer.GeneratedTrees[currNode].rhn.type == "OAdd" or Buffer.GeneratedTrees[currNode].rhn.type =="OSub":
                    if Buffer.GeneratedTrees[currNode].rhn.rhn.value == 0 or Buffer.GeneratedTrees[currNode].rhn.lhn.value == 0:
                        print("Zero Addition/Subtraction detected")
                        Operations.remove_node(Buffer, currNode)
        
# Entry point for the optimiser 
def icOptimise(Buffer):
    currNode = 0
    for Node in Buffer.GeneratedTrees:
        print("\nOptimising node", currNode)
        Optimisations.check_redundant_assign(Buffer, currNode)
        Optimisations.check_zero_addition(Buffer, currNode)
        currNode+=1
    print("Done optimising!\n")