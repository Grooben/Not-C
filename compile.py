# compile.py
# Author: Tom Zajac
# Description: Compilation script. Utilises all modules of the compiler to generate assembly code.

import sys
import copy
import asm  # Imports ASM classes to generate x86 asm code
import bridge
import intercodegen as icg

def buildProgram(tree, symbolTable, outFile = "output.asm"):
    # Get intermediate program representation
    intermediate = icg.generate(tree, symbolTable)

    # Maps built-in command names to system calls to provide core functions to the language
    syscalls = {
            "print": asm.SysCallPrint(),
            "_!c_assign": asm.Core_AssignVal(),
            "_!c_math_add": asm.Core_Math_Add(),
            "_!c_math_mod": asm.Core_Math_Mod(),
            "_!c_math_sub": asm.Core_Math_Sub(),
            "_!c_math_divide": asm.Core_Math_Div(),
            "_!c_math_multi": asm.Core_Math_Mul(),
            }

    # Initialise program container
    outputProg = asm.ProgramCode()

    # Add static data from intermediate code to program container
    for x in intermediate.data:
        if x.typename == "String":
            outputProg.addData(asm.String(x.value, "nc_str_" + x.identifier))
        elif x.typename == "Integer":
            outputProg.addData(asm.Integer(x.value, "nc_int_" + x.identifier))

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
                prefix = ""
                if y.typename == "Integer":
                    prefix = "nc_int"
                elif y.typename == "String":
                    prefix = "nc_str"
                # Unique label for this data
                dataname = prefix + "_const_{0}_{1}".format(x.command, literalCount)
                print("Type: {0}".format(y.typename))
                validData = False # Prevents incorrectly scanned data (e.g. commas separating parameters) from being added
                if y.typename == "String": 
                    newString = asm.String(y.value, dataname)
                    outputProg.addData(newString)
                    validData = True
                elif y.typename == "Integer":
                    newInteger = asm.Integer(y.value, dataname)
                    outputProg.addData(newInteger)
                    validData = True
                # Add this data's unique label to the syscall symbol list 
                
                if validData:
                    print("Log (compile): Adding constant '{0}'".format(dataname))
                    syscall.symbols.append(bridge.CallData(y.typename, dataname, True)) 
            else:
                prefix = ""
                if y.typename == "Integer":
                    prefix = "nc_int_"
                elif y.typename == "String":
                    prefix = "nc_str_"
                # Add this data's identifier to the syscall symbol list
                syscall.symbols.append(bridge.CallData(y.typename, prefix + y.value, True))
        # Add the syscall to the program's command list
        outputProg.addCall(syscall)
        print("Added syscall for {0} command with {1} symbols.".format(x.command, len(syscall.symbols)))

    # TODO: Remove as this is handled by caller
    # Use provided filename or use default
    #if len(sys.argv) > 2:
    #        outputFilename = sys.argv[2]
    #else:
    #        outputFilename = "output.asm"
    outputFilename = outFile

    resultAsm = outputProg.asm()
    if resultAsm == "":
        print("There was an error compiling the code.\n")
    else:
        outf = open(outputFilename, "w")
        outf.write(resultAsm)
        outf.close()
        print("Code written successfully to " , outputFilename, ".")
