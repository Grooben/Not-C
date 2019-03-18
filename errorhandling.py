#Author : Craig Clephane 
#Last edited : 10/03/2019

#File which contains error functions throughout all phases of the complier.

#Error Handling for Lexical Analysis functions - Displays error message, as well as exits. 
def error(line, col, msg):
    print(line, col, msg)
    exit(1)

def error(name, type):
    print("Error: - Dup")