# bridge_test.py
# Author: Tom Zajac
# Description: Tests symbol table and bridge

import symtable
import bridge
import LexicalAnalysis as lex

lex.file = open("sourceFile.txt", "r")

# Intermediate code
intercode = bridge.Program()

prevLine = 1

lineTokens = []

def processLine():
    # left-hand side identifier
    leftId = None
    prevToken = None
    isCall = False
    for lt in lineTokens:
        if lt["token"] == lex.tokentable.TokenIdent and leftId is None:
            leftId = lt["attrib"]
            print("found left-hand side identifier: ", leftId)
        if prevToken is lex.tokentable.TokenIdent and leftId is not None and lt["token"] is lex.tokentable.TokenLparen:
            isCall = True
            print("Found function call '", leftId, "'")
            intercode.calls.append(bridge.Call(leftId))
        elif isCall and lt["token"] is lex.tokentable.TokenIdent:
            intercode.calls[-1].data.append(bridge.CallData(symtable.lookup(lt["attrib"]).type, lt["attrib"], True))
        elif isCall:
            if lt["token"] is lex.tokentable.TokenInteger or lt["token"] is lex.tokentable.TokenString:
                intercode.calls[-1].data.append(bridge.CallData(lex.tokentable.all_syms[lt["token"]], lt["attrib"], False))
        if leftId is not None and prevToken is lex.tokentable.TokenAssign:
            if lt["token"] == lex.tokentable.TokenString or lt["token"] == lex.tokentable.TokenInteger:
                if symtable.lookup(leftId) is False:
                    print("adding identifier '", leftId, "' to symtable")
                    datatype = lex.tokentable.all_syms[lt["token"]]
                    symtable.insert(leftId, datatype, lt["attrib"])
                    intercode.data.append(bridge.Data(datatype, leftId, lt["attrib"]))
        prevToken = lt["token"]
    lineTokens.clear()

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

    print("found token '", lex.tokentable.all_syms[token], "' on line", line)
    lineTokens.append({"token": token, "attrib": value})

print("Listing declared data: ")
for x in intercode.data:
    print("\t", x.identifier, ", (", x.typename, ", '", x.value, "')")

print("Listing function calls: ")
for x in intercode.calls:
    print("\t", x.command, " (", len(x.data), " parameters):")
    for y in x.data:
        print("\t", y.value, ", (", y.typename, ", isName: ", y.isName, ")")

