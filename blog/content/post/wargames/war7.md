---
title: "Wargames 7"
date: 2020-06-22T12:00:00+10:00

categories: ["Wargames"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

draft: true

---

## usemedontabuseme

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/usemedontabuseme)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/solve-usemedontabuseme.py)]

### Scenario

Functions are given that allow us to create, rename and delete a certain of each allocated memory structure. We need to leverage the fact that chunk metadata and content are stored in the same location.

### Solution

We are able to view the name of a killed clone. Due to the way free chunks are stored, the pointer of the next free chunk is stored in the same location as the name. This allows us to override the location of the second-next chunk location.  

By allocating a chunk (A), then allocating a chunk (B) that starts `0xc` bytes after (A), we can modify the function pointer. By using the Give Hint functionality, the modified function pointer will be executed

---

## ezpz1

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/ezpz1)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/solve-ezpz1.py)]

### Scenario

The program performs two malloc calls for each question creation.  
When freed, if they are not cleared - their contents can be accessed.  
The order of freeing is also important, as the last freed item becomes the head of the free list.

### Solution

When creating and freeing a question, the two allocated chunks are freed in the wrong order.  
By still having access to previous container chunk, we can set the contents of a new question - which will actually modify the previous container chunk.

---

## ezpz2

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/ezpz2)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/solve-ezpz2.py)]

### Scenario

Compared to ezpz1, ezpz2 frees the two chunks for each question in the right order.  
However, the `fgets` function in `set_question` is vulnerable to a buffer overlfow.  

### Solution

By performing a buffer/heap overflow, we are able to control the contents chunks of adjacent questions.  
This allows us to modify the address of those questions' buffers.  
We can leak the address of the libc calls from the GOT table by overwriting the buffer location to the GOT table entry.  
By leaking several addresses, we can find the correct libc version - to then calculate the correct offset for the `system` call.  
The `free` address of the GOT can be overridden to the `system` call, to gain access to the shell.

---

## ezpz2

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/ezpz2)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/solve-ezpz2.py)]

### Scenario

Compared to ezpz1, ezpz2 frees the two chunks for each question in the right order.  
However, the `fgets` function in `set_question` is vulnerable to a buffer overlfow.  

### Solution

By performing a buffer/heap overflow, we are able to control the contents chunks of adjacent questions.  
This allows us to modify the address of those questions' buffers.  
We can leak the address of the libc calls from the GOT table by overwriting the buffer location to the GOT table entry.  
By leaking several addresses, we can find the correct libc version - to then calculate the correct offset for the `system` call.  
The `free` address of the GOT can be overridden to the `system` call, to gain access to the shell.

---

## notezpz

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/notezpz)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week8/solve-notezpz.py)]

