---
uuid: 133
layout: node
title: "Basic cores, arms"
tags:
 - "%hoon"
prerequisites:
  - "130"
postrequisites:
  - "135"
  - "156"
objectives:
  - "Consider Hoon structures as cores."
  - "Identify the special role of the `$` buc arm in many cores."
  - "Order neighboring cores within the subject for addressibility."
runes:
  - "|%"
  - "++"
  - "+$"
  - "=<"
  - "=>"
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

#   Cores

Cores are the most important data structure in Hoon. They allow you to solve many coding problems by identifying a pattern and supplying a proper data structure apt to the challenge. You have already started using cores with `|=` bartis gate construction and use, because a gate is a cell of code—the operation—and data—the value passed in to the gate.

Formally, we'll say a core is a cell `[battery payload]`, where `battery` describes the things that can be done (the operations) and `payload` describes the data on which those operations rely.  We further divide the `payload` in a cell `[sample context]`.

Urbit adopts an innovative programming paradigm called _subject-oriented programming_.  Hoon and Nock very carefully bound the known context of any part of the program as the _subject_. Basically, the subject or `context` is the noun against which any arbitrary Hoon code is evaluated.  The regular `context` includes the Hoon standard library.

A core's `battery` consists of a number of _arms_ of expressions which can be evaluated when invoked.  A core's `payload` is then provided to the `battery` expressions, including any arguments in the `sample`.

In essence, a core organizes operations and the data to which those operations apply together within a shared scope.  They act similar to objects in other programming languages.

---

##  Kinds of Cores

A core is a cell `[battery payload]`, essentially code and data.

Cores can be organized based on how their `battery` is organized and on how their `payload` is organized.  This structure determines the practical utility of a core.

Perhaps the best place to begin is by taking a look at the structure of a gate.  A gate consists of a _body_ of code, which corresponds to the `battery`, and an input argument of some kind, which is the `sample`.  It also receives information about its operating environment, or `context`; together the `sample` and `context` define the `payload`, or data which the battery has available to operate.

```hoon
::  (a*b)+c
|=  [a=@ b=@ c=@]
(add (mul a b) c)
```

Let's consider a number of core structures and how they reduce to the most fundamental core representation, `|%` barcen.

The simplest core, the `trap`, has no `sample` but only a `context`.  We create traps with `|-` barhep or `|.` bardot and use them as recursion points.  A trap has only one arm or block of code, named `$` buc.

A `|.` bardot trap is created like a function which can be used at any time.

```hoon
|%  ++  $  a=hoon
--
```

A `|-` barhep trap is created and then used immediately.

```hoon
=<  $
|%  ++  $  a=hoon
--
```

By adding a `sample` to this simplest core, we arrive at the `|=` bartis gate.  A gate is a one-armed core with a sample.  Since the sample must be provided to evaluate the `battery` of the core, there is no “active” analogue that immediately evaluates, as with the trap.

```hoon
=+  ^~(*a=spec)
|%  ++  $  b=hoon
--
```

However, instead of adding a sample to a trap we could instead add multiple helper arms to the `battery` and still evaluate the `$` buc arm immediately.  This is the `|^` barket core, which can be useful for expression clarity.

```hoon
=>  |%
    ++  $  a=hoon
    ++  b=term  c=hoon
    ++  d=term  e=hoon
           ...
    ++  f=term  g=hoon
    --
$
```

The most general form of a core is the `|%` barcen core, which produces a core with any number of arms in the `battery` and a full `payload` including `sample` and `context`.  
Libraries and structure files are `|%` barcen cores which organize access to particular expressions in each arm.  Arms may be `++` luslus arm definitions or `+$` lusbuc type definitions.

```hoon
::  show /lib/number-to-words.hoon
```

The most general form of a gate is the _door_, produced with `|_` barcab.  A door has an additional sample for the entire core, as well as a particular sample in arms where appropriate.  Doors are useful when shared information needs to be available at a level above a gate's `sample`.  For instance, a Gall agent is a door so that system information like the ship name and entropy can be provided to the entire agent.

```hoon
=|  a=spec
|%
++  b=term  c=hoon
++  d=term  e=hoon
       ...
++  f=term  g=hoon
--
::  show /app/time.hoon
```

There are a few other kinds of cores as well, which alter how different components like the `sample` are handled.

##  `battery`

Cores provide a standard interface for Hoon to construct expressions and evaluate them against data.  This is important because Hoon and Nock are _homoiconic_:  that is, there is no difference in representation between code and data.

A `battery` consists of arms which evaluate to particular Hoon expressions.  Arm definitions have a name associated with them so that they can be retrieved directly rather than by numeric address.  The `battery` is located at address `+2` in the core, but only the already-compiled Nock code is visible.

```hoon
> +2:add
[6 [5 [1 0] 0 12] [0 13] 9 2 10 [6 [8 [9 2.398 0 7] 9 2 10 [6 0 28] 0 2] 4 0 13] 0 1]
```

Type definitions made with `+$` lusbuc use structure mode to describe what a value should look like.  Structure mode is the kind of Hoon spoken by `$` buc runes when producing molds:  for instance, the idea of a type of a cell is distinct from any particular instance of a cell.  `+$` lusbuc arms frequently alias existing type values for clarity within the core.

Normal arms made with `++` luslus use Hoon in value mode (the regular way you interpret values).  Any Hoon expression can be included as a valid arm, from simple atoms to compile-time calculations to entire nested cores.

##  `sample`

The `sample` describes the data provided to the core for the expressions to be completed.  When a cell with a `sample` is invoked, the actual values are slotted in for their definition and then the code is evaluated.

```hoon
  ++  add
    |=  [a=@ b=@]
    ^-  @
    ?:  =(0 a)  b
    $(a (dec a), b +(b))

  ++  add
    =+  ^-(*a=)

=+  ^~(*a=spec)
|%  ++  $  b=hoon
--
```

The `sample` sits at address `+6` in a given core.

```hoon
> +6:add
[a=0 b=0]
```

A typical `sample` defaults to the bunt of its values.  Normally this is zero, but the default values can be overridden with either a `|:` buccol gate specification or a `$~` bucsig `sample` definition.  `sample`s are of course defined in structure mode, as with all mold expressions.

```hoon
> (add)
0

> (mul)
1

> +6:mul
[a=1 b=1]
```

##  `context`

The `context` describes the scope of visible code for any particular core.  This typically consists of Hoon, the standard library, and any loaded libraries.  By convention, the pretty-printer shows the number of arms in each nested core along with an identifying hash.

```hoon
> +7:mul
<46.hgz 1.pnw %140>

> +7:pi-tell
<77.kga 232.mmf 51.qbt 123.ppa 46.hgz 1.pnw %140>
```
