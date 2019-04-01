{MODNAME}start:
xor eax, eax ; Reset values as needed
mov [{subs}], eax
mov [{steps}], eax
mov [{strSz}], eax
mov [{strLen}], eax
mov [{highestExp}], eax
inc eax
mov [{highestPow}], eax
{MODNAME}mainLoop: ; while number != 0
        mov ecx, [{num}] ; check loop condition
        mov eax, 0
        cmp ecx, eax
        je {MODNAME}result
{MODNAME}findHighestPow:
        xor eax, eax
        mov [{highestExp}], eax ; resets exponent to be 0
        inc eax
        mov [{highestPow}], eax ; resets power to be 1
        dec eax ; resets eax to be 0 for the loop
{MODNAME}powFindLoop: ; while 10**highestPow <= number
        mov ecx, [{num}]
        mov ebx, [{highestPow}] ; check loop condition
        cmp ebx, ecx
        ja {MODNAME}powFindExit
        mov eax, 10
        imul ebx
        mov [{highestPow}], eax
        mov eax, 1
        mov ebx, [{highestExp}]
        inc ebx
        mov [{highestExp}], ebx
        jmp {MODNAME}powFindLoop
{MODNAME}powFindExit: 
        mov edx, 0
        cmp [{strSz}], edx ; if strSz == 0 then assign a size
        jne {MODNAME}powFindAlign
        mov edx, [{highestExp}]
        mov [{strSz}], edx
        xor edx, edx
{MODNAME}powFindAlign:
        mov ebx, 10
        mov eax, [{highestPow}]
        cdq
        idiv ebx
        mov [{highestPow}], eax
        mov eax, [{highestExp}]
        dec eax
        mov [{highestExp}], eax ; highestExp -= 1
        xor eax, eax
        mov [{subs}], eax; set subs = 0
{MODNAME}convertLoop: ; while True
        mov eax, [{num}]
        mov ebx, [{highestPow}]
{MODNAME}convertBuild:
        cmp eax, ebx; if number < 10**highestExp
        jge {MODNAME}convertRoot
        mov eax, [{subs}]
        mov ebx, [{strLen}]
        mov edx, [{chars}+eax]
        mov [{buf}+ebx], edx ; finalStr = finalStr + chars[subs]
        inc ebx
        mov [{strLen}], ebx
        xor eax, eax
        mov [{steps}], eax ; steps = 0
{MODNAME}convertBuildLoop1:
        mov ebx, 10
        xor eax, eax
        xor edx, edx
        mov eax, [{highestPow}]
{MODNAME}cbl1Div:
        cdq
        idiv ebx
        mov ebx, [{num}]
        cmp ebx, eax ; while number < 10**highestPow-1
        jge {MODNAME}convertBuildLoop2Pre
{MODNAME}cbl1Inc:
        mov eax, [{steps}]
        inc eax
        mov [{steps}], eax
        mov eax, [{highestExp}]
{MODNAME}cbl1Dec:
        dec eax
        mov [{highestExp}], eax
        mov eax, [{highestPow}]
        mov ebx, 10
        cdq
        idiv ebx
        mov [{highestPow}], eax
        jmp {MODNAME}convertBuildLoop1
{MODNAME}convertBuildLoop2Pre:
        xor ecx, ecx
{MODNAME}convertBuildLoop2:
        mov eax, [{steps}]
        dec eax
        cmp ecx, eax ; check 1 <= s < steps-1
        jg {MODNAME}convertLoopExit
        mov eax, '0'
        mov edx, [{strLen}]
        mov [{buf}+edx], eax
        inc edx
        mov [{strLen}], edx
        mov edx, [{steps}]
        dec edx
        dec edx
        cmp ecx, edx; if s >= steps - 2
        jl {MODNAME}convertBuildLoop2Post
{MODNAME}convertBuildLoop2Post:
        inc ecx ; s += 1
        jmp {MODNAME}convertBuildLoop2
{MODNAME}convertLoopExit:
        jmp {MODNAME}mainLoop
{MODNAME}convertRoot: ; number -= 10**highestExp
        mov eax, [{num}]
        mov ebx, [{highestPow}]
        sub eax, ebx
        mov [{num}], eax
        mov eax, [{subs}] ; subs += 1
        inc eax
        mov [{subs}], eax
        jmp {MODNAME}convertLoop
{MODNAME}result:
        mov ecx, {buf}
        mov edx, [{strLen}]
        ret
