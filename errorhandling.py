#Author : Craig Clephane 

#Error Handling for Lexical Analysis functions 
def error(line, col, msg):
    print(line, col, msg)
    exit(1)