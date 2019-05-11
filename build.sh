#!/bin/bash
python3 ./main.py $1 $2.asm && nasm -f elf64 ./$2.asm && ld ./$2.o -o./$2
