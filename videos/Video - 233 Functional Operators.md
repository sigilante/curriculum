---
uuid: 233
layout: node
title: "Functional Operators"
tags:
 - "%stdlib"
prerequisites:
  - "183"
  - "184"
postrequisites:
  - "288"
objectives:
  - "Reel, roll, turn a list."
  - "Curry, cork functions."
  - "Change arity of a gate."
runes:
  - ";:"
irregular: []
key_points: []
assessments: []
comments: |
    "<!-- 2b, 2n -->"
content: ""
---

##  Functional Operators

Functional programming languages such as Haskell, OCaml, Clojure, and APL organize programs around composing functions and applying them to build declarative expressions to operate on data.  A functional programming style tends to focus on building small functions which can be combined modularly to accomplish programmer intent.

Some aspects of functional programming focus on setting or modifying function behavior.  Others acts as higher-order operations to apply functions across members of data sets.  In this lesson, we'll examine both function-modifying operators and function application operators.

<!-- some graphic of things, maybe APL or a grid -->

##  Modifying a Gate

A gate serves as the archetypal function in Hoon:  it has a `sample` containing input values and a `$` buc arm which operates on those values to yield a result.  However, the sample is fixed by the original function definition, leaving it inflexible even where our intent may seem clear.

```hoon
> (add 3 4)
7

> (add 3 4 5)
-tack.,.+26
-find.,.+26
dojo: hoon expression failed
```

By modifying the nature of the sample, we can change a two-valued binary operator like `++add` such that it can serially apply across many values as an _n_-ary operator.  Alternatively, we can bind one of its sample arguments so that it is always known:  it can become a _unary_ operator.

### Increasing Arity

To increase the _arity_ of a binary gate, or the number of arguments it can be applied across, we use the `;:` miccol rune.  This allows us to specify a sequence of values to which the result of previous operations will be applied.  The sequence begins with the bunt of the sample.

```hoon
> (add 3 (add 4 5))
12

> :(add 3 4 5)
12

> (mul 3 (mul 4 5))
60

> :(mul 3 4 5)
60

> +6:mul
[a=1 b=1]
```

### Decreasing Arity

To decrease the arity of a gate, we can _bind_ arguments in the sample.  For instance, since `++add` takes two operators, we can bind one of them to produce an `++add-ten` unary gate.  This is another example of Hoon preferring to employ gate-building gates.

```hoon
> =add-ten (curr add 10)

> (add-ten 15)
25
```

It is also possible simply to define a new gate which represents the same net concept.

```hoon
> =add-ten |=(a=@ (add 10 a))

> (add-ten 15)
25
```

### Composing Functions

The `;:` miccol rune allowed us to increase the arity of a gate, but we can also glue gates together in a serial composition where one gate is applied to the result of another automatically.  This results in a new gate which can be applied normally.

```hoon
> ((cork dec add-ten) 20)
29
```

##  Applying a Gate

Higher-order functions accept and modify other functions.  `++curr` and `++cork` are examples of these, but there are of course many others.  In particular, we will use higher-order functions to implement some common design patterns preferred by functional programmers.  Hoon `list`s, `map`s, and `set`s all have their own operators for each category, and we will illustrate using `list`s.

### Map

The Map operation describes the situation in which, given a collection of data, a function is applied to each member of that collection.  (Note that this is not the same usage as Hoon's `+$map` data structure.)

`++turn` accepts a `list` and a gate, and returns a list of the products of applying the gate to each item of the input list.  The top-level organization of the data should reflect the gate's expected `sample`.

```hoon
> (gulf 65 76)
~[65 66 67 68 69 70 71 72 73 74 75 76]

> (turn (gulf 65 75) @t)
<|A B C D E F G H I J K|>

> (turn `(list (pair @ @))`~[[1 1] [2 2] [3 3] [4 4]] mul)
~[1 4 9 16]
```

### Reduce

The Reduce operation describes how, given a collection of data, a function applied as a pairwise operator to each item results in one summary value, or _reduction_.

`++roll` moves left-to-right across an ordered list to arrive at a final value.

```hoon
> (roll (gulf 1 5) mul)
120
```

### Filter

The Filter operation applies a logical test to each member of a collection of data.

`++skim` cycles through a list using a logical gate to produce a list of all members for which the gate evaluates to `TRUE`.

```hoon
> (skim (gulf 1 10) (curr gth 5))
[i=6 t=~[7 8 9 10]]

> `(list @)`(skim (gulf 1 10) (curr gth 5))
~[6 7 8 9 10]
```

To understand how higher-order functions are constructed in Hoon, investigate _wet gates_ and the `|*` bartar rune.
