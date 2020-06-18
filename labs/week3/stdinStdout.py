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
    
    ## Read in 20 bytes
    mov eax, 0x03    # syscall 3: read
    xor ebx, ebx     # fd 0: stdin
    sub esp, 0x14    # allocate 20 bytes in the stack
    mov ecx, esp     # read into ecx // esp-0x14
    mov edx, 0x14    # read 20 bytes
    int 0x80

    # syscall 3 puts the number of read bytes into eax

    mov edx, eax     # print the number of read in bytes
    mov eax, 0x04    # syscall 4: write
    mov ebx, 0x01    # fd 1: stdout
    mov ecx, esp     # read from ecx // esp-0x14
    int 0x80         # syscall
"""


payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))
# payload = (b'\x90' * (512-len(payload))) + payload

p.send(payload)
p.sendline("6447 is the best")
print(p.recv())
