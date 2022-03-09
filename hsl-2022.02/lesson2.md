---
title: "Hoon Conventions"
teaching: 45
exercises: 15
nodes:
- "115"
- "120"
- "125"
- "175"
objectives:
- "Identify current known irregular syntax."
- "Convert between regular and irregular forms of runes to date."
- "Identify a mold in the hierarchy of Urbit types (nouns, molds, marks)."
- "Understand how type inference and type checking takes place."
- "Bunt a mold."
- "Identify type using `!>`."
- "Annotate Hoon code with comments."
- "Produce a generator to convert a value between auras."
- "Employ a gate to defer a computation."
- "Produce a gate as a generator."
- "Build code samples with `-build-file` thread."
- "Discuss Ford import runes."
runes:
- "`^+`"
- "`^*`"
- "`$?`"
- "`$:`"
- "`!>`"
- "`|=`"
- "`::`"
- "`!!`"
- "`/+`"
keypoints:
- "Many runes have irregular syntax, called “sugar syntax”.  This makes it easier to write aesthetically communicative Hoon code."
- "Molds define Hoon structures.  They have a default value (“bunt”) and are strictly statically typed (i.e. they must match)."
- "Find the type of a value using the `!>` zapgar rune."
- "Use comments (`::`) to explain the logic of any code you produce."
- "A gate (made with `|=` bartis) lets you store a computation for future use."
- "You can store a gate as a standalone reusable file called a generator."
- "You can build code from a file directly with `-build-file` or import its contents with `/+` from `/lib`."
---
#   Hoon Conventions
##  Hoon School Lesson 2

##  A Spoonful of Sugar

In Lesson 1, we rigorously adhered to the regular syntax of runes so that you could get used to using them.  In fact, the only two irregular forms we used were these:

- Cell definition `[a b]` which represents the `:-` colhep rune, `:-  a  b`
- Aura application ``@ux`500`` which represents a double `^-` kethep, `^-  @ux  ^-  @  500`.  (Why two `^-`s?)

Hoon developers often employ irregular forms, sometimes called “sugar syntax”.  Besides the `:-` colhep and `^-` kethep forms, we will commonly use a new form for `%-` cenhep “function calls”:

```
%-  add  [1 2]
(add 1 2)
```

You should get used to reading and interpreting these forms and we will start to use them actively during this lesson.

> ### Converting Between Forms
>
> Convert each of the following irregular forms into the correct regular runic syntax.
>
> 1. `(add 1 2)`
> 2. ``@ub`16`
> 3. `[%lorem %ipsum]`
> 4. `[%lorem %ipsum %dolor]` (can do two ways)
>
> Convert each of the following regular forms into the correct irregular syntax.
>
> 1. :-  %lemon  %jello
> 2. %-  pow  :-  2  16
> 3. ^-  @p  ^-  @  256
{: .challenge}


##  Deferring Computations

So far, every time we have calculated something, we have had to build it from scratch in Dojo.  This is completely untenable for nontrivial calculations, and clearly the Urbit OS itself is built on persistent files defining its behavior.

Hoon uses _gates_ as deferred computations.  What this means is that we can build a Hoon expression now and use it at will later on, perhaps many times.  More than that, we can also use it on different data values.  A gate is the Hoon analogue of a function or subroutine in other programming languages.

Structurally, a gate is a [`|=` bartis](https://urbit.org/docs/hoon/reference/rune/bar#-bartis) rune with two children:  a `spec` (specification of input) and a `hoon` (body). 

```
::  Confirm whether a value is greater than one.
|=  a=@ud
?:  (gth a 1)
  %.n
%.y
```

Compare this to other programming languages, if you know any:
- Does it have a name?
- Does it have a return value?

Beyond those, what is the purpose of each line?

The [`spec`](https://urbit.org/docs/hoon/reference/stdlib/4o#spec) gives the type as a mold and attaches a face to it for use in the gate.

The body evaluates and returns its result, ultimately to the call site.

The input value, what is included in the `spec`, is sometimes called the argument or parameter in mathematics and other programming languages.  It's basically the input value.  Hoon prefers to call it the _sample_.

Gates use enforce the type of incoming and outgoing values.  In other words, a `spec` is a kind of type which is fixing the possible noun inputs.  (See “Molds” below.)

Gates can take multiple arguments as a cell:

```
::  Return which of two numbers is larger.
|=  [a=@ud b=@ud]
?:  (gth a b)
  a
b
```

You can also call them different ways with raw [`%` cen](https://urbit.org/docs/hoon/reference/rune/cen) runes:

```
%-  max  [100 200]
%+  max  100  200
```

Remember `^-` kethep?  We will use `^-` as a _fence_, a way of making sure only data matching the appropriate structure get passed on.

```
::  Confirm whether a value is greater than one.
|=  a=@ud
^-  @ud
?:  (gth a 1)
  %.n
%.y
```

*This is the correct way to define a gate.*  Frequent annotation of type with `^-` kethep fences is essential to producing good Hoon code.

In technical language, we describe Hoon as a _statically typed_ language.  This means that it enforces type constraints on all values very aggressively.  If you are used to a dynamic language like Python or Ruby, this will seem very restrictive at first.  The flip side is that once your code compiles correctly, you will often find that it is very much along the way towards being a working correct product.


##  Mold Essentials

- "Identify current known irregular syntax."
- "Convert between regular and irregular forms of runes to date."
- "Identify a mold in the hierarchy of Urbit types (nouns, molds, marks)."
- "Understand how type inference and type checking takes place."
- "Bunt a mold."
- "Identify type using `!>`."

Programming languages use data types to distinguish different kinds of data and associated rules.  For instance, what does it mean to add 3 to the letter A?  Depending on your programming language, you could see `A3`, `D`, or an error.

A _type_ is really a rule for interpretation.  But for our Hoonish purposes, it's rather too broad a notion and we need to clarify some different kinds of things we could refer to as “type”.  It is instructive for us to distinguish three kinds of types in Hoon:

1. Atoms:  values with auras.
2. Molds:  structures.  Think of cells, lists, sets, and arrays.
3. Marks:  file types.  Compare to conventional files distinguished by extension and definite internal structure.

To re-employ the chemical metaphor, an atom is an atom; a cell is a molecule; a mold is an ideal molecule, a definition or structural representation; a mark is like a protein, a more complex transformation rule.

Trivial types you have seen and worked with.  Marks we will leave until a later discussion of Gall agents or Clay, which use marks to type filesystem data.  For now, we focus on molds.

We commonly need to do one of two things with a mold:

1. Validate the shape of a noun (“clam”).
2. Produce an example value (“bunt”).

We often use bunts to clam, e.g.,

```
^-  @ud
```

uses the `@ud` default value (`0`) as the type specimen which the computation must match.

To _actually_ get the bunt value, use the [`^*` kettar](https://urbit.org/docs/hoon/reference/rune/ket#kettar) rune, almost always used in its irregular form `*`:

```
^*  @ud
^*  @da
*@da
*[@ud @ux @ub]
```

One more way to validate against type is to use an example instead of the extracted mold.  This uses [`^+` ketlus](https://urbit.org/docs/hoon/reference/rune/ket#ketlus) similarly to how we used `^-` ketlus previously:

```
^+  1.000  100
```

(This is what `^-` is actually doing:  `6-  p  q` reduces to `^+  ^*  p  q`.  Many runes we use actually reduce to other rune forms, and have been introduced for ease of use.)

Technically, we can say that a mold is a function from a noun to a noun.  What this means is that we can use a mold to map any noun to a typed value—if this fails, then the mold crashes.

We can use more complex structures for molds though, including built-in types like `list`s and `tape`s:

```
`(list @)`[104 101 108 108 111 32 77 97 114 115 33 ~]
`tape``(list @)`[104 101 108 108 111 32 77 97 114 115 33 ~]

`(list @)`[144 57 195 46 200 165 186 88 118 99 ~]
`(list @p)``(list @)`[144 57 195 46 200 165 186 88 118 99 ~]
```

(Sometimes you see a `%bad-text` when using `tape`s, which means that you've tried to convert a number into text which isn't text.  More on `tape`s in Lesson 4.)

-   Why does this mold conversion fail?

     ```
     `(list @ux)`[1 2 3 ~]
     ```

    What do we need to do in order to make it succeed?

We can have more complex molds as well:

```
::  [[from-ship to-ship] points]
[[@p @p] @ud]
```

Most of the time, we will define such complex types using specific runes and “mold builder” tools.

### Identifying Molds

The quick way to figure out which mold the Hoon compiler thinks something is (and definitionally is, I suppose) is to use the [`!>` zapgar](https://urbit.org/docs/hoon/reference/rune/zap#-zapgar) rune.

```
!>  0xace2.bead
```

For reasons which will be elaborated in Lesson 3, this is often employed as the so-called “type spear”:

```
-:!>(0xace2.bead)
```

### Mold Runes

At this point, we really need to know about only two mold runes:

1.  [`$?` bucwut](https://urbit.org/docs/hoon/reference/rune/buc#-bucwut), which forms a type union.

    For instance, if you wanted a gate to return one of an unsigned aura type, but no other type, you could define a type union thus:
    
    ```
    $?  [@ud @ux @ub ~]
    ```
    
    and use it in a gate:
    
    ```
    |=  [n=$?(@ud @ux @ub)]
    (add n 1)
    ```
    
    ```
    > (foo 4)  
    5  
    > (foo 0x5)  
    6  
    > (foo 0b110)  
    7  
    > (foo ~zod)  
    -need.?(@ub @ud @ux)  
    -have.@p  
    nest-fail  
    dojo: hoon expression failed
    ```

    The irregular form of `%?` bucwut looks like this:
    
    ```
    ?(@ud @ux @ub)
    ```
    
    Type unions are mainly helpful when you need to match something that can have multiple options.

2. [`$:` buccol](https://urbit.org/docs/hoon/reference/rune/buc#-buccol), which forms a named tuple.

    We don't need to do a lot with these directly, unless we want to build a special type like a vector (e.g. with two components like an _x_ and a _y_).
    
    But these are what is actually going on inside of gate definitions:
    
    ```
    |=  data=$:(ship=@p money=@ud)
    ^-  $:(ship=@p money=@ud)
    [(add ship.data 1) (add money.data 100)]
    ```
    
    (A bit contrived, but we're still quite limited by what we know of Hoon.  We'll get more comfortable with using molds in Lesson 3.)


##  Building Code

The missing piece to really tie all of this together is the ability to store a gate and use it at a later time, not just in the same long Dojo session.  Enter the _generator_.

A generator is a simple program which can be called from the Dojo.  It is a gate, so it takes some input as sample and produces some result.  Naked generators are the simplest generators possible, having access only to information passed to them directly in their sample.

In this module, we will compose our first generator.

### The Gate

```
::  Square a number.
|=  a=@ud
^-  @ud
%+  mul
  a
a
```

(Any time you write code to use later, you should include some comments to explain what the code does and perhaps how it does that.)

### The Process

1. Open a text editor.
2. Copy the gate above into the text editor.  (Double-check that two-space gaps are still gaps; some text editors chew them up into single-space aces.)
3. Save the gate as `square.hoon` in the `base/gen` folder of your fakeship.
4. In the Dojo, `|commit %base`.  _You should see a message indicating that the file has been loaded._
5. Run the generator with `+square 5`.

Any generator can be run the same way, beginning with the `+` lus character and followed by the name of a file in the `base/gen` directory.

> ## Triangular Function
> 
> In `%hw1`, you implement the triangular function.
> 
> ![](https://lh4.googleusercontent.com/zdauTDEWvhhOkFEb6VcDEJ4SITsHOgcStf4NYFQSIVjTDPjaCqYGdin9TDCCeTG3OyMrUUdq-JtViiu_c9wuojim_mHpV6-DoTNwZzYz5_6qVVvN5fc3hEuSna2GwY15RQ=w740)
> 
> Take your code from that, turn it into a gate, and save it as a generator `tri.hoon`.
{: .challenge}

If you need to test code without completing it, you can stub out as-yet-undefined arms with the [`!!` zapzap](https://urbit.org/docs/hoon/reference/rune/zap#-zapzap) crash rune.  `!!` is the only rune which has no children, and it's helpful when you need something to satisfy Hoon syntax but aren't ready to flesh out the program yet.

### Building Code Generally

A generator gives us on-demand access to code, but it is helpful to load and use code from files while we work in the Dojo.

A conventional library import with [`/+` faslus](https://urbit.org/docs/arvo/ford/ford#ford-runes) will work in a generator or another file, but won't work in Dojo, so you can't use `/+` faslus interactively.

Instead, you need to use the `-build-file` thread to load the code.  Most commonly, you will do this with library code when you need a particular gate's functionality.

`-build-file` accepts a file path and returns the built operational code.  For instance:

```hoon
> =ntw -build-file %/lib/number-to-words/hoon
> one-hundred:numbers:ntw  
100
> (to-words:eng-us:numbers:ntw 19)
[~ "nineteen"]
```

There are also a number of other import runes which make library, structure, and mark code available to you.  For now, the only one you need to worry about is `/+` faslus.

For simplicity, everything we do will take place on the `%base` desk for now.  We will learn how to create a library in a subsequent lesson.

> ### Loading a Library
>
> In a generator, load the `number-to-words` library using the
> `/+` tislus rune.  (This must take place at the very top of
> your file.)
> 
> Use this to produce a gate which accepts an unsigned decimal
> integer and returns the text interpretation of its increment.
{: .challenge}

