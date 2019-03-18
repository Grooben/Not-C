# Author : Macauley Scullion
# symtable.py 

# Symbol class - Name, Type, and Attribute
class Symbol:
    def __init__(self, name, type, value = None):
        self.name = name
        self.type = type
        self.value = value

# Symbol table array
symbol_table = []

# Operations of symbol table 
# Free - remove all entries and free storage 
def free():
    symbol_table.clear()
    print("Symbol table cleared")

# Lookup - search for a name and return pointer to entry
def lookup(name):
    # Check if the symbol table is empty
    if len(symbol_table) == 0:
            print("Symbol table empty")
            return False
    # For each symbol in the symbol table, check if the parameter name matches the symbol name
    else:
        for sym in symbol_table:
            if sym.name == name:
                print("symbol found: name - " + name)
                return sym
        return False

# Insert - insert a name and return pointer to entry
def insert(name, type, value = None):
    # Lookup function call to check for matches 
    if (lookup(name) == False):
        new_entry = Symbol(name, type, value)
        symbol_table.append(new_entry)
        print("Symbol appended: " + name)
    else:
         print("Symbol duplicate: " + name)

# Set_attribute - associate an attribute with a given entry
def set_attribute(sym, value):
    sym.value = value

# Get_attribute - get an attribute associated with an entry
def get_attribute(sym):
    return sym.value

# Print Symbol table
def printTable():
     for sym in symbol_table:
         print("Item: \n""     Type:" + sym.type + "\n""     Name:"+ sym.name)
    
              

        