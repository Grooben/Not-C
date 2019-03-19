#Author : Craig Clephane 
#Last edited : 10/03/2019

#File which contains error functions throughout all phases of the complier.

#Error Handling for Lexical Analysis functions - Displays error message, as well as exits. 
def error(line, col, msg):
    print(line, col, msg)
    exit(1)


# Looking back on this i dont think function overloading is possible
def error(name, type):
    print("Error: - Dupilicate variable initialized")
    exit(1)

def error(node):
    print("Error: - node")
    exit(1)