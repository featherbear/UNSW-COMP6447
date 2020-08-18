'''
Helper function to generate shellcode from assembly instructions that contain #comments
'''
def shellGen(assembly):
    from pwn import asm
    import re

    return asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

