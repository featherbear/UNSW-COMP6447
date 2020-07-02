---
title: "Fuzzing"
date: 2020-06-30T20:01:08+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Fuzz Testing

Fuzzing is an automated software testing technique that involves providing invalid or unexpected or random data as inputs to a program. They automatically generate and send payloads to programs, and monitor changes in the program's behaviour.  

Fuzzers take in sets of inputs, and attempts to mutate them. Some can take in the source code of a program to intelligently analyse the required inputs to a program.

Fuzzers are useful to provide code coverage tests (How well does the code work against all possible situations)

## Limitations

* Hard to know about custom protocols / file formats without prior reversing / knowledge
* Non-crashing bugs are hard to detect
  * Arbitrary read/write access
  * SQLi
  * Privilege Escalation
* Hard to know about fuzzing progress
  * If you don't get a crash for a long time... maybe your fuzzer is broken
  * If you get too many crashes ... maybe your fuzzer isn't discovering any new bugs
* Hard/Impossible to generate all possible inputs

As not every bug will cause a crash, a fuzzer can add hooks into a program which crashes the program if a certain particular condition is met - allowing us to find when these happen.  
An address sanitiser is an example of this - where it crashes the program on an invalid memory read/write.

## Components

### Fuzzer

Generates the input, and attaches the harness to a program

### Harness

The tool that watches how the program behaves.  

e.g. debugger, code coverage result, hypervisor, return code

Looks for crashes, weird states, code coverage, error messages, information leaks

---

# Open Source Fuzzers

## American Fuzzy Lop (AFL)

AFL is a copus-based (mutates sample data), coverage guided fuzzing tool.  
It requires the source code of a program.

## Libfuzzer

.

# A Good Fuzzer

* Fast
* Use multiple threads
* Pass files/data through memory

# Fuzzing Strategies

## Mutation Based

No understanding of the instruction of inputs.  
Randomised inputs - i.e. bit flips

## Generation Based

Generate input based on some format or test case
