---
title: "Wargames 1"
date: 2020-06-03T12:00:00+10:00

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

## intro

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week1/intro)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week1/solve_intro.py)]

### Scenario

There's a bunch of input prompts which we need to send the right answer to.

### Solution

The questions are hard-coded, so we can hard-code our responses.  
Using `strings` / a disassembler (i.e. BinaryNinja), we can find the final answer (`password`), and send that to get access to the shell.

---

## too-slow

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week1/too-slow)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week1/solve_too-slow.py)]

### Scenario

We need to answer a bunch of addition questions in a short amount of time

### Solution

Programmatically read the input and send the output many times, until we are given access to the shell

