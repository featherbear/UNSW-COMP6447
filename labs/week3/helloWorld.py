from pwn import *
import re

p = process("./runner")
p.recv()

assembly = f"""
    ;;;;;;;;;;;;;;;;;; Clear all the registers
    xor eax, eax  
    xor ebx, ebx
    xor edx, edx
    xor ecx, ecx
    
    mov eax, 0x04    ; syscall 4: write
    mov ebx, 0x01    ; fd 1: stdout
    push 0x21646C72  ; "rld!"
    push 0x6F77206F  ; "o wo"
    push 0x6C6C6568  ; "hell"
    mov ecx, esp     
    mov edx, 12      ; print 12 bytes
    int 0x80         ; syscall
"""

payload = asm(re.sub(';.*$', '', assembly, flags=re.MULTILINE))

payload = (b'\x90' * (512-len(payload))) + payload
p.send(payload)
print(p.recv())

