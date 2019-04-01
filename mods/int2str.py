def getAsm(dataRefs):
    f = open("mods/int2str.asm", "r")
    asm = f.read() # TODO: Read from file 
    f.close()
    asm = asm.replace("{MODNAME}", "nc_mod_int2ascii_fnc_")
    for ref in dataRefs:
        print(ref)
        print(dataRefs[ref].name)
        print("{{{0}}}".format(ref))
        asm = asm.replace("{{{0}}}".format(ref), dataRefs[ref].name)
    return asm
