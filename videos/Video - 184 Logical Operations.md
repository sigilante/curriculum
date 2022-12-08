---
uuid: 184
layout: node
title: "Logical Operations"
tags:
 - "%hoon"
prerequisites:
  - "156"
postrequisites:
  - "233"
objectives:
  - "Produce loobean expressions."
  - "Reorder conditional arms."
  - "Switch against a union with or without default."
runes:
  - "?|"
  - "?&"
  - "?!"
  - "?."
  - "?-"
  - "?+"
irregular:
  - "&"
  - "|"
  - "!"
key_points: []
assessments: []
comments: ""
content: ""
---

#   Logical Operations

The `?` wut runes and `.=` dottis together define the scope of comparison supported by Hoon.  A variety of auxiliary functions like greater-than and member-of support various common data structures and design patterns.

As with all other systems, the logical basis of Hoon is `&` `TRUE` and `|` `FALSE`.  Sometimes "boolean" logic is called "loobean" logic since the root value of `TRUE` is actually zero, but for all practical purposes this doesn't matter.

```hoon
> &
%.y

> |
%.n
```

Essentially, a program uses logical statements to decide whether or not some expression evaluates as `%.y` `TRUE` (in which case it will do one thing) or `%.n` `FALSE` (in which case it will do another). Some basic expressions are mathematical, but one can also check for existence, for equality of two values, and so forth.

```hoon
> ?:((gth 5 4) 'bigger' 'smaller')
'bigger'
```

##  Noun Equality

The most fundamental comparison in Hoon is provided by `.=` dottis, a test for equality of two nouns using Nock 5.  This is almost always used in its irregular form of `=` tis.

```hoon
> =(0 0)
%.y

> =('a' 'b')
%.n
```

Since Nock is unaware of the Hoon metadata type system, only bare atoms in the nouns are compared.  If you need to compare include type information, create vases with `!>` zapgar.

```hoon
> =('a' 97)
%.y

> =(!>('a') !>(97))
%.n
```

##  Comparisons

Many logical expressions are predicated on simple mathematical comparisons:  greater than, less than or equal to, etc.

```hoon
> (gth 10 12)
%.n

> (lte 5 5)
%.y
```

##  Logical Operators

Mathematical logic allows the collocation of propositions to determine other propositions. In computer science, we use this functionality to determine which part of an expression is evaluated.  An `AND` statement requires both sides to be `TRUE` to result in `TRUE`.  Hoon provides `AND` as `?&` wutpam, commonly used as `&` pam:

```hoon
> &(%.y %.y)
%.y

> &(%.n %.y)
%.n
```

An `OR` statement only requires at least one side to be `TRUE` to result in `TRUE`.  Hoon has the `?|` wutbar rune with irregular form `|` bar:

```hoon
> |(%.y %.n)
%.y

> |(%.n %.n)
%.n
```

##  Conditional Branching

One of the most common uses of logic is to branch on a condition.  The `?:` wutcol rune takes one of two daughter expressions on the basis of its conditional value.

```
> =/  my-list  ~[1 2 3 4 5]
  =/  index  0
  |-
  ?:  =(index (lent my-list))
    'done'
  $(index +(index))
'done'
```

`?.` wutdot reverses the cases, and is preferred when the case-when-true is much longer than the case-when-false.  (Heavier Hoon expressions should be lower in the program.)

```hoon
> =/  my-list  ~[1 2 3 4 5]
  =/  index  0
  |-
  ?.  =(index (lent my-list))
    $(index +(index))
  'done'
'done'
```

##  Type Comparisons

The remaining `?` wut runes make decisions based on type.  There are limitations on most of these, such as type needing to be unknown at compile time.

`?+` wutlus and `?-` wuthep are similar to `?:` in that they allow branching on the basis of a value, but unlike `?:` they do not branch on a logical statement, but on type matching.  These are used extensively with type unions over `@tas` terms.  They also tend to be structured using the otherwise uncommon queenside indentation.  `?+` wutlus permits a default fallback condition, while `?-` wuthep requires all cases to be considered explicitly.

```
> =/  a  %2
  ?+    a  'default'
      %1
    'one'
    ::
      %2
    'two'
    ::
      %3
    'three'
  ==
```

`?@` wutpat and `?^` wutket check whether a value is an atom or a cell, respectively.  Somewhat frustratingly, the type must not be known at compile time or a `mint-vain` error occurs.  Here I'll cast the checked value as a `*` noun so that all type information is lost before the check occurs.

```
> ?@(1 %a %b)
mint-vain
dojo: hoon expression failed

> ?@(`*`1 %a %b)
%a

> ?@(`*`[5 5] %a %b)
%b

> ?^(`*`[5 5] %a %b)
%a
```

`?=` wuttis tests for a pattern match in type, or rather whether the type of the value structurally nests inside the check type.

```hoon
> ?=(?(%a %b %c) %a)
%.y

> ?=(?(%a %b %c) %d)
%.n
```

##  Assertions

Some `?` wut runes require a particular value from their conditional expression.  We call these _assertions_.

For instance, `?~` wutsig branches on whether a value is null.  Similar to `?@` wutpat, the type information must not be known at compile time.

```
> ?~(`*`~ %a %b)
%a
```

`?>` wutgar is a positive assertion, or a requirement that its condition be true.  Otherwise it crashes.

```
> ?>(%.y %a)
%a

> ?>(%.n %a)
dojo: hoon expression failed
```

`?<` wutgal is a negative assertion, or a requirement that its condition be false.  Otherwise it crashes.

```
> ?<(%.n %a)
%a

> ?<(%.y %a)
dojo: hoon expression failed
```