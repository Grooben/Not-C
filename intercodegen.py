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
# TODO: Rewrite using trees
def generate(tree, symbolTable):
    # Copy the caller's current state of symtable
    symtable.symbol_table = symbolTable
    for node in tree:
        print("Log (icg): Found node ({2}::{0}: {1}) in tree".format(node.type, node.value, node.catagory))
        if node.catagory == "Function" and node.type != "KeywordIF":
            coreFunc = {"KeywordPRINT": "print"}
            funcParams = []
            parentNode = node
            currentNode = node.rhn
            # Are there multiple comma-separated parameters?
            multiParam = False
            if currentNode.type == "Comma":
                multiParam = True
            print("Log (icg): Found ({2}::{0}: {1}) in function call".format(currentNode.type, currentNode.value, currentNode.catagory))
            while currentNode != None:
                if currentNode.type == "Comma":
                    print("Log (icg): Found comma in function call params. Copying left node '{0}'".format(currentNode.lhn.value))
                    parentNode = copy.deepcopy(currentNode)
                    currentNode = parentNode.lhn
                if currentNode.type != "Identifier":
                    print("Log (icg): Found function parameter as constant '{0}'".format(currentNode.value))
                    funcParams.append(bridge.CallData(currentNode.type, currentNode.value, False))
                else:
                    namePrefix = "nc_{0}var"
                    print("Log (icg): Found identifier ({0})".format(symtable.lookup(currentNode.value).type))
                    if symtable.lookup(currentNode.value).type == "String":
                        namePrefix = namePrefix.format("str_")
                    elif symtable.lookup(currentNode.value).type == "Int":
                        namePrefix = namePrefix.format("int_")
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
            varName = node.lhn.value
            # Initialising static data first
            lhSym = symtable.lookup(node.lhn.value)
            rhSym = symtable.lookup(node.rhn.value)
            if node.lhn.type == "KeywordInt" or (node.lhn.type == "Identifier" and lhSym != False and lhSym.type == "Integer"):
                if node.rhn.type == "Integer" or (node.rhn.type == "Identifer" and rhSym != False):
                    lhDataName = "var_{0}".format(node.lhn.rhn.value)
                    if rhSym != False:
                        rhDataName = "var_{0}".format(rhSym.name)
                        if intercode.findData(lhDataName):
                            assignCall = bridge.Call("_!c_assign")
                            assignCall.addData(bridge.CallData("Integer", lhDataName, True))
                            assignCall.addData(bridge.CallData("Integer", rhDataName, True))
                            intercode.calls.append(assignCall)
                        else:
                            intercode.data.append(bridge.Data("Integer", lhDataName, rhSym.value))
                    elif rhSym == False and node.rhn.type == "Integer":
                        intercode.data.append(bridge.Data("Integer", lhDataName, node.rhn.value))
                    else:
                        print("Error (icg): '{0} = {1}'\t '{1}' has not been found".format(node.lhn.rhn.value, node.rhn.value))
                elif node.rhn.type == "OAdd" or node.rhn.type == "OMulti" or node.rhn.type == "ODivide" or node.rhn.type == "OMod" or node.rhn.type == "OSub":
                    # Try precalculating the arithmetic if both nodes are integers
                    if node.rhn.lhn.type == "Integer" and node.rhn.rhn.type == "Integer":
                        endValue = 0
                        if node.rhn.type == "OAdd":
                            endValue = (int)(node.rhn.lhn.value) + (int)(node.rhn.rhn.value)
                        if node.rhn.type == "OSub":
                            endValue = (int)(node.rhn.lhn.value) - (int)(node.rhn.rhn.value)
                        elif node.rhn.type == "OMulti":
                            endValue = (int)(node.rhn.lhn.value) * (int)(node.rhn.rhn.value)
                        elif node.rhn.type == "ODivide":
                            endValue = (int)(node.rhn.lhn.value) / (int)(node.rhn.rhn.value)
                        elif node.rhn.type == "OMod":
                            endValue = (int)(node.rhn.lhn.value) % (int)(node.rhn.rhn.value)
                        if intercode.findData(node.lhn.value):
                            intercode.calls.append(bridge.Call("_!c_assign", [bridge.CallData("Integer", endValue, False)]))
                        else:
                            intercode.data.append(bridge.Data("Integer", "var_{0}".format(node.lhn.rhn.value), endValue))
                    else:
                        mathCallName = "_!c_math_{0}".format(node.rhn.replace("O", "").lower())
                        mathCall = bridge.Call(mathCallName)

                        # left side number
                        if node.rhn.lhn.type == "Integer":
                            mathCall.addData(bridge.CallData("Integer", node.rhn.lhn.value, False))
                        elif node.rhn.lhn.type == "Identifier":
                            mathCall.addData(bridge.CallData("Integer", node.rhn.lhn.value, True))
                        # right side number
                        if node.rhn.rhn.type == "Integer":
                            mathCall.addData(bridge.CallData("Integer", node.rhn.rhn.value, False))
                        elif node.rhn.rhn.type == "Identifier":
                            mathCall.addData(bridge.CallData("Integer", node.rhn.rhn.value, True))
                        intercode.calls.append(mathCall)
                else:
                    print("Error (icg): '{0} = {1}'\t '{1}' is not Integer type".format(node.lhn.rhn.value, node.rhn.value))
            elif node.lhn.type == "KeywordSTRING":
                lhDataName = "var_{0}".format(node.lhn.rhn.value)
                if node.rhn.type == "String":
                    intercode.data.append(bridge.Data("String", lhDataName, node.rhn.value))
                else:
                    print("Error (icg): '{0} = {1}'\t '{1}' is not String type".format(node.lhn.rhn.value, node.rhn.value))

    return intercode
