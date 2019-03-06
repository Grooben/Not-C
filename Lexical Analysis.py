import sys
##test
input_file = sys.stdin

### Dummy Values ### 
Character = " "

Column = 0

Line = 1
file = None

TokenEOF, TokenMultiply, TokenDivide, TokenMod, TokenAdd,       \
TokenSubtract, TokenNegate, TokenNOT, TokenLss, TokenLeq,       \
TokenGTR, TokenGEQ, TokenEQ, TokenNeg, TokenAssign,             \
TokenAND, TokenOR, TokenIF, TokenELSE, TokenWHILE,              \
TokenPrint, TokenPutc, TokenLparen, TokenRparen, TokenLbrace,   \
TokenRbrace, TokenSemi, TokenComma, TokenIdent, TokenInteger,   \
TokenString = range(31)

all_syms = ['End_of_File', 'OMulti', 'ODivide','OMod', 'OAdd', 
            'OSub', 'ONeg', 'ONot', 'OLess','OLessequal',
            'OGreater','OperationGreaterequal', 'OperationEqual', 'ONotequal', 'Oassign',
            'OAnd', 'Oor', 'KeywordIF', 'KeywordELSE', 'KeywordWHILE', 
            'KeywordPRINT', 'KeywordPutc', 'LeftParen', 'RightPaaren', 'LeftBrace', 
            'RightBrace', 'SemiColon', 'Comma', 'Identifier', 'Integer', 
            'String']

Symbols = { '{': TokenLbrace,
            '}': TokenRbrace,
            '(': TokenLparen,
            ')': TokenRparen,
            '+': TokenAdd,
            '-': TokenSubtract,
            '*': TokenMultiply,
            '%': TokenMod,
            ';': TokenSemi,
            ',': TokenComma }

keyWords = { 'if': TokenIF,
             'else':TokenELSE,
             'print': TokenPrint,
             'putc': TokenPutc,
             'while': TokenWHILE }

def string(start, errLine, errCol):
    text = ""
    text += Character
    grabNextCharacter()
    return TokenString, errLine, errCol, text

def error(line, col, msg):
    print(line, col, msg)
    exit(1)

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
    return TokenString, errLine, errCol, text

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
        return TokenInteger, errLine, errCol, n

    if Text in keyWords:
        return keyWords[Text], errLine, errCol

    return TokenIdent, errLine, errCol, Text

def getToken():

    while Character.isspace():
        grabNextCharacter()

    errLine = Line
    errCol = Column
    if len(Character) == 0: return TokenEOF, errLine, errCol                            ##RETURN END OF FILE 
    elif Character == '=': return follow('=', TokenEQ, TokenAssign, errLine, errCol)
    elif Character == '<': return follow ('=', TokenLeq, TokenLess, errLine, errCol)
    elif Character == '"': return stringLit(Character, errLine, errCol)
    elif Character in Symbols:
        sym = Symbols[Character]
        grabNextCharacter()
        return sym, errLine, errCol
    else: return indentOrInt(errLine, errCol)

### MAIN PROGRAM ### 
#READS FILE 
file = open("test.txt", "r")

#LOOPS UNTIL END OF FILE, WILL AUTOMATICALLY RUN
while True:
    tokenStream  =  getToken()         ##GRABS TOKEN STREAM 
    token        =  tokenStream[0]     ##GRABS TOKEN
    Line         =  tokenStream[1]     ##GRABS LINE OF TOKEN
    Column       =  tokenStream[2]     ##GRABS COLUMN OF TOKEN 

    print("%5d  %5d   %-14s" % (Line, Column, all_syms[token]), end='')

    if token == TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == TokenIdent: print("  %s" % (tokenStream[3]))
    else: print("")
    if token == TokenEOF:
        break

