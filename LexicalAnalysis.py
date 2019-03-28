#Author : Craig Clephane 
#Last edited : 22/03/2019

#File contains functions which support the lexical analysis of a compiler (Phase one).

#Imported files.
import sys
import tokentable       #reads token file.
import errorhandling    #reads errorhandling file.
import symtable      #reads symbol table.
input_file = sys.stdin

#Dummy files.
Character = " "
Column = 0
Line = 1
file = None

Idname = ""

#Array containing tokens, as well as number of tokens
TokenArray = []
tokenCount = 0

#Grabs next character from the file, as well as shifting columns (Character) along everytime this function is called.
#Once a new line is detected, the column (Character) will reset to the start of the line, and shift line.
def grabNextCharacter():

    global Character, Column, Line

    Character = file.read(1)      
    Column += 1       
    if Character == '\n':       
        Line += 1
        Column = 0
    return Character

#Function which identifies the following character after a previous character and returns the correct token, based on the parameters. 
def follow(expect, ifyes, ifno, errLine, errCol):

    if grabNextCharacter() == expect:
        grabNextCharacter()
        bufferTokens(ifyes)
        return ifyes, errLine, errCol

    if ifno == tokentable.TokenEOF:
        followUnrecognized(errLine ,errCol)

    #Store Buffer Token, and return the token
    bufferTokens(ifno)
    return ifno, errLine, errCol

#Function which reads the string, and returns a string token as well as the text. 
def stringLit(start, errLine, errCol):

    text = ""

    #Loop appends characters onto the text if the character does not equal to the first character (")
    while grabNextCharacter() != start:
        if len(Character) == 0:
            endOfFile2(errLine, errCol)
        if Character == '\n':
           endOfLine(errLine, errCol)
        text += Character

    grabNextCharacter()
  
    #Add to symbol table whether an String has been decleared 
    if tokenCount > 1:
       findtok = tokenCount - 3

       #Check if the token 'String' was found, if not do nothing
       if TokenArray[findtok] == 32: 
          pushToSymbolTable(Idname, 'String', text)

    bufferTokens(tokentable.TokenString)
    return tokentable.TokenString, errLine, errCol, text

#Function which handles identifiers and integers by running a series of if statements and while loops. 
def identifiersOrIntegers(errLine, errCol):

    is_number = True
    Text = ""
    global Idname 

    #While loop to append the characters to a text string, also idenify whether the set of character is a digit or not. 
    while Character.isalnum() or Character == '_':
        Text += Character
        if not Character.isdigit():
            is_number = False
        grabNextCharacter()

    #If the text is a digit, convert to a number, and return integer token. 
    if Text[0].isdigit():
        if not is_number:
            invalidNumber(errLine, errCol, text)
        n = int(Text)
        
        #Add to symbol table whether an Int has been decleared 
        if tokenCount > 1:
            findtok = tokenCount - 3

            #Check if the token 'Int' was found, if not do nothing
            if TokenArray[findtok] == 31: 
                pushToSymbolTable(Idname, 'Int', n)

        bufferTokens(tokentable.TokenInteger)
        return tokentable.TokenInteger, errLine, errCol, n

    #If text matches a keyword, find keyword and return keyword token.
    if Text in tokentable.keyWords:
        bufferTokens(tokentable.keyWords[Text])
        return tokentable.keyWords[Text], errLine, errCol

    #If text is not an integer or a keyword, return identifier token, with what the identifier is.
    #Buffer Value
    Idname = Text
    bufferTokens(tokentable.TokenIdent)
    return tokentable.TokenIdent, errLine, errCol, Text

#Function which identifies whether the string is a comment as well as return the divide token.
def commentsAndDiv(errLine, errCol):

    #If the character after '/' does not equal to a *, return token divide. 
    if grabNextCharacter() != '*':
        bufferTokens(tokentable.TokenDivide)
        return tokentable.TokenDivide, errLine, errCol

    #Grab the next character, and if it equals to *, ignore the following text until '/' is identified again. 
    grabNextCharacter()
    while True:
    
        if Character == '*':
            if grabNextCharacter() == '/':  
                grabNextCharacter()
                return getToken()

        elif len(Character) == 0:
                endOfFile(errLine, errCol)
        else:
             grabNextCharacter()

#Function which pushes nessceray components to the symbol table. 
def pushToSymbolTable(name, type, value):
    symtable.insert(name, type, value)

def bufferTokens(token):
    global TokenArray 
    global tokenCount

    TokenArray.append(token)
    tokenCount += 1


#Get Token function calls the grab next character function and identifies what token the character is by a series of if statements.
def getToken():

    #Checks whether the character is white space or not, if true return next character. 
    while Character.isspace():      
        grabNextCharacter()

    #Temp Line and Column variables 
    errLine = Line
    errCol = Column
    
    #If the number of characters is zero, return the end of file token, meaning there are no more tokens within the file.
    if len(Character) == 0: 
        bufferTokens(tokentable.TokenEOF)
        return tokentable.TokenEOF, errLine, errCol      
    
    #If the character equals to the following Symbol, return the results from the respected function. 
    elif Character == '/': return commentsAndDiv(errLine, errCol)
    elif Character == '=': return follow ('=', tokentable.TokenEQ, tokentable.TokenAssign, errLine, errCol) 
    elif Character == '<': return follow ('=', tokentable.TokenLeq, tokentable.TokenLess, errLine, errCol)
    elif Character == '>': return follow ('=', tokentable.TokenGEQ, tokentable.TokenGTR, errLine, errCol)
    elif Character == '!': return follow ('=', tokentable.TokenEQ, tokentable.TokenAssign, errLine, errCol)
    elif Character == '&': return follow ('&', tokentable.TokenAnd, tokentable.TokenEOF, errLine, errCol)
    elif Character == '|': return follow ('|', tokentable.TokenOR, tokentable.TokenEOF, errLine, errCol) 
    elif Character == '"': return stringLit(Character, errLine, errCol)

    #If the character is equal to anything within the symbol table, return the corrosponding token.
    elif Character in tokentable.Symbols:
        sym = tokentable.Symbols[Character]
        grabNextCharacter()
        bufferTokens(sym)
        return sym, errLine, errCol
    
    #If the character does not match anything from above, fun the indent or interger function. 
    else: return identifiersOrIntegers(errLine, errCol)


