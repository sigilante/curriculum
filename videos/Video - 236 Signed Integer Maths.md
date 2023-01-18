---
uuid: 236
layout: node
title: "Signed integer mathematics"
tags:
 - "%stdlib"
prerequisites:
  - "163"
postrequisites: []
objectives:
  - "Examine `@s` atomic representation of signed integer values."
  - "Use `+si` to manipulate `@s` signed integer values."
  - "Examine the rest of the modular arithmetic library, `+fo` and `++egcd`."
runes: []
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

##  Representing Signed Integers

In Hoon, all atoms are unsigned integers.  This poses a challenge for the representation of negative integers, which of course arise in the course of many operations.  As with floating-point values, the actual bit structure of a value can be interpreted in such a way as to permit us to think of and use a number as if it were a negative value.

There are several conventions that can be used to represent signed integers.  For instance, one could simply designate the leading bit in a fixed-width representation to indicate whether the whole should be mutipled by -1.

$$
\texttt{0010.1011}_{2}\;\text{for}\;\texttt{43}_{10}
$$

$$
\texttt{1010.1011}_{2}\;\text{for}\;\texttt{-43}_{10}
$$

This is similar to the solution employed by IEEE 754 floating point.

One could instead use a bitwise `NOT` operation for negative values, which has the advantage of making arithmetic operations trivial to calculate for the CPU.

$$
\texttt{0010.0000}_{2}\;\text{for}\;\texttt{43}_{10}
$$

$$
\texttt{1101.0100}_{2}\;\text{for}\;\texttt{-43}_{10}
$$

Hoon employs the ZigZag scheme in its `@s`-aura atoms.  ZigZag maps even unsigned integers to twice their value as a positive signed integer, and odd unsigned integers to twice their value minus one as a negative signed integer.  This economical pattern fits well with Hoon's convention of stripping leading zeroes.

$$
\texttt{0b101.0110}_{2}\;\text{for}\;\texttt{43}_{10}
$$

$$
\texttt{0101.0101}_{2}\;\text{for}\;\texttt{-43}_{10}
$$

Signed atoms are written similar to unsigned atoms of the same class, but with a single `-` in front for negative values and two `--` in front for positive values.  Two negations make an unambiguous signed positive value.  We can use the type spear to verify this type behavior.

```hoon
> -1
-1

> --1
--1

> -:!>(-1)
#t/@sd

> -:!>(--1)
#t/@sd
```

The `++si` core provides operators for `@s` atoms.  To avoid potential confusion with `@u` unsigned atom mathematics, slightly different names are used for operations.

-   [`++sum:si`](https://developers.urbit.org/reference/hoon/stdlib/3a#sumsi) provides addition,
-   [`++dif:si`](https://developers.urbit.org/reference/hoon/stdlib/3a#difsi) provides subtraction,
-   [`++pro:si`](https://developers.urbit.org/reference/hoon/stdlib/3a#prosi) provides multiplication, and
-   [`++fra:si`](https://developers.urbit.org/reference/hoon/stdlib/3a#frasi) provides division.

```hoon
> (sum:si --1 -2)
-1

> (dif:si --100 --10)
--90

> (pro:si --10 -20)
-200

> (fra:si --60 -5)
-12
```

To produce a signed integer from an unsigned atom, use `++new:si` with a sign flag:

```hoon
> (new:si & 2)
--2
```

To recover an unsigned integer from a signed atom, use `++old:si`, which returns the magnitude and the sign.

```hoon
> (old:si --5)
[%.y 5]

> (old:si -5)
[%.n 5]
```
