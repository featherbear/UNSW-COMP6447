#!/bin/sh

gcc -m32 -mpreferred-stack-boundary=2 -masm=intel -no-pie 1.c -o lol

gcc -m32 -mpreferred-stack-boundary=2 -masm=intel -pie 2.c -o monalisa

gcc -m32 -pie 3.c -o root
