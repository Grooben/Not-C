# Author : Macauley Scullion
# Interpreter version
# will need editing into representing intermediate code and after collaboration with syntax analysis

 #Import symtable functions
import symtable

##
# Class defintion - will be removed, require by syntax and functions can simply be imported and called
class Node: 
    def __init__(self, nodetype, char, lhn = None, rhn = None):
        self.nodetype = nodetype
        self.char = char 
        self.lhn = lhn
        self.rhn = rhn


# Node evaluation function - will evaluate the root node or passed node through a swither and call function
def eval(node):
    switcher = {
        "equal": node.equal,
        "addition": node.add,
        "subtraction": node.sub,
        "multiply": node.mult,
        "divide": node.div,
        "variable": node.var,
        "constant": node.const
        }
    function = switcher[node.nodetype]
    return function()

# Equal function - evals right side, assigns left return value from right eval
def equal(node):
    r = node.rhn.eval()
    l = symtable.lookup(node.lhn.char)
    symtable.set_attribute(l, r)
    return

# Add function - returns left and right addition
def add(node):
    l = node.lhn.eval()
    r = node.rhn.eval()
    return l + r

# Sub function - returns left and right subtraction 
def sub(node):
    l = node.lhn.eval()
    r = node.rhn.eval()
    return l - r

# mult function - returns left and right multiplication 
def mult(node):
    l = node.lhn.eval()
    r = node.rhn.eval()
    return l * r

# div function - returns left and right division
def div(node):
    l = node.lhn.eval()
    r = node.rhn.eval()
    return l / r

# var function - returns variable value after lookup 
def var(node):
    var = symtable.lookup(node.char)
    return var.value

# const function - returns the constant i.e. its name
def const(node):
    return node.char