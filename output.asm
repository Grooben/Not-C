section .data
nc_int_var_a:	dd 0
nc_int_var_b:	dd 0
nc_int_var_c:	dd 0
_const__nc_assign_1:	dd 0
_const__nc_assign_2:	dd 2
_const__nc_assign_3:	dd 2
_const__nc_assign_4:	dd 69
_const_print_5:	db '', 10, 0
_const_print_5_LEN:	equ $-_const_print_5
_const_print_7:	db ' + ', 0
_const_print_7_LEN:	equ $-_const_print_7
_const_print_8:	db ' = ', 0
_const_print_8_LEN:	equ $-_const_print_8
_const_print_9:	db '', 10, 0
_const_print_9_LEN:	equ $-_const_print_9
_const_print_10:	db '', 10, 0
_const_print_10_LEN:	equ $-_const_print_10
nc_mod_int2ascii_org:	dd 0
nc_mod_int2ascii_num:	dd 0
nc_mod_int2ascii_buf:	times 1024 db 0, 0
nc_mod_int2ascii_chars:	db '0123456789', 0
nc_mod_int2ascii_chars_LEN:	equ $-nc_mod_int2ascii_chars
nc_mod_int2ascii_strLen:	dd 0
nc_mod_int2ascii_strSz:	dd 0
nc_mod_int2ascii_highestExp:	dd 0
nc_mod_int2ascii_highestPow:	dd 1
nc_mod_int2ascii_subs:	dd 0
nc_mod_int2ascii_steps:	dd 0

section .text
global _start
_start:
mov eax, [_const__nc_assign_1]
mov [nc_int_var_a], eax


mov eax, [nc_int_var_a]
mov [nc_mod_int2ascii_org], eax
mov [nc_mod_int2ascii_num], eax
call nc_mod_int2ascii_fnc_start
mov eax, 4
mov ebx, 1
int 80h

mov eax, [_const__nc_assign_2]
mov [nc_int_var_a], eax

mov eax, [_const__nc_assign_3]
mov [nc_int_var_b], eax

mov eax, [_const__nc_assign_4]
mov [nc_int_var_c], eax

mov ecx, _const_print_5
mov edx, _const_print_5_LEN
mov eax, 4
mov ebx, 1
int 80h


mov eax, [nc_int_var_a]
mov ebx, [nc_int_var_b]
add eax, ebx


mov [nc_int_var_c], eax


mov eax, [nc_int_var_a]
mov [nc_mod_int2ascii_org], eax
mov [nc_mod_int2ascii_num], eax
call nc_mod_int2ascii_fnc_start
mov eax, 4
mov ebx, 1
int 80h
mov ecx, _const_print_7
mov edx, _const_print_7_LEN
mov eax, 4
mov ebx, 1
int 80h

mov eax, [nc_int_var_b]
mov [nc_mod_int2ascii_org], eax
mov [nc_mod_int2ascii_num], eax
call nc_mod_int2ascii_fnc_start
mov eax, 4
mov ebx, 1
int 80h
mov ecx, _const_print_8
mov edx, _const_print_8_LEN
mov eax, 4
mov ebx, 1
int 80h

mov eax, [nc_int_var_c]
mov [nc_mod_int2ascii_org], eax
mov [nc_mod_int2ascii_num], eax
call nc_mod_int2ascii_fnc_start
mov eax, 4
mov ebx, 1
int 80h
mov ecx, _const_print_9
mov edx, _const_print_9_LEN
mov eax, 4
mov ebx, 1
int 80h


mov eax, [nc_int_var_c]
mov [nc_mod_int2ascii_org], eax
mov [nc_mod_int2ascii_num], eax
call nc_mod_int2ascii_fnc_start
mov eax, 4
mov ebx, 1
int 80h
mov ecx, _const_print_10
mov edx, _const_print_10_LEN
mov eax, 4
mov ebx, 1
int 80h


mov eax, 1
mov ebx, 0
int 80h
; This is an integer-to-ASCII conversion module for the Not-C compiler.
; Use the attached Python script to include it in the program.
nc_mod_int2ascii_fnc_start:
xor eax, eax ; Reset values as needed
cmp [nc_mod_int2ascii_num], eax ; check if number is zero and return immediately if so
jne nc_mod_int2ascii_fnc_algorithm
mov ebx, '0'
mov [nc_mod_int2ascii_buf], ebx
mov ecx, nc_mod_int2ascii_buf
mov edx, 1
xor ebx, ebx
ret
nc_mod_int2ascii_fnc_algorithm:
mov [nc_mod_int2ascii_subs], eax
mov [nc_mod_int2ascii_steps], eax
mov [nc_mod_int2ascii_strSz], eax
mov [nc_mod_int2ascii_strLen], eax
mov [nc_mod_int2ascii_highestExp], eax
inc eax
mov [nc_mod_int2ascii_highestPow], eax
nc_mod_int2ascii_fnc_mainLoop: ; while number != 0
        mov ecx, [nc_mod_int2ascii_num] ; check loop condition
        mov eax, 0
        cmp ecx, eax
        je nc_mod_int2ascii_fnc_result
nc_mod_int2ascii_fnc_findHighestPow:
        xor eax, eax
        mov [nc_mod_int2ascii_highestExp], eax ; resets exponent to be 0
        inc eax
        mov [nc_mod_int2ascii_highestPow], eax ; resets power to be 1
        dec eax ; resets eax to be 0 for the loop
nc_mod_int2ascii_fnc_powFindLoop: ; while 10**highestPow <= number
        mov ecx, [nc_mod_int2ascii_num]
        mov ebx, [nc_mod_int2ascii_highestPow] ; check loop condition
        cmp ebx, ecx
        ja nc_mod_int2ascii_fnc_powFindExit
        mov eax, 10
        imul ebx
        mov [nc_mod_int2ascii_highestPow], eax
        mov eax, 1
        mov ebx, [nc_mod_int2ascii_highestExp]
        inc ebx
        mov [nc_mod_int2ascii_highestExp], ebx
        jmp nc_mod_int2ascii_fnc_powFindLoop
nc_mod_int2ascii_fnc_powFindExit:
        mov edx, 0
        cmp [nc_mod_int2ascii_strSz], edx ; if strSz == 0 then assign a size
        jne nc_mod_int2ascii_fnc_powFindAlign
        mov edx, [nc_mod_int2ascii_highestExp]
        mov [nc_mod_int2ascii_strSz], edx
        xor edx, edx
nc_mod_int2ascii_fnc_powFindAlign:
        mov ebx, 10
        mov eax, [nc_mod_int2ascii_highestPow]
        cdq
        idiv ebx
        mov [nc_mod_int2ascii_highestPow], eax
        mov eax, [nc_mod_int2ascii_highestExp]
        dec eax
        mov [nc_mod_int2ascii_highestExp], eax ; highestExp -= 1
        xor eax, eax
        mov [nc_mod_int2ascii_subs], eax; set subs = 0
nc_mod_int2ascii_fnc_convertLoop: ; while True
        mov eax, [nc_mod_int2ascii_num]
        mov ebx, [nc_mod_int2ascii_highestPow]
nc_mod_int2ascii_fnc_convertBuild:
        cmp eax, ebx; if number < 10**highestExp
        jge nc_mod_int2ascii_fnc_convertRoot
        mov eax, [nc_mod_int2ascii_subs]
        mov ebx, [nc_mod_int2ascii_strLen]
        mov edx, [nc_mod_int2ascii_chars+eax]
        mov [nc_mod_int2ascii_buf+ebx], edx ; finalStr = finalStr + chars[subs]
        inc ebx
        mov [nc_mod_int2ascii_strLen], ebx
        xor eax, eax
        mov [nc_mod_int2ascii_steps], eax ; steps = 0
nc_mod_int2ascii_fnc_convertBuildLoop1:
        mov ebx, 10
        xor eax, eax
        xor edx, edx
        mov eax, [nc_mod_int2ascii_highestPow]
nc_mod_int2ascii_fnc_cbl1Div:
        cdq
        idiv ebx
        mov ebx, [nc_mod_int2ascii_num]
        cmp ebx, eax ; while number < 10**highestPow-1
        jge nc_mod_int2ascii_fnc_convertBuildLoop2Pre
nc_mod_int2ascii_fnc_cbl1Inc:
        mov eax, [nc_mod_int2ascii_steps]
        inc eax
        mov [nc_mod_int2ascii_steps], eax
        mov eax, [nc_mod_int2ascii_highestExp]
nc_mod_int2ascii_fnc_cbl1Dec:
        dec eax
        mov [nc_mod_int2ascii_highestExp], eax
        mov eax, [nc_mod_int2ascii_highestPow]
        mov ebx, 10
        cdq
        idiv ebx
        mov [nc_mod_int2ascii_highestPow], eax
        jmp nc_mod_int2ascii_fnc_convertBuildLoop1
nc_mod_int2ascii_fnc_convertBuildLoop2Pre:
        xor ecx, ecx
nc_mod_int2ascii_fnc_convertBuildLoop2:
        mov eax, [nc_mod_int2ascii_steps]
        dec eax
        cmp ecx, eax ; check 1 <= s < steps-1
        jg nc_mod_int2ascii_fnc_convertLoopExit
        mov eax, '0'
        mov edx, [nc_mod_int2ascii_strLen]
        mov [nc_mod_int2ascii_buf+edx], eax
        inc edx
        mov [nc_mod_int2ascii_strLen], edx
        mov edx, [nc_mod_int2ascii_steps]
        dec edx
        dec edx
        cmp ecx, edx; if s >= steps - 2
        jl nc_mod_int2ascii_fnc_convertBuildLoop2Post
nc_mod_int2ascii_fnc_convertBuildLoop2Post:
        inc ecx ; s += 1
        jmp nc_mod_int2ascii_fnc_convertBuildLoop2
nc_mod_int2ascii_fnc_convertLoopExit:
        jmp nc_mod_int2ascii_fnc_mainLoop
nc_mod_int2ascii_fnc_convertRoot: ; number -= 10**highestExp
        mov eax, [nc_mod_int2ascii_num]
        mov ebx, [nc_mod_int2ascii_highestPow]
        sub eax, ebx
        mov [nc_mod_int2ascii_num], eax
        mov eax, [nc_mod_int2ascii_subs] ; subs += 1
        inc eax
        mov [nc_mod_int2ascii_subs], eax
        jmp nc_mod_int2ascii_fnc_convertLoop
nc_mod_int2ascii_fnc_result:
        mov ecx, nc_mod_int2ascii_buf
        mov edx, [nc_mod_int2ascii_strLen]
        ret
