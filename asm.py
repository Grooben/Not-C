# asm.py
# Author: Tom Zajac
# Description: Provides classes to translate program logic into assembly code. 

from mods import int2str

class String:
    strCount = 0
    typename = "String"
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
        suffix = ""
        while self.data.find("\\n") >= 0:
            suffix = "10, "
            self.data = self.data.replace("\\n", "")
        return "{0}:\tdb '{1}', {2}0\n{0}_LEN:\tequ $-{0}".format(self.name, self.data, suffix)

class Integer:
    intCount = 0
    typename = "Integer"
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

class ByteBuffer:
    bufCount = 0
    def __init__(self, name=None, count=1024):
        self.arr = [None] * 1024
        self.name = name
        if name is None:
            bufCount += 1
            self.name = "buf{0}".format(bufCount)
    def asm(self):
        return "{0}:\ttimes {1} db 0, 0".format(self.name, len(self.arr))

class ProgramCode:
    def __init__(self):
        self.data = {}
        self.calls = []
    def addData(self, asmData):
        self.data[asmData.name] = asmData
    def addCall(self, asmCall):
        print("ASM: Adding call")
        for sym in asmCall.symbols:
            print("\t\t parameter: {0}".format(sym))
        self.calls.append(asmCall)
    def asm(self):
        ret = ""
        self.mods = {}
        # Prepare required modules
        self.mods["itoa"] = ModInt2Ascii()
        # Add required modules' internal data
        for data in self.mods["itoa"].internals["data"]:
            self.addData(self.mods["itoa"].internals["data"][data])
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
            ret += x.asm(self.mods) + "\n"
        # Exit code
        ret += "\nmov eax, 1\nmov ebx, 0\nint 80h"
        # Add modules code at the end
        for m in self.mods:
            ret += "\n" + self.mods[m].internals["code"]
        return ret

class SysCallPrint:
    def __init__(self, paramNames=[], reqMods=[]):
        self.symbols = paramNames
    def asm(self, reqMods=[]):
        ret = ""
        for x in self.symbols:
            if x.find("nc_int_") == 0:
                ret = ret + "{0}\n".format(reqMods["itoa"].asm(x))
            else:
                ret = ret + "mov ecx, {0}\nmov edx, {0}_LEN\n".format(x)
            ret = ret + "mov eax, 4\nmov ebx, 1\nint 80h\n"
        return ret

class ModInt2Ascii:
    # This is a module for the int2ascii algorithm.
    # The algorithm runs at run-time and
    # loads the resultant buffer pointer into ecx, and string length into edx
    def __init__(self):
        self.internals = {
            "data": 
                {
                    "org": Integer(0, "nc_mod_int2ascii_org"),
                    "num": Integer(0, "nc_mod_int2ascii_num"),
                    "buf": ByteBuffer("nc_mod_int2ascii_buf", 1024),
                    "chars": String("0123456789", "nc_mod_int2ascii_chars"),
                    "strLen": Integer(0, "nc_mod_int2ascii_strLen"),
                    "strSz": Integer(0, "nc_mod_int2ascii_strSz"),
                    "highestExp": Integer(0, "nc_mod_int2ascii_highestExp"),
                    "highestPow": Integer(1, "nc_mod_int2ascii_highestPow"),
                    "subs": Integer(0, "nc_mod_int2ascii_subs"),
                    "steps": Integer(0, "nc_mod_int2ascii_steps")
                },
            "code": ""
            }
        self.internals["code"] = int2str.getAsm(self.internals["data"])
    def asm(self, intName):
        return "\nmov eax, [{0}]\nmov [{1}], eax\nmov [{2}], eax\ncall nc_mod_int2ascii_fnc_start".format(intName, self.internals["data"]["org"].name, self.internals["data"]["num"].name)
