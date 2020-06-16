---
title: "Analysing Assembly"
date: 2020-06-16T18:39:21+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Compiler Optimisation

## While Loops

```
while (condition) { ... }
```

The less things we have to loop, the faster it is!  
The compiler optimises this by changing the structure

```
if (condition) {
  do { ... } while (condition);
}
```

---

## Switch Statements

### Sequential Values

> i.e. case 1, case 2, case 3

A jump table is used.  
A jump table is an array of function pointers.  

To reach the correct outcome, a variable is set to the start of the jump array, and the lowest case value is subtracted. By then adding the value, we find the address in the jump table that we will jump to.

### Non-Sequential

Also a jump table, but when dealing with non-sequential case values, default jumps are used

### Randomised Values

A binary tree is used to optimise the search time.

## strcpy

When copying a static string, the compiler can decide to just set value at the destination location to the string

----

# Word!

In data structures - a `word` is 4 bytes.  
In registers, a `word` is 2 bytes, a `dword` is 4 bytes.  

---

# Structs

* Offsets from the base of a value

---

# Functions

* Return values are - by convention - in `eax`
* [`leave`](https://stackoverflow.com/questions/38030356/what-is-the-difference-between-leave-and-ret) - restore the stack pointer (ebp)
* `ret` - return from the function
