#Author : Craig Clephane
#Last edited : 10/03/2019

#Main file for !C compiler.

#Imported files
import LexicalAnalysis as lex

#Reads source file
lex.file = open("sourceFile.txt", "r")

while True:
    tokenStream  =  lex.getToken()     #Grabs the token stream, which includes the type of token, column, line and variable if present.
    token        =  tokenStream[0]     #Grabs token.
    Line         =  tokenStream[1]     #Grabs line.
    Column       =  tokenStream[2]     #Grabs column.

    #Prints token visually, comment over when needed.
    print("%5d  %5d   %-14s" % (Line, Column, lex.tokentable.all_syms[token]), end='')     

    if token == lex.tokentable.TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == lex.tokentable.TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == lex.tokentable.TokenIdent: print("  %s" % (tokenStream[3]))
    else: print("")

    #Ends loop if 'TokenEOF' is detected. 
    if token == lex.tokentable.TokenEOF:
        break
