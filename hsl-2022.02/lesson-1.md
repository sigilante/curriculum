---
title: "Introduction to Computing"
teaching: 60
exercises: 0
nodes: []
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

---
_Instructor notes:_
- This lesson intends to get students excited about the arc and foundations of Urbit-style computing.  Tell the historical parts with anecdotes.
- There are many other examples of representation that can be brought forward, and you can engage the students in this.
- Emphasize that they don't need to deeply understand the _mechanics_ of binary mathematics, Gödel numbering, assembler language, lambda calculus, etc., just how these concepts matter to the overall picture.

---

How does a machine “reason”?  “Thou shalt not make a machine in the likeness of a human mind,” as _Dune_ has it.  But the act of calculation, of computation, is universal to human experience, and it is only at strange extrema such as machine learning that we find representations beyond our grasp.

Our objective in this lesson is to motivate why computers generally (and Urbit specifically) have the structure they do, and how to think about computation as an activity.

1. Representations are interchangeable.
2. Any computation requires a representation.
3. Computation requires values, operations, and state.
4. All of these can be represented unambiguously on the machine.
5. Higher-level languages map to lower-level representations for the machine.

Let's discuss what each of these principles means in practical terms.

Computation = calculation

##  Numeric Representation

From early in history, humans found the need to represent events and observations with number.  One imagines our deep ancestors counting antelope, or days, or moons.  The earliest physical structures remaining today are temples with alignment to solstices, physically embodying a computation.  Later, they found themselves enumerating things that weren't stacks of discrete single units (like area, or fractions, or volume).

1. Base-1:  tally marks as most primitive number
2. Base-60:  highly divisible
3. Base-10
4. Base-20
5. Base-2
6. Base-16

A counting base is the “tens” place, the unit you use to mark the “rollover”.

You are in fact comfortable with switching between bases of representation in your regular life, as when you count with your fingers to track something.  Other examples include:
- money/change (quarters)
- time
- 1-2-3-4, 2-2-3-4, 3-2-3-4, 4-2-3-4

The magician Pythagoras saw through number as a convention to a deeper reality, relating string vibrations, the chords of a circle, and counting numbers to each other.  Written numbers are merely a signpost to the underlying idea of number.

1. Representations are interchangeable.


##  Computation via Representation

Ancient mathematicians calculated necessary quantities to predict astronomical phenomena and record land mensuration for taxation.

Babylonian mathematics, base-60, was considered very sophisticated and presaged many of the later Greek developments.

Greek mathematics were based on geometry, and in large part on calculations using the chord of a circle rather than the sine.  This is an equivalent formulation, and makes some calculations easier and others harder.

Greeks were also very concerned with the notion of proof, as Euclid's _Elements_ demonstrated and left a legacy for all subsequent mathematicians to follow.

Pythagoras' insight was that number was magical
(ratios, musical notes, etc.)

So other computing media can work:
- Soviet water computer
- John Conway's WINNIE:  https://twitter.com/fermatslibrary/status/1495391552394383362
- Pneumatic machines
- Analog computers
- Decimal computers (like Babbage's engines)

These are a particular representation, or instantiation, or embodiment:  realizing the universal abstraction in a concrete form.

2. Any computation requires a representation.


##  Algorithms

This multiplication procedure, described in an early Egyptian papyrus, is one of the first general-purpose tools.  Most early mathematical handbooks demonstrate how to solve specific concrete problems and leave it to the reader to decide how to extend or adapt the method.  This procedure, however, is phrased completely generally and works for any two numbers.  We call such a general statement of a problem-solving approach an _algorithm_.

What are the kinds of things in this algorithm?
- values
- operations
- state or steps

Charles Babbage drew on the idea of Jacquard looms using physical cards with holes to store the thread patterns in a physical embodiment.

3. Computation requires values, operations, and state.


##  Gödel Numbers

Early modern philosophers became fascinated by the idea of writing down and proving propositions:  Llull, Wilkins, Leibniz.  Ultimately the mathematicians figured out how to nail down the kinds of statements for which this reasoning is effective.  En route to proving his famous incompleteness theorems, Kurt Gödel developed a way of writing propositions as numbers (and thus rendering them susceptible of certain kinds of numerical reasoning).

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
