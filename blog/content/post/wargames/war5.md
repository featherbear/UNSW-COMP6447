---
title: "Wargames 5"
date: 2020-07-12T12:00:00+10:00

categories: ["Wargames"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

## Shellcrack

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/shellcrack)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/solve-shellcrack.py)]

### Scenario

There is an 8 byte long canary (generated from /dev/urandom) stored at ebp-0x14.  
Input is read into a buffer at ebp-0x44 to ebp-0x34, which is copied to ebp-0x24 to ebp-0x14.  
A vulnerability with the "%s" format specifier exists which allows the canary to be read from

### Solution

Send a name that is 16 bytes long, such as to remove the NULL terminator from the string.  
This will cause the program to print out the canary after the name.  
We can then perform a buffer overflow, and shellcode into the buffer whilst keeping the canary value correct.

---

## Stack Dump 2

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/stack-dump2)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/solve-stack-dump2.py)]

### Scenario

Similar to the week 3 stack-dump exercise, however this time with all protections enabled.  
We will need to leak the canary (input -> dump) in order to successfully override the return address of main

### Solution

An address on the stack is given, which we can use to calculate the address of the canary. By then using the memory map, we can figure out where the win function address has been relocated to.  
With the canary value and the win address, we can perform a buffer overflow at ebp-0x68.

---

## Image Viewer

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/image-viewer)]  
[[Source](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/image-viewer.c)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/solve-image-viewer.py)]

### Scenario

A flag supposedly exists in the file "flat earth truth", however there is censorship >:(. If the image ID corresponding to the flag file is entered, the program terminates early.  

We need a way to bypass the filename check.  
The `buf` address is immediately adjacent to the `images` variable, and the atoi function could be exploitable...


### Solution

The program reuses the `buf` buffer (128 bytes) for both the password and ID input. The `atoi` takes in a string and parses however many characters as it can, as an integers. We can exploit this functionality by entering a number, but taking control of the rest of the buffer with our own input data.  

As the memory for `buf` and `images` are next to each other, we can make `atoi` return a negative number, which would be used as a negative index of `images` - hence accessing `buf` as an image struct.

Our image structure needs to contain an ID and a pointer to a filename string. For the ID, we use `-2`, rather than `-1` due to the nature of `fgets` replacing the last character with a `\0`. The filename string can reside inside the buffer as well, in a different memory location.

To bypass the `strcmp` function, we can prepend a `./` to the flag file, resulting in `./flat earth truth`. Leaking the contents of this file reveals that the flag is actually located in the `/flag` file.

The password check is trivial.

---

## Source Code Audit

[[Source](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/source.c)]

* Directory traversal vulnerability - arbitrary write to any file
  * Location: `source.c:71`
  * Example: `action = "../../../../../../../../../../../../../etc/passwd"`
* Directory traversal vulnerability - arbitrary read of any file
  * Location: `source.c:97`
  * Example: `action = "../../../../../../../../../../../../../etc/passwd"`
* Race condition - possible corruption of result data
  * Location: `source.c:116-118`
  * Example: Two simultaneous `list_files` calls may both attempt to read/write from `list.txt`
* SET_PERMISSION_LEVEL - Incorrect check logic
  * Location: `source.c:171`
  * `admin_level` by default is set to `0` - allowing any user to perform RCE
* SET_PERMISSION_LEVEL - `level` not scanned properly
  * Location: `source.c:160`
  * Fix: `sscanf(action + 1, "%d", &level)`
  * Also, the level is reset with every new command???
* SET_PERMISSION_LEVEL - Implicit type cast
  * Location: `source.c:167`
  * `admin_level` is of type `uint8_t`, whilst `level` is of type `int`
  * An input of 256 will skip the `level == 0` check, but will result in `0` when casted to an 8-bit value, granting the user administrative privilege

---

## Reversing Challenge

[[Disassembly](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/chal.jpg)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week5/chall.c)]

The assembly code contains a function that returns a value.  
`0x2aaaaaaab` appears to be a rounded value of `2**32 // 6`, which appears to be a signed integer division by 6.

Two arguments, `arg1` and `arg2` are added together as a sum, and are worked on.  

The final return value appears to be `arg1 + arg2 - 6 * [ HI((arg1+arg2) * 0x2aaaaaaab) - (arithmetic (arg+arg2) >> by 0x1f (31)) ]`

In simplification, we reach the expression `sum - (sum / 6 * 6)`

* `sum/6`         => number of times 6 fits in the sum
* `(sum/6) * 6`   => quotient * 6 => highest multiple of 6 in the sum
* `sum - sum/6*6` => remainder when dividing by 6

This finally simplifies to the `mod 6` operation.
