# intercodegen.py
# Author: Tom Zajac
# Description: Generates intermediate code

import symtable
import bridge
import LexicalAnalysis as lex

# Intermediate code that will be returned after calling generate()
intercode = bridge.Program()

# Previously scanned line
prevLine = 1

# List of tokens found in the current line
# Each element is a dictionary. Key "token" points to an entry in the tokentable, and key "attrib" contains the attribute of this token.
# Example: {"token": TokenIdent, "attrib": "testVariable"}
lineTokens = []

# Scans tokens from current line
def processLine():
    # Use these variables from global scope
    global intercode
    global prevLine
    global lineTokens

    # left-hand side identifier in tihs line
    leftId = None

    # Previously scanned token
    prevToken = None

    # Is the current line a function call?
    isCall = False

    # Iterate through each token (lt) from the current line token list (lineTokens)
    for lt in lineTokens:
        # Case: This token is an Identifier.
        # If no left-hand side identifier has been found yet, assign this as one.
        # TODO: Had to consider Keywords (e.g. 'print', 'if') as identifiers too,
        # this should be changed at some point to avoid confusion.
        if lt["token"] == lex.tokentable.TokenIdent or lex.tokentable.all_syms[lt["token"]].find("Keyword") == 0:
            if leftId is None:
                # Either:
                # Assign keyword name
                if lex.tokentable.all_syms[lt["token"]].find("Keyword") == 0:
                    leftId = lex.tokentable.all_syms[lt["token"]].replace("Keyword", "").lower()
                # Assign identifier name
                else:
                    leftId = lt["attrib"]
                print("found left-hand side identifier: {0}.".format(leftId))

        # Case: A left-hand side identifier (OR a keyword) has been found in the previous iteration, and the current token is a left parenthesis.
        # This indicates that there is a command call on this line. Set isCall to indicate that.
        # The left-hand side identifier/keyword therefore contains the command name, which gets added to intermediate code.
        if prevToken is not None:
            if prevToken == lex.tokentable.TokenIdent or lex.tokentable.all_syms[prevToken].find("Keyword") == 0:
                if leftId is not None and lt["token"] == lex.tokentable.TokenLparen:
                    isCall = True
                    print("Found function call '{0}'".format(leftId))
                    newCall = bridge.Call(leftId.strip(), [])
                    intercode.calls.append(newCall)
                    print("Added new function call. Checking data count and call count: {0} calls, {1} data in this new call".format(intercode.callCount(), intercode.calls[-1].dataCount()))
        # Case: A command call has been found prior to this iteration, and an identifier has been found in this iteration.
        # Add this identifier to this call's data list in the intermediate code.
        if isCall == True and lt["token"] == lex.tokentable.TokenIdent:
            print("Adding data")
            numCalls = intercode.callCount()
            intercode.calls[numCalls-1].addData(bridge.CallData(symtable.lookup(lt["attrib"].strip()).type.strip(), lt["attrib"].strip(), True))
        # Case: A command call has been found prior to this iteration. No identifier has been found.
        # Check for data constants/literals, and add them to the call's data list in the intermediate code.
        elif isCall == True and lt["token"] == lex.tokentable.TokenRparen:
            isCall = False
            print("'{0}' call finished ('{1}' parameters passed)".format(intercode.calls[-1].command, len(intercode.calls[-1].data)))
        elif isCall == True:
            if lt["token"] == lex.tokentable.TokenInteger or lt["token"] == lex.tokentable.TokenString:
                numCalls = intercode.callCount()
                print("Number of calls: {0}".format(numCalls))
                print("Number of arguments in current call: {0}".format(intercode.calls[intercode.callCount()-1].dataCount()))
                intercode.calls[numCalls-1].addData(bridge.CallData(lex.tokentable.all_syms[lt["token"]].strip(), lt["attrib"], False))

        # Case: A left-hand side identifier has been found, and the previous token was an assignment operator.
        # Assign value to identifier. If the identifier can't be found in the symbol table, add it.
        if leftId is not None and prevToken is lex.tokentable.TokenAssign:
            if lt["token"] == lex.tokentable.TokenString or lt["token"] == lex.tokentable.TokenInteger:
                # Declare the identifier if it doesn't exist yet
                if symtable.lookup(leftId.strip()) == False or symtable.lookup(leftId.strip()) == None:
                    print("adding identifier '{0}' to symtable".format(leftId))
                    # Find datatype string based on tokentable entry.
                    datatype = lex.tokentable.all_syms[lt["token"]].strip()

                    # Insert identifier along with its datatype string and value into symbol table
                    symtable.insert(leftId.strip(), datatype, lt["attrib"])
                    # Insert identifier along with its datatype string and value into intermediate code static data
                    intercode.data.append(bridge.Data(datatype, leftId.strip(), lt["attrib"]))
                else:
                    print("identifier {0} already exists in symtable".format(leftId.strip()))
        # Update previous token with current token for the next iteration
        prevToken = lt["token"]
    # Empty the current line token list
    lineTokens.clear()

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
            parentNode = None
            currentNode = node
            # TODO
            if currentNode.type != "Comma":
                currentNode = node.rhn
            else:
                currentNode = node.rhn.lhn
            print("Log (icg): Found ({2}::{0}: {1}) in function call".format(currentNode.type, currentNode.value, currentNode.catagory))
            while currentNode != None and currentNode.catagory == "Variable":
                if currentNode.type != "Comma":
                    currentNode = node.rhn
                else:
                    currentNode = node.rhn.lhn
                if currentNode.type != "Identifier":
                    print("Log (icg): Found function parameter as constant '{0}'".format(currentNode.value))
                    funcParams.append(bridge.CallData(currentNode.type, currentNode.value, False))
                else:
                    namePrefix = "nc_{0}var"
                    print("Log (icg): Found identifier")
                    if symtable.lookup(currentNode.value).type == "String":
                        namePrefix = namePrefix.format("str_")
                    elif symtable.lookup(currentNode.value).type == "Integer":
                        namePrefix = namePrefix.format("int_")
                    else:
                        namePrefix = namePrefix.format("")
                    print("Log (icg): Found function parameter as identifier '{0}'".format(currentNode.value))
                    funcParams.append(bridge.CallData(symtable.lookup(currentNode.value).type, "{0}_{1}".format(namePrefix, currentNode.value), True))
                currentNode = currentNode.rhn
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

