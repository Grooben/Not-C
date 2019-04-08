# Author : Macauley Scullion

#Import files
import symtable as sym
import errorhandling as err
from parseTreeGeneration import Node 

# Node evaluation function - will evaluate the root node or passed node through a swither and call function, require bool for type check loop then setting loop
def eval(node, line):
    switcher = {
        "Oassign": equal,
        "OAdd": add,
        "OSub": sub,
        "OMulti": mult,
        "ODivide": div,
        "Identifier": var,
        "KeywordInt": var,
        "KeywordSTRING": var,
        "Integer": const,
        "String": const,
        "KeywordIF": ifstate,
        "KeywordPRINT": printstate,
        "Comma": comma
        }
    function = switcher[node.type]
    return function(node, line)

# Equal function - evals right side, assigns left return value from right eval
def equal(node, line):
    print("\t Equal node")
    #Check node type for keywords, if not - lookup left node value
    if (node.lhn.type == "KeywordInt"):
        #print("key int")
        l = check_lookup(node.lhn.rhn, line)
    
    elif (node.lhn.type == "KeywordSTRING"):
        #print("key str")
        l = check_lookup(node.lhn.rhn, line)

    else:
        #print("else")
        l = check_lookup(node.lhn, line)
    
    r = eval(node.rhn, line)
    type_check_assign(node, r, line)
    sym.set_attribute(l,r)
    return

# Add function - returns left and right addition
def add(node, line):
    print("\t Add node")
    l = eval(node.lhn, line)
    r = eval(node.rhn, line)
    
    #type check 
    type_check_sum(l, r, line)
    return l + r

# Sub function - returns left and right subtraction 
def sub(node, line):
    print("\t Sub node")
    l = eval(node.lhn, line)
    r = eval(node.rhn, line)
    
    #type check 
    type_check_sum(l, r, line)
    return l - r

# mult function - returns left and right multiplication 
def mult(node, line):
    print("\t Multi node")
    l = eval(node.lhn, line)
    r = eval(node.rhn, line)
    
    #type check 
    type_check_sum(l, r, line)
    return l * r


# div function - returns left and right division
def div(node, line):
    print("\t Div node")
    l = eval(node.lhn, line)
    r = eval(node.rhn, line)
    
    #type check 
    type_check_sum(l, r, line)
    return int(l / r)


# var function - returns variable value after lookup 
def var(node, line):
    print("\t Variable node")
    var = check_lookup(node, line)

    #tyep check
    #if type is int convert to int
    if (var.type == 'Int'):
        return int(var.value)
    #if not leave as str
    else:
        return var.value


# const function - returns the node value
def const(node, line):
    print("\t Constant node")
    #return value
    return node.value


# comma function - evaluates left and right of print punctuation
def comma(node, line):
    l = eval(node.lhn, line)
    r = eval(node.rhn, line)
    return

# If function - used to get child nodes of comparison
def ifstate(node, line):
    print("\t If node")
    if (node.rhn.type == "OperationEqual"):
        l = eval(node.rhn.lhn, line)
        r = eval(node.rhn.rhn, line)
        type_check_if(l,r, line)
        return
    else:
        err.errorifcompare(line)

# Print function - used to evaluated node within print function 
def printstate(node, line):
    print("\t Print node")
    r = eval(node.rhn, line)
    return

# Type check sums, 'left' operator 'right'
def type_check_sum (left, right, line):
    if (isinstance(left, int) and isinstance(right, int)):
        return
    else: 
        #If anything other Int's are summed
        err.errornodetypesum(line)

# Type checking assignments, 'left' equals 'right'
def type_check_assign(node, right, line):

    if (node.lhn.type == "KeywordInt"):
        #print("key int")
        l = node.lhn.rhn
    
    elif (node.lhn.type == "KeywordSTRING"):
        #print("key str")
        l = node.lhn.rhn

    else:
        #print("else")
        l = node.lhn

    if (l.type == "Identifier"):
        if (check_lookup(l, line) != False):
            l = check_lookup(l, line)
            #print("sym grabbed")
            if ((l.type == "Int") and (isinstance(right, int))):
                #print("both int")
                return
            elif (l.type == "String" and isinstance(right, str)):
                #print("both str")
                return
            else:
                err.errornodetypeassign(line)
    else:
        err.errornodetypeassign(line)

# Type check if - function which checks if if statement both match
def type_check_if(left, right, line):
    if (isinstance(left, int) and isinstance(right, int)):
        return
    if (isinstance(left, str) and isinstance(right, str)):
        return
    else: 
        #add error explain only ints can be added
        err.errorifnodes(line)

# Check lookup - function returns symbol if found, if not it'll run an error
def check_lookup(node, line):
    if (sym.lookup(node.value) != False):
        symbol = sym.lookup(node.value)
        line_check(symbol, line)
        return symbol
    else:
        err.errornotdeclared(node.value, line)

# Line check - checks if the variable is used before its declared 
def line_check(symbol, line):
    if (line < symbol.line):
        err.errorbeforedeclared(symbol.name, line)
    else:
        return