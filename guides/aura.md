# Implementing an Aura

1. **Design the aura.**  A lot of existing letter pairs are spoken for, and new auras _should_ nest logically. Currently unoccupied letters include: `abeghjkmovwxyz`.  If you can make a case for why your new aura logically nests under an existing aura, then you implement such a nesting; you'll just need to make the case for it in your pull request submission.

2. **Implement base logic in `/sys/hoon.hoon`.**  This, by and large, means providing a core or door which can correctly carry out arithmetic, conversion, processing, and so forth on your atom.

3. **Implement pretty-printer in `|co`.**

  1. **Produce a formatted text `tank`.**  Due to nesting rules, you will likely have to implement all of the logic here if you are adding your code to the end of `hoon.hoon`.

  2. **Produce `tape`.** Take your `tank`-maker and wrap it in `%~ ram re`.

4. **Implement parser in `|so`.**  Compose a parsing rule which is distinct from all others and add it in the appropriate sections here.  The aura parser prefixes elements with a type `term`; properly the pair is called a `dime`.

##  Example:  Sexagesimal Degrees

Classically, angular measurements using degrees subdivided each degree into 60 minutes and each minute into 60 seconds.  Although less common in an age of [floating-point values](https://xkcd.com/2170/), proficiency with [sexagesimal notation](https://en.wikipedia.org/wiki/Degree_(angle)#Subdivisions) lends distinction and _gravitas_.

$$
5°6'7''
$$


### Design

In this example, we will produce a degree–minute–second (DMS) aura.  We will call it `@dms` and nest it under `@d` date (in violation of the aura nesting proclamation).

It will have the visual form of three integers prefixed with `.` dots, e.g. `.359.59.59` for 359°59'59''.  This distinguishes it from `@rs`, which has two similarly-separated values, e.g. `.1.2`; and from `@if`, which has four, e.g. `.1.2.3.4`.

It will have the bit-logical form of four eight-bit bytes:  two for the degrees (since we'll eventually cap at one circle, 360°), and one each for the minutes and seconds (since we'll cap at 60' and 60'').

```hoon
0xssss.ssss.mmmm.mmmm.dddd.dddd.dddd.dddd
```

### Base Logic

We need to be able to perform arithmetic and type conversion with `@dms` values.  Some value representations have an “unpacked“ form, like dates and floating-point values.  This makes it easier to shunt the values between auxiliary functions.  We'll define one as well here, `sexa` (for _sexagesimal_, base-60).

```hoon
++  da
  |%
  +$  sexa  [d=@ud m=@ud s=@ud]
  ++  reck
    |=  p=@dms
    ^-  sexa
    =/  q  (flop `(list @ux)`(rip [4 2] a))
    :+
      d=(rep 5 ~[(snag 1 q) (snag 0 q)])
      m=(snag 2 q)
      s=(snag 3 q)
  ++  wrap
    |=  p=sexa
    ^-  @dms
    (rep 6 ~[(rev 5 2 d.p) (rep 5 ~[m.p s.p])])
  ++  add
    |=  [p=@dms q=@dms]
    ^-  @dms
    =/  pp  (reck p)
    =/  qq  (reck q)
    
    (op (reck p) (reck q) add)
  ++  norm
    |=  p=@dms
    ^-  @dms
```


> =a 0x4444.4444.3333.3333.2222.2222.1111.1111
> `(list @ux)`(rip [1 8] a)

### Parsing

A parsing rule which correctly handles this is:

```hoon
;~(pfix dot ;~((glue dot) bisk:so bisk:so bisk:so))
```

as demonstrated by:

```hoon
> (;~(pfix dot ;~((glue dot) bisk:so bisk:so bisk:so)) [[1 1] ".1.2.3"])
[p=[p=1 q=7] q=[~ u=[p=[[%ud 1] [%ud 2] [%ud 3]] q=[p=[p=1 q=7] q=""]]]]

> (scan ".5.6.7" ;~(pfix dot ;~((glue dot) bisk:so bisk:so bisk:so)))
[[%ud 5] [%ud 6] [%ud 7]]

> (scan ".5.6" ;~(pfix dot ;~((glue dot) bisk:so bisk:so bisk:so)))
{1 5}
syntax error
dojo: hoon expression failed

> (scan ".5.6.7.8" ;~(pfix dot ;~((glue dot) bisk:so bisk:so bisk:so)))
{1 9}
syntax error
dojo: hoon expression failed
```




(For now, we'll ignore overflow:  e.g., `.0.0.60` will store as-is rather than promote to `.0.1.0`.  We'll fix this later.  You'd also want to decide how to deal with negative arcs, if supported.)


Our parser logic needs to be cited in `++zust:so` because that deals with values prefixed with `.` dot.
```

++ co

++ rend

:: add parser here, can't rely on later materials due to core nesting

:: must produce tape, so `%~ ram re` on your tank

```

4. Implement parser in `|so`.
