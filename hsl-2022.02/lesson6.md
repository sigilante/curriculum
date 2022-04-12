---
title: "Molding Values, Using Doors"
teaching: 45
exercises: 15
nodes:
- "156"
- "183"
objectives:
- "Use assertions to enforce type constraints."  
- "Identify a `lest` (as opposed to a list)."  
- "Produce a type arm."  
- "Identify units, sets, maps, and compound structures like jars and jugs."  
- "Explain why units and vases are necessary."  
- "Use helper arms and syntax:  `` ` ``, `biff`, `some`, etc."
runes:  
- "`?>`"  
- "`?<`"  
- "`?~`"  
- "`+$`"
keypoints:
- ""
- "Units allow one to distinguish a null result (failure) from a zero."
---

#   Molding Values, Using Doors

##  Satisfying Static Typing

Hoon enforces its type system at compile time (build time).  This means that any code which makes assumptions about how values will be used is checked for mold compatibility when you `|commit` it or type it at the Dojo.  It also means that you've probably seen a fair number of problems with matching types.

While we'll discuss general debugging strategies in more detail later, there are three basic things that tend to go wrong:

1. Syntax error, general (just typing things out wrong, for instance a way Dojo would prevent)
2. Syntax error, mismatched rune daughters (due to `ace`/`gap` or miscounting children)
3. Type issues (`need`/`have`, notoriously)

This last case can be handled with a couple of expedients:

- Frequent use of `^-` kethep/`^+` ketlus to make sure that types match at various points in the code.

    This has two benefits:  it verifies your expectations about what values are being passed around, and it means that mismatches raise an error more closely to the source of the error.

    (Since Hoon checks type at build time, this does not incur a computational cost when the program is running.)

- Use of assertions to enforce type constraints.  Assertions are a form of `?` wut rune which check the structure of a value.  Ultimately they all reduce back to `?:` wutcol, but are very useful in this sugar form:

    - [`?>` wutgar](https://urbit.org/docs/hoon/reference/rune/wut#-wutgar) is a positive assertion, that a condition _must_ be true.
    - [`?<` wutgal](https://urbit.org/docs/hoon/reference/rune/wut#-wutgal) is a negative assertion, that a condition _must_ be false.
    - [`?~` wutsig](https://urbit.org/docs/hoon/reference/rune/wut#-wutsig) is a branch on null.

    For instance, some operations require a `lest`, a `list` guaranteed to be non-null (that is, `^-  (list)  ~` is excluded).

    ```hoon
    > =/  list=(list @)  ~[1 2 3]
     i.list
    -find.i.list
    find-fork
    dojo: hoon expression failed
    ```

    `?~` wutsig solves the problem for this case:

    ```hoon
    > =/  list=(list @)  ~[1 2 3]
     ?~  list  !!
     i.list
    1
    ```
    
    In general, if you see an error like `find.fork`, it means that the type system is confused by your use of a too general of a type for a particular case.  Use the assertion runes to correct its assumption.


##  Type Arms as Mold Builders

We previously commented on [`+$` lusbuc](https://urbit.org/docs/hoon/reference/rune/lus#-lusbuc) as a type builder arm.  We are now better equipped to discuss what these are doing and how they work.

`+$` lusbuc only permits `$` buc mold builders and basic structure expressions (like `@`).  Sometimes we rename a value for clarity, such as working with a particular class of values:

```hoon
|%
+$  url  @t
--
```

(There's no formal restriction on the value, but subsequent code may be made much more legible by such definitions.)

```hoon
|%
+$  rank  ?(%galaxy %star %planet)
--
```

In essence, a type builder arm is producing a mold resolvable within a given subject.  It's resolved as a gate (because a mold is a gate) and applied to the sample.

As you'll see in later more complicated applications, long names with complicated limbs are often aliased this way as well:

```hoon
|%
+$  card  card:agent:gall
--
```

##  Better Data Structures through Doors

Hoon is statically typed, which means (among other things) that auras are subject to strict nesting rules, molds are crash-only, and the whole thing is rather cantankerous about matching types.

However, since gate-building arms are possible, Hoon developers frequently employ them as templates to build type-appropriate cores, including gates.

Let's briefly review our two main tools for evaluating Hoon with `%` cen runes:

- [`%-` cenhep](https://urbit.org/docs/hoon/reference/rune/cen#cenhep) accepts two children, a wing which resolves to a gate; and a sample which is provided at `+6` to the gate.  It yields the result of the Hoon expression, which may be a simple value, a data structure, or a core.
- [`%~` censig](https://urbit.org/docs/hoon/reference/rune/cen#censig) accepts three children, a wing which resolves to an arm in a door; the aforesaid door; and a sample which is provided at `+6` to the door.  It conventionally yields a gate which can then be applied to a sample.

Now it turns out that `%-` cenhep is actually a special case of `%~` censig:  it resolves to `%~($ a b)`, evaluating the `$` buc arm of a gate core.  (A door really is just a more general case of a gate.  Think carefully about this.)

### `map`

In general terms, a map is a pattern from a key to a value.  You can think of a dictionary, or an index, or a data table.  Essentially it scans for a particular key, then returns the data associated with that key (which may be any noun).

| Key         | Value      |
| ----------- | ---------- |
| 'Mazda'     | 'RX-8'     |
| 'Dodge'     | 'Viper'    |
| 'Ford'      | 'Mustang'  |
| 'Chevrolet' | 'Chevelle' |
| 'Porsche'   | 'Boxster'  |
| 'Bugatti'   | 'Type 22'  |

While `map` is the mold or type of the value, the door which affords `map`-related functionality is named `++by`.  (This felicitously affords us a way to read `map` operations in an English-friendly phrasing.)

In Urbit, all values are static and never change.  (This is why we “overwrite” or replace the values in a limb to change it with `%=` centis.)  This means that when we build a `map`, we often rather awkwardly replace it with its modified value explicitly.

We'll build a color `map`, from a `@tas` of a [color's name](https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors) to its HTML hexadecimal representation as a `@ux` hex value.

We can produce a `map` from a `list` of key-value cells using the `++my` function:

```hoon
> =colors (my ~[[%red 0xed.0a3f] [%yellow 0xfb.e870] [%green 0x1.a638] [%blue 0x66ff]])
```

We could designate the mold of this as a `(map @tas @ux)`, altho examine the type spear and see why this isn't completely correct.  In fact, due to the way `@tas` `term`s work, it's more convenient to explicitly supertype the key mold when defining the `map` in the first place:

```hoon
> =colors `(map @tas @ux)`(my ~[[%red 0xed.0a3f] [%yellow 0xfb.e870] [%green 0x1.a638] [%blue 0x66ff]])
```

To insert one key-value pair at a time, we use `put`.  We need to either pin it into the subject for Dojo or modify it with `=/` tisfas.

```hoon
> =colors (~(put by colors) [%orange 0xff.8833])
> =colors (~(put by colors) [%violet 0x83.59a3])
> =colors (~(put by colors) [%black 0x0])
```

Note the pattern here:  there is a `++put` arm of `++by` which builds a gate to modify `colors` by inserting a value.

What happens if we try to add something that doesn't match the type?

```hoon
> =colors (~(put by colors) [%cerulean '#02A4D3'])
```

We'll see a `mull-grow`, a `mull-nice`, and a `nest-fail`.  Essentially these are all flavors of mold-matching errors.

(As an aside, `++put:by` is also how you'd replace a key's value.)

The point of a `map` is to make it easy to retrieve data values given their appropriate key.  Use `++get:by`:

```hoon
> (~(get by colors) %orange)
[~ 0xff.8833]
```

What is that cell?  Wasn't the value stored as `0xff.8833`?  Well, one fundamental problem that a `map` needs to solve is to allow us to distinguish an _empty_ result (or failure to locate a value) from a _zero_ result (or an answer that's actually zero).  To this end, the `unit` was introduced, a type union of a `~` (for no result) and `[~ item]` (for when a result exists).

- What does `[~ ~]` mean when returned from a `map`?

`unit`s are common enough that they have their own syntax and set of operational functions.  We'll look at them more in a bit.

```hoon
> (~(get by colors) %brown)
~
```

([`++got:by`](https://urbit.org/docs/hoon/reference/stdlib/2i#gotby) returns the value without the `unit` wrapper, but crashes on failure to locate.  I recommend just using `++get` and extracting the tail of the resulting cell after confirming it isn't null with `?~` wutsig.  See also [`++gut:by`](https://urbit.org/docs/hoon/reference/stdlib/2i#gutby) which allows a default in case of failure to locate.)

You can check whether a key is present using `++has:by`:

```hoon
> (~(has by colors) %teal)
%.n
> (~(has by colors) %green)
%.y
```

You can get a list of all keys with `++key:by`:

```hoon
> ~(key by colors)
{%black %red %blue %violet %green %yellow %orange}
```

You can apply a gate to each value, rather like `++turn` in Lesson 4, using `++run:by`.  For instance, these gates will break the color hexadecimal value into red, green, and blue components:

```hoon
> =red |=(a=@ux ^-(@ux (cut 2 [4 2] a)))
> =green |=(a=@ux ^-(@ux (cut 2 [2 2] a)))
> =blue |=(a=@ux ^-(@ux (cut 2 [0 2] a)))
> (~(run by colors) blue)
{ [p=%black q=0x0]  
 [p=%red q=0x3f]  
 [p=%blue q=0xff]  
 [p=%violet q=0xa3]  
 [p=%green q=0x38]  
 [p=%yellow q=0x70]  
 [p=%orange q=0x33]  
}
```

### `set`

A `set` is rather like a `list` except that each entry can only be represented once.  As with a `map`, a `set` is typically associated with a particular type, such as `(set @ud)` for a collection of decimal values.  (`set`s also don't have an order, so they're basically a bag of unique values.)

`set` operations are provided by `++in`.  Most names are similar to `map`/`++by` operations when applicable.

`++sy` produces a `set` from a `list`:

```hoon
> =primes (sy ~[2 3 5 7 11 13])
```

`++put:in` adds a value to a `set` (and null-ops when the value is already present):

```hoon
> =primes (~(put in primes) 17)
> =primes (~(put in primes) 13)
```

`++del:in` removes a value from a `set`:

```hoon
> =primes (~(put in primes) 18)
> =primes (~(del in primes) 18)
```

`++has:in` checks for existence:

```hoon
> (~(has in primes) 15)
%.n
> (~(has in primes) 17)
%.y
```

`++tap:in` yields a `list` of the values:

```hoon
> ~(tap in primes)  
~[3 2 7 5 11 13 17]  
> (sort ~(tap in primes) lth)  
~[2 3 5 7 11 13 17]
```

`++run:in` applies a function across all values:

```hoon
> (~(run in primes) dec)  
{10 6 12 1 2 16 4}
```

### `unit` Redux (and `vase`)

We encountered the `unit` as a tool for distinguishing null results from actual zeroes:  “using a `unit` allows you to specify something that may not be there.”

You can build a `unit` using the tic special notation or [`++some`](https://urbit.org/docs/hoon/reference/stdlib/2a#some):

```
> `%mars
[~ %mars]
> (some %mars)
[~ u=%mars]
```

While `++got:by` is one way to get a value back without wrapping it in a `unit`, it's better practice to use the [`unit` logic](https://urbit.org/docs/hoon/reference/stdlib/2a) gates to manipulate gates to work correctly with `unit`s.

For one thing, use [`++need`](https://urbit.org/docs/hoon/reference/stdlib/2a#need) to unwrap a `unit`, or crash if the `unit` is `~` null.

```hoon
> =colors `(map @tas @ux)`(my ~[[%red 0xed.0a3f] [%yellow 0xfb.e870] [%green 0x1.a638] [%blue 0x66ff]])
> (need (~(get by colors) %yellow))
0xfb.e870
> (need (~(get by colors) %teal))  
dojo: hoon expression failed
```

Rather than unwrap a `unit`, one can modify gates to work with `unit`s directly even if they're not natively set up that way.  For instance, one cannot decrement a `unit` because `++dec` doesn't accept a `unit`.  [`++bind`](https://urbit.org/docs/hoon/reference/stdlib/2a#bind) can bind a non-`unit` function

```hoon
> (bind ((unit @ud) [~ 2]) dec)  
[~ 1]
> (bind (~(get by colors) %orange) red)  
[~ 0xff]
```

(There are several others tools listed [on that page](https://urbit.org/docs/hoon/reference/stdlib/2a) which may be potentially useful to you.)

A `+$vase` is a pair of type and value, such as that returned by `!>` zapgar.  A `vase` is useful when transmitting data in a way that may lose its type information.

### `jar` and `jug`

`map`s and `set`s are frequently used in the standard library and in the extended ecosystem (such as in `graph-store`).  There are a couple of common patterns which recur often enough that they have their own names:

- [`++jar`](https://urbit.org/docs/hoon/reference/stdlib/2o#jar) is a mold for a `map` of `list`s.

- [`++jug`](https://urbit.org/docs/hoon/reference/stdlib/2o#jug) is a mold for a `map` of `set`s.

(There's an example in the slides of a `jar`.)

These are supported by the [`++ja`](https://urbit.org/docs/hoon/reference/stdlib/2j#ja) core and the [`++ju`](https://urbit.org/docs/hoon/reference/stdlib/2j#ju) core.


##  Example:  Caesar Cipher

The Caesar cipher is a shift cipher ([that was indeed used anciently](https://en.wikipedia.org/wiki/Caesar_cipher)) wherein each letter in a message is encrypted by replacing it with one shifted some number of positions down the alphabet.

Save this as `caesar.hoon` in `/gen`:

```hoon
!:
|=  [msg=tape steps=@ud]
=<
=,  msg  (cass msg)
:-  (shift msg steps)
    (unshift msg steps)
::
|%
++  alpha  "abcdefghijklmnopqrstuvwxyz"
::  Shift a message to the right.
::
++  shift
  |=  [message=tape steps=@ud]
  ^-  tape
  (operate message (encoder steps))
::  Shift a message to the left.
::
++  unshift
  |=  [message=tape steps=@ud]
  ^-  tape
  (operate message (decoder steps))
::  Rotate forwards into encryption.
::
++  encoder
  |=  [steps=@ud]
  ^-  (map @t @t)
  =/  value-tape=tape  (rotation alpha steps)
  (space-adder alpha value-tape)
::  Rotate backwards out of encryption.
::
++  decoder
  |=  [steps=@ud]
  ^-  (map @t @t)
  =/  value-tape=tape  (rotation alpha steps)
  (space-adder value-tape alpha)
::  Apply the map of decrypted->encrypted letters to the message.
::
++  operate
  |=  [message=tape shift-map=(map @t @t)]
  ^-  tape
  %+  turn  message
  |=  a=@t
  (~(got by shift-map) a)
::  Handle spaces in the message.
::
++  space-adder
  |=  [key-position=tape value-result=tape]
  ^-  (map @t @t)
  (~(put by (map-maker key-position value-result)) ' ' ' ')
::  Produce a map from each letter to its encrypted value.
::
++  map-maker
  |=  [key-position=tape value-result=tape]
  ^-  (map @t @t)
  =|  chart=(map @t @t)
  ?.  =((lent key-position) (lent value-result))
  ~|  %uneven-lengths  !!
  |-
  ?:  |(?=(~ key-position) ?=(~ value-result))
  chart
  $(chart (~(put by chart) i.key-position i.value-result), key-position t.key-position, value-result t.value-result)
::  Cycle an alphabet around, e.g. from
::  'ABCDEFGHIJKLMNOPQRSTUVWXYZ' to 'BCDEFGHIJKLMNOPQRSTUVWXYZA'
::
++  rotation
  |=  [my-alphabet=tape my-steps=@ud]
  =/  length=@ud  (lent my-alphabet)
  =+  (trim (mod my-steps length) my-alphabet)
  (weld q p)
--
```

The commentary is dense, but I've added some remarks above which hopefully decompress it a bit for you.  The use of `++space-adder` clutters it a bit, and it would probably be cleaner to just work with an “expanded alphabet” including space and punctuation characters, or to manually modify the `map` to handle those directly.

There are four runes in this which we haven't seen yet:

- `=,` tiscom modifies a leg in the subject, similar to `=/` tisfas (Lesson 8)
- `=|` tisbar introduces a named noun to the subject, like a `=/` tisfas that just has the bunt (Lesson 8)
- `~|` sigbar is a “tracing printf”, which only outputs a message if the code crashes (Lesson 9)
- `?|` wutbar in its irregular `|()` form, a logical `OR` operation (Lesson 7)

We also didn't look at [`++trim`](https://urbit.org/docs/hoon/reference/stdlib/4b#trim), which splits the first set of characters off of a `tape` (similar to [`++scag`](https://urbit.org/docs/hoon/reference/stdlib/2b#scag) except returning both sides back to you as a cell).

- [“Caesar Cipher”](https://urbit.org/docs/hoon/hoon-school/caesar)
