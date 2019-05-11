# compile.py
# Author: Tom Zajac
# Description: Compilation script. Utilises all modules of the compiler to generate assembly code.

import sys
import copy
import asm  # Imports ASM classes to generate x86 asm code
import bridge # Imports intermediate code classes
import intercodegen as icg # Imports intemediate code generation functions


def buildProgram(tree, symbolTable, outFile = "output.asm"):
    # Maps built-in command names to sets of ASM instructions to provide core functions to the language
    syscalls = {
        "print": asm.Core_IO_Print(),
        "_!c_assign": asm.Core_AssignVal(),
        "_!c_math_add": asm.Core_Math_Add(),
        "_!c_math_mod": asm.Core_Math_Mod(),
        "_!c_math_sub": asm.Core_Math_Sub(),
        "_!c_math_divide": asm.Core_Math_Div(),
        "_!c_math_multi": asm.Core_Math_Mul(),
        "_!c_memory_savereg": asm.Core_Memory_SaveReg(),
        "_!c_condition_check": asm.Core_Condition_Check()
        }

    print("Log (compile): Beginning compilation. Generating intermediate code...")
    # Get intermediate program representation
    intermediate = icg.generate(tree, symbolTable, syscalls)
    print("Log (compile): Finished generating intermediate code.")

    print("Log (compile): Generating assembly code...")
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
            if y == None or isinstance(y, bridge.CallData) == False:
                continue
            y.checkTypes = False # hotfix to incorrect variable naming
            # Is the data NOT assigned to an identifier?
            if not y.isName:
                # Increment the counter
                literalCount = literalCount + 1
                prefix = ""
                if y.checkTypes:
                    if y.typename == "Integer":
                        prefix = "nc_int"
                    elif y.typename == "String":
                        prefix = "nc_str"
                # Unique label for this data
                dataname = prefix + "_const_{0}_{1}".format(x.command, literalCount)
                validData = False # Prevents incorrectly scanned data (e.g. commas separating parameters) from being added
                if isinstance(syscall, asm.Core_Memory_SaveReg) == False:
                    if y.typename == "String":
                        newString = asm.String(y.value, dataname)
                        outputProg.addData(newString)
                        validData = True
                    elif y.typename == "Integer":
                        newInteger = asm.Integer(y.value, dataname)
                        outputProg.addData(newInteger)
                        validData = True

                # Add this data's unique label to the syscall symbol list
                if isinstance(syscall, asm.Core_Memory_SaveReg) == True:
                    syscall.symbols.append(bridge.CallData("String", y.value, False))
                elif validData:
                    print("Log (compile): Adding constant '{0}'".format(dataname))
                    syscall.symbols.append(bridge.CallData(y.typename, dataname, True))
            else:
                prefix = ""
                if y.checkTypes:
                    if y.typename == "Integer":
                        prefix = "nc_int_"
                    elif y.typename == "String":
                        prefix = "nc_str_"
                # Add this data's identifier to the syscall symbol list
                syscall.symbols.append(bridge.CallData(y.typename, prefix + y.value, True))
        # Add the syscall to the program's command list
        outputProg.addCall(syscall)
        print("Log (compile): Added syscall for {0} command with {1} symbols.".format(x.command, len(syscall.symbols)))

    outputFilename = outFile

    resultAsm = outputProg.asm()
    if resultAsm == "":
        print("Error (compile): An unknown error occurred while compiling the code.\n")
    else:
        outf = open(outputFilename, "w")
        outf.write(resultAsm)
        outf.close()
        print("Log (compile): Code written successfully to " , outputFilename, ".")
