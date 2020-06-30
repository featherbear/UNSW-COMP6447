---
title: "Format Strings"
date: 2020-06-23T18:00:00+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Format Strings 

`%<flags><width><precision><modifier><type>`

---

`printf(variable_fmt_string)` is bad!  

If we have control over the format string, i.e `variable_fmt_string = "%d%d%d%d"` we can read (and also write!!!) data arbitrarily

* `printf("%*s", n, str)` -> Print `str` with minimum `n` pad

# `%n`

`%n` sets a variable to the number of written bytes.  

This can help with ASCII art, but we can use it maliciously to write to memory!

> `printf` uses the items stored from the stack.  
If we don't pass items into the `printf(fmt,...)` it will just use the next things on the stack.  
Security vulnerability!

<!-- xxd -> bytes to hex representation -->

# `%s`

`%s` prints the content in a pointer, as a string

If you put 4 bytes in your buffer and tell printf to use it as a pointer... dun dun unnn!?

# Stack Index

`%8$p` - print 8th item as pointer


# Write x bytes into %n

Use format string to generate x characters

`%100c` -> prints 100 characters ( pad + hex)

---

## Writing in smaller chunks

It may be better to write two 2 byte-chunks, or 4 1-byte chunks, rather than one 4-byte chunk
This will save the number of data bits needed to be outputted

* `%n` - 4 bytes
* `%hn` - 2 bytes
* `%hhn` - 1 byte
