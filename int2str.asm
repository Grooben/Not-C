section .data
	org: dd 900
	num: dd 900
	chars: db '0123456789', 0
	buf: times 1024 db 0, 0
	lastChar: db ' ', 0
	strSz: dd 0
	strLen: dd 0
	highestExp: dd 0
	highestPow: dd 1
	subs: dd 0
	steps: dd 0
section .text
	global _start
	_start:
	mainLoop: ; while number != 0
		mov ecx, [num] ; check loop condition
		mov eax, 0
		cmp ecx, eax
		je printStr
	findHighestPow:
		xor eax, eax
		mov [highestExp], eax ; resets exponent to be 0
		inc eax
		mov [highestPow], eax ; resets power to be 1
		dec eax ; resets eax to be 0 for the loop
	powFindLoop: ; while 10**highestPow <= number
		mov ecx, [num]
		mov ebx, [highestPow] ; check loop condition
		cmp ebx, ecx
		ja powFindExit
		mov eax, 10
		imul ebx
		mov [highestPow], eax
		mov eax, 1
		mov ebx, [highestExp]
		inc ebx
		mov [highestExp], ebx
		jmp powFindLoop
	powFindExit: 
		mov edx, 0
		cmp [strSz], edx ; if strSz == 0 then assign a size
		jne powFindAlign
		mov edx, [highestExp]
		mov [strSz], edx
		xor edx, edx
	powFindAlign:
		mov ebx, 10
		mov eax, [highestPow]
		cdq
		idiv ebx
		mov [highestPow], eax
		mov eax, [highestExp]
		dec eax
		mov [highestExp], eax ; highestExp -= 1
		xor eax, eax
		mov [subs], eax; set subs = 0
	convertLoop: ; while True
		mov eax, [num]
		mov ebx, [highestPow]
	convertBuild:
		cmp eax, ebx; if number < 10**highestExp
		jge convertRoot
		mov eax, [subs]
		mov ebx, [strLen]
		mov edx, [chars+eax]
		mov [buf+ebx], edx ; finalStr = finalStr + chars[subs]
		inc ebx
		mov [strLen], ebx
		xor eax, eax
		mov [steps], eax ; steps = 0
	convertBuildLoop1:
		mov ebx, 10
		xor eax, eax
		xor edx, edx
		mov eax, [highestPow]
	cbl1Div:
		cdq
		idiv ebx
		mov ebx, [num]
		cmp ebx, eax ; while number < 10**highestPow-1
		jge convertBuildLoop2Pre
	cbl1Inc:
		mov eax, [steps]
		inc eax
		mov [steps], eax
		mov eax, [highestExp]
	cbl1Dec:
		dec eax
		mov [highestExp], eax
		mov eax, [highestPow]
		mov ebx, 10
		cdq
		idiv ebx
		mov [highestPow], eax
		jmp convertBuildLoop1
	convertBuildLoop2Pre:
		xor ecx, ecx
	convertBuildLoop2:
		mov eax, [steps]
		dec eax
		cmp ecx, eax ; check 1 <= s < steps-1
		jg convertLoopExit
		mov eax, '0'
		mov edx, [strLen]
		mov [buf+edx], eax
		mov [lastChar], eax
		inc edx
		mov [strLen], edx
		mov edx, [steps]
		dec edx
		dec edx
		cmp ecx, edx; if s >= steps - 2
		jl convertBuildLoop2Post
	convertBuildLoop2Post:
		inc ecx ; s += 1
		jmp convertBuildLoop2
	convertLoopExit:
		jmp mainLoop
	convertRoot: ; number -= 10**highestExp
		mov eax, [num]
		mov ebx, [highestPow]
		sub eax, ebx
		mov [num], eax
		mov eax, [subs] ; subs += 1
		inc eax
		mov [subs], eax
		jmp convertLoop
	printStr:
		mov eax, 4
		mov ebx, 1
		mov ecx, buf
	printStrCall:
		mov edx, [strLen]
		int 80h
		mov eax, 1
		mov ebx, 0
		int 80h
	
