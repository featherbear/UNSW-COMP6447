# intro

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMS1pbnRybyIsImlhdCI6MTU5MTEwNTc2NiwiaXAiOiIyMDIuODcuMTYyLjI4In0.tJvBGlAdwXCFeGsWPqcGZMtzoKpCx70SX38nUV5-7-k}

## Scenario

There's a bunch of input prompts which we need to send the right answer to.

## Solution

The questions are hard-coded, so we can hard-code our responses.  
Using `strings` / a disassembler (i.e. BinaryNinja), we can find the final answer (`password`), and send that to get access to the shell.

## Script

```python3
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
connection.interactive() ## cat /flag
```

---

# too-slow

> Flag: FLAG{eyJhbGciOiJIUzI1NiJ9.eyJjaGFsIjoid2FyMS10b3Nsb3ciLCJpYXQiOjE1OTExMDYzMzEsImlwIjoiMjAyLjg3LjE2Mi4yOCJ9.-XwcHuPQWDbSVv1cF1XMPrxGTV1fdScB5j1d7c7VnTs}

## Scenario

We need to answer a bunch of addition questions in a short amount of time

## Solution

Programmatically read the input and send the output many times, until we are given access to the shell

## Script

```python3
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
```
