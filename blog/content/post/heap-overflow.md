---
title: "Heap Overflow"
date: 2020-07-21T18:11:11+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

* Heap is hard!
* Heap exploit is linked to your `libc` version
  * May be useful to run a dockerised container
  * `docker run -d --rm -h banana --name banana -v $(pwd):/ctf/work --cap-add=SYS_PTRACE skysider/pwndocker`

# Malloc

Malloc is a first-fit allocator (finds the first memory space that fits the requested size).  
(i.e the last thing that was freed)

* dlmalloc - general
* ptmalloc - glibc
* jemalloc - Firefox
* tcmalloc - Chrome


# Arena

The arena is the region where free chunks are stored for a thread.

# Chunk Usage

A chunk is either **in use**, or **free**

* Minimum size of a chunk is `4 * sizeof(void*)`

When allocating, the contents of the forward pointer is given to the user

## In-Use

* Previous size (helps us to get the address of the previous address)
* Size
* AMP (Allocated Arena, Memory Mapped, Previous is Use)
* Payload

When `malloc` is called, the address of the payload is returned

## Free Chunk

* Previous Size
* Size
* AMP
* fwd
* back
* fd_nextsize
* fd_previoussize
* previous size

Metadata contains how big the chunk is (inclusive of the metadata overhead)

# Freeing

* Freeing chunks need to be fast!

## Fast Bins

* Small chunks are stored in size-specific bins.  
* There are 10 fast bins (sizes: 16, 24, 32, 40, 48, 56, 64, 72, 80 and 88)
* Chunks added to a fast bin are not combined with adjacent chunks
* Stored in a single linked lists

The next time a space of 16 bytes is requested, the first item in the 16-byte fast bin is allocated

## Unsorted Bins

* When free'd, chunks are initially stored in a single bin
* They are later sorted by malloc to be optimised

## Others

The normal bins are divided into 62 smaller bins (each bin has chunks of the same size), and two large bins (where each large bin has chunks of similar size)

## tcache (as of glibc 2017)

> "It's 2020. We've got coronavirus, bushfires, and now tcache exploit mitigations"

Thread-local cache (faster than a global cache!)

tcache has a limit of 7 chunks (by default).  
If 7 chunks have been free'd, tcache won't be used

## glibc (2019)

double free

# Security!

**Metadata and user data of chunks are often stored together...**  

Don't mix control and data!!!!!!

## gdb / pwndbg

* `heap` - overview of chunks
* `vis_heaps_chunks` - prints out all of the chunks
* `context` - overview of current gdb state
* `bins` - Shows the state of memory bins
* `arena` - Contains a structure of the arena state

# Exploitation

There are many heap exploitation techniques!  
Generally the goal is to make a malloc return an arbitrary pointer

* Double free
* Forging chunks
* Unlink
* Shrinking free chunks
* House of Spirit
* House of Love
* House of Force
* ...

## Use After Free

When a chunk is freed, its content is reused as part of a node in a linked list.  
If we tamper with the contents in this memory region, we can corrupt the linked list.  
This allows us to control the addresses of the chunks that will be freed in the future.

* i.e Modify the forward pointer, so that the next `malloc` returns our own address. If there is a function that reads into that (supposed new) address, we can perform an arbitrary memory write.
  * Write to GOT
  * `malloc_hook`, `free_hook`
  * vtable

## Double Free

Systems check that you haven't `free`'d a memory address twice **in a row**.  
However, we can bypass that by freeing some dummy address between the two `free(x)` calls.

Creates a infinite circular free chunk list -> causing future `malloc`'ss to return a previous address

## Leaking

The first element in a chunk list points back to libc.  
If we can leak the first 4 bytes of a free small chunk, we have libc address leak!  

## Forging Chunks

When there are two chunks next to each other, we could perform a buffer overflow on the first!  

If the second chunk is free: Can overflow into the freelist metadata  

If the second chunk is used: Can overflow into the chunk metadata - modify size and change its bin; e.g. convert fastbin into small bin and leak an address with it

## One Gadgets

A ROP gadget that instantly launches a shell!  
Requires certain critera to be met.

## Malloc Hook functions

When malloc is called, it checks if there are any malloc hooks - which allow custom functionality.

Ideally, we'd want to set the malloc hook to a one-gadget / stack-pivot to our buffer!

## Heap Spraying

Heap spraying is a technique in which we fill all the free space in the heap, such that all the free chunks are at the top of the heap (and next to each other!)

# House of Einherjar

* Requires a single byte overflow

---

https://heap-exploitation.dhavalkapil.com/