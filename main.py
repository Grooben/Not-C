##IMPORT 
execfile("LexicalAnalysis.py")

### MAIN PROGRAM ### 
#READS FILE 
file = open("sourceFile.txt", "r")

#LOOPS UNTIL END OF FILE, WILL AUTOMATICALLY RUN
while True:
    tokenStream  =  getToken()         ##GRABS TOKEN STREAM 
    token        =  tokenStream[0]     ##GRABS TOKEN
    Line         =  tokenStream[1]     ##GRABS LINE OF TOKEN
    Column       =  tokenStream[2]     ##GRABS COLUMN OF TOKEN 

    ##PRINTS TOKEN VISIUALY. COMMENT OVER IF NEEDED.
    print("%5d  %5d   %-14s" % (Line, Column, all_syms[token]), end='')     

    if token == TokenInteger: print("  %5d" % (tokenStream[3]))
    elif token == TokenString: print(' "%s"' % (tokenStream[3]))
    elif token == TokenIdent: print("  %s" % (tokenStream[3]))
    else: print("")

    #ENDS LOOP IF AT END OF FILE.
    if token == TokenEOF:
        break