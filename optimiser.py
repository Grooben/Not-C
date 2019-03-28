# Optimiser v2 - electric bugaloo
# Author: Oliver Grooby

import LexicalAnalysis as lex
import parseTreeGeneration as pT

def remove_node(node):
    print("Will Remove Node...")

# Check for redundant Assignments
def remove_redundant_assign():

    for node in tree: # Tree doesn't exist
        if node.token[0].type == Oassign:
            if node.token[0].value == sym.value:
                remove_node(node)
                

# Lol most of this isn't needed now

# Check for if statements that always eval as true

def remove_always_true():

    for node in tree:
        if node.token[0].type == KeywordIF:
            # Insert Logic to detect a If statement that always evaluates as true
            remove_node(node)