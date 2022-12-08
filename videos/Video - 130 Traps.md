---
uuid: 130
layout: node
title: "Traps, recursion"
tags:
 - "%hoon"
prerequisites:
  - "125"
postrequisites:
  - "133"
objectives:
  - "Employ a trap to produce a reentrant block of code."
  - "Produce a recursive gate."
  - "Distinguish head and tail recursion."
runes:
  - "|-"
  - ".+"
  - "%="
irregular:
  - "+()"
  - "$()"
key_points: []
assessments: []
comments: ""
content: ""
---

#   Traps & Recursion

Computers are designed to carry out tasks repetitively until a particular condition is met, such as once for each item in a collection.  Many programming languages call this a “loop”, or a process which is looped back through again and again.

Hoon can implement a loop using a `|-` barhep trap, which defines a point to which a program can logically return with certain changes made.

This program calculates a factorial from `value`.

```hoon
=/  value  6
=/  sum  1
|-
?:  =(1 value)  sum
%=  $
  value  (sub value 1)
  sum    (mul sum value)
==
```

You will notice some new runes in this program:  a `|-` barhep trap rune which marks the logical beginning of the loop; a `?:` wutcol test which lets us distinguish two expressions based on the result of a comparison; and a `%=` centis rune which contains the changes which will be included the next time through the loop.

First, let's rewrite this program in an “unrolled” form that carries out an equivalent calculation.

```hoon
=/  value  6
=/  sum  1
::
?:  =(1 value)  sum              :: value = 6
=/  value  (sub value 1)         :: value → 5
=/  sum    (mul sum value)       :: sum   → 1×6 = 6
::
?:  =(1 value)  sum              :: value = 5
=/  value  (sub value 1)         :: value → 4
=/  sum    (mul sum value)       :: sum   → 6×5 = 30
::
?:  =(1 value)  sum              :: value = 4
=/  value  (sub value 1)         :: value → 3
=/  sum    (mul sum value)       :: sum   → 30×4 = 120
::
?:  =(1 value)  sum              :: value = 3
=/  value  (sub value 1)         :: value → 2
=/  sum    (mul sum value)       :: sum   → 120×5 = 720
::
?:  =(1 value)  sum              :: value = 2
=/  value  (sub value 1)         :: value → 1
=/  sum    (mul sum value)       :: sum   → 720×1 = 720
::
sum                              :: value = 1
```

Each `?:` wutcol check branches the between the case-if-true and case-if-false.  Since `value` doesn't become equal to `1` until the end, the `value` and `sum` continue to be altered progressively.

This mode of writing a loop is complicated and inflexible:  should we need a different starting `value`, we would have to rewrite all of the code to accommodate the change.

A trap allows us to collect the code which is repeated in one place and to collect the associated changes at each step in a `%=` centis clause.

```hoon
=/  value  6
=/  sum  1
|-
?:  =(1 value)  sum
%=  $
  value  (sub value 1)
  sum    (mul sum value)
==
```

The entire `%=` centis clause is evaluated at the same time, so the `value` used in the `sum` calculation is the `value` from \*this\* time through the loop.

Let's examine a different formulation of a factorial:

```hoon
=/  value  6
|-
?:  =(value 1)  1
%+  mul
value
%=  $
  value  (sub value 1)
==
```

In this form, you can see a `++mul` gate applied to the result of resetting the trap with new values.  We can visualize this operation as a pyramid instead:

```hoon
(factorial 6)
(mul 6 (factorial 5)))
(mul 6 (mul 5 (factorial 4)))
(mul 6 (mul 5 (mul 4 (factorial 3))))
(mul 6 (mul 5 (mul 4 (mul 3 (factorial 2)))))
(mul 6 (mul 5 (mul 4 (mul 3 (mul 2 (factorial 1))))))
(mul 6 (mul 5 (mul 4 (mul 3 (mul 2 1)))))
(mul 6 (mul 5 (mul 4 (mul 3 2))))
(mul 6 (mul 5 (mul 4 6)))
(mul 6 (mul 5 24))
(mul 6 120)
720
```

$$
6! = 6 \times 5! = 6 \times 5 \times 4! = 6 \times 5 \times 4 \times 3! = 6 \times 5 \times 4 \times 3 \times 2! = 6 \times 5 \times 4 \times 3 \times 2 \times 1!
$$

$$
6 \times 5 \times 4 \times 3 \times 2 \times 1 = 6 \times 5 \times 4 \times 3 \times 2 = 6 \times 5 \times 4 \times 6 = 6 \times 5 \times 24 = 6 \times 120 = 720
$$

Essentially, we float gate calls until the final iteration of the call produces a value.  Then that is propagated back through the trap until a final result is yielded.

A trap should end in a value, in this case `sum`.  Otherwise one can end up with an infinite loop wherein the expression never terminates.

The `%=` cenhep rune is always used to reset part of a core with a list of indicated changes.  Later when we take a look at cores, we can explain why `$` buc is used.
