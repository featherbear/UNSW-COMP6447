from pwn import *

connection = remote("plsdonthaq.me", 1026)
print(connection.recvline())

while True:
    data = connection.recv()
    print(data)
    if b"Well done" in data:
        connection.interactive() ## cat /flag
    else:
        connection.sendline(str(eval(data[:-3])))
        connection.recvline()

# FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMS10b3Nsb3ciLCJpYXQiOjE1OTExMDYzMzEsImlwIjoiMjAyLjg3LjE2Mi4yOCJ9.-XwcHuPQWDbSVv1cF1XMPrxGTV1fdScB5j1d7c7VnTs}