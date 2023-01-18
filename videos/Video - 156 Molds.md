---
uuid: 156
layout: node
title: "Typechecking"
tags:
 - "%hoon"
prerequisites:
  - "133"
postrequisites:
  - "184"
objectives:
  - "Use assertions to enforce type constraints."
  - "Identify a `lest` (as opposed to a list)."
  - "Produce a type arm."
runes:
  - "?>"
  - "?<"
  - "?~"
  - "+$"
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

#   Molds

Hoon uses type to determine the rules which apply when interpreting and using a value.  Although everything in Nock is ultimately a noun, so either a cell or an unsigned decimal, Hoon provides a type system including many common kinds of values:  numbers, text, dates, and so forth.  You can also define your own types to validate input and processing.

A type is a rule of interpretation.  The first role a mold fills in the Hoon world is to validate that a value fits the structure.  Here we check whether a value is an atom `@` pat, and the statement crashes if not.

```hoon
> (@ 5)
5

> (@ [1 2])
dojo: hoon expression failed
```

Notice that we are using the irregular parenthetical syntax for `%:` cencol and `%-` cenhep:  it turns out that molds are a kind of gate, functions which convert the structure successfully or crash.

The simplest molds are atoms, which are unsigned integers that have some type attached.  The type allows the value to be interpreted as a hexadecimal value, as ASCII text, as a date, as a floating-point value, as an Azimuth point, and so forth.

```hoon
> `@ux`64
0x40

> `@t`64
'@'

> `@da`64
~292277024401-.1.1..00.00.00..0000.0000.0000.0040

> `@rs`64
.9e-44

> `@p`64
~rys
```

The special `` ` `` tic notation we are using here is the irregular form of the `^-` kethep rune.  `^-` kethep compares the inferred type of an expression with a desired known type.  If the expression's inferred type nests under the desired type, then the product of the expression is returned with that type.

```hoon
> ^-(@da ~2023.1.9)
~2023.1.9

> ^-(@da ~zod)
mint-nice
-need.@da
-have.@p
nest-fail
dojo: hoon expression failed
```

Molds use a special kind of Hoon syntax called _structure mode_.  Structure mode describes using `$` buc runes to build molds, or descriptions of structure.  Some special identifiers like `@` and `^` exist, but for anything more complicated you will need to use runes like `$:` buccol instead.

```
> (^ [1 2])
[1 2]

> ([@ @] [1 2])
dojo: hoon expression failed

> ($:(@ @) [1 2])
[1 2]
```

The `$` buc rune family encompasses a variety of ways to build type unions, tuples, trees, and any other kinds of structures.
