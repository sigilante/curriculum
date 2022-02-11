---
title: "Introduction to Computing"
teaching: 60
exercises: 0
objectives:
- "Identify fundamental principles common to all computing (manual, analog, and digital)."
- "Explain how representations of value are interchangeable."
- "Demonstrate how any computation requires a representation."
- "Name the components any computation requires:  values, operations, and state."
- "Explain how higher-level languages map to lower-level representations."
- "Enumerate the components of the Urbit platform and how they relate to the components of computation."
runes: []
keypoints:
- "Representations are interchangeable."
- "Any computation requires a representation."
- "Computation requires values, operations, and state."
- "All of these can be represented unambiguously on the machine."
- "Higher-level languages map to lower-level representations for the machine."
- "Urbit consists of Nock (a computation specification), Hoon (a high-level language), Arvo (the system event handler and state), and Azimuth (the identity system)."
---

#   Introduction to Computing
##  Hoon School Lesson –1

##  Numeric Representation

1. Base-1:  tally marks as most primitive number
2. Base-60:  highly divisible
3. Base-10
4. Base-20
5. Base-2
6. Base-16

You are in fact comfortable with switching between bases of representation in your regular life, as when you count with your fingers to track something.  Other examples include:
- money/change
- time
- 1-2-3-4, 2-2-3-4, 3-2-3-4, 4-2-3-4

1. Representations are interchangeable.


##  Computation via Representation

Ancient mathematicians calculated necessary quantities to predict astronomical phenomena and record land mensuration for taxation.

Babylonian mathematics, base-60, was considered very sophisticated and presaged many of the later Greek developments.

Greek mathematics were based on geometry, and in large part on calculations using the chord of a circle rather than the sine.  This is an equivalent formulation, and makes some calculations easier and others harder.

Greeks were also very concerned with the notion of proof, as Euclid's _Elements_ demonstrated and left a legacy for all subsequent mathematicians to follow.

Pythagoras' insight was that number was magical
(ratios, musical notes, etc.)

2. Any computation requires a representation.


##  Algorithms

This multiplication procedure, described in an early Egyptian papyrus, is one of the first general-purpose tools.  Most early mathematical handbooks demonstrate how to solve specific concrete problems and leave it to the reader to decide how to extend or adapt the method.  This procedure, however, is phrased completely generally and works for any two numbers.  We call such a general statement of a problem-solving approach an _algorithm_.

What are the kinds of things in this algorithm?
- values
- operations
- state or steps

3. Computation requires values, operations, and state.


##  Gödel Numbers

Given a formal language for writing down propositions, we can convert the terms of the proposition to a numeric representation.  Each part still corresponds to a value, an operation, or a part of the state, but now the entire expression or proposition is written down as an number.  As a result, we can apply algorithmic reasoning to carefully treat the proposition mathematically and arrive at a judgment about its truth or falsity.

Given a rule for conversion, we can write down any proposal from the formal language as a number and subject it to mathematical proofs and reasoning.

4. All of these can be represented unambiguously on the machine.


##  Programming Languages

Computers use assembler (or assembly) language as their fundamental binary language.

Each instruction has a determinate length.  The bitness of the machine determines the number and to some extent the range of values:

- 8-bit machines (like the original NES or the IBM System/360) can only have 256 (2⁸) possible commands, values up to 256, and memory addresses to 256.  (There were ways around this, like reading subsequent bytes.)
- 16-bit machines (like the DEC PDP-11, the Intel 8088, and the Super Nintendo) can have the equivalent values to 65,536 (2¹⁶).
- 32-bit machines (like the Pentium Pro or the original PlayStation) became popular starting in the 1990s.  They can represent up to 4,294,967,296 (2³²) in value.
- 64-bit machines are ubiquitous today and adequate for all contemporary and near-term future applications.

The first number in a command represents the operation (_opcode_), which then determines the interpretation of the other numbers (values or addresses, which access stored state).

- [x86 Instruction Listings](https://en.wikipedia.org/wiki/X86_instruction_listings)

5. Higher-level languages map to lower-level representations for the machine.


##  Mathematical Formulations

The lambda calculus is a formal mathematical specification for computation.

The lambda calculus consists of lambda terms and defines a set of formal operations for manipulating them.

Other (equivalent) logic systems exist; Urbit’s Nock language is most closely related to the SKI combinator calculus.


##  Summary of Principles

1. Representations are interchangeable.
2. Any computation requires a representation.
3. Computation requires values, operations, and state.
4. All of these can be represented unambiguously on the machine.
5. Higher-level languages map to lower-level representations for the machine.

