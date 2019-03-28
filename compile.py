# compile.py
# Author: Tom Zajac
# Description: Compilation script. Utilises all modules of the compiler to generate assembly code.

import sys
import copy
import asm  # Imports ASM classes to generate x86 asm code
import intercodegen as icg

# Get intermediate program representation
intermediate = icg.generate(sys.argv[1])

# Maps built-in command names to system calls to provide core functions to the language
syscalls = {
        "print": asm.SysCallPrint()
        }

# Initialise program container
outputProg = asm.ProgramCode()

# Add static data from intermediate code to program container
for x in intermediate.data:
    if x.typename == "String":
        outputProg.addData(asm.String(x.value, x.identifier))
    elif x.typename == "Integer":
        outputProg.addData(asm.Integer(x.value, x.identifier))

# Data belonging to no identifier still has to be declared as static data.
# This serves as a global counter to assign unique labels for this data in ASM.
# The variable is used in the commandcall loop that follows.
literalCount = 0

# Add commands from intermediate code to program container
for x in intermediate.calls:
    # Get syscall object based on command name
    syscall = copy.deepcopy(syscalls[x.command])

    # Reference command parameters in ASM code
    for y in x.data:
        # Is the data NOT assigned to an identifier?
        if not y.isName:
            # Increment the counter
            literalCount = literalCount + 1
            # Unique label for this data
            dataname = "_constant_{0}_{1}".format(x.command, literalCount)
            if y.typename == "String": 
                newString = asm.String(y.value, dataname)
                outputProg.addData(newString)
            elif y.typename == "Integer":
                newInteger = asm.Integer(y.value, dataname)
                outputProg.addData(newInteger)
            # Add this data's unique label to the syscall symbol list 
            syscall.symbols.append(dataname)
            print("Added syscall for {0} command with {1} symbols.".format(x.command, len(syscall.symbols)))
        else:
            # Add this data's identifier to the syscall symbol list
            syscall.symbols.append(y.value)
    # Add the syscall to the program's command list
    outputProg.addCall(syscall)

# Use provided filename or use default
if len(sys.argv) > 2:
	outputFilename = sys.argv[2]
else:
	outputFilename = "output.asm"

resultAsm = outputProg.asm()
if resultAsm == "":
    print("There was an error compiling the code.\n")
else:
    outf = open(outputFilename, "w")
    outf.write(resultAsm)
    outf.close()
    print("Code written successfully to " , outputFilename, ".")
