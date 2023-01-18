---
uuid: 113
layout: node
title: "Naked generator design, syncing, etc., control structures"
tags:
 - "%hoon"
prerequisites:
  - "110"
  - "111"
postrequisites:
  - "115"
  - "195"
objectives:
  - "Pin a face to the subject."
  - "Make a decision at a branch point."
  - "Distinguish loobean from boolean operations."
  - "Slam a gate (call a function)."
  - "Produce a generator to convert a value between auras."
runes:
  - "%-"
  - "=/"
  - "?:"
  - "^-"
  - "~&"
irregular: []
key_points: []
assessments: []
comments: |
    ""
    "<!-- (implied `|=` for later discussion) -->"
content: ""
---

#   Basic Coding

At the simplest level, every Hoon program is a cascade of mother and daughter runes that result in some noun structure, made up of cells and atoms.

Consider a program that makes a decision.  The first thing we need to be able to do is produce a condition, some criterion for making a decision.  If we would like to know if one value is greater than another, for instance, we can use `%-`, `++gth`, and two values to produce a `TRUE` or `FALSE` value.

```hoon
> %-  gth  [5 6]
%.n

> %-  gth  [6 5]
%.y
```

```
          %-
        /    \
      gth   [5 6]
```

In this case, you can see that the first number is compared to the second and either `%.n` for `FALSE` or `%.y` for `TRUE` is produced.  Other mathematical comparisons exist, including checking for equality.

We are actually already using two nested expressions.  Hoon is possessed of an array of irregular syntax which can be daunting to the new learner.  Here, a cell is actually explicitly composed using the `:-` cencol rune, which itself takes two children.

```
          %-
        /    \
      gth    :-
           /    \
          5      6
```

We chain rune expressions together to produce more complex expressions.  For instance, if we want to make a decision between two outcomes, we can use the `?:` wutcol rune, which takes three children:  a condition, a value if true, and a value if false.

```
          ?:
        /  |  \
       /   |   \
?(%.n %.y) | (if false)
       (if true)
```

Combining these, let's say that the program should return the text `'true'` if the condition results in `TRUE`, and the text `'false'` if the condition results in `FALSE`.  Diagrammatically:

```
              ?:
            /  |  \
           /   |   \
          %-  'true'  'false'
        /  |
      gth  :-
          /  \
         5    6
```

This reads a bit like a flowchart, but gives you a sense of how expressions interrelate in Hoon.  We could write such a program with a variety of layouts, but the simplest way is simply to branch daughter expressions down a text file.  Thus, one way to write this program could look like:

```hoon
?:  %-  gth  :-  5  6
'true'
'false'
```

More commonly, we will use irregular syntax and judicious indentation to produce a legible source file.  This source file is more stylistically apt:

```hoon
?:  (gth 5 6)
  'true'
'false'
```

We can type or copy-and-paste this program into the Dojo, which will evaluate the entire statement and yield the resulting value.  Since the Dojo won't let you input invalid code, you should take pains to ensure that double-spaced gaps are treated correctly.

A source file typically exposes a _core_, or a Hoon construction that is slightly more complex.  We'll take a look at the first of those, the _gate_, in the next video.
