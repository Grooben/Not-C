# intercodegen.py
# Author: Tom Zajac
# Description: Generates intermediate code

import symtable
import bridge
import LexicalAnalysis as lex
import copy

# Intermediate code that will be returned after calling generate()
intercode = bridge.Program()

# Generates intermediate code representation.
# The return value is a bridge.Program class object,
# which the backend uses to understand the source program's logic and create ASM code accordingly.
def generate(tree, symbolTable, syscalls):
    # Copy the caller's current state of symtable
    # This is so we maintain the same symtable state as in main.py
    symtable.symbol_table = symbolTable
    # Iterate through the program tree
    for node in tree:
        if node == None:
            continue
        print("Log (icg): Found node ({2}::{0}: {1}) in tree".format(node.type, node.value, node.catagory))
        # Check for functions
        if node.catagory == "Function" and node.type != "KeywordIF":
            # Maps keywords to core functions
            coreFunc = {"KeywordPRINT": "print"}

            # Parameters to be passed to this function call
            funcParams = []

            parentNode = node
            currentNode = node.rhn
            # Are there multiple comma-separated parameters?
            multiParam = False
            if currentNode.type == "Comma":
                multiParam = True
            print("Log (icg): Found ({2}::{0}: {1}) in function call".format(currentNode.type, currentNode.value, currentNode.catagory))

            # Iterate through parameter nodes
            while currentNode != None:
                if currentNode.type == "Comma":
                    print("Log (icg): Found comma in function call params. Copying left node '{0}'".format(currentNode.lhn.value))
                    parentNode = copy.deepcopy(currentNode)
                    currentNode = parentNode.lhn
                if currentNode.type != "Identifier":
                    print("Log (icg): Found function parameter as constant '{0}'".format(currentNode.value))
                    funcParams.append(bridge.CallData(currentNode.type, currentNode.value, False))
                else:
                    namePrefix = "nc_{0}_var"
                    if symtable.lookup(currentNode.value) != None and symtable.lookup(currentNode.value) != False:
                        print("Log (icg): Found identifier ({0})".format(symtable.lookup(currentNode.value).type))
                    else:
                        print("Error (icg): Identifier node value '{0}' was not found in symbol table".format(currentNode.value))
                        break
                    if symtable.lookup(currentNode.value).type == "String":
                        namePrefix = namePrefix.format("str")
                    elif symtable.lookup(currentNode.value).type == "Int":
                        namePrefix = namePrefix.format("int")
                    else:
                        namePrefix = namePrefix.format("")
                    print("Log (icg): Found function parameter as identifier '{0}'".format(currentNode.value))
                    funcParams.append(bridge.CallData(symtable.lookup(currentNode.value).type, "{0}_{1}".format(namePrefix, currentNode.value), True))
                if not multiParam:
                    break
                if parentNode != None:
                    currentNode = parentNode.rhn
                else:
                    currentNode = None
                if currentNode != None:
                    parentNode = currentNode.rhn
                else:
                    parentNode = None
            if coreFunc[node.type] != None:
                intercode.calls.append(bridge.Call(coreFunc[node.type], funcParams))
            else:
                print("Error (icg): Function '{0}' has not been found in built-in function list.".format(node.value))
        if node.type == "Oassign":
            # Check if new static data needs to be added
            newData = None
            currentNode = node.lhn
            identifier = ""
            if currentNode.type == "KeywordSTRING":
                intercode.data.append(bridge.Data("String", "var_{0}".format(currentNode.rhn.value), node.rhn.value))
            if currentNode.type == "KeywordInt":
                newData = bridge.Data("Integer", "var_{0}".format(currentNode.rhn.value), "0")
                identifier = "nc_int_var_{0}".format(currentNode.rhn.value)
                currentNode = currentNode.rhn
                intercode.data.append(newData)
            if currentNode.type == "Identifier":
                sym = symtable.lookup(node.lhn.value)
                if sym != False and sym.type == "Int":
                    print("Log (icg): Adding Int assign param '{0}'".format(currentNode.value))
                    identifier = "nc_int_var_{0}".format(sym.name)
            currentNode = node.rhn
            if currentNode.type == "Integer" or currentNode.type == "Identifier":
                if currentNode.type == "Identifier":
                    print("Log (icg): Adding assign param '{0}'".format(currentNode.value))
                    intercode.calls.append(bridge.Call("_!c_assign", [bridge.CallData("Integer", identifier, True), bridge.CallData("Integer", str(currentNode.value), True)]))
                    intercode.calls[-1].data[0].checkTypes = intercode.calls[-1].data[1].checkTypes = False
                else:
                    print("Log (icg): Adding assign param '{0}'".format(currentNode.value))
                    intercode.calls.append(bridge.Call("_!c_assign", [bridge.CallData("Integer", identifier, True), bridge.CallData("Integer", str(currentNode.value), False)]))
                    intercode.calls[-1].data[0].checkTypes = intercode.calls[-1].data[1].checkTypes = False
            elif currentNode.type == "OAdd" or currentNode.type == "OMulti" or currentNode.type == "ODivide" or currentNode.type == "OMod" or currentNode.type == "OSub":
                mathOpName = currentNode.type[1:].lower() # this gets rid of the 'O' and converts to lowercase
                mathOpName = "_!c_math_{0}".format(mathOpName)
                mathCall = bridge.Call(mathOpName)
                assignCall = bridge.Call("_!c_memory_savereg", [bridge.CallData("String", identifier, True), bridge.CallData("String", syscalls[mathOpName].result())]) # change call to saveregister function since the math functions don't save into memory
                assignCall.data[0].checkTypes = False
                if currentNode.lhn.type == "Identifier":
                    mathCall.addData(bridge.CallData("Integer", "nc_int_var_{0}".format(currentNode.lhn.value), True))
                elif currentNode.lhn.type == "Integer":
                    mathCall.addData(bridge.CallData("Integer", str(currentNode.lhn.value), False))
                if currentNode.rhn.type == "Identifier":
                    mathCall.addData(bridge.CallData("Integer", "nc_int_var_{0}".format(currentNode.rhn.value), True))
                elif currentNode.rhn.type == "Integer":
                    mathCall.addData(bridge.CallData("Integer", str(currentNode.rhn.value), False))
                intercode.calls.append(mathCall)
                intercode.calls.append(bridge.Call("_!c_memory_savereg", [bridge.CallData("Integer", identifier, True), bridge.CallData("String", syscalls[mathOpName].result(), False)]))
                intercode.calls[-1].data[0].checkTypes = intercode.calls[-1].data[1].checkTypes = False
    return intercode
