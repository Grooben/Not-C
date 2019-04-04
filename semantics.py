# Author : Macauley Scullion

#Import symtable functions
import symtable
import errorhandling
from parseTreeGeneration import Node 

# Node evaluation function - will evaluate the root node or passed node through a swither and call function, require bool for type check loop then setting loop
def eval(node, bool):
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
    return function(node, bool)

# Equal function - evals right side, assigns left return value from right eval
def equal(node, bool):
    if (bool != True): 
        # Type checking loop
        print("type check loop")
        l = symtable.lookup(node.lhn.value) 
        r = eval(node.rhn, bool)
        type_check_assign(node)
        eval(node, True)
    else:
        # Setting loop
        print("set loop")
        l = symtable.lookup(node.lhn.value) 
        r = eval(node.rhn, True)
        symtable.set_attribute(l, r)
        return 

# Add function - returns left and right addition
def add(node, bool):
    if (bool != True):
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        type_check_sum(l, r)
        return l + r
    else:
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        return (l + " + " + r)


# Sub function - returns left and right subtraction 
def sub(node, bool):
    if (bool != True):
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        type_check_sum(l, r)
        return l - r
    else:
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        return (l + " - " + r)

# mult function - returns left and right multiplication 
def mult(node, bool):
    if (bool != True):
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        type_check_sum(l, r)
        return l * r
    else:
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        return (l + " * " + r)

# div function - returns left and right division
def div(node, bool):
    if (bool != True):
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        type_check_sum(l, r)
        return l / r
    else:
        l = eval(node.lhn, bool)
        r = eval(node.rhn, bool)
        return (l + " / " + r)

# var function - returns variable value after lookup 
def var(node, bool):
    var = symtable.lookup(node.value)
    if (bool != True):
        return var.value
    else:
        return var.name 

# const function - returns the constant i.e. its name
def const(node, bool):
    if (bool != True):
        return node.value
    else:
        return str(node.value) 

# Type checking function - will check if the variables/constants being summed are of the same type
def type_check_sum(leftnode, rightnode):  
    if (isinstance(leftnode,int) and isinstance(rightnode,int)):
        return

    else:
        errorhandling.errornodetype(1)

# Type checking function - will check if the variables/constants being assigned are of the same type
def type_check_assign(node):  
    # Only if left handside is a variable otherwise run an error
    if (node.lhn.type == 'variable'):
        # if left and right both return a symbol, match types otherwise run error
        if (symtable.lookup(node.lhn.value) != False and symtable.lookup(node.rhn.value) != False):
            if ((symtable.lookup(node.lhn.value)).type == 'Int' and (symtable.lookup(node.rhn.value)).type == 'Int'):
                return

            elif ((symtable.lookup(node.lhn.value)).type == 'Str' and (symtable.lookup(node.rhn.value)).type == 'Str'):
                return

            else: 
                errorhandling.errornodetype(node)

        # if left returns a symbol and right is a constant, match types otherwise run error
        elif (symtable.lookup(node.lhn.value) != False and node.rhn.type == 'constant'):
            if ((symtable.lookup(node.lhn.value)).type == 'Int' and isinstance(node.rhn.value, int)):
                return
            
            elif ((symtable.lookup(node.lhn.value)).type == 'Str' and isinstance(node.rhn.value, str)):
                return

            else: 
                errorhandling.errornodetype(node)

    else:
        errorhandling.errornodetype(node)

## Test node eval code - will have to remove all code from file to test - PLEASE DO THIS IN A SEPERATE FILE
#symtable.insert("X", "Int", 5)
#nodel = Node("variable", "X")
#noder = Node("constant", 5)
#root = Node("divide", "/", nodel, noder)
#print(eval(root))
#symtable.printTable()

#symtable.insert("X", "Int", 5)
#symtable.insert("Y", "Int", 5)
#nodel = Node("variable", "X")
#noder = Node("variable", "Y")
#root = Node("multiply", "*", noder, nodel)
#print(eval(root))

#symtable.insert("X", "Int", 0)
#symtable.insert("y", "Str", 6)
#symtable.printTable()
#nodel = Node("variable", "X")
#noder = Node("variable", "y")
#root = Node("equal", "=", nodel, noder)
#print(eval(root))
#symtable.printTable()

#symtable.insert("X", "Int", 0)
#symtable.printTable()
#nodel = Node("variable", "X")
#noder = Node("variable", "y")
#root = Node("equal", "=", nodel, noder)
#print(eval(root))
#symtable.printTable()

#symtable.insert("X", "Int", 0)
#symtable.insert("y", "Int", 6)
#nodel1 = Node("variable", "X")
#nodel2 = Node("variable", "y")
#noder2 = Node("constant", 12)
#noder1 = Node("addition", "+", nodel2, noder2)
#root = Node("equal", "=", nodel1, noder1)
#print(eval(root, False))
#symtable.printTable()