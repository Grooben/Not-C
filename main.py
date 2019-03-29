#Author : Craig Clephane
#Last edited : 22/03/2019

#Main file for !C compiler.

#Imported files
import LexicalAnalysis as lex
import symtable

#Reads source file
lex.file = open("sourceFile.txt", "r")
Idname =""
while True:
    tokenStream  =  lex.getToken()     #Grabs the token stream, which includes the type of token, column, line and variable if present.
    token        =  tokenStream[0]     #Grabs token.
    Line         =  tokenStream[1]     #Grabs line.
    Column       =  tokenStream[2]     #Grabs column.
    #Catagory = categories[tokenStream[0]]

    #Prints token visually, comment over when needed.
    print ("%5d  %10d %-20s %-14s" % (Line, Column,lex.tokentable.categories[tokenStream[0]], lex.tokentable.all_syms[tokenStream[0]]), end='')    

    if token == lex.tokentable.TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == lex.tokentable.TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == lex.tokentable.TokenIdent: print("  %s" % (tokenStream[3])) 
    else: print("")

    #Grabs END OF LINE Token, appends over filestream to output this. 
    if lex.endOfLine == True:
        lex.endOfLine = False
        tokenStream = lex.tokentable.TokenEOL, Line, Column
        print ("%5d  %10d %-20s %-14s" % (Line, Column,lex.tokentable.categories[tokenStream[0]], lex.tokentable.all_syms[tokenStream[0]]), end='') 
        print ("\n")

    #Ends loop if 'TokenEOF' is detected. 
    if token == lex.tokentable.TokenEOF:
        break

#Example of printing table, remove when needed
symtable.printTable()