#Author : Craig Clephane 
#Last edited : 10/03/2019

#File which contains error functions throughout all phases of the complier.

#Error Handling for Lexical Analysis functions - Displays error message, as well as exits. 
def error(line, col, msg):
    print(line, col, msg)
    exit(1)


def error_dup(name, type):
    print("Error: - Dupilicate variable initialized. Please check that all variables are unique.")
    exit(1)

#Error Handling for Semantic Analyser functions - Displays error message, as well as exits.
def errornodetype(node):
    if (isinstance(node, int)):
        print("Error: - Sum types do not match e.g. 'int + str', etc. Please check that datatypes match.")
    else:
        print("Error: - Type of object, right of assignment, does not match type of object, left of the assignment, e.g. 'int = str', etc. Please check that datatypes match")
    exit(1)