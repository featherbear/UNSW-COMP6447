---
title: "Global Offset Table"
date: 2020-06-23T19:55:04+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# GOT - Global Offset Table

Every binary contains a jump table that points to functions of other libraries - this is known as the Global Offset Table.

At first all functions just point to themselves.  
Only when a function is called, does the entry in the GOT table change.

`pwndbg` has a `plt` and `got` function to identify entries of the GOT

# Attacking the GOT

We can modify the GOT table to point a library function to our own function.  
Whenever that library function is called, our own function will be called instead!

## Protecting from GOT modification

Relocation Read-Only (RELRO) protection can be set, which _should_ prevent the GOT table from being rewritten.

There is Partial RELRO - Which is actually useless because it doesn't protect anything...  
And there's Full RELRO - Which _actually_ stops us from attacking the GOT

