---
title: "Tutorial 7"
date: 2020-07-19T18:12:51+10:00

description: "ROP Chains"
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

It's :trivial: when we have a win function and/or NX enabled/disabled.  
When disabled, we need to use ROP chains!

_This solution was found in around 1997_

Buffer that we control contains pointers to instructions that exist in the program.  
When we override the return address.  

The program will then set the EIP to that address.  

The ESP probably won't change, meaning that the next `ret` will cause the EIP to change to the next gadget!  
When using a gadget that takes arguments, in order to clear up the arguments from the stack we need to find a `pop ret` gadget

## Stack Pivots

These are gadgets which modify the `ESP`

For example

```asm
sub esp, 0x100
ret
```

## libc

`libc` is a library that contains many useful functions things for the program to use.  
It also contains many useful gadgets :)

If we can find the version of `libc` that is used, we can use the addresses specific to that `libc` library

We'll need a pointer to `libc` though... which we might be able to leak from the GOT!  
Note: We can only leak from the GOT once the function has been linked.

`puts(puts)`

## ldd

> Print shared object dependencies

```bash
$> ldd ./swrop

linux-gate.so.1 (0xf7fc1000)
libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7daa000)
/lib/ld-linux.so.2 (0xf7fc2000)
```

## Using your own LIBC

```
LD_PRELOAD=/my/abs/path/to/my_custom_libc.so ./program
```

## Finding Gadgets

* Ropper
  * `ropper -f file`
  * Search | `ropper -f file --search "asm instruction"` (Search for exact)
  * Search | `ropper -f file --nocolor | grep "asm instruction"` (Search contains)

## Finding Strings

* <s>`strings -t x file`</s>
* BINJAAAA

## Useful gadgets to find

* Syscall gadget (`int 0x80`)

## Pwning

* `checksec`
* Find useful gadgets and addresses
  * `ropper` on the program
  * `ropper` on libc
  * `strings`
* Check PIE
  * If enabled, leak base
  * If disabled, add PIE base
* Overflow to control the return (get it to crash by going to an address)
* Fill buffer with gadgets

## Lazy

Add to your `.bashrc`

```
gropper () { ropper -f "$1" --nocolor | grep "$2"; }
```

Then you can run `gropper program "ret"`

