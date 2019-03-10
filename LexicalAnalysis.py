#Author : Craig Clephane 

import sys

import tokentable       #reads token file.
import errorhandling    #reads errorhandling file.

##test
input_file = sys.stdin

### Dummy Values ### 
Character = " "

Column = 0

Line = 1
file = None

def string(start, errLine, errCol):
    text = ""
    text += Character
    grabNextCharacter()
    return tokentable.TokenString, errLine, errCol, text

### GRABS THE NEXT VALUE FROM INPUT  ### 
#Stores Character in variable, then shifts column, if the column is at the end of the row
#it will shift to the next row
def grabNextCharacter():

    global Character, Column, Line

    Character = file.read(1)      
    Column += 1       
    if Character == '\n':       
        Line += 1
        Column = 0
    return Character

def follow(expect, ifyes, ifno, errLine, errCol):
    if grabNextCharacter() == expect:
        grabNextCharacter()
        return ifyes, errLine, errCol

    return ifno, errLine, errCol

def stringLit(start, errLine, errCol):
    text = " "
    while grabNextCharacter() != start:
        text += Character

    grabNextCharacter()
    return tokentable.TokenString, errLine, errCol, text

def indentOrInt(errLine, errCol):
    is_number = True
    Text = " "

    while Character.isalnum() or Character == '_':
        Text += Character
        if not Character.isdigit():
            is_number = False
        grabNextCharacter()

    if Text[0].isdigit():
        if not is_number:
            error(errLine, errCol, "Invalid number: %s" % (Text))
        n = int(Text)
        return tokentable.TokenInteger, errLine, errCol, n

    if Text in tokentable.keyWords:
        return tokentable.keyWords[Text], errLine, errCol

    return tokentable.TokenIdent, errLine, errCol, Text

#Needs FIXING
def comments(errLine, errCol):
    if grabNextCharacter() != '*':
        print("hello")
        return tokentable.TokenDivide, errLine, errCol

    grabNextCharacter()
    while True:
        if Character == '*':
            if grabNextCharacter() == '/':   
                grabNextCharacter()
                return getToken()
            elif len(Character) == 0:
                error(errLine, errCol, "Error")
            else:
                grabNextCharacter()

def getToken():

    while Character.isspace():
        grabNextCharacter()

    errLine = Line
    errCol = Column
    if len(Character) == 0: return tokentable.TokenEOF, errLine, errCol                            ##RETURN END OF FILE 
    elif Character == '/': return comments(errLine, errCol)
    elif Character == '=': return follow ('=', tokentable.TokenEQ, tokentable.TokenAssign, errLine, errCol)
    elif Character == '<': return follow ('=', tokentable.TokenLeq, tokentable.TokenLess, errLine, errCol)
    elif Character == '>': return follow ('=', tokentable.TokenGEQ, tokentable.TokenGTR, errLine, errCol)
    elif Character == '!': return follow ('=', tokentable.TokenEQ, tokentable.TokenAssign, errLine, errCol)
    elif Character == '&': return follow ('&', tokentable.TokenAnd, tokentable.TokenEOF, errLine, errCol)
    elif Character == '|': return follow ('|', tokentable.TokenOR, tokentable.TokenEOF, errLine, errCol) 
    elif Character == '"': return stringLit(Character, errLine, errCol)
    elif Character in tokentable.Symbols:
        sym = tokentable.Symbols[Character]
        grabNextCharacter()
        return sym, errLine, errCol
    else: return indentOrInt(errLine, errCol)


