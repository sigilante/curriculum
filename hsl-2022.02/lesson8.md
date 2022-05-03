---
title: "Managing State"
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
---

#   Managing State

##  `%say` Generators

A naked generator is merely a gate:  a core with a `$` arm that Dojo knows to call.  However, we can also invoke a generator which is a cell of a metadata tag and a core.  The next level-up for our generator skills is the `%say` generator, a cell of `[%say core]` that affords slightly more sophisticated evaluation.

We use `%say` generators when we want to provide something else in Arvo, the Urbit operating system, with metadata about the generator's output. This is useful when a generator is needed to pipe data to another program, a frequent occurrence.

To that end, `%say` generators use `mark`s to make it clear, to other Arvo computations, exactly what kind of data their output is. A `mark` is akin to a MIME type on the Arvo level. A `mark` describes the data in some way, indicating that it's an `%atom`, or that it's a standard such as `%json`, or even that it's an application-specific data structure like `%talk-command`. `mark`s are not specific to `%say` generators; whenever data moves between programs in Arvo, that data is marked.

So, more formally, a `%say` generator is a `cell`. The head of that cell is the `%say` tag, and the tail is a `gate` that produces a `cask` -- a pair of the output data and the `mark` describing that data.

Save this example as `add.hoon` in the `/gen` directory of your `%base` desk:

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

Dojo will automatically supply these values to the gate unless they are stubbed out with `*`.

### `%say` generators with arguments

We can modify the boilerplate code to allow arguments to be passed into a `%say` generator, but in a way that gives us more power than we would have if we just used a naked generator.

Naked generators are limited because they have no way of accessing data that exists in Arvo, such as the date and time or pieces of fresh entropy.  In `%say` generators, however, we can access that kind of subject by identifying them in the gate's sample, which we only specified as `*` in the previous few examples. But we can do more with `%say` generators if we do more with that sample.  Any valid sample will follow this 3-tuple scheme:

`[[now=@da eny=@uvJ bec=beak] [list of unnamed arguments] [list of named arguments]]`

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


##  Deferring Computation

Default Hoon expressions are stateless.  This means that they don't really make reference to any other transactions or events in the system.

However, clearly regular applications, such as Gall agents, are stateful, meaning that they modify their own subject regularly.

There are several ways to manage state.  One approach, including `%=` cenhep, directly modifies the subject using a rune.  Another method is to use the other

We will use `%say` generators as a bridge concept.  We will produce some short applications that maintain state while carrying out a calculation; they still result in a single return value, but gesture at the big-picture approach to maintaining state in persistent agents.

There are a few runes for modifying the state of the subject, aside from `%=` cenhep which you've already seen:

- [`=.` tisdot](https://urbit.org/docs/hoon/reference/rune/tis#-tisdot) is used to change a leg in the subject.
- [`=^` tisket](https://urbit.org/docs/hoon/reference/rune/tis#-tisket) is similarly used to change a leg in the tail of the subject then evaluate against it.  This is commonly used for sequential calls to `++og`, the random number generator, and for events that need to be ordered in their resolution e.g. with a `%=` cenhep.  (Used in agents frequently.)
- [`=*` tistar](https://urbit.org/docs/hoon/reference/rune/tis#tistar) defers an expression (rather like a macro).
- [`;<` micgal](https://urbit.org/docs/hoon/reference/rune/mic#-micgal) sequences two computations, particularly for an asynchronous event like a remote system call.  (Used in threads.)
- [`;~` micsig](https://urbit.org/docs/hoon/reference/rune/mic#-micsig) produces a pipeline, a way of piping the output of one gate into another in a chain.  (This is particularly helpful when parsing text.)

### Example:  Bank Account as a Door

This door essentially replaces the sample of the door with new values as each transaction proceeds.

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

- Commentary at [“1.8.1 Bank Account”](https://urbit.org/docs/hoon/hoon-school/bank-account)

### Example:  Random Numbers (`=^` tisket)

A given seed will produce the same result every time it is run.  We need to use `eny` to seed it non-deterministically, but we can also pin the state using `=^` tisket.

```hoon
> =+  rng=~(. og eny)  [-:(rads:rng 100) -:(rads:rng 100)]  
[60 60]

> =+  rng=~(. og eny)
  =^  r1  rng  (rads:rng 100)
  =^  r2  rng  (rads:rng 100)
  [r1 r2]
[21 47]
```

### Example:  Traffic Light (`=.` tisdot)

From the now-defunct Hoon Workbook:

```hoon
:-  %say
|=  *
:-  %noun
=+  |%
    ++  state  ?(%red %yellow %green)
    --
=/  current-state=state  %red
=+  ^=  traffic-light
    |%
    ++  look  current-state
    ++  set
      |=  s=state
      +>.$(current-state s)
    --
=+  a=traffic-light
=+  b=traffic-light
=.  a  (set.a %yellow)
[current-state.a current-state.b]
```

Generator boilerplate:

```hoon
:-  %say
|=  *
:-  %noun
```

Pin a core with the state.  Having new types in a separate core is a common idiom in Hoon programs that allows the compiler to do [constant folding](https://en.wikipedia.org/wiki/Constant_folding), which improves performance.

```hoon
=+  |%
    ++  state  ?(%red %yellow %green)
    --
```

```hoon
=/  current-state=state  %red
=+  ^=  traffic-light
    |%
    ++  look  current-state
    ++  set
      |=  s=state
      +>.$(current-state s)
    --
=+  a=traffic-light
=+  b=traffic-light
=.  a  (set.a %yellow)
[current-state.a current-state.b]
```


https://web.archive.org/web/20210315032448/https://urbit.org/docs/tutorials/hoon/workbook/traffic-light/

### Example:  Parsing `tape`s (`;~` micsig)

We need to build a tool to accept a `tape` containing some characters, then turn it into—something else, something computational.

For instance, a calculator could accept an input like `3+4` and return `7`.  A command-line interface may look for a program to evaluate (like Bash and `ls`).  A search bar may apply logic to the query (like Google and `-` for `NOT`).

The basic problem is this:

1. You need to accept a `tape` containing some characters.
2. You need to ingest one or more characters and decide what they “mean”, including storing the result of this meaning.
3. You need to loop back to #1 again and again until you are out of characters.

We could build a simple parser out of a trap and `++snag`, but it would be brittle and difficult to extend.  The Hoon parser is very sophisticated, since it has to take a file of ASCII characters (and some UTF-8 strings) and turn it into Nock code.  What makes parsing challenging is that we have to wade directly into a sea of new types and processes.  To wit:

-   A `tape` is the string to be parsed.
-   A `hair` is the position in the text the parser is at, as a cell of column & line, `[p=@ud q=@ud]`.
-   A `nail` is parser input, a cell of `hair` and `tape`.
-   An `edge` is parser output, a cell of `hair` and a `unit` of `hair` and `nail`.  (There are some subtleties around failure-to-parse here that we'll defer a moment.)
-   A `rule` is a parser, a gate which applies a `nail` to yield an `edge`.

Basically, one uses a `rule` on `[hair tape]` to yield an `edge`.

A substantial swath of the standard library is built around parsing for various scenarios, and there's a lot to know to effectively use these tools.  **If you can parse arbitrary input using Hoon after this lesson, you're in fantastic shape for building things later.**  It's worth spending extra effort to understand how these programs work.

- [Hoon Guide, “Parsing”](https://urbit.org/docs/hoon/guides/parsing)

### Scanning Through a `tape`

[`++scan`](https://urbit.org/docs/hoon/reference/stdlib/4g#scan) parses a `tape` or crashes, simple enough.  It will be our workhorse.  All we really need to know in order to use it is how to build a `rule`.

Here we will preview using `++shim` to match characters with in a given range, here lower-case.  If you change the character range, e.g. putting `' '` in the `++shim` will span from ASCII `32`, `' '` to ASCII `122`, `'z'`.

```hoon
> `(list)`(scan "after" (star (shim 'a' 'z')))  
~[97 102 116 101 114]  

> `(list)`(scan "after the" (star (shim 'a' 'z')))  
{1 6}  
syntax error  
dojo: hoon expression failed
```

### `rule` Building

The `rule`-building system is vast and often requires various components together to achieve the desired effect.

#### `rule`s to parse fixed strings

- [`++just`](https://urbit.org/docs/hoon/reference/stdlib/4f/#just) takes in a single `char` and produces a `rule` that attempts to match that `char` to the first character in the `tape` of the input `nail`.

    ```hoon
    > ((just 'a') [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ [p='a' q=[p=[p=1 q=2] q="bc"]]]]
    ```

- [`++jest`](https://urbit.org/docs/hoon/reference/stdlib/4f/#jest) matches a `cord`.  It takes an input `cord` and produces a `rule` that attempts to match that `cord` against the beginning of the input.

    ```hoon
    > ((jest 'abc') [[1 1] "abc"])
    [p=[p=1 q=4] q=[~ [p='abc' q=[p=[p=1 q=4] q=""]]]]

    > ((jest 'abc') [[1 1] "abcabc"])
    [p=[p=1 q=4] q=[~ [p='abc' q=[p=[p=1 q=4] q="abc"]]]]
    
    > ((jest 'abc') [[1 1] "abcdef"])
    [p=[p=1 q=4] q=[~ [p='abc' q=[p=[p=1 q=4] q="def"]]]]
    ```

    (Keep an eye on the structure of the return `edge` there.)

- [`++shim`](https://urbit.org/docs/hoon/reference/stdlib/4f/#shim) parses characters within a given range. It takes in two atoms and returns a `rule`.

    ```hoon
    > ((shim 'a' 'z') [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ [p='a' q=[p=[p=1 q=2] q="bc"]]]]
    ```

- [`++next`](https://urbit.org/docs/hoon/reference/stdlib/4f/#next) is a simple `rule` that takes in the next character and returns it as the parsing result.

    ```hoon
    > (next [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ [p='a' q=[p=[p=1 q=2] q="bc"]]]]
    ```

#### `rule`s to parse flexible strings

So far we can only parse one character at a time, which isn't much better than just using `++snag` in a trap.

```hoon
> (scan "a" (shim 'a' 'z'))  
'a'  

> (scan "ab" (shim 'a' 'z'))  
{1 2}  
syntax error  
dojo: hoon expression failed
```

How do we parse multiple characters in order to break things up sensibly?

- [`++star`](https://urbit.org/docs/hoon/reference/stdlib/4f#star) will match a multi-character list of values.

    ```hoon
    > (scan "a" (just 'a'))
    'a'

    > (scan "aaaaa" (just 'a'))
    ! {1 2}
    ! 'syntax-error'
    ! exit

    > (scan "aaaaa" (star (just 'a')))
    "aaaaa"
    ```

- [`++plug`](https://urbit.org/docs/hoon/reference/stdlib/4e/#plug) takes the `nail` in the `edge` produced by one rule and passes it to the next `rule`, forming a cell of the results as it proceeds.

    ```hoon
    > (scan "starship" ;~(plug (jest 'star') (jest 'ship')))
    ['star' 'ship']
    ```

- [`++pose`](https://urbit.org/docs/hoon/reference/stdlib/4e/#pose) tries each `rule` you hand it successively until it finds one that works.

    ```hoon
    > (scan "a" ;~(pose (just 'a') (just 'b')))
    'a'
    
    > (scan "b" ;~(pose (just 'a') (just 'b')))
    'b'
    
    > (;~(pose (just 'a') (just 'b')) [1 1] "ab")  
    [p=[p=1 q=2] q=[~ u=[p='a' q=[p=[p=1 q=2] q=[i='b' t=""]]]]]
    ```

- [`++glue`](https://urbit.org/docs/hoon/reference/stdlib/4e/#glue) parses a delimiter in between each `rule` and forms a cell of the results of each `rule`.  Delimiter names hew to the aural ASCII pronunciation of symbols, plus `prn` for printable characters and

    ```hoon
    > (scan "a b" ;~((glue ace) (just 'a') (just 'b')))  
    ['a' 'b']

    > (scan "a,b" ;~((glue com) (just 'a') (just 'b')))
    ['a' 'b']
    
    > (scan "a,b,a" ;~((glue com) (just 'a') (just 'b')))
    {1 4}
    syntax error
    
    > (scan "a,b,a" ;~((glue com) (just 'a') (just 'b') (just 'a')))
    ['a' 'b' 'a']
    ```

- The [`;~` micsig](https://urbit.org/docs/hoon/reference/rune/mic/#-micsig) will create `;~(combinator (list rule))` to use multiple `rule`s.

    ```hoon
    > (scan "after the" ;~((glue ace) (star (shim 'a' 'z')) (star (shim 'a' 'z'))))  
    [[i='a' t=<|f t e r|>] [i='t' t=<|h e|>]
    
    > (;~(pose (just 'a') (just 'b')) [1 1] "ab")  
    [p=[p=1 q=2] q=[~ u=[p='a' q=[p=[p=1 q=2] q=[i='b' t=""]]]]]
    ```

At this point we have two problems:  we are just getting raw `@t` atoms back, and we can't iteratively process arbitrarily long strings.  `++cook` will help us with the first of these:

- [`++cook`](https://urbit.org/docs/hoon/reference/stdlib/4f/#cook) will take a `rule` and a gate to apply to the successful parse.

    ```hoon
    > ((cook ,@ud (just 'a')) [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ u=[p=97 q=[p=[p=1 q=2] q="bc"]]]]

    > ((cook ,@tas (just 'a')) [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ u=[p=%a q=[p=[p=1 q=2] q="bc"]]]]

    > ((cook |=(a=@ +(a)) (just 'a')) [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ u=[p=98 q=[p=[p=1 q=2] q="bc"]]]]

    > ((cook |=(a=@ `@t`+(a)) (just 'a')) [[1 1] "abc"])
    [p=[p=1 q=2] q=[~ u=[p='b' q=[p=[p=1 q=2] q="bc"]]]]
    ```

However, to parse iteratively, we need to use the [`++knee`]() function, which takes a noun as the bunt of the type the `rule` produces, and produces a `rule` that recurses properly.  (You'll probably want to treat this as a recipe for now and just copy it when necessary.)

```hoon
|-(;~(plug prn ;~(pose (knee *tape |.(^$)) (easy ~))))
```

There is an example of a calculator [in the docs](https://urbit.org/docs/hoon/guides/parsing#recursive-parsers) that's worth a read.  It uses `++knee` to scan in a set of numbers at a time.

```hoon
|=  math=tape
|^  (scan math expr)
++  factor
  %+  knee  *@ud
  |.  ~+
  ;~  pose
    dem
    (ifix [pal par] expr)
  ==
++  term
  %+  knee  *@ud
  |.  ~+
  ;~  pose
    ((slug mul) tar ;~(pose factor term))
    ((slug pow) ket ;~(pose term expr))
    factor
  ==
++  expr
  %+  knee  *@ud
  |.  ~+
  ;~  pose
    ((slug add) lus ;~(pose term expr))
    term
  ==
--
```

#### Example:  Parse a String of Numbers

A simple `++shim`-based parser:

```hoon
> (scan "1234567890" (star (shim '0' '9')))  
[i='1' t=<|2 3 4 5 6 7 8 9 0|>]
```

A refined `++cook`/`++cury`/`++jest` parser:

```hoon
> ((cook (cury slaw %ud) (jest '1')) [[1 1] "123"])  
[p=[p=1 q=2] q=[~ u=[p=[~ 1] q=[p=[p=1 q=2] q="23"]]]]  

> ((cook (cury slaw %ud) (jest '12')) [[1 1] "123"])  
[p=[p=1 q=3] q=[~ u=[p=[~ 12] q=[p=[p=1 q=3] q="3"]]]]
```


##  `%ask` Generators

We use an `%ask` generator when we want to create an interactive program that prompts for inputs as it runs, rather than expecting arguments to be passed in at the time of initiation.

Once you can parse input as above, then you can start to produce some fun CLI agents.  (I'd love to see Zork-on-Mars someday!)

If you are interested in producing command-line-based tools, look into the `%shoe` and `%sole` libraries.

- [Hoon Guide, “CLI apps”](https://urbit.org/docs/hoon/guides/cli-tutorial)
- [`~wicdev-wisryt`, “Input and Output in Hoon”](https://urbit.org/blog/io-in-hoon)
