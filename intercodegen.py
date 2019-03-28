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
def generate(filename: str):
    lex.file = open(filename, "r")

    # Use these variables from global scope
    global intercode
    global prevLine
    global lineTokens

    # Reset global variables
    intercode = bridge.Program()
    prevLine = 1
    lineTokens = []

    # Iterate through the file line-by-line until TokenEOF is found
    while True:
        tokenStream = lex.getToken()
        token = tokenStream[0]
        line = tokenStream[1]
        column = tokenStream[2]
        value = None
        if len(tokenStream) > 3:
            value = tokenStream[3]

        # Reached end of line. Process the last scanned line.
        if line > prevLine or token == lex.tokentable.TokenEOF:
            processLine()
            lineTokens = []
            prevLine = line
            print("processing line")
            print(len(intercode.data))

        if token == lex.tokentable.TokenEOF:
            break

        print("found token '{0}' on line {1}.".format(lex.tokentable.all_syms[token], line))
        # Add to current line token list
        lineTokens.append({"token": token, "attrib": value})

    print("Listing declared data: ")
    for x in intercode.data:
        print("\t'{0}', ({1}, '{2}')".format(x.identifier, x.typename, x.value))

    print("Listing function calls: ")
    for x in intercode.calls:
        print("\t'{0}' ({1} params)".format(x.command, len(x.data)))
        for y in x.data:
            print("\t'{0}', ({1}, isName: {2})".format(y.value, y.typename, y.isName))
    return intercode

