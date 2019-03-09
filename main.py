#Author : Craig Clephane

execfile("LexicalAnalysis.py")

#Reads source file
file = open("sourceFile.txt", "r")

#Loop which 
while True:
    tokenStream  =  getToken()         ##GRABS TOKEN STREAM 
    token        =  tokenStream[0]     ##GRABS TOKEN
    Line         =  tokenStream[1]     ##GRABS LINE OF TOKEN
    Column       =  tokenStream[2]     ##GRABS COLUMN OF TOKEN 

    #Prints token visually, comment over if needed.
    print("%5d  %5d   %-14s" % (Line, Column, all_syms[token]), end='')     

    if token == TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == TokenIdent: print("  %s" % (tokenStream[3]))
    else: print("")

    #Ends loop if 'TokenEOF' is detected. 
    if token == TokenEOF:
        break