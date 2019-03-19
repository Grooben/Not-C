# Author : Macauley Scullion
# Interpreter version

#Import symtable functions
import symtable
import errorhandling


# Class defintion - will be removed, require by syntax and functions can simply be imported and called

class Node: 
    def __init__(self, type, value, lhn = None, rhn = None):
        self.type = type
        self.value = value 
        self.lhn = lhn
        self.rhn = rhn


# Node evaluation function - will evaluate the root node or passed node through a swither and call function
def eval(node):
    switcher = {
        "equal": equal,
        "addition": add,
        "subtraction": sub,
        "multiply": mult,
        "divide": div,
        "variable": var,
        "constant": const
        }
    function = switcher[node.type]
    return function(node)

# Equal function - evals right side, assigns left return value from right eval
def equal(node):
    l = symtable.lookup(node.lhn.value) 
    r = eval(node.rhn)
    type_check(node)
    symtable.set_attribute(l, r)
    return

# Add function - returns left and right addition
def add(node):
    l = eval(node.lhn)
    r = eval(node.rhn)
    type_check(l, r)
    return l + r

# Sub function - returns left and right subtraction 
def sub(node):
    l = eval(node.lhn)
    r = eval(node.rhn)
    type_check(l, r)
    return l - r

# mult function - returns left and right multiplication 
def mult(node):
    l = eval(node.lhn)
    r = eval(node.rhn)
    type_check(l, r)
    return l * r

# div function - returns left and right division
def div(node):
    l = eval(node.lhn)
    r = eval(node.rhn)
    type_check(l, r)
    return l / r

# var function - returns variable value after lookup 
def var(node):
    var = symtable.lookup(node.value)
    return var.value

# const function - returns the constant i.e. its name
def const(node):
    return node.value

# Type checking function - will check if the variables/constants being summed are of the same type
def type_check(leftnode, rightnode):  
    if (isinstance(leftnode,int) and isinstance(rightnode,int)):
        return

    else:
        module2.error(1)
    
    return

def type_check(node):  
    if (node.lhn.type == 'variable'):
        if (symtable.lookup(node.lhn.value) != False and symtable.lookup(node.rhn.value) != False):
            if ((symtable.lookup(node.lhn.value)).type == 'Int' and (symtable.lookup(node.rhn.value)).type == 'Int'):
                return

            elif ((symtable.lookup(node.lhn.value)).type == 'Str' and (symtable.lookup(node.rhn.value)).type == 'Str'):
                return

            else: 
                errorhandling.error(node)

        elif (symtable.lookup(node.lhn.value) != False and node.rhn.type == 'constant'):
            if ((symtable.lookup(node.lhn.value)).type == 'Int' and isinstance(node.rhn.value, int)):
                return
            
            elif ((symtable.lookup(node.lhn.value)).type == 'Str' and isinstance(node.rhn.value, str)):
                return

            else: 
                errorhandling.error(node)

    else:
        errorhandling.error(node)
    
    return


## Test node eval code - will have to remove all code from file to test - PLEASE DO THIS IN A SEPERATE FILE
#module1.insert("X", "Int", 5)
#nodel = Node("variable", "X")
#noder = Node("constant", 5)
#root = Node("divide", "+", nodel, noder)
#print(eval(root))
#module1.printTable()

#module1.insert("X", "Int", 5)
#module1.insert("Y", "Int", 5)
#nodel = Node("variable", "X")
#noder = Node("variable", "Y")
#root = Node("multiply", "+", noder, nodel)
#print(eval(root))

#module1.insert("X", "Int", 5)
#module1.insert("y", "Str", 5)
#nodel = Node("variable", "X")
#noder = Node("variable", "y")
#root = Node("equal", "+", nodel, noder)
#print(eval(root))
#module1.printTable()
