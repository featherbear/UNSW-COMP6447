from pwn import *
import re

p = process("./runner")
p.recv()

assembly = f"""
    ################## Clear all the registers
    xor eax, eax  
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx
    
    # Use esi for count
    xor esi, esi
    jmp print

done:
    push 0x0000000A
    push 0x216e6977
    push 0x20756f59
    mov eax, 0x04    # syscall 4: write
    mov ebx, 0x01    # fd 1: stdout
    mov ecx, esp     # read from ecx
    mov edx, 9       
    int 0x80         # syscall
    ret

print:
    # Efficient method
    mov ecx, esi
    add ecx, 0x0A30

    # Not so efficient method
        # mov ecx, 0x30
        # add ecx, esi
        # and ecx, 0xFFFF00FF
        # or ecx,  0x00000A00
    push ecx

    mov eax, 0x04    # syscall 4: write
    mov ebx, 0x01    # fd 1: stdout
    mov ecx, esp     # read from ecx
    mov edx, 0x2     # print byte and new line
    int 0x80         # syscall
    pop ecx

    cmp esi, 9
    je done
    inc esi

    jmp print
"""

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

p.send(payload)

while True:
    try:
        print(p.recvline().decode(), end="")
    except:
        break
