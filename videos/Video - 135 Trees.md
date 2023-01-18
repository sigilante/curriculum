---
uuid: 135
layout: node
title: "Addressing, trees"
tags:
 - "%hoon"
prerequisites:
  - "133"
postrequisites:
  - "140"
  - "170"
objectives:
  - "Address nodes in a tree using numeric notation."
  - "Address nodes in a tree using lark notation."
  - "Address data in a tree using faces."
  - "Distinguish `.` and `:` notation."
  - "Diagram Hoon structures such as gates into the corresponding abstract syntax tree."
runes:
  - "=+"
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

#   Trees & Addressing

Every Hoon expression is composed of nouns:  atoms and cells.  Furthermore, Hoon data and Hoon code are _homoiconic_, sharing the same representation.

An interesting corollary of these facts is that every Hoon noun and every Hoon program is a binary tree.

(diagram of a large binary tree)

Each node in this binary tree may contain either an atom, in which case it has no children, or a cell, which has two children.  Many possible nodes may be empty.

If we wish to refer to information located somewhere in this tree, we can use one of three methods:

1. The first method is numeric addressing, in which each possible node is assigned a number.

    ```hoon
    > +5:[[1 2] [3 4]]
    2
    ```

2. The second method is positional addressing, in which the left or right daughter is indicated at each juncture.  Somewhat confusingly, the original designers of Hoon opted to alternate `+`/`-` lus/hep and `<`/`>` gal/gar at each level.  Positional addressing should be avoided except for simple choices of one or two levels deep.

    ```hoon
    > +<:[[1 2] [3 4]]
    3
    ```

3. The final, and most common, method is to use wings.  Wings are search paths—in other words, they are names that resolve to particular locations in the tree.

    ```hoon
    > p:[p=[1 2] q=[3 4]]
    [1 2]
    ```

    Faces label locations in the overall tree so that you don't have to track any positional knowledge of your program—which would be tedious and unforgiving in any case.  This is also one way in which Hoon-style faces are different from conventional variable names, since the underlying tree remains in principle transparent.

A running tuple occupies the rightwards-branching nodes in a tree until the final element closes the tuple.

```
[1 2 3 4 5 6 7 8 9 10]
```

It's easier to see this if you re-introduce the brackets which the pretty-printer leaves out for running cells:

```
[1 [2 [3 [4 [5 [6 [7 [8 [9 10]]]]]]]]]
```
