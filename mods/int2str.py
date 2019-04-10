# Reads assembly code for this module and changes internal names to separate from user program labels
def getAsm(dataRefs):
    f = open("mods/int2str.asm", "r")
    asm = f.read() # TODO: Read from file
    f.close()
    asm = asm.replace("{MODNAME}", "nc_mod_int2ascii_fnc_")
    for ref in dataRefs:
        asm = asm.replace("{{{0}}}".format(ref), dataRefs[ref].name)
    return asm
