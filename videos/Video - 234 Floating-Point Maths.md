---
uuid: 234
layout: node
title: "Floating-point mathematics"
tags:
 - "%stdlib"
prerequisites:
  - "163"
postrequisites: []
objectives:
  - "Review floating-point mathematics including IEEE-754."
  - "Examine `fn` representation of floating-point values."
  - "Examine `@r` atomic representation of floating-point values."
  - "Manipulate and convert floating-point values using the `@r` operations."
runes: []
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

##  IEEE-754 Floating-Point Bit Structure

A number with a fractional part is called a “floating-point number” in computer science. This derives from its solution to the problem of representing the part less than one.

When you think about writing down a number other than an integer, you have to decide how the fractional part of the number will be represented.  As a child, you learn to write fractions as whole-number ratios; later, you learn decimals and finally a scientific or engineering notation.

$$
\frac{1}{4} = \frac{25}{100}
$$
$$
0.25
$$
$$
25 \times 10^{-2}
\;\textrm{or}\;
25\textrm{e}\textrm{-2}
$$

Whenever you write a value in a scientific notation, it really requires that you specify three numbers:

1. the _sign_, positive or negative
2. the _significand_, or value expressed in whole numbers
3. the _exponent_, or power of ten by which the number will be multiplied.

$$
(-1)^{0} \times 25 \times 10 ^ {-2}
$$

One could imagine a shorthand in which such a value is written as

```
0.-2.25
```

or the like, just storing the relevant values by position and allowing the full value to be retrieved on demand.

Modern systems write numbers with a fractional part in a binary analogue of what we have just described.  The name “floating point value” refers to how the decimal point can apparently be made to “float” from one position to another by this technique.

```
0011.1110.1000.0000.0000.0000.0000.0000
```
(diagram here)

Certain bit patterns allow the machine to represent invalid values (called NaNs) and infinity $\infty$ as well as numbers with a fractional part in a broad range of values.

Different bit widths, such as 32-bits or 64-bits, allow for different specificity in expressing numbers.  We don't need to worry about the specifics of these implementations here, but be aware that the choice of 32-bit single-precision values as opposed to 64-bit double-precision values will have consequences on the speed of calculation as well as its ability to adequately represent values in your calculation system.

Floating-point representations work reasonably well, but just as how attempting to write $\frac{1}{3}$ as a decimal results in an infinitely-repeating sequence, $0.33\bar{3}...$, so base-2 representations can have shortcomings in representing or carrying out math with certain values.

##  `+$fn` Representation

Hoon has two native representation styles for floating-point values.  The first is `+$fn`, a mold which holds the sign, exponent, and significand as separate atoms.

- `s=?` is the sign.
- `e=@s` is a signed representation of the exponent.
- `a=@u` is the unsigned representation of the significand.

Since atoms can be any size, we call `+$fn` an arbitrary-precision floating-point system.

The `++fl` core operates on `+$fn` values.


##  `@r` Representation

The other Hoon-native representation of floating-point values is the `@r` atom series.

1. `@rh` 16-bit half-precision.
2. `@rs` 32-bit single-precision.
3. `@rd` 64-bit double-precision.
4. `@rq` 128-bit quadruple-precision.

For simplicity, we will focus our discussion in this video on `@rs` 32-bit single-precision floating-point values, or C `float`s.

The atom is 32 bits wide and hews to the IEEE-754 specification we saw earlier.

```
0011.1110.1000.0000.0000.0000.0000.0000
```

Since Hoon strips off leading zeroes, we arrive at the representation in `@ub` format:

```
> `@rs`0b11.1110.1000.0000.0000.0000.0000.0000
.0.25
```

The leading `.` (or `.~` for other `@r` atoms) is not a decimal point, but is used to uniquely identify this atom as written for the parser.

```
> .0.1
.0.1

> .1000000
.1e6
```

As you can see here, a power of ten can be indicated by a trailing `e` much as on old-school calculators:

```
> .0.1e2
.10
```

##  Operators

When we work with `@r` values, we cannot use regular `@ud`-compatible operations.

```
> (add .1 .2)
2.139.095.040
```

This happens because the binary representation of the two numbers is simply added together without regard for the structure of the scientific notation.  Instead, we have to use `++rs` and similar cores to supply the appropriate operations:

```
> (add:rs .1 .2)  
.3

> (mul:rs .2 .3)
.6

> (sqt:rs .2)
.1.4142135

> (lth:rs .9.9e1 .1.1e2)
%.y

> (equ:rs .2 .3)
%.n

> (sig:rs .-1)
%.n
```

Don't be deceived by the similarity of some operators to mathematical notation:  `++exp:rs` returns the floating-point exponent, not the exponential function:

```
> (exp:rs .1)
--0

> (exp:rs .2)
--1

> (exp:rs .3)
--1
```

##  Conversions

Since `@r` values are not regular integers, we require functions to convert between `@ud` representations and floating-point equivalents.  This process may lose information, such as dropping a decimal component.

To convert a `@ud` atom to `@rs` atom, use `++sun:rs`:

```
> (sun:rs 4.000)
.4e3
```

To convert from a `@rs` atom back to an integer atom may require rounding, such as with `++toi:rs`.  Note that this converts to `@sd`, the signed decimal aura:

```
> (toi:rs .3.1415927)
[~ --3]
```

To convert between `@r` types generally requires using `+$fn` as intermediary and may be lossy:

```
> =/  val   .3.1415927
  =/  fnrs  (sea:rs val)
  (bit:rd fnrs)
.~3.1415927410125732
```

A fairly common use case for parsing decimals arises when working with JSON-derived data.  A special arm `++ne` exists in `++dejs:format` to convert `json` values to `@rd` atoms.

```
> (ne:dejs:format `json`[%n '3.1415927'])  
.~3.1415927
```

There are other conversion arms as well for specialized cases.
