from pwn import *
import re

connection = remote("plsdonthaq.me", 1025)
data = connection.recvlines(timeout=1)
print(data)

match = re.findall("\{(.*)\}", data[2].decode())[0]
match = eval(match) # ohohoho...

connection.sendline(str(match))
print(connection.recvlines(timeout=1))

connection.sendline(str(hex(match - 0x103)))
print(connection.recvlines(timeout=1))

connection.sendline(struct.pack('H', 0x1337))
data = connection.recvlines(timeout=1)
print(data)

r = struct.unpack('I', data[2])[0]
connection.sendline(str(r))
print(connection.recvlines(timeout=1))

connection.sendline(str(hex(r)))
print(connection.recvlines(timeout=1))

connection.sendline(str(12835 + 12835))
print(connection.recvlines(timeout=1))

connection.sendline("password")
connection.interactive()

# FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMS1pbnRybyIsImlhdCI6MTU5MTEwNTc2NiwiaXAiOiIyMDIuODcuMTYyLjI4In0.tJvBGlAdwXCFeGsWPqcGZMtzoKpCx70SX38nUV5-7-k}

