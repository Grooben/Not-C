section .data
	org: dd 420
	num: dd 420
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
	powFindExit: ; TODO: Assign strSz
		mov edx, 0
		cmp [strSz], edx
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
		mov [lastChar], edx ; DEBUGGING
		inc ebx
		mov [strLen], ebx
		mov ebx, [strSz]
		dec ebx
		cmp [strLen], ebx
		je printStr
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
		jge convertBuildCheck ; TODO: Loop dosn't terminate
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
	convertBuildCheck:
		mov ebx, 2
		mov edx, [strLen]
		cmp [steps], ebx ; if steps == 2
		jne convertBuildLoop2Pre
		mov eax, '0'
		mov [buf+edx], eax 
		mov [lastChar], eax
		inc edx
		mov [strLen], edx
		mov edx, [strSz]
		dec edx
		cmp [strLen], edx
		je printStr
	convertBuildLoop2Pre:
		xor ecx, ecx
		inc ecx ; range(1, steps-1)
	convertBuildLoop2:
		mov eax, [steps]
		dec eax
		dec eax
		cmp ecx, eax ; check 1 <= s < steps-1
		jge convertLoopExit
		mov eax, '0'
		mov edx, [strLen]
		mov [buf+edx], eax
		mov [lastChar], eax
		inc edx
		mov [strLen], edx
		mov edx, [strSz]
		dec edx
		cmp edx, [strLen]
		je printStr
		mov edx, [steps]
		dec edx
		dec edx
		cmp ecx, edx; if s >= steps - 2
		jl convertBuildLoop2Post
		mov eax, '0'
		mov edx, [strLen]
		mov [buf+edx], eax
		mov [lastChar], eax
		inc edx
		mov [strLen], edx
		mov edx, [strSz]
		dec edx
		cmp [strLen], edx
		je printStr
	convertBuildLoop2Post:
		inc ecx ; s += 1
		jmp convertBuildLoop2
	convertLoopExit: ; if number == 0 and org % 10 == 0
		mov eax, [num]
		mov ebx, 0
		cmp eax, ebx
		jne mainLoop
		mov ebx, [org]
		xor edx, edx
		mov eax, 10
		cdq
		idiv ebx
		mov ebx, 0
		cmp edx, ebx
		jne mainLoop
		mov eax, '0'
		mov edx, [strLen]
		mov [buf+edx], eax ; finalStr += "0"
		mov [lastChar], eax
		inc edx
		mov [strLen], edx
		mov edx, [strSz]
		dec edx
		cmp [strLen], edx
		je printStr
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
		mov edx, [strLen]
		inc edx
		mov [strLen], edx
	printStrCall:
		mov edx, strLen
		int 80h
		mov eax, 1
		mov ebx, 0
		int 80h
		; TODO: print string from buf
	
