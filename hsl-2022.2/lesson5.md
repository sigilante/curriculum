---
title: "Subject-Oriented Programming"
teaching: 45
exercises: 15
nodes:
- "150"
- "153"
- "155"
objectives:
- "Build cores for deferred use and with custom samples."
- "Identify the `$` buc arm in several structures and its role."
- "Identify the structure of a door and relate it to a core."
- "Pull an arm in a door."
- "Identify the role of a desk in the Clay filesystem."
- "Identify the components of a beak."
- "Identify filesystem locations (including desks)."
- "Identify the components of a path."
runes:
- "`!:`"
- "`|^`"
- "`|.`"
- "`|:`"
- "`|_`"
- "`%~`"
- "`$_`"
keypoints:
- "Core patterns can be used to build many kinds of customized gates."
- "The door is a common configuration for an Urbit core."
- "The arms of doors are gate-builders."
- "A desk in Clay organizes collections of code and data resources."
- "A path in Clay describes a unique access path to a resource."
- "The beak describes the current triplet of ship, desk, and timestamp for the filesystem."
---

#   Subject-Oriented Programming

##  The Subject

Before we talk about a single line of Hoon today, I want to talk about the subject-oriented programming paradigm.

Classically, programming styles are categorized into:

1. Imperative:  focused on _control_ flow, recipe-like steps.
2. Declarative:  focused on _data_ flow than control flow; think of database queries or regular expressions, if you've worked with them.
3. Functional:  focused on composition of functions and expressions as a logical tree (subcategory of declarative programming).
4. Object-Oriented:  focused on relationships between entities containing data and code that pass messages to each other to control what happens.

Sometimes these map to languages but you can basically do any of them in any language (if you're really willing to kick against the pricks sometimes).  The affordances and tools tend to facilitate one way over others though.

Subject-oriented programming combines aspects of object-oriented programming and functional programming.  You can think of it as a functional language with strict scoping rules.  If I lost you there, that's fine, we'll come back to this point.

The _subject_ of any Hoon expression is basically the binary tree which spawned it.  In essence, subject-oriented programming is a way of fusing context, stack, and variable scope into one.  Subject-oriented programming means that this scope or limit of what you can see, kind of like a horizon, is all you really have to take into account.

### Wing Resolution

We've had to jump through some (small) hoops to make our values visible to subsequent expressions in the Dojo.  This is because the Dojo can _either_ manually pin a value into the subject (using `=name` syntax) or evaluate a full Hoon expression including values (using `=/` tisfas syntax).

We saw a little bit of wing resolution in Lesson 3:

```hoon
> =data [a=[aa=[aaa=[1 2] bbb=[3 4]] bb=[5 6]] b=[7 8]]

> -:aaa.aa.a.data
1
```

How does an expression like this actually resolve?  Hoon doesn't know whether a particular value is a face or an arm name until it conducts a search looking for name matches.  If it finds a face first, the value of the face is returned.  If it finds an arm first, the arm will be evaluated and the product returned.

The names are breadcrumbs as a “wing” or limb search path.  (There is one critical difference between address-based search paths and name-based search paths:  address-based search paths always return the value as data, never as code.  Use name-based search paths if you need to evaluate it as an expression.)

> Urbit does not use the lambda calculus, an environment or symbol table, or linking. Because it pushes name resolution out of the fundamental interpreter and up into the language, it can play many more namespace juggling tricks.

There is no restriction against using the same face name for multiple limbs of the subject. This is one way in which faces aren't like ordinary variables:

`^` skips the first _n_ matches in the subject.  What this means to you is that the _n_ “nearest” names are skipped first, so what `^` does is pull a name from an outer core.  (Naturally, you only use this when you know what you’re looking for in the subject.)  `^$` is one way of setting up a `%=` cenhep loop/recursion with two nested `|-` barket traps, for instance.

```hoon
> double:[double=123 c]
123

> ^double:[double=123 c]
24

> ^double:[double=123 double=456 c]
456

> ^^double:[double=123 double=456 c]
24
```

- [Hoon School, “The Subject and Its Legs”](https://urbit.org/docs/hoon/hoon-school/the-subject-and-its-legs)

> ## Improving Debugging
>
> The [`!:` zapcol](https://urbit.org/docs/hoon/reference/rune/zap#-zapcol) rune turns on a stack trace, or table of data 
> related to a crash, in the event that the daughter expression 
> fails.  `!:` zapcol is frequently used at the top of a 
> generator to help track and guide debugging.
{: .callout}


##  More Cores

Cores store code (`battery`) and data (`payload`).  Although gates are a type of core, other cores can be used to build gates to carry out particular operations.  Since Hoon is very rigorous about type constraints and type checking, as you have been discovering to your chagrin in the homework, we will use gate-building cores to satisfy this rigor.  (In the last lesson, we saw the `list` and `sane` gate-building arms.)

### Building Gates on Demand

For instance, most of the time when we have called a gate, the gate has already existed:

```hoon
> =inc |=(a=@ud (add 1 a))
> (inc 10)
11
```

In this case, `inc` is a gate which already exists in the subject, and Hoon looks up the name in the current subject, then slots the payload into the battery arm `$` and evaluates the expression.

We could also skip producing the gate ahead of time and build it on-demand right where we use it:

```hoon
> (|=(a=@ud (add 1 a)) 123)
124
> (|=(a=@ud (mul 2 a)) 123)
246
```

Although it rarely matters to us much, the standard library arms `++add`, `++mul`, etc. are more like the second:  they are gates built on demand by the arms.

Let's build a core which has arms to modify values in a characteristic way by building gates.  In the Dojo:

```hoon
=c |%
++  add-10
  |=  a=@ud
  (add a 10)
++  sub-10
  |=  a=@ud
  (sub a 10)
++  mul-10
  |=  a=@ud
  (mul a 10)
++  div-10
  |=  a=@ud
  (div a 10)
++  mul-20
  |=  a=@ud
  (add (mul-10 a) (mul-10 a))
--
```

We use these by locating them in the core `c` with `:` col limb resolution:

```hoon
> (add-10:c 6)
16
> (sub-10:c 16)
6
> (mul-10:c 16)
160
> (div-10:c 160)
16
```

### What's in the Payload?

The `payload` contains the data necessary for a core to evaluate its expressions.  Formally, the `payload` itself is also a cell of two standard parts:  `[sample context]`.

- `sample` refers to the input arguments.
- `context` refers to the effective subject including the parent core.

When you type a core name at the Dojo prompt, the pretty-printer displays a summary of known information:

```hoon
> dec  
<1.hkg [a=@ <46.hgz 1.pnw %140>]>
```

Let's dissect this.  Since the top-level description is a cell of `[battery payload]`, it makes sense that the head of `++dec` is the battery:

```hoon
> -:dec  
[ 11  
 [ 1.851.876.717  
   [ 1  
     [1 1.717.658.988]  
     7  
     [0 1]  
     8  
     [1 1 100 101 99 114 101 109 101 110 116 45 117 110 100 101 114 102 108 111 119 0]  
     9  
     2  
     0  
     1  
   ]  
   0  
   1  
 ]  
 6  
 [5 [1 0] 0 6]  
 [0 0]  
 8  
 [1 0]  
 8  
 [1 6 [5 [0 30] 4 0 6] [0 6] 9 2 10 [6 4 0 6] 0 1]  
 9  
 2  
 0  
 1  
]
```

As this is Nock code, it's rather hard for us to do anything with directly, but there it is.

Let's look at the `payload`, at the tail or address `+3` of the core's tree:

```hoon
> +3:dec  
[a=0 <46.hgz 1.pnw %140>]
```

Now this is a cell again, `[sample context]`.  Let's see the `sample` alone:

```hoon
> +6:dec
a=0
```

(The pretty-printer now resolves the aura of the input value to the bunt of the mold.)

The `context` is the current system subject, which has 46 arms and refers to Hoon version 140K:

```hoon
> +7:dec
<46.hgz 1.pnw %140>
```

> ##  Examining `battery`s
> 
> Recall that as we saw a moment ago, the `battery` of any gate
> refers to the code, located at the address `+2` or `-`:
> 
> ```hoon
> > -:add
> [6 [5 [1 0] 0 12] [0 13] 9 2 10 [6 [8 [9 2.398 0 7] 9 2 10 [6 0 28] 0 2] 4 0 13] 0 1]
> ```
{: .callout}

> ##  Examining `sample`s
> 
> You can check out the default `sample` of any gate by name:
> 
> ```hoon
> > +6:add
> [a=0 b=0]
> ```
{: .callout}

Every arm of a core is evaluated with its parent core as the subject.  `.` is the subject, so `..` is the subject of a given arm (second dot being wing resolution).  You can check details of the parent core using the `..` syntax `..add`.  This trick is used when producing agents that have highly nested operations (search `..` in the `/app` directory), or when composing [jets](https://urbit.org/docs/vere/jetting#edit-the-hoon-source-code), for instance.

### Modifying Gate Behavior

Sometimes you need to modify parts of a core (like a gate) on-the-fly to get the desired behavior.  For instance, if you are using `++roll` to calculate the multiplicative product of the elements of a list, this “just works”:

```hoon
> (roll `(list @ud)`~[10 12 14 16 18] mul)  
483.840
```

In contrast, if you do the same thing to a list of numbers with a fractional part (`@rs` floating-point values), the naïve operation will fail:

```hoon
> (roll `(list @rs)`~[.10 .12 .14 .16 .18] mul:rs)  
.0
```

Why is this?  Let's peek inside the gates and see.  Since we know a core is a cell of `[battery payload]`, let's take a look at the `payload`:

```hoon
> +:mul  
[[a=1 b=1] <46.hgz 1.pnw %140>]  
> +:mul:rs  
[[a=.0 b=.0] <21.hqd [r=?(%d %n %u %z) <51.qbt 123.zao 46.hgz 1.pnw %140>]>]
```

The correct behavior for `++mul:rs` is really to multiply starting from one, not zero, so that `++roll` doesn't wipe out the entire product.

If we want to set the default sample to have a different value than the bunt of the type, we can use the [`$_` buccab](https://urbit.org/docs/hoon/reference/rune/buc#-buccab) rune, whose irregular form is simply `_`.

```hoon
> =mmul |=([a=_1 b=_1] (mul:rs a b))
> (roll `(list @rs)`~[.10 .12 .14 .16 .18] mmul)
> .483840
```

> ##  Custom Samples
> 
> The [`|:` barcol](https://urbit.org/docs/hoon/reference/rune/bar#-barcol) rune also allows you to build a new gate (core) 
> with a custom sample.  For instance, we can take the original 
> `++mul:rs` gate and give it a sample with default values of 
> `.1`:
>
> ```hoon
> > =mmul |:([a=`@rs`.1 b=`@rs`.1] (mul:rs a b))  
> > (roll `(list @rs)`~[.10 .12 .14 .16 .18] mmul)
> .483840
> ```
> 
> It allows you to do the same thing as `$_` buccab in a 
> different way.
{: .callout}


##  Doors
- "Identify the structure of a door and relate it to a core."
- "Pull an arm in a door."

Doors are another kind of core whose arms evaluate to make gates.  The difference is that a door also has its own sample.  A door is the most general case of a function in Hoon.  (You could say a "gate-building core" or a "function-building function" to clarify what these are.)

Doors are created with the [`|_` barcab](https://urbit.org/docs/hoon/reference/rune/bar#_-barcab) rune.  Doors get used for a few different purposes in the standard library:

- instrumenting and storing persistent data structures like `map`s (Lesson 6, Lesson 7)
- implementing state machines (Lesson 8)

One BIG pitfall for thinking about doors is thinking of them as “containing” gates, as if they were more like “objects”.  Instead, think of them the same way as you think of gates, just that they can be altered at a higher level.

Here's a mathematical example.  If we wanted to calculate a quadratic polynomial, _y = a x² + b x + c_, then we need to know two kinds of things:  the unknown or variable _x_, AND the parameters _a_, _b_, and _c_.

If we were to build this as a gate, we would need to pass in four parameters:

```hoon
=poly-gate |=  [x=@ud a=@ud b=@ud c=@ud]
(add (add (mul a (mul x x)) (mul b x)) c)
```

Any time we call the gate, we have to provide all four values:  one unknown, three parameters.  But there's a sense in which we want to separate the three parameters and only call the gate with one _x_ value.  One way to accomplish this is to wrap the gate inside of another:

```hoon
=wrapped-gate |=  [x=@ud]
=/  a  5
=/  b  4
=/  c  3
(poly-gate x a b c)
```

> ##  Currying
> 
> If we instead used the _currying_ gate builders, [`++cury`](https://urbit.org/docs/hoon/reference/stdlib/2n#cury) and 
> [`++curr`](https://urbit.org/docs/hoon/reference/stdlib/2n#curry), we could build these up into a gate with a single sample a
> different way.  Consider this a stretch exercise if you're
> interested.
{: .challenge}

If we built this as a door instead, we could push the parameters out to a more inner layer of abstraction.  In this case, the parameters are the sample of the door, while the arm `++quad` builds a gate that corresponds to those parameters and only accepts one unknown variable `x`.

```hoon
=poly |_  [a=@ud b=@ud c=@ud]
++  quad
  |=  x=@ud
  (add (add (mul a (mul x x)) (mul b x)) c)
--
```

This will be used in two steps:  a gate-building step then a gate usage step.

We produce a gate from a door's arm using the [`%~` censig](https://urbit.org/docs/hoon/reference/rune/cen#-censig) rune, almost always used in its irregular form, `~()`.

```hoon
~(quad poly [5 4 3])
```

By itself, not so useful.  We could pin it into the Dojo, for instance, to use later.

Our ultimate goal is to use the built gate on particular data, e.g.,

```hoon
> (~(quad poly [5 4 3]) 2)
31
```

By hand:  5×2² + 4×2 + 3 = 31, so that's correct.

Doors will enable us to build some very powerful data storage tools over the next couple of lessons.

> ##  Adding an Arm
> 
> Add an arm to the door which calculates the linear function
> _a×x + b_.
> 
> Add another arm which calculates the derivative of the first
> quadratic function, _2×a×x + b_.
{: .challenge}

In the above example we created a door `poly` with sample `[a=@ud b=@ud c=@ud]`.  If we investigated, we would find that the initial value of each is `0`, the bunt value of `@ud`.  What if we wish to define a door with a chosen sample value directly?  We can make use of the `$_` rune, whose irregular form is simply `_`.  To create the door `poly` with the sample set to have certain values in the Dojo, we would write

```unknown
> =poly |_  [a=_5 b=_4 c=_3]
++  quad
  |=  x=@ud
  (add (add (mul a (mul x x)) (mul b x)) c)
--

> (quad:poly 2)  
31
```

- [Hoon School, “Doors”](https://urbit.org/docs/hoon/hoon-school/doors#doors) is worth a read.


### A Few Ramifications of Cores and Doors

[`|^` barket](https://urbit.org/docs/hoon/reference/rune/bar#-barket) is an example of what we can call a _convenience rune_, similar to the idea of sugar syntax (irregular syntax to make writing certain things out in a more expressive manner).  `|^` barket produces a core with _at least_ a `$` buc arm and computes it immediately.  (So it's a bit like a trap in the regard of computing immediately.)

This code calculates the volume of a cylinder, _A=πr²h_.

```hoon
=volume-of-cylinder |^
(mul:rs (area-of-circle .2.0) height)
++  area-of-circle
  |=  r=@rs
  (mul:rs pi r)
++  pi  .3.1415926
++  height  .10.0
--
```

Since all of the values either have to be pinned ahead of time or made available as arms, a `|^` barket would probably be used inside of a gate.  Of course, since it is a core with a `$` buc arm, one could also use it recursively to calculate values like the factorial.

---

If you read the docs, you'll find that a [`|-` barhep](https://urbit.org/docs/hoon/reference/rune/bar#-barhep) rune “produces a trap (a core with one arm `$`) and evaluates it.”  So a trap actually evaluates to a `|%` barcen core with an arm `$`:

```hoon
:: count to five
=/  index  1
|-
?:  =(index 5)  index
$(index +(index))
```

actually translates to

```hoon
:: count to five
=/  index  1
=<  $
|%
++  $
  ?:  =(index 5)  index
  %=  $
    index  +(index)
  ==
--
```

You can also create a trap for later use with the [`|.` bardot](https://urbit.org/docs/hoon/reference/rune/bar#-bardot) rune.  It's quite similar, but without the `=<($...` part then it doesn't get evaluated immediately.

```hoon
> =forty-two |.(42)
> $:forty-two
42
> (forty-two)
42
```

---

What is a gate?  It is a door with only one arm `$` buc, and whenever you invoke it then that default arm's expression is referred to and evaluated.

A _gate_ and a _trap_ are actually very similar:  a [gate](https://urbit.org/docs/hoon/reference/rune/bar#-bartis) simply has a sample (and can actively change when evaluated or via a `%=` cenhep), whereas a trap does not (and can _only_ be passively changed via something like `%=` cenhep).

In fact, to relate slamming a gate back to working with doors, `%-` cenhep and friends all evaluate to [`%~` censig](https://urbit.org/docs/hoon/reference/rune/cen#cenhep) on the `$` buc arm.


##  Paths on Mars

An Earth filesystem orients itself around some key metaphor:

- Windows machines organize the world by drive, e.g. `C:\`.
- Unix machines (including macOS and Linux) organize the world from `/`, the root directory.

On Mars, we treat a filesystem as a way of organizing arbitrary access to blocks of persistent data.  There are some concessions to Earth-style filesystems, but Clay (Urbit's filesystem) organizes everything with respect to a `desk`, a discrete collection of static data on a particular ship.  Of course, like everything else in Hoon, a desk is a tree as well.

> ##  Desks as Branches
> 
> If you are comfortable with version control systems like Git,
> then thinking of the Clay filesystem as a version control
> repository may be a fruitful metaphor for you.
> 
> In this case, we think of a desk as an independent branch of
> data on the ship, with its own apps, marks, structure files,
> libraries, generators, and so forth.
> 
> A desk is actually a series of numbered commits, and each time
> you `|commit` a file with changes, you'll see a new revision
> number listed after the ship and the desk name, but before the
> folder and file path.
> 
> You can access an older version of a file in Clay by referring
> to the revision number you are looking for instead of the
> timestamp, e.g. `/~zod/base/2/gen/boxcar/hoon`.
{: .callout}

Whenever we access something in Clay, we provide three pieces of information before the path:  the ship, the desk, and the timestamp.  Typically we are looking for the most up-to-date version of a file, so our triplet consists of our ship name, the desk name (defaulting to `%base`), and the current time.

Two of these can be queried at any time:

- `our` always contains the ship's identity, as a `@p`.
- `now` resolves to the current system time, as a `@da`.

The “current” desk is a Dojo concept, since for Clay we can access any desk at any time (with permission).


We call this triplet the `beak`.  It can be manually constructed using the parts above, or more commonly used with the `/` fas prefix and `=` tis signs for the three components:

```hoon
> /===  
[~.~zod ~.base ~.~2022.4.5..20.34.15..6e5c ~]  
```

(You'll also sometimes see `%` cen stand in for the whole.  So much for consistency!)

The beak is a `(list @ta)` or `(list knot)`.  The pretty-printer may catch and format it a little different depending on how you present it, but they are all commensurate:

```hoon
> /===  
[~.~zod ~.base ~.~2022.4.4..22.03.03..43c1 ~]  
> `(list @ta)`/===  
/~zod/base/~2022.4.4..22.04.36..9f37
> `(list knot)`/===  
/~zod/base/~2022.4.4..22.03.55..7f76  
```

Swapping out a value for one of the equals signs allows you to talk about (hypothetical) other beaks:

```
> /=sandbox=
[~.~zod %sandbox ~.~2022.4.5..20.34.18..1d2b ~]
> /~nec==
[~.~nec ~.base ~.~2022.4.5..20.37.28..cf3e ~]
> /==(@da 0)
[~.~zod ~.base ~292277024401-.1.1 ~]
```

(You can write any path, whether or not it exists; you cannot, of course, access data at any path because most paths don't exist, just as most possible street addresses do not exist.)

At this point in Urbit's history, most interesting changes to Clay are done on Earth and then synchronized back to Mars via `|commit`.  The `cat` generator can show you the contents of a file at a particular path in Clay:

```hoon
> +cat /===/gen/trouble/hoon  
/~zod/base/~2022.4.5..20.42.06..2ad6/gen/trouble/hoon  
/-  *hood  
:-  %say  
|=  $:  [now=@da eny=@uvJ bec=beak]  
       [arg=~ ~]  
   ==  
[%tang (report-vats p.bec now)]
```

The `ls` generator does something similar:

```hoon
> +ls /===/gen
 acme/domain-validation/hoon
 agents/hoon
 aqua/
 aqua-export/hoon
 azimuth/
 azimuth-block/hoon
 ...
```
