#Author : Craig Clephane 
#Last edited : 09/04/2019
#Last editor : Macauley Scullion

#File which contains error functions throughout all phases of the complier.

#Error Handling for Lexical Analysis functions - Displays error message, as well as exits. 
def error(line, col, msg):
    print(line, col, msg)
    exit(1)

def followUnrecognized(line, col):
    print("Error: - 'Follow' : Unrecognized character./nLine 5%/nColumn 5%" % (line, col) )
    exit(1)

def invalidNumber(line, col, text):
    print("Error: - 'identifiersOrIntegers' : Invalid number: %s/nLine 5%/nColumn 5%" % (Text, line, col))
    exit(1)

def endOfFile(line, col):
    print("Error: - 'commentsAndDiv' : End of file detected within comment /nLine 5%/nColumn 5%" % (line, col))
    exit(1)

def endOfFile2(line, col):
    print("Error: - 'stringLit' : End of file detected while scanning literal /nLine 5%/nColumn 5%" % (line, col))
    exit(1)

def endOfLine(line, col):
    print("Error: - 'stringLit' : End of line detected while scanning literal /nLine 5%/nColumn 5%" % (line, col))
    exit(1)

#Error Handling for Symble Table functions - Displays error message, as well as exits. 
def error_dup(name, type):
    print("Error: - Dupilicate variable initialized. Please check that all variables are unique.")
    exit(1)

#Error Handling for Semantic Analyser functions - Displays error message, as well as exits.
def errornodetypeassign(line):
    print("Error: - Type of object, right of assignment, does not match type of object, left of the assignment, e.g. 'int = str', etc. Please check that datatypes match."
          "\n Line: ", line)
    exit(1)

def errornodetypesum(line):
    print("Error: - Sum types do not match e.g. 'int + str', etc. Please check that datatypes match. Only Int's can be summmed."
          "\n Line: ", line)
    exit(1)


def errorifcompare(line):
    print("Error: - If statment does not contain a comparison. Please make sure that the if statement compares data."
          "\n Line: ", line)
    exit(1)

def errorifnodes(line):
    print("Error: - If statement comparisons are not of the same type. e.g. int == str. Please check comparison datatypes match."
          "\n Line: ", line)
    exit(1)


def errornotdeclared(val, line):
    print("Error: - Use of undelared variable: " + val +
          "\n Line: ", line)
    exit(1)

def errorbeforedeclared(val, line):
    print("Error: - Use of variable before declaration: " + val +
          "\n Line: ", line)
    exit(1)