# Author : Macauley Scullion

#Import symtable functions
import symtable as sym
import errorhandling as err
from parseTreeGeneration import Node 

# Node evaluation function - will evaluate the root node or passed node through a swither and call function, require bool for type check loop then setting loop
def eval(node, bool):
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
        "String": const
        }
    function = switcher[node.type]
    return function(node, bool)

# Equal function - evals right side, assigns left return value from right eval
def equal(node, bool):
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
    
    #bool for type checking loop check
    if (bool != True):
        r = eval(node.rhn, bool)
        type_check_assign(node)
        eval(node , True)

    #String symbol value assignment loop
    else:
        r = eval(node.rhn, bool)
        sym.set_attribute(l,r)
    return

# Add function - returns left and right addition
def add(node, bool):
    print("\t Add node")
    l = eval(node.lhn, bool)
    r = eval(node.rhn, bool)
    
    #type check 
    if (bool != True):
        type_check_sum(l, r)
        return l + r

    #string return
    else:
        return (l + " + " + r)

# Sub function - returns left and right subtraction 
def sub(node, bool):
    print("\t Sub node")
    l = eval(node.lhn, bool)
    r = eval(node.rhn, bool)

    #type check
    if (bool != True):
        type_check_sum(l, r)
        return l - r

    #string return
    else:
        return (l + " - " + r)

# mult function - returns left and right multiplication 
def mult(node, bool):
    print("\t Multi node")
    l = eval(node.lhn, bool)
    r = eval(node.rhn, bool)

    #type check
    if (bool != True):
        type_check_sum(l, r)
        return l * r

    #string return
    else:
        return (l + " * " + r)

# div function - returns left and right division
def div(node, bool):
    print("\t Div node")
    l = eval(node.lhn, bool)
    r = eval(node.rhn, bool)

    #type check
    if (bool != True):
        type_check_sum(l, r)
        return int(l / r)

    #string return
    else:
        return (l + " / " + r)

# var function - returns variable value after lookup 
def var(node, bool):
    print("\t Variable node")
    var = sym.lookup(node.value)

    #tyep check
    if (bool != True):
        #if type is int convert to int
        if (var.type == 'Int'):
            return int(var.value)
        #if not leave as str
        else:
            return var.value
    # string return
    else:
        return var.name 

# const function - returns the constant i.e. its name
def const(node, bool):
    print("\t Constant node")
    #return value
    if (bool != True):
        return node.value
    #string return
    else:
        return str(node.value) 

# Type check sums, 'left' operator 'right'
def type_check_sum (left, right):
    print("\t"*2,"Type checking sum: -")
    #check both sides match at int
    if (isinstance(left, int) and isinstance(right, int)):
        print("\t"*3,"Type checking sum complete")
        return
    #if not return error
    else:
        err.errornodetypesum()

# Type checking assignments, 'left' equals 'right'
def type_check_assign(node):
    print("\t"*2,"type check assign: -")
    #Check node type for keywords, if not - lookup left node value
    if (node.lhn.type == "KeywordInt"):
        #print("key int")
        l = node.lhn.rhn
    
    elif (node.lhn.type == "KeywordSTRING"):
        #print("key str")
        l = node.lhn.rhn

    else:
        #print("else")
        l = node.lhn

    # if left is an identifier, continue to type check    
    if (l.type == 'Identifier'):
        #if both vales of left and right return a symbol
        if (sym.lookup(l.value) != False and sym.lookup(node.rhn.value) != False):
            #if both symbols are Ints
            if ((sym.lookup(l.value)).type == 'Int' and (sym.lookup(node.rhn.value)).type == 'Int'):
                print("\t"*3,"Type checking assignment complete")
                return
            #if both symbols are Strings
            elif ((sym.lookup(l.value)).type == 'String' and (sym.lookup(node.rhn.value)).type == 'String'):
                print("\t"*3,"Type checking assignment complete")
                return
            #else, run the error
            else: 
                err.errornodetypeassign()

        # if left returns a symbol and right is a constant, match types otherwise run error
        elif (sym.lookup(l.value) != False and node.rhn.type == 'constant'):
            #if left symbol is an int and right is a integer
            if ((sym.lookup(l.value)).type == 'Int' and isinstance(node.rhn.value, int)):
                print("\t"*3,"Type checking assignment complete")
                return
            #if left symbol is an string and right is a string
            elif ((sym.lookup(l.value)).type == 'String' and isinstance(node.rhn.value, str)):
                print("\t"*3,"Type checking assignment complete")
                return
            #else, run the error
            else: 
                err.errornodetypeassign()
        
    # else, run the error
    else:
        err.errornodetypeassign()
    
