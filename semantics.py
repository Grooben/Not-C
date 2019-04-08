# Author : Macauley Scullion

#Import files
import symtable as sym
import errorhandling as err
from parseTreeGeneration import Node 

# Node evaluation function - will evaluate the root node or passed node through a swither and call function, require bool for type check loop then setting loop
def eval(node):
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
        "Comma": comma,
        "End_of_File": eof
        }
    function = switcher[node.type]
    return function(node)

# Dummy function for end of file
def eof(node):
    return

# Equal function - evals right side, assigns left return value from right eval
def equal(node):
    print("\t Equal node")
    #Check node type for keywords, if not - lookup left node value
    if (node.lhn.type == "KeywordInt"):
        #print("key int")
        l = sym.lookup(node.lhn.rhn.value)
    
    elif (node.lhn.type == "KeywordSTRING"):
        #print("key str")
        l = sym.lookup(node.lhn.rhn.value)

    else:
        #print("else")
        l = sym.lookup(node.lhn.value)
    
    r = eval(node.rhn)
    type_check_assign(node, r)
    sym.set_attribute(l,r)
    return

# Add function - returns left and right addition
def add(node):
    print("\t Add node")
    l = eval(node.lhn)
    r = eval(node.rhn)
    
    #type check 
    type_check_sum(l, r)
    return l + r

# Sub function - returns left and right subtraction 
def sub(node):
    print("\t Sub node")
    l = eval(node.lhn)
    r = eval(node.rhn)

    #type check
    type_check_sum(l, r)
    return l - r

# mult function - returns left and right multiplication 
def mult(node):
    print("\t Multi node")
    l = eval(node.lhn)
    r = eval(node.rhn)

    #type check
    type_check_sum(l, r)
    return l * r


# div function - returns left and right division
def div(node):
    print("\t Div node")
    l = eval(node.lhn)
    r = eval(node.rhn)

    #type check
    type_check_sum(l, r)
    return int(l / r)


# var function - returns variable value after lookup 
def var(node):
    print("\t Variable node")
    var = sym.lookup(node.value)

    #tyep check
    #if type is int convert to int
    if (var.type == 'Int'):
        return int(var.value)
    #if not leave as str
    else:
        return var.value


# const function - returns the node value
def const(node):
    print("\t Constant node")
    #return value
    return node.value


# comma function - evaluates left and right of print punctuation
def comma(node):
    l = eval(node.lhn)
    r = eval(node.rhn)
    return

# If function - used to get child nodes of comparison
def ifstate(node):
    print("\t If node")
    if (node.rhn.type == "OperationEqual"):
        l = eval(node.rhn.lhn)
        r = eval(node.rhn.rhn)
        type_check_if(l,r)
        return
    else:
        err.errorifcompare()

# 
def printstate(node):
    print("\t Print node")
    r = eval(node.rhn)
    return

# Type check sums, 'left' operator 'right'
def type_check_sum (left, right):
    if (isinstance(left, int) and isinstance(right, int)):
        return
    else: 
        #If anything other Int's are summed
        err.errornodetypesum()

# Type checking assignments, 'left' equals 'right'
def type_check_assign(node, right):

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
        if (sym.lookup(l.value) != False):
            l = sym.lookup(l.value)
            #print("sym grabbed")
            if ((l.type == "Int") and (isinstance(right, int))):
                #print("both int")
                return
            elif (l.type == "String" and isinstance(right, str)):
                #print("both str")
                return
            else:
                err.errornodetypeassign()
    else:
        err.errornodetypeassign()


def type_check_if(left, right):
    if (isinstance(left, int) and isinstance(right, int)):
        return
    if (isinstance(left, str) and isinstance(right, str)):
        return
    else: 
        #add error explain only ints can be added
        err.errorifnodes()
