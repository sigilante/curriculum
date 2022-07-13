---
title: "Hoon Syntax"
teaching: 45
exercises: 15
nodes:
- "110"
- "113"
objectives:
- "Distinguish nouns, cells, and atoms."
- "Apply auras to transform an atom."
- "Identify common Hoon molds, such as cells, lists, and tapes."
- "Pin a face to the subject."
- "Make a decision at a branch point."
- "Distinguish loobean from boolean operations."
- "Slam a gate (call a function)."
runes:
- "`::`"
- "`%-`"
- "`:-`"
- "`=/`"
- "`?:`"
- "`^-`"
keypoints:
- "A noun is an atom or a cell.  A noun is an unsigned integer.  A cell is a pair of two nouns."
- "An aura is a metadata “interpretation” of an atom."
- "Functional expressions always result in a value."
- "You preserve a value with a name (“face”) in Hoon using a `=/` tisfas rune."
- "You make a decision between alternatives in Hoon using a `?:` wutcol rune."
- "You can use existing code (“gates” = “functions”) in Hoon using a `%-` cenhep."
---

#   Hoon Syntax
##  Hoon School Lesson 1

##  Self-Introduction & Teaching Philosophy

I want the materials we present to you to be as transparent as possible, without confusing anyone.  (I do commit to not telling you anything inaccurate.  This may lead to odd phrasing.)

![](https://i.dailymail.co.uk/i/pix/2015/02/02/2541F2DB00000578-0-This_Holden_utility_was_seized_by_police_for_Hooning_in_Tennant_-a-24_1422867990080.jpg)

#   Hoon Syntax

It's important to get to writing code fast.  Open a fakeship Dojo, type

```
%-  add  [5 6]
```

and press `Return`.  (Note that there are _two_ spaces between some components, and that if you attempt to write without both spaces, the Dojo prompt will not let you type.)

The operation you just completed is straightforward enough:  `5 + 6`, in many languages, or `(+ 5 6)` in a Lisp like Clojure.  If we want to know why things look the way they do in Hoon, we need to step back to talk about why the system needs the Hoon representation at all.


##  Why Hoon?

The Urbit operating system hews to a conceptual model wherein each expression takes place in a certain context (the “subject”).  While sharing a lot of practicality with other programming paradigms and platforms, Urbit's model is mathematically well-defined and unambiguously specified.

At its root, Urbit is completely specified by [Nock](https://urbit.org/docs/nock/definition), sort of a machine language for the Urbit virtual machine layer and event log.  However, Nock code is basically unreadable (and unwriteable) for a human.  [One worked example](https://urbit.org/docs/nock/example) yields, for decrementing a value by one, the Nock formula:

```
[8 [1 0] 8 [1 6 [5 [0 7] 4 0 6] [0 6] 9 2 [0 2] [4 0 6] 0 7] 9 2 0 1]
```

This is like reading binary machine code:  perhaps a silicon engineer needs to know this, but we mortals need a clearer vernacular.

Hoon serves as Urbit's practical programming language.  Everything in Urbit OS is written in Hoon, and many of the ancillary tools as well.  

Any operation in Urbit ultimately results in a value.  Much like machine language designates any value as a command, an address, or a number, a Hoon value is interpreted per the Nock rules and results in a basic data value at the end.  So what are our data values in Hoon?  How does it _work_?

-   [Ted Blackman ~rovnys-ricfer, “Why Hoon?”](https://urbit.org/blog/why-hoon/)


##  Nouns and Verbs

Think about a child persistently asking you what a thing is made of.  At first, you may respond, "plastic", or "metal".  Eventually, the child may wear you down to a more fundamental level:  atoms and molecules.

In a very similar sense, everything in a Hoon program is an atom or a molecule.  A Hoon program is a complex molecule, a digital chemistry that describes one mathematical representation of data caught in a crystal.

The most general data category in Hoon is a _noun_.  This is just about as broad as saying “thing”, so let's be more specific:

> A noun is an atom or a cell.

Progress?  We can say, in plain English, that

- An _atom_ is a nonzero integer number (0–∞).
- A _cell_ is a pair of two nouns.  (In our chemical metaphor, a cell is a molecule!)

_Everything_ in Hoon (and Nock, and Urbit) is a noun.  The Urbit OS itself is a noun.  So given any noun, the Urbit VM simply applies the Nock rules to change the noun in well-defined mechanical ways.

> Back to the Dojo!  Enter both of the following:
>
> ```
> 729
> [1 2]
> ```
>
> the first being an atom, the second being a cell.  All cells and atoms (and hence all nouns) have the same structure and display even if they are much more complicated than these.
{: .challenge}

### Atoms

If an atom is a nonzero number, how do we represent anything else?  Hoon provides an “aura” or tag which lets you treat a number as text, time, date, Urbit address, IP address, and much more.

An aura always begins with `@` pat, which denotes an atom (as opposed to a cell, `^` ket).  The next letter or letters tells you what kind of representation you want the value to have.

For instance, to change the representation of a regular decimal number like `32` to a binary representation (i.e. for 2⁵), use `@ub`:

```
> `@ub`32
0b10.0000
```

(The tic marks are a shorthand which we'll explain later.)

While there are dozens of auras for specialized applications, here are the most important ones for you to know:

| Aura | Meaning | Example | Comment |
| ---- | ------- | ------- | ------- |
| `@`  | Empty aura | `100` | (displays as `@ud`) |
| `@da` | Date (absolute) | ~2022.2.8..16.48.20..b53a | Epoch calculated from 292 billion B.C. |
| `@p` | Ship name | `~zod` |  |
| `@rs` | Number with fractional part | `.3.1415` | Note the preceding `.` dot. |
| `@t` | Text (“cord”) | `'hello'` | One of Urbit's several text types; only UTF-8 values are valid. |
| `@ub` | Binary value | `0b1100.0101` |  |
| `@ud` | Decimal value | `100.000` | Note that German-style thousands separator is used, `.` dot. |
| `@ux` | Hexadecimal value | `0x1f.3c4b` |  |

(In our chemical metaphor, these are rather like different elements.  Unlike chemical elements, however, these are completely interconvertible.)

Hearkening back to our discussion of interchangeable representations in Lesson -1, you can see that these are all different-but-equivalent ways of representing the same underlying data values.

The `^-` kethep rune is useful for ensuring that everything in the second child matches the type (aura) of the first, e.g.

```
^-  @ux  0x1ab4
```

We will use `^-` kethep extensively to enforce type constraints, a very useful tool in Hoon code.

> Convert between some of these at the command line, e.g.:
>
> ```
> > `@p`100  
> ~syr  
> > `@p`0b1100.0101  
> ~luc  
> > `@x`0b1100.0101  
> 0xc5  
> > `@ud`0b1100.0101  
> 197
> ```
> 
> (You may see an error particular with `@t`, due to some binary sequences being valid UTF-8 text and others not.)
{: .challenge}

### Cells

A cell is a pair of two nouns.  Cells are traditionally written using square brackets:  `[]`.  For now, just recall the square brackets and that cells are always _pairs_ of values.

```
[1 2]
[@p @t]
[[1 2] [3 4]]
```

This is actually a shorthand for a rune as well:

```
:-  1  2
```

produces a cell `[1 2]`.  You can chain these together:

```
:-  1  :-  2  3
```

to produce `[1 [2 3]]` or `[1 2 3]`.

We deal with cells in more detail below.

> ### Hoon as Noun
> 
> We mentioned earlier that everything in Urbit is a noun, including the program itself.  This is true, but getting from the rune expression in Hoon to the numeric expression requires a few more tools than we currently are prepared to introduce.
> 
> For now, you can preview the structure of the Urbit OS as a noun by typing `.` dot at the Dojo prompt.  This displays a summary of the structure of the operating function itself as a noun.
{: .callout}


##  The Phylum _Chordata_

The backbone of any Hoon expression is a scaffolding of _runes_, which are essentially mathematical relationships between daughter components.  If nouns are nouns, then runes are verbs:  they describe what nouns do.

For instance, when we called a function earlier (or, in Hoon parlance, _slammed a gate_), we needed to provide the [`%-` cenhep](https://urbit.org/docs/hoon/reference/rune/cen#-cenhep) rune with two bits of information, a function name and the values to associate with it:

```
%-
  add
  [1 2]
```

`++add` expects precisely two values (or _arguments_), which are provided by `%-` in the neighboring child expression.  There's really no limit to the complexity of Hoon expressions:  they can track deep and wide.  They also don't care much about layout, which leaves you a lot of latitude.  The only hard-and-fast rule is that there are single spaces (_ace_) and everything else (_gap_).

```
%-
  add
  [%-(add [1 2]) 3]
```

(Notice that inside of the `[]` cell notation we are using a slightly different form of the `%-` rune call.  In general, there are several ways to use many runes, and we will introduce these gradually.)

(While this requirement is rather stiff, we'll see more expressive ways to write Hoon code after you're comfortable using runes.)

For instance, here are some of the standard library functions which have a similar architecture:

- [`++add`](https://urbit.org/docs/hoon/reference/stdlib/1a#add) (addition)
- [`++sub`](https://urbit.org/docs/hoon/reference/stdlib/1a#sub) (subtraction, positive results only—what happens if you subtract past zero?)
- [`++mul`](https://urbit.org/docs/hoon/reference/stdlib/1a#mul) (multiplication)
- [`++div`](https://urbit.org/docs/hoon/reference/stdlib/1a#div) (integer division, no remainder)
- [`++pow`](https://urbit.org/docs/hoon/reference/stdlib/1a#pow) (power or exponentiation)
- [`++mod`](https://urbit.org/docs/hoon/reference/stdlib/1a#add) (modulus, remainder after integer division)
- [`++dvr`](https://urbit.org/docs/hoon/reference/stdlib/1a#dvr) (integer division with remainder)
- [`++max`](https://urbit.org/docs/hoon/reference/stdlib/1a#max) (maximum of two numbers)
- [`++min`](https://urbit.org/docs/hoon/reference/stdlib/1a#min) (minimum of two numbers)


> ### Writing Incorrect Code
>
> At the Dojo, you can attempt to operate using the wrong values; for instance, `++add` doesn't know how to add three numbers at the same time.
>
> ```
> > %-  
>  add  
>  [1 2 3]  
> -need.@  
> -have.[@ud @ud]  
> nest-fail  
> dojo: hoon expression failed
> ```
>
> So this statement above is _syntactically_ correct (for the `%-` rune) but in practice fails because the expected input arguments don't match.  Any time you see a `need`/`have` pair, this is what it means.
{: .callout}

Any Hoon program is architected around runes.  If you have used another programming language, you can see these as analogous to keywords, although they also make explicit what most language syntax parsers leave implicit.  Hoon aims at a parsimony of representation while leaving latitude for aesthetics.  In other words, Hoon strives to give you a unique characteristic way of writing a correct expression, but it leaves you flexibility in how you lay out the components to maximize readability.

We are only going to introduce a handful of runes in this lesson, but by the time we're done you'll know the twenty or twenty-five runes that yield 80% of the capability.

> ### Identifying Unknown Runes
>
> Here is a (lightly-edited) snippet of Hoon code from the OS itself.  Anything written after a `::` colcol is a _comment_ and is ignored by the computer.  (Comments are useful for human-language explanations.)
> 
> ```
> %-  send
> ::  forwards compatibility with next-dill
> ?@  p.kyz  [%txt p.kyz ~]
> ?:  ?=  %hit  -.p.kyz
>   [%txt ~]
> ?.  ?=  %mod  -.p.kyz
>   p.kyz
> =/  =@c
>   ?@  key.p.kyz  key.p.kyz
>     ?:  ?=  ?(%bac %del %ret)  -.key.p.kyz 
>       `@`-.key.p.kyz
>     ~-
> ?:  ?=  %met  mod.p.kyz  [%met c]  [%ctl c]
> ```
> 
> 1. Mark each rune.
> 2. For each rune, find its corresponding children.  (You don't need to know what a rune does to identify how things slot together.)
> 3. Consider these questions:
>     - Is every pair of punctuation marks a rune?
>     - How can you tell a rune from other kinds of marks?
> 
> One clue:  every rune in Hoon (except for one, not in the above code) has _at least one child_.
{: .challenge}

> ### Inferring Rune Behavior
>
> Here is a snippet of Hoon code from the OS itself.
> 
> ```
> =.  moz
> %+  weld  moz
> ^-  list
> :~  [hen %lsip %e %init ~]
>     [hen %lsip %d %init ~]
>     [hen %lsip %g %init ~]
>     [hen %lsip %c %init ~]
>     [hen %lsip %a %init ~]
> ==
> ```
> 
> What does the `==` tistis do for the `:~` colsig?
{: .challenge}


##  Preserving Values with Faces

Unlike many procedural programming languages, a Hoon expression only knows what it has been told.  This means that as soon as we calculate a value, it returns and falls back into the ether.

```
%-  sub  [5 1]
```

Right now, we don't have a way of preserving values for subsequent use in a more complicated Hoon expression.

We are going to store the value as a variable, or in Hoon, “pin a face to the subject”.

When we used `++add` or `++sub`, we basically wanted an immediate answer.  There's not much more to say than `5 + 1`.  In contrast, pinning a face accepts three daughter expressions:  a name (or face), a value, and the rest of the program.

```
=/  perfect-number  28
%-  add  [perfect-number 10]
```

Although it works quite well in long-form code, using this rune in the Dojo is little bit counter-intuitive because the assignment is not preserved in subsequent expressions. The Dojo offers a workaround to retain named values:

```
=perfect-number 28
%-  add  [perfect-number 10]
```

The difference is that the Dojo “pin” is permanent until deleted:

```
=perfect-number
```

rather than only effective for the daughter expressions of a `=/` tisfas rune.  (We also won't be able to use this Dojo pin in a regular Hoon program.)

> ### A Large Power of Two
>
> Create two numbers named `two` and `twenty`, with appropriate values, using the `=/` tisfas rune.
> 
> Then use these values to calculate 2²⁰ with `++pow` and `%-` cenhep.
{: .challenge}


##  Holding Things

Atoms are well and fine for relatively simple data, but we already know about cells as pairs of nouns.  How else can we think of collections of data?

### Cells

A cell is formally a pair of two objects, but as long as the second (right-hand) object is a cell, these can be written stacked together:

```
> [1 [2 3]]
[1 2 3]
> [1 [2 [3 4]]]
[1 2 3 4]
```

This convention keeps the notation from getting too cluttered.  For now, let's call this a “running cell” because it consists of several cells run together.

There's some subtlety to this, but mostly these read to the right, i.e. `[1 2 3]` is the same as `[1 [2 3]]`.

> Enter the following cells:
>
> ```
> [1 2 3]
> [1 [2 3]]
> [[1 2] 3]
> [[1 2 3]]
> [1 [2 [3]]]
> [[1 2] [3 4]]
> [[[1 2] [3 4]] [[5 6] [7 8]]]
> ```
{: .challenge}

Are they all the same?  We'll revisit cell structure in Lesson 3 and see why not.


### Lists

A running cell which terminates in a `~` atom is a list.

- What is `~`'s value?  Try casting it to another aura.

  `~` is the null value, and here acts as a list terminator.
  
Lists are ubiquitous in Hoon, and many specialized tools exist to work with them.  (For instance, to apply a gate to each value in a list, or to sum up the values in a list, etc.)
  
You can apply an aura to explicitly designate a null-terminated running cell as a list containing particular types of data.

```
> `(list @ud)`[1 2 3 ~]  
~[1 2 3]  
> `(list @ux)`[1 2 3 ~]  
mint-nice  
-need.?(%~ [i=@ux t=it(@ux)])  
-have.[@ud @ud @ud %~]  
nest-fail  
dojo: hoon expression failed  
> `(list @)`[1 2 3 ~]  
~[1 2 3]  
> `(list @ux)``(list @)`[1 2 3 ~]  
~[0x1 0x2 0x3]
```

### Text

There are two ways to represent text in Urbit:  cords (`@t` aura atoms) and tapes (lists of individual characters).

Why represent text?  What does that mean?  We have to have a way of distinguishing words that mean something to Hoon (like `list`) from words that mean something to a human or a process (like `'hello world'`).

Right now, all you need to know is that there are (at least) two valid ways to write text:

- `'with single quotes'` as a cord.
- `"with double quotes"` as a tape.

We will use these incidentally for now and explain their characteristics in Lesson 3.


##  Make a Decision

The final rune we will use today will allow us to select between two different Hoon expressions, like picking a fork in a road.  Any computational process requires the ability to distinguish options.  For this, we first require a basis for discrimination:  truthness (_not_ “truthiness”).

Essentially, we have to be able to decide whether or not some value or expression evaluates as `%.y` _true_ (in which case we will do one thing) or `%.n` _false_ (in which case we do another).  At this point, our basic expressions are always mathematical; later on we will check for existence, for equality of two values, etc.

- [`++gth`](https://urbit.org/docs/hoon/reference/stdlib/1a#gth) (greater than `>`)
- [`++lth`](https://urbit.org/docs/hoon/reference/stdlib/1a#lth) (less than `<`)
- [`++gte`](https://urbit.org/docs/hoon/reference/stdlib/1a#gte) (greater than or equal to `≥`)
- [`++lte`](https://urbit.org/docs/hoon/reference/stdlib/1a#lte) (less than or equal to `≤`)

If we supply these with a pair of numbers to a `%-` cenhep call, we can see if the expression is considered `%.y` true or `%.n` false.

```
> %-  gth  [5 6]
%.n
> %-  lth  [7 6]
%.n
> %-  gte  [7 6]
%.y
> %-  lte  [7 7]
%.y
```

Given a test expression like those above, we can use the `?:` wutcol rune to decide between the two possible alternatives.  `?:` wutcol accepts three children:  a true/false statement, an expression for the `%.y` true case, and an expression for the `%.n` false case.

[Piecewise mathematical functions](https://en.wikipedia.org/wiki/Piecewise) require precisely this functionality.  For instance, the Heaviside function is a piecewise mathematical function which is equal to zero for inputs less than zero and one for inputs greater than or equal to zero.

$$
H(x)
:=
\begin{cases} 1, & x > 0 \\ 0, & x \le 0 \end{cases}
$$

_However_, we don't yet know how to represent a negative value!  All of the decimal values we have used thus far are unsigned (non-negative) values, `@ud`.  For now, the easiest solution is to just translate the Heaviside function so it activates at a different value:

$$
H_{10}(x)
:=
\begin{cases} 1, & x > 10 \\ 0, & x \le 10 \end{cases}
$$

Thus equipped, we can evaluate the Heaviside function for particular values of `x`:

```
=/  x  10
?:  %-  gte  [x 10]
  1
0
```

(Notably, we don't know yet how to store this capability for future use on as-yet-unknown values of `x`; we'll see how to do that in Lesson 2.)

Carefully map how the runes in that statement relate to each other, and notice how the taller structure makes it relatively easier to read and understand what's going on.

> ### “Absolute” Value
>
> Implement a version of the absolute value function, $|x|$, similar to the Heaviside implementation above.  (Translate it to 10 as well since we still can't deal with negative numbers; call this $|x|_{10}$.)
> 
> $$
> |x|_{10}
> :=
> \begin{cases} x-10, & x > 10 \\ 0, & 10-x \le 10 \end{cases}
> $$
> 
> Test it on a few values like 8, 9, 10, 11, and 12.
{: .challenge}
