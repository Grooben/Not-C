# compile.py
# Author: Tom Zajac
# Description: Compilation script. Utilises all modules of the compiler to generate assembly code.

import sys
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
    if x.typename is "String":
        outputProg.addData(asm.String(x.value, x.identifier))

# Add commands from intermediate code to program container
for x in intermediate.calls:
    # Get syscall object based on command name
    syscall = syscalls[x.command]

    # Data belonging to no identifier still has to be declared as static data.
    # This serves as a global counter to assign unique labels for this data in ASM.
    literalCount = 0

    # Reference command parameters in ASM code
    for y in x.data:
        # Is the data NOT assigned to an identifier?
        if not y.isName:
            # Increment the counter
            literalCount = literalCount + 1
            # Unique label for this data
            dataname = "_constant_{0}_{1}".format(x.command, literalCount)
            if y.typename is "String": 
                outputProg.addData(asm.String(y.value, dataname))
            # Add this data's unique label to the syscall symbol list 
            syscall.symbols.append(dataname)
            print("Added syscall for {0} command with {1} symbols.".format(x.command, len(syscall.symbols)))
        else:
            # Add this data's identifier to the syscall symbol list
            syscall.symbols.append(y.value)
    # Add the syscall to the program's command list
    outputProg.addCall(syscall)

outputFilename = "output.asm"

resultAsm = outputProg.asm()
if resultAsm is "":
    print("There was an error compiling the code.\n")
else:
    outf = open(outputFilename, "w")
    outf.write(resultAsm)
    outf.close()
    print("Code written successfully to " , outputFilename, ".")
