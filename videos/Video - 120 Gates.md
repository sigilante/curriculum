---
uuid: 120
layout: node
title: "Basic dry gates"
tags:
 - "%hoon"
prerequisites:
  - "115"
postrequisites:
  - "125"
objectives:
  - "Employ a gate to defer a computation."
  - "Produce a gate as a generator."
runes:
  - "|="
  - "!!"
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

# Gates

Any practical program sooner rather than later requires the ability to calculate an expression based on values not known at the time of composition.  Most programming languages think of such a deferred computation similar to a mathematical function, which accepts one or more _variables_ (here $x$) and returns a single-valued result.

$$
f(x) = x + 1
$$

Middle-school and high-school mathematics spent a lot of energy classifying and characterizing such functions, such as the above line.  You can talk about $f$ without as yet knowing anything about $x$, which is why I called it a _deferred computation_ or _deferred expression_.  Whenever you use $f$, you provide a particular value of $x$ for the calculation to proceed:

| $x$ | $f(x)$ |
| --- | --- |
| `0` | `0 + 1 = 1` |
| `1` | `1 + 1 = 2` |
| `2` | `2 + 1 = 3` |
| `3` | `3 + 1 = 4` |
| `4` | `4 + 1 = 5` |

What we are concerned with now is simply how to use or define such a deferred expression in Hoon.

Hoon calls such a function a _gate_.  A gate is defined using the `|=` bartis rune and invoked or used via the `%:` cencol rune and its `%` cen-family relatives.

Since at this point you have already invoked a gate with `%-` cenhep, let's look at what took place at a high level.

```
%-(add [1 2])
```

`%-` cenhep expects two daughters:  a gate and a `sample`.  Here `++add` refers to the gate and the cell `[1 2]` serves as `sample`.  The definition of `++add` is loaded by Urbit, the `sample` replaces the deferred variables, and the result is calculated much as we did by hand previously.

Let's use `|=` bartis to define a simple gate in the Dojo, then use it for particular values to see how the whole process works.  A `|=` bartis takes two daughters:  an expected `sample` and the associated expression.

```hoon
> =add-one |=  x=@ud
  (add x 1)
```

`++add-one` is now a name which Dojo knows about and can calculate.

```hoon
> add-one
< 1.mqv
  [ x=@ud
    [our=@p now=@da eny=@uvJ]
    <17.zfg 35.yza 14.oai 54.uao 77.ars 232.puz 51.qbt 123.ppa 46.hgz 1.pnw %140>
  ]
>
```

The pretty-printer shows us a lot of information that we'll learn how to interpret later, but for now notice that one of the lines does indeed say `x=@ud` and thus `++add-one` is confirmed to expect a single variable `x`.

Whenever we calculate the result of this gate, the `sample` value as structured in the first daughter of `|=` bartis is provided to the second daughter, the expression, with the associated faces (or variable names).  These are then used to calculate a result.

```hoon
> %-(add-one 5)
6
```

We can actually use a few different runes to invoke or _slam_ gates based on how many arguments they have, but most often we will simply use the irregular Lisp-like form with parentheses:

```hoon
> %-  add-one  5
6

> %:(add-one 5)
6

> (add-one 5)
6
```

Ultimately, gate usage is possible the single most common action taken in Hoon code.  Gates allow you to structure logic and expressions in one location separate from where they are used, which makes for cleaner code composition and testing.  Gates can produce other gates on demand, a powerful design pattern we'll explore more subsequently.  Gates even serve as the basis of Hoon's type system, which we'll explore next.
