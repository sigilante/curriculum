---
title: "Managing State & Computations"
teaching: 45
exercises: 15
nodes:
- "163"
- "180"
objectives:
- "Create a `%say` generator."
- "Identify how Dojo sees and interprets a generator as a cell with a head tag."
- "Identify the elements of a `sample` for a `%say` generator."
- "Produce a `%say` generator with optional arguments."
- "Discuss stateful v. stateless applications and path dependence."
- "Enumerate Hoon's tools for dealing with state:  `=.` tisdot, `=^` tisket, `;<` micgal, `;~` micsig."
- "Defer a computation."
runes:
- "`=.`"
- "`=^`"
- "`=~`"
- "`;<`"
- "`;~`"
keypoints:
- "A `%say` generator (and its cousin the `%ask` generator) affords you more flexibility in generator inputs."
- "Stateful applications requiring deferring parts of an expression relative to other parts."
readings:
- "https://developers.urbit.org/guides/core/hoon-school/O-subject"
- "https://developers.urbit.org/guides/core/hoon-school/P-stdlib-io"
- "https://developers.urbit.org/guides/core/hoon-school/Q-func"
---

#   Managing State & Computations

##  `%say` Generators

A naked generator is merely a gate:  a core with a `$` arm that Dojo knows to call.  However, we can also invoke a generator which is a cell of a metadata tag and a core.  The next level-up for our generator skills is the `%say` generator, a cell of `[%say core]` that affords slightly more sophisticated evaluation.

We use `%say` generators when we want to provide something else in Arvo, the Urbit operating system, with metadata about the generator's output. This is useful when a generator is needed to pipe data to another program, a frequent occurrence.

To that end, `%say` generators use `mark`s to make it clear, to other Arvo computations, exactly what kind of data their output is. A `mark` is akin to a MIME type on the Arvo level. A `mark` describes the data in some way, indicating that it's an `%atom`, or that it's a standard such as `%json`, or even that it's an application-specific data structure like `%talk-command`. `mark`s are not specific to `%say` generators; whenever data moves between programs in Arvo, that data is marked.

So, more formally, a `%say` generator is a `cell`. The head of that cell is the `%say` tag, and the tail is a `gate` that produces a `cask` -- a pair of the output data and the `mark` describing that data.

Save this example as `say.hoon` in the `/gen` directory of your `%base` desk:

```hoon
:-  %say
|=  *
:-  %noun
(add 40 2)
```

Run it with:

```hoon
> |commit %base

> +say
42
```

Notice that we used no argument, something that is possible with `%say` generators but impossible with naked generators. We'll explain that in a moment. For now, let's focus on the code that is necessary to make something a `%say` generator.

```hoon
:-  %say
```

Recall that the rune `:-` produces a cell, with the first following expression as its head and the second following expression as its tail.

The expression above creates a cell with `%say` as the head. The tail is the `|= *` expression on the line that follows.

```hoon
|=  *
:-  %noun
(add 40 2)
```

`|= *` constructs a [gate](https://urbit.org/docs/glossary/gate/) that takes a noun. This [gate](https://urbit.org/docs/glossary/gate/) will itself produce a `cask`, which is cell formed by the prepending `:-`. The head of that `cask` is `%noun` and the tail is the rest of the program, `(add 40 2)`. The tail of the `cask` will be our actual data produced by the body of the program: in this case, just adding 40 and 2 together.

A `%say` generator has access to values besides those passed into it and the Hoon standard subject.  Namely, a `%say` generator knows about `our`, `eny`, and `now`:

- `our` is our current ship identity.
- `eny` is entropy, a source of randomness.
- `now` is the current system timestamp.
- `bec` is the current path.

Dojo will automatically supply these values to the gate unless they are stubbed out with `*`.

### `%say` generators with arguments

We can modify the boilerplate code to allow arguments to be passed into a `%say` generator, but in a way that gives us more power than we would have if we just used a naked generator.

Naked generators are limited because they have no way of accessing data that exists in Arvo, such as the date and time or pieces of fresh entropy.  In `%say` generators, however, we can access that kind of subject by identifying them in the gate's sample, which we only specified as `*` in the previous few examples. But we can do more with `%say` generators if we do more with that sample.  Any valid sample will follow this 3-tuple scheme:

`[[now=@da eny=@uvJ bec=beak] [list of unnamed arguments] [list of named arguments]]`

TODO: null-terminated tuple

This entire structure is a noun, which is why `*` is a valid sample if we wish to not use any of the information here in a generator. But let's look at each of these three elements, piece by piece.

### Example:  Magic 8-Ball

The [Magic 8-Ball](https://github.com/urbit/hoon-workbook/blob/master/eightball.udon) is a classic Hoon example that returns one of a variety of answers in response to a call.  In its entirety:

```hoon
!:
:-  %say
|=  [[* eny=@uvJ *] *]
:-  %noun
^-  tape
=/  answers=(list tape)
  :~  "It is certain."
      "It is decidedly so."
      "Without a doubt."
      "Yes - definitely."
      "You may rely on it."
      "As I see it, yes."
      "Most likely."
      "Outlook good."
      "Yes."
      "Signs point to yes."
      "Reply hazy, try again"
      "Ask again later."
      "Better not tell you now."
      "Cannot predict now."
      "Concentrate and ask again."
      "Don't count on it."
      "My reply is no."
      "My sources say no."
      "Outlook not so good."
      "Very doubtful."
  ==
=/  rng  ~(. og eny)
=/  val  (rad:rng (lent answers))
(snag val answers)
```

Most of the “work” is being done by these two lines:

```hoon
=/  rng  ~(. og eny)
=/  val  (rad:rng (lent answers))
```

`~(. og eny)` starts a random number generator with a seed from the current entropy.  A [random number generator](https://en.wikipedia.org/wiki/Random_number_generation) is a stateful mathematical function that produces an unpredictable result (unless you know the algorithm AND the starting value, or seed).  Here we pull the subject of [`++og`](https://urbit.org/docs/hoon/reference/stdlib/3d#og), the randomness core in Hoon, to start the RNG.

Then we slam the `++rad:rng` gate which returns a random number from 0 to _n_-1 inclusive.  This gives us a random value from the list of possible answers.

Since this is a `%say` generator, we can run it without arguments:

```hoon
> +magic-8
"Ask again later."
```

### Example:  Dice Roll

Let's look at an example that uses all three parts. Save the code below in a file called `dice.hoon` in the `/gen` directory of your `%base` desk.

```hoon
:-  %say
|=  [[now=@da eny=@uvJ bec=beak] [n=@ud ~] [bet=@ud ~]]
:-  %noun
[(~(rad og eny) n) bet]
```

This is a very simple dice program with an optional betting functionality. In the code, our sample specifies faces on all of the Arvo data, meaning that we can easily access them. We also require the argument `[n=@ud ~]`, and allow the _optional_ argument `[bet=@ud ~]`.

We can run this generator like so:

```unknown
> +dice 6, =bet 2
[4 2]

> +dice 6
[5 0]

> +dice 6
[2 0]

> +dice 6, =bet 200
[0 200]

> +dice
nest-fail
```

We get a different value from the same generator between runs, something that isn't possible with a naked generator. Another novelty is the ability to choose to not use the second argument.

- [Hoon School, “1.9 Generators”](https://urbit.org/docs/hoon/hoon-school/generators)


##  State & Deferred Computation

Default Hoon expressions are stateless.  This means that they don't really make reference to any other transactions or events in the system.

However, clearly regular applications, such as Gall agents, are stateful, meaning that they modify their own subject regularly.

There are several ways to manage state.  One approach, including `%=` centis, directly modifies the subject using a rune.  Another method is to use the other runes to compose or sequence changes together (e.g. as a pipe of gates).  By and large the `=` tis runes are responsible for modifying the subject, and the `;` mic runes permit chaining deferred computations together.

We will use `%say` generators as a bridge concept.  We will produce some short applications that maintain state while carrying out a calculation; they still result in a single return value, but gesture at the big-picture approach to maintaining state in persistent agents.

When I say _deferred computation_ in this context, I mean that parts of the subject changes may be underdetermined at first, and must be calculated later using the appropriate runes as new or asynchronous information becomes available.

There are a few runes for modifying the subject and chaining deferred computations together, aside from `%=` cenhep which you've already seen:

- [`=.` tisdot](https://urbit.org/docs/hoon/reference/rune/tis#-tisdot) is used to change a leg in the subject.
- [`=^` tisket](https://urbit.org/docs/hoon/reference/rune/tis#-tisket) is similarly used to change a leg in the tail of the subject then evaluate against it.  This is commonly used for sequential calls to `++og`, the random number generator, and for events that need to be ordered in their resolution e.g. with a `%=` cenhep.  (Used in agents frequently.)
- [`=*` tistar](https://urbit.org/docs/hoon/reference/rune/tis#tistar) defers an expression (rather like a macro).
- [`=~` tissig](https://urbit.org/docs/hoon/reference/rune/tis#-tissig) composes many expressions together serially.
- [`;<` micgal](https://urbit.org/docs/hoon/reference/rune/mic#-micgal) sequences two computations, particularly for an asynchronous event like a remote system call.  (Used in threads.)
- [`;~` micsig](https://urbit.org/docs/hoon/reference/rune/mic#-micsig) produces a pipeline, a way of piping the output of one gate into another in a chain.  (This is particularly helpful when parsing text.)

### Example:  Bank Account as a Door

This door essentially replaces the sample of the door with new values as each transaction proceeds.  This is similar to how a Gall agent will modify its own state over time.

Unlike a Gall agent, however, this generator has no persistence:  once run, it starts from scratch again.

```hoon
:-  %say
|=  *
:-  %noun
=<  =~  new-account
      (deposit 100)
      (deposit 100)
      (withdraw 50)
      balance
    ==
|%
++  new-account
  |_  balance=@ud
  ++  deposit
    |=  amount=@ud
    +>.$(balance (add balance amount))
  ++  withdraw
    |=  amount=@ud
    +>.$(balance (sub balance amount))
  --
--
```

<!-- ~littel-fodrex: the construction ~(. new-account 1.000) does indeed work, without the need to pin a copy of the door to a face. and i think i understand why so that's exciting -->

- Commentary at [“1.8.1 Bank Account”](https://urbit.org/docs/hoon/hoon-school/bank-account)

### Example:  Random Numbers (`=^` tisket)

A given seed will produce the same result every time it is run.  We need to use `eny` to seed it non-deterministically, but we can also pin the state using `=^` tisket.

```hoon
> =+  rng=~(. og eny)  [-:(rads:rng 100) -:(rads:rng 100)]  
[60 60]

> =/  rng  ~(. og eny)
  =^  r1  rng  (rads:rng 100)
  =^  r2  rng  (rads:rng 100)
  [r1 r2]
[21 47]
```


##  `%ask` Generators

We use an `%ask` generator when we want to create an interactive program that prompts for inputs as it runs, rather than expecting arguments to be passed in at the time of initiation.

Once you can parse input as above, then you can start to produce some fun CLI agents.  (I'd love to see Zork-on-Mars someday!)

If you are interested in producing command-line-based tools, look into the `%shoe` and `%sole` libraries.

- [Hoon Guide, “CLI apps”](https://urbit.org/docs/hoon/guides/cli-tutorial)
- [`~wicdev-wisryt`, “Input and Output in Hoon”](https://urbit.org/blog/io-in-hoon)


##  Formatted Text

A `+$tank` is a formatted print tree.  Error messages and the like are built of `tank`s.  They are defined in `hoon.hoon`:

```hoon
::  $tank: formatted print tree
::
::    just a cord, or
::    %leaf: just a tape
::    %palm: backstep list
::           flat-mid, open, flat-open, flat-close
::    %rose: flat list
::           flat-mid, open, close
::
+$  tank
  $~  leaf/~
  $@  cord
  $%  [%leaf p=tape]
      [%palm p=(qual tape tape tape tape) q=(list tank)]
      [%rose p=(trel tape tape tape) q=(list tank)]
  ==
+$ tang (list tank) :: bottom-first error
```

The [`++ram:re`](https://urbit.org/docs/hoon/reference/stdlib/4c#ramre) arm is used to convert these to actual formatted output, e.g.

```hoon
> ~(ram re leaf+"foo")
"foo"
> ~(ram re [%palm ["|" "(" "!" ")"] leaf+"foo" leaf+"bar" leaf+"baz" ~])
"(!foo|bar|baz)"
> ~(ram re [%rose [" " "[" "]"] leaf+"foo" leaf+"bar" leaf+"baz" ~])
"[foo bar baz]"
```

Many generators build sophisticated output using `tank`s and the short-format builder `+`, e.g. in `/gen/azimuth-block/hoon`:

```hoon
[leaf+(scow %ud block)]~
```

At this point we aren't going to use `tank`s directly yet, but you'll see them more and more as you move into more advanced generators.

### Deep Dive:  `cat.hoon`

For instance, how does `+cat` work?  Let's look at the structure of `/gen/cat/hoon`:

```hoon
::  ConCATenate file listings
::
::::  /hoon/cat/gen
  ::
/?    310
/+    pretty-file, show-dir
::
::::
  ::
:-  %say
|=  [^ [arg=(list path)] vane=?(%g %c)]
=-  tang+(flop `tang`(zing -))
%+  turn  arg
|=  pax=path
^-  tang
=+  ark=.^(arch (cat 3 vane %y) pax)
?^  fil.ark
  ?:  =(%sched -:(flop pax))
    [>.^((map @da cord) (cat 3 vane %x) pax)<]~
  [leaf+(spud pax) (pretty-file .^(noun (cat 3 vane %x) pax))]
?-     dir.ark                                          ::  handle ambiguity
    ~
  [rose+[" " `~]^~[leaf+"~" (smyt pax)]]~
::
    [[@t ~] ~ ~]
  $(pax (welp pax /[p.n.dir.ark]))
::
    *
  =-  [palm+[": " ``~]^-]~
  :~  rose+[" " `~]^~[leaf+"*" (smyt pax)]
      `tank`(show-dir vane pax dir.ark)
  ==
==
```

- What is the top-level structure of the generator?  (A cell of `%say` and the gate, previewing `%say` generators.)
- What don't you recognize?
  - `/?` faswut pins the expected Arvo kelvin version; right now it doesn't do anything
  - [`.^` dotket](https://urbit.org/docs/hoon/reference/rune/dot#-dotket) loads a value from Arvo (called a “scry”)
  - `++smyt` pretty-prints a path
  - [`=-` tishep](https://urbit.org/docs/hoon/reference/rune/tis#--tishep) combines with the subject, inverted relative to `=+`/`=/`.
  - There are some `tape` interpolation and `list` construction tools we haven't used yet:
      
      ```hoon
      > [<56>]
      "56"
      > [<56>]~
      ["56" ~]
      > ~[<56>]
      ["56" ~]
      > /[4]  
      [4 ~]
      ```
  - `?-` wuthep we saw up above:  it's a `switch` statement.


## Functional Programming Calculations

Functional languages emphasize calculations to be free of side effects and to simply result in a value.  Good Hoon expressions generally avoid modifying state and certainly avoid modifying state outside of the current operational subject (frequently the core).

Functional programmers frequently rely on three design patterns to produce operations on collections of data:

1. Map. The Map operation describes applying a function to each item of a set or iterable object, resulting in the same final number of items transformed. In Hoon terms, we would say slamming a gate on each member of a `list` or `set`. The standard library arms that accomplish this include [`++turn`](https://developers.urbit.org/reference/hoon/stdlib/2b#turn) for a `list`, [`++run:in`](https://developers.urbit.org/reference/hoon/stdlib/2h#repin) for a `set`, and [`++run:by`](https://developers.urbit.org/reference/hoon/stdlib/2i#runby) for a `map`.

2. Reduce. The Reduce operation applies a function as a sequence of pairwise operations to each item, resulting in one summary value. The standard library arms that accomplish this are [`++roll`](https://developers.urbit.org/reference/hoon/stdlib/2b#roll) and [`++reel`](https://developers.urbit.org/reference/hoon/stdlib/2b#reel) for a `list`, [`++rep:in`](https://developers.urbit.org/reference/hoon/stdlib/2h#repin) for a `set`, and [`++rep:by`](https://developers.urbit.org/reference/hoon/stdlib/2i#repby) for a `map`.  

3. Filter. The Filter operation applies a true/false function to each member of a collection, resulting in some number of items equal to or fewer than the size of the original set. In Hoon, the library arms that carry this out include [`++skim`](https://developers.urbit.org/reference/hoon/stdlib/2b#skim), [`++skid`](https://developers.urbit.org/reference/hoon/stdlib/2b#skid), [`++murn`](https://developers.urbit.org/reference/hoon/stdlib/2b#murn) for a `list`, and [`++rib:by`](https://developers.urbit.org/reference/hoon/stdlib/2i#ribby) for a `map`.
