# intercodegen.py
# Author: Tom Zajac
# Description: Generates intermediate code

import symtable
import bridge
import LexicalAnalysis as lex

# Intermediate code
intercode = bridge.Program()

prevLine = 1

lineTokens = []

def processLine():
    global intercode
    global prevLine
    global lineTokens

    # left-hand side identifier
    leftId = None
    prevToken = None
    isCall = False
    for lt in lineTokens:
        if lt["token"] == lex.tokentable.TokenIdent and leftId is None:
            leftId = lt["attrib"]
            print("found left-hand side identifier: {0}.".format(leftId))
        if prevToken is lex.tokentable.TokenIdent and leftId is not None and lt["token"] is lex.tokentable.TokenLparen:
            isCall = True
            print("Found function call '{0}'".format(leftId))
            intercode.calls.append(bridge.Call(leftId.strip()))
        elif isCall and lt["token"] is lex.tokentable.TokenIdent:
            intercode.calls[-1].data.append(bridge.CallData(symtable.lookup(lt["attrib"].strip()).type.strip(), lt["attrib"].strip(), True))
        elif isCall:
            if lt["token"] is lex.tokentable.TokenInteger or lt["token"] is lex.tokentable.TokenString:
                intercode.calls[-1].data.append(bridge.CallData(lex.tokentable.all_syms[lt["token"]].strip(), lt["attrib"].strip(), False))
        if leftId is not None and prevToken is lex.tokentable.TokenAssign:
            if lt["token"] == lex.tokentable.TokenString or lt["token"] == lex.tokentable.TokenInteger:
                if symtable.lookup(leftId.strip()) == False or symtable.lookup(leftId.strip()) == None:
                    print("adding identifier '{0}' to symtable".format(leftId))
                    datatype = lex.tokentable.all_syms[lt["token"]].strip()
                    symtable.insert(leftId.strip(), datatype, lt["attrib"])
                    intercode.data.append(bridge.Data(datatype, leftId.strip(), lt["attrib"]))
                else:
                    print("identifier {0} already exists in symtable".format(leftId.strip()))
        prevToken = lt["token"]
    lineTokens.clear()

def generate(filename: str):
    lex.file = open(filename, "r")

    global intercode
    global prevLine
    global lineTokens

    # Intermediate code
    intercode = bridge.Program()

    prevLine = 1

    lineTokens = []

    while True:
        tokenStream = lex.getToken()
        token = tokenStream[0]
        line = tokenStream[1]
        column = tokenStream[2]
        value = None
        if len(tokenStream) > 3:
            value = tokenStream[3]

        if line > prevLine or token == lex.tokentable.TokenEOF:
            processLine()
            prevLine = line
            print("processing line")
            print(len(intercode.data))

        if token == lex.tokentable.TokenEOF:
            break

        print("found token '{0}' on line {1}.".format(lex.tokentable.all_syms[token], line))
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

