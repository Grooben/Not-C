# asm_test.py
# Author: Tom Zajac
# Description: Test script to utilise assembly code generation classes.

import asm  # Imports ASM classes to generate x86 asm code

helloData = asm.String("Hello, world! This is a code-generated string.", "testStr")
helloCall = asm.SysCallPrint(helloData.name)
helloProg = asm.ProgramCode()
helloProg.addCall(helloCall)
helloProg.addData(helloData)

resultAsm = helloProg.asm()
if resultAsm is "":
    print("There was an error compiling the code.\n")
else:
    outf = open("hello_compile_test.asm", "w")
    outf.write(resultAsm)
    outf.close()
