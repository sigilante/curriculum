---
uuid: 150
layout: node
title: "Doors"
tags:
 - "%hoon"
prerequisites:
  - "145"
postrequisites:
  - "155"
  - "183"
objectives:
  - "Identify the structure of a door and relate it to a core."
  - "Pull an arm in a door."
runes:
  - "|_"
  - "%~"
irregular:
  - "~()"
key_points: []
assessments: []
comments: ""
content: ""
---

#   Doors

A core is a cell `[battery payload]`, and a gate is a core which includes one arm `$` buc.  We often use gates similar to how functions are employed in many languages.

Mathematically, some functions distinguish between variables such as $x$ and parameters such as $a$, $b$, and $c$.  Most of the time we will evaluate this function $f$ only as a function of $x$, leaving $a$, $b$, and $c$ fixed.

$$
f(x) = a x^2 + b x + c
$$

There's a higher-level description of the function that recognizes that the parameters $a$, $b$, and $c$ are more fundamental to a particular call of the function than the variable $x$.  Parameters describe whole classes of behavior for the function.  Occasionally a mathematician may write these out explicitly:

$$
f(x; a,b,c) = a x^2 + b x + c
$$

Similarly, we can define a core-level `sample` much like parameters, which allows daughter arms to access both the parent core `sample` and their own `sample`, if any.  We call such a general-purpose core a _door_, which effectively acts as a gate-building core through its arms.  Put simply, a door is a core with a sample but no restrictions on the constituent arms.  It's the most general case of a function in Hoon.

```
        door
       /    \
battery      .
            / \
      sample   context
```

We create a door using the `|_` barcab rune, and we call the arms within it using the `%~` censig rune to handle the door's sample separately from the arm's sample.

For instance, to convert the foregoing quadratic expression into a door with a parameter sample and a variable sample, we compose 

```hoon
> =po |_  [a=@ud b=@ud c=@ud]
++  quad
  |=  x=@ud
  (add (add (mul a (mul x x)) (mul b x)) c)
--
```

If you are new to Hoon, you may find the usage a bit surprising.  We will effectively use the door and its arm in two steps:

1. First we use `%~` censig to build a gate on demand which has the door's sample set.
2. Then we invoke that gate normally using `%:` cencol and friends.

```hoon
~(quad po [5 4 3])
```

```hoon
(~(quad po [5 4 3]) 2)
```

By hand, we find that 5×2² + 4×2 + 3 = 31 and this is correct.

To repeat, the pattern we have to use is building the gate using a given sample for the door, then slamming that gate.  Doors by convention have two-letter designations, and you will come to recognize `++by`, `++in`, and others.

Doors enable us to build tools through the design pattern of building a gate on demand.  We can defer parts of a gate calculation to when certain values are known.  We will use this capability first with simple data storage tools like `+$map` and `+$set`, but even regular Urbit apps or Gall agents are in fact doors.
