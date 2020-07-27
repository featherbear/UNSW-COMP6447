---
title: "Midsem Exam"
date: 2020-06-30T22:30:00+10:00

categories: ["Exam"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

## ezpz

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/ezpz)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/solve-ezpz.py)]

The program reads in 0xFE bytes in underflow, and writes those bytes in overflow.  
However, the buffer written to in overflow is less than 0xFE bytes.  
Buffer overflow attack!  

## ezpz2

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/ezpz2)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/solve-ezpz2.py)]

PIE is enabled, meaning that our base address has been randomised.  
We'll need to leak some address, which thankfully is done in `print_flag`, which is where printf is executed.  
0x131b can be subtracted from third address on the stack, which will give us the base address.  
We can then figure out the `win` address, and the `puts@GOT` address, then perform a printf injection to points `puts@GOT` to our `win` function

## leakme

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/leakme)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/midsem/solve-leakme.py)]

The program does a strcmp(RANDOM_STR, ebp-0x12), which errors if not equal.  
As we only have 12 bytes in our printf-vulnerable buffer, instead of leaking the contents of in RANDOM_STR, we can forcibly set it.  
We can then overflow gets(ebp-0x32) by 0x32-0x12 bytes, and write an 0x06.  
Therefore the string comparison will return true, and we get a shell.  
