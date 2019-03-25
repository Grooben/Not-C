# asm.py
# Author: Tom Zajac
# Description: Provides classes to translate program logic into assembly code. 

class String:
    strCount = 0
    def __init__(self, content=None, name=None):
        if content is None:
            self.data = ""
        else:
            self.data = content
        if name is None:
            strCount += 1
            self.name = "string{0}".format(strCount)
        else:
            self.name = name
    def asm(self):
        return "{0}:\tdb '{1}', 0\n{0}_LEN:\tequ $-{0}".format(self.name, self.data)

class Integer:
    intCount = 0
    def __init__(self, value=None, name=None):
        if value is None:
            self.data = ""
        else:
            self.data = value
        if name is None:
            intCount += 1
            self.name = "int{0}".format(intCount)
        else:
            self.name = name
    def asm(self):
        return "{0}:\tdd {1}".format(self.name, self.data)


class ProgramCode:
    def __init__(self):
        self.data = {}
        self.calls = []
    def addData(self, asmData):
        self.data[asmData.name] = asmData
    def addCall(self, asmCall):
        self.calls.append(asmCall)
    def asm(self):
        ret = ""
        # Initialise data
        ret = "section .data\n"
        for x in self.data:
            ret += self.data[x].asm() + "\n"
        # Add logic
        ret += "\nsection .text\nglobal _start\n_start:\n"
        for x in self.calls:
            for s in x.symbols:
                if s not in self.data:
                    print("COMPILE ERROR: Symbol '{0}' referenced in source has not been found in program data!\n".format(s))
                    return ""
            ret += x.asm() + "\n"
        # Exit code
        ret += "\nmov eax, 1\nmov ebx, 0\nint 80h"
        return ret

class SysCallPrint:
    def __init__(self, paramNames=[]):
        self.symbols = paramNames
    def asm(self):
        ret = ""
        for x in self.symbols:
            ret = ret + "mov eax, 4\nmov ebx, 1\nmov ecx, {0}\nmov edx, {0}_LEN\nint 80h\n".format(x)
        return ret


