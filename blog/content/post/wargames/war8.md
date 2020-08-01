---
title: "Wargames 8"
date: 2020-07-29T12:00:00+10:00

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

## bsl

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week9/bsl)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week9/solve-bsl.py)]

### Scenario

The two `fgets` functions do not have a very large buffer space. And they won't overflow much.  
The `fgets` function in `least_fav` does seem to read in one too many bytes...

### Solution

By sending the maximum input size for the `least_fav::fgets` function, by nature of how `fgets` works, it writes an 0x00 into the last space.  
This space happens to be the LSB of the saved `ebp` value.  
When the function returns, the returning `fav` function now has a modified ebp at a lower address, which allows `most_fav::fgets` to become an opening for overflowing the stack frame for itself. This allows us to overwrite the EBP.

---

## piv_it

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week9/piv_it)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week9/solve-piv_it.py)]

### Scenario

Possible stack pivot, given the small buffer space from the vulnerable `read` call.

### Solution

Jokes! :trivial:  

Using the printf leak, we can find the address of the libc base.  
We can then find the addresses of `system` and the `/bin/sh` string, and overwrite the return address to system.
