#Author : Craig Clephane

import LexicalAnalysis as lex

#Reads source file
lex.file = open("sourceFile.txt", "r")

#Loop which 
while True:
    tokenStream  =  lex.getToken()         ##GRABS TOKEN STREAM 
    token        =  tokenStream[0]     ##GRABS TOKEN
    Line         =  tokenStream[1]     ##GRABS LINE OF TOKEN
    Column       =  tokenStream[2]     ##GRABS COLUMN OF TOKEN 

    #Prints token visually, comment over if needed.
    print("%5d  %5d   %-14s" % (Line, Column, lex.tokentable.all_syms[token]), end='')     

    if token == lex.tokentable.TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == lex.tokentable.TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == lex.tokentable.TokenIdent: print("  %s" % (tokenStream[3]))
    else: print("")

    #Ends loop if 'TokenEOF' is detected. 
    if token == lex.tokentable.TokenEOF:
        break
