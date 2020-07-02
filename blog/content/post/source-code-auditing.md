---
title: "Source Code Auditing"
date: 2020-06-30T18:00:00+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

> People are bad programmers.

# Why read the source?

* Best way to find the bugs
* Easier than reversing the assembly
* [Fuzzers](../fuzzing) exist
* The more you understand, the easier it is to exploit

# Types of Bad Stuff...

## Bad API usage

* `printf(fmtString)` vulnerability
* `strcpy` - Keeps writing until a null terminator
  * What if there is no null-byte?
* `strncpy` - Doesn't place a null-terminator by itself
  * What if there is no null-byte?
* `memset(s, 100, 0)` sets 0 bytes to `100`
  * `memset(..., ..., 0)` does nothing!!!

## Integer overflows

```c
int a = INT_MAX
a += 1
// a ->>> -2147483648
```

```c
unsigned int a = 0
a -= 1
// a ->>> 2147483647
```

```c
if (length + 1 > maxLength) {
  error();
}
// If length is MAX_INT, MAX_INT+1 == 0; the program won't error
```

## Type conversions

Casting `short` to `int` etc

(int) 0x10000000 -> (short)0x0000

# Race conditions

Two functions that require to be executed in order.  
If they're not completed in the right order, what happens?

# Array out of bounds access

# Incorrect operator usage

# Incorrect pointer arithmetic

## Logic bugs

Yeah.