# compile.py
# Author: Tom Zajac
# Description: Compilation script. Utilises all modules of the compiler to generate assembly code.

import sys
import asm  # Imports ASM classes to generate x86 asm code
import intercodegen as icg

# Get intermediate program representation
intermediate = icg.generate(sys.argv[1])

helloData = asm.String("Hello, world! This is a code-generated string.", "testStr")
helloCall = asm.SysCallPrint(helloData.name)
helloProg = asm.ProgramCode()
helloProg.addCall(helloCall)
helloProg.addData(helloData)

syscalls = {
        "print": asm.SysCallPrint()
        }

outputProg = asm.ProgramCode()

for x in intermediate.data:
    if x.typename is "String":
        outputProg.addData(asm.String(x.value, x.identifier))
# Need to declare hardcoded values as static data - come up with a naming convention for them
for x in intermediate.calls:
    syscall = syscalls[x.command]
    literalCount = 0
    for y in x.data:
        if not y.isName:
            literalCount = literalCount + 1
            dataname = "_constant_{0}_{1}".format(x.command, literalCount)
            if y.typename is "String": 
                outputProg.addData(asm.String(y.value, dataname))
            syscall.symbols.append(dataname)
            print("Added syscall for {0} command with {1} symbols.".format(x.command, len(syscall.symbols)))
        else:
            syscall.symbols.append(y.value)
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
