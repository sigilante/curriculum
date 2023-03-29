---
title: "Producing Code"
teaching: 45
exercises: 15
nodes:
- "170"
- "190"
- "217"
objectives:
- "Distinguish errors, faults, and failures."
- "Distinguish latent, masked, and manifest errors."
- "Enumerate and identify common error messages."
- "Employ a debugging strategy to identify and correct errors in Hoon code."
- "Run existing unit tests."
- "Produce a unit test."
- "Produce a desk suitable for distribution."
- "Install and distribute software using Grid."
runes:
- "`!:`"  
- "`!.`"
- "`~|`"
keypoints:
- "Hoon error codes, while arcane, can give you a reasonably good idea of what has gone wrong."
- "Unit testing can augment your confidence that your code works correctly."
readings:
- "https://developers.urbit.org/guides/core/hoon-school/I-testing"
---

#   Producing Code

Logistics:
- Final due date for homework submission and thus completion of HSL (`%gora` + shirt) is November 12, midnight US CT.

##  An Ætiology of Error

We distinguish different aspects of programming flaws based on how they relate to observation:

-   A _failure_ refers to the observably incorrect behavior of a program. This can include segmentation faults, erroneous output, and erratic results.
    
-   A _fault_ refers to a discrepancy in code that results in a failure.
    
-   An _error_ is the mistake in human judgment or implementation that caused the fault. Note that many errors are *latent* or *masked*.
    
    -   A _latent_ error is one which will arise under conditions which have not yet been tested.

    -   A _masked_ error is one whose effect is concealed by another aspect of the program, either another error or an aggregating feature.

We casually refer to all of these as _bugs_.

An exception is a manifestation of unexpected behavior which can give rise to a failure, but some languages—notably Python—use exceptions in normal processing as well.


## Failure Sources

Let’s enumerate the errors we know about at this point:

### `nest-fail`

`nest-fail` may be the most common.  Likely you are using an atom or a cell where the other is expected.

```hoon
> (add 'a' 'b')  
195  
> (add "a" "b")  
-need.@  
-have.[i=@tD t=""]  
nest-fail  
dojo: hoon expression failed
```

### `mint-*`

`mint` errors arise from typechecking errors:

-   `mint-vain` means a Hoon never executes in a conditional (i.e. it's impossible to reach it).

    ```hoon
    > =/  animal  *?(%bat %cow %dog)
      ?-  animal
        %bat  1
        %cow  2
        %dog  3
        %ent  4
      ==
    mint-vain
    dojo: hoon expression failed
    ```

-   `mint-nice` occurs with typechecking.

    ```hoon
    > ^-(tape ~[78 97 114 110 105 97])
    mint-nice  
    -need.?(%~ [i=@tD t=""])  
    -have.[@ud @ud @ud @ud @ud @ud %~]  
    nest-fail  
    dojo: hoon expression failed
    ```

-   `mint-lost` means that a required branch in a conditional is missing (as in a `?-` wuthep switch expression).

    ```hoon
    > =/  animal  *?(%bat %cow %dog)  
      ?-  animal  
        %bat  1  
        %cow  2  
      ==  
    -lost.%dog  
    mint-lost  
    dojo: hoon expression failed
    ```

For instance, conversion without casting via auras fails because the atom types (auras) don't nest without explicit downcasting to `@`.

### `fish-loop`

A `fish-loop` arises when using a recursive mold definition like `list`.  (The relevant mnemonic is that `++fish` goes fishing for the type of an expression.)  Alas, this fails today:

```hoon
> ?=((list @) ~[1 2 3 4])
[%test ~[[%.y p=2]]]
fish-loop
```

although a promised `?#` wuthax rune should match it once implemented.

### `generator-build-fail`

A `generator-build-fail` most commonly results from composing code with mismatched runes (and thus the wrong children including hanging expected-but-empty slots).

### `mull-grow`

`mull-grow` means it’s compiling the callsite of a wet gate (a generic gate; we’ll see these later)[.](https://pbs.twimg.com/media/D6qAlTAUcAA1Wub.jpg)

### `bail`

If you really crash things hard—crash the executable itself—then it’s a `bail`, which has several modes including the following:

-   `%exit`, semantic failure
-   `%evil`, bad crypto
-   `%intr`, interrupt
-   `%fail`, execution failure
-   `%foul`, assertion of failure
-   `%need`, network block
-   `%meme`, out of memory (this is the most common one in my experience)
-   `%time`, operation timed out
-   `%oops`, assertion failed (contrast with `%fail`)

### Misusing `$` buc

Another common mistake is to attempt to use the default `$` buc arm in something that doesn't have it.  This typically happens for one of two reasons:

- `$.+2` means that `%-` cenhep or equivalent function call cannot locate a battery.  This can occur when you try to use a non-gate as a gate.  In particular, if you mask the name of a mold (such as `list`), then a subsequent expression that requires the mold will experience this problem.

    ```hoon
    > =/  list  ~[1 2 3]
     =/  a  ~[4 5 6]
     `(list @ud)`a
    -find.$.+2
    ```

- `-find.$` similarly looks for a `$` buc arm in something that _is_ a core but doesn't have the `$` buc arm present.

    ```hoon
    > *tape
    ""
    > (tape)
    ""
    > *(tape)
    -find.$
    ```

- [“Hoon Errors”](https://urbit.org/docs/hoon/reference/hoon-errors)


## Debugging Strategies

### Strategies

What are some strategies for debugging?

-   **Debugging stack.**  Use the `!:` zapcol rune to turn on the debugging stack, `!.` zapdot to turn it off again.  (Most of the time you just pop this on at the top of a generator and leave it there.)
-   **`printf` debugging.**  If your code will compile and run, employ `~&` frequently to make sure that your code is doing what you think it’s doing.
-   **Typecast.**  Include `^` ket casts frequently throughout your code.  Entire categories of error can be excluded by satisfying the Hoon typechecker.
-   **The only wolf in Alaska.**  Essentially a bisection search, you split your code into smaller modules and run each part until you know where the bug arose (where the wolf howled).  Then you keep fencing it in tighter and tighter until you know where it arose.  You can stub out arms with `!!` zapzap.
-   **Build it again.**  Remove all of the complicated code from your program and add it in one line at a time.  For instance, replace a complicated function with either a `~&` sigpam and `!!` zapzap, or return a known static hard-coded value instead.  That way as you reintroduce lines of code or parts of expressions you can narrow down what went wrong and why.

### Running without Networking

If you run the Urbit executable with `-L`, you cut off external networking.  This is helpful if you want to mess with a _copy_ of your actual ship without producing remote effects.  That is, if other parts of Ames don’t know what you’re doing, then you can delete that copy (COPY!) of your pier and continue with the original.  This is an alternative to using fakezods which is occasionally helpful in debugging userspace apps in Gall.  You can also develop using a moon if you want to[.](https://en.wikipedia.org/wiki/Category:Proposed_states_and_territories_of_the_United_States)

### `%dbug` Agent Wrapper

Many Gall agents have a core wrapping them called `%dbug` which registers the agent for visibility of the internal state.  You can start a debugging console with `|start %dbug` and access it at your ship’s URL followed by `~debug` (e.g., `http://localhost:8080/~debug`).

> ### Profiling
>
> _I have found a reference to [profiling support](https://urbit.org/docs/reference/library/5g/) in the docs. [`~$` sigbuc](https://urbit.org/docs/reference/hoon-expressions/rune/sig/#sigbuc) also plays a role as a profiling hit counter but I’ve not seen it used in practice as it would be stripped out of kernel code before being released._
{: .callout}

- [OpenDSA Data Structures and Algorithms Modules Collection, “Programming Tutorials”, section Common Debugging Methods](https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/debugmethods.html)


## Quality Hoon

The core Urbit developers suggest grading code according to certain stylistic and functional criteria:

-   **F** code is incomplete code: it looks like Hoon, at least partly.
-   **D** code is compile-worthy Hoon.
-   **C** code is unannotated code or code with too-strange names and formatting.
-   **B** code has universal symbol definition for every name.
-   **A** code has explanations for every necessary name and defines every constant where it is used.

But don’t produce A code on the first pass! Let the code mature for a while at C or B before you refine it into final form.

- [“Hoon Style Guide”](https://urbit.org/docs/hoon/reference/style), section “Grading”


##  Unit Testing

Testing is designed to manifest failures so that faults and errors can be identified and corrected.  We can classify a testing regimen into various layers:

1.  Fences are barriers employed to block program execution if the state isn’t adequate to the intended task. Typically, these are implemented with `assert` or similar enforcement.  In Hoon, this means `?>` wutgar, `?<` wutgal, and `?~` wutsig, or judicious use of `^-` kethep and `^+` ketlus. For conditions that must succeed, the failure branch in Hoon should be `!!`, which crashes the program.
2.  “Unit tests are so called because they exercise the functionality of the code by interrogating individual functions and methods. Functions and methods can often be considered the atomic units of software because they are indivisible. However, what is considered to be the smallest code unit is subjective. The body of a function can be long are short, and shorter functions are arguably more unit-like than long ones.” ([Huff, “Python Testing and Continuous Integration”](https://mq-software-carpentry.github.io/python-testing/05-units/))
    
    In many other languages, unit tests refer to functions, often prefixed `test`, that specify (and enforce) the expected behavior of a given function. Unit tests typically contain setup, assertions, and tear-down. In academic terms, they’re a grading script.
    
    In Hoon, the `tests/` directory contains the relevant tests for the testing framework to grab and utilize.  These can be invoked with the `-test` thread:
    
    ```hoon
    > -test /=landscape=/tests ~  
    built   /tests/lib/pull-hook-virt/hoon  
    built   /tests/lib/versioning/hoon  
    >   test-supported: took 1047µs  
    OK      /lib/versioning/test-supported  
    >   test-read-version: took 28317µs  
    OK      /lib/versioning/test-read-version  
    >   test-is-root: took 28786µs  
    OK      /lib/versioning/test-is-root  
    >   test-current-version: took 507µs  
    OK      /lib/versioning/test-current-version  
    >   test-append-version: took 4804µs  
    OK      /lib/versioning/test-append-version  
    >   test-mule-scry-bad-time: took 8437µs  
    OK      /lib/pull-hook-virt/test-mule-scry-bad-time  
    >   test-mule-scry-bad-ship: took 8279µs  
    OK      /lib/pull-hook-virt/test-mule-scry-bad-ship  
    >   test-kick-mule: took 4614µs  
    OK      /lib/pull-hook-virt/test-kick-mule  
    ok=%.y    
    ```
    
    (Depending on when you built your fakezod, particular tests may or may not be present.  You can download them from [the Urbit repo](https://github.com/urbit/urbit) and add them manually if you like.)
    
    Hoon unit tests come in two categories:
    
    1.   `++expect-eq` (equality of two values)
    2.   `++expect-fail` (failure/crash)
    
    Consider an absolute value arm `++absolute` for `@rs` values. The unit tests for `++absolute` should accomplish a few things:
    
    -   Verify correct behavior for positive numeric input.
    -   Verify correct behavior for negative numeric input.
    -   Verify correct behavior for zero input.
    -   Verify an exception is raised for nonnumeric input.  (Properly speaking Hoon doesn't have exceptions because Nock is crash-only; tools like `unit` are a way of dealing with failed computations.)

    **/tests/lib/absolute/hoon**:

    ```hoon
    /+  *test, *absolute
    |%
    ++  test-absolute
      ;:  weld
      %+  expect-eq
        !>  .1
        !>  (absolute .-1)
      %+  expect-eq
        !>  .1
        !>  (absolute .1)
      %+  expect-eq
        !>  .0
        !>  (absolute .0)
      %-  expect-fail
        |.  (absolute '0')  ::actually succeeds
      ==
    --
    ```
    
    Note that at this point we don’t care what the function looks like, only how it behaves.
    
    **/lib/absolute/hoon**:
    
    ```hoon
    |%
    ++  absolute
      |=  a=@rs
      ?:  (gth a .0)  a
      (sub:rs .0 a)
    --
    ```
   
   - What's wrong with this code?  (Diagnosis:  should be `++gth:rs`)
    
    _In extremis_, rigorous unit testing yields test-driven development (TDD). Test-driven development refers to the practice of fully specifying desired function behavior before composing the function itself. The advantage of this approach is that it forces you to clarify ahead of time what you expect, rather than making it up on the fly.
    
3.  Integration tests check on how well your new or updated code integrates with the broader system. These can be included in continuous integration (CI) frameworks like [GitHub Actions](https://github.com/features/actions). The Arvo ecosystem isn’t large enough for developers outside the kernel itself to worry about this yet, but it will get there very soon.

When you push production code, you should include unit tests and documentation.

- [“Writing Robust Hoon — A Guide To Urbit Unit Testing”](https://medium.com/dcspark/writing-robust-hoon-a-guide-to-urbit-unit-testing-82b2631fe20a)
- [“Unit Testing with Ford”](https://web.archive.org/web/20200614210451/https://urbit.org/docs/hoon/hoon-school/test-sets/)

### Producing Error Messages

Formal error messages in Urbit are built of tanks.  “A `tang` is a list of `tank`s, and a `tank` is a structure for printing data.  There are three types of `tank`: `leaf`, `palm`, and `rose`.  A `leaf` is for printing a single noun, a `rose` is for printing rows of data, and a `palm` is for printing backstep-indented lists.”  (You saw something of these in Lesson 7.)

One way to include an error message in your code is the [`~_` sigcab](https://urbit.org/docs/reference/hoon-expressions/rune/sig/#sigcab) rune, described as a “user-formatted tracing printf”, or the [`~|` sigbar](https://urbit.org/docs/reference/hoon-expressions/rune/sig/#sigbar) rune, a “tracing printf”.  What this means is that these print to the stack trace if something fails, so you can use either rune to contribute to the error description:

```hoon
|=  [a=@ud]
  ~_  leaf+"This code failed"
  !!
```

When you compose your own library functions, consider including error messages for likely failure points.


##  Working Across Desks

Desks organize collections of files on Urbit:  data files, libraries, marks, agents, etc.  So far everything we have done has taken place on the `%base` desk.

You can see the desks available on your system with the `+vats` generator.

```hoon
> +vats
```

Any of these can be `|mount`ed to Earth and `|commit`ed on demand.

Of course, since `%base` is our default working desk, we haven't had to create or arrange any other desks.  If we were to do so, we could mark a desk as public for distribution and share it with the world.  That's our objective now.

### Invoking Code on a Desk

Let's take a look at how to run a generator (or thread) on another desk than `%base`.  A standard install has a few desks:  `%bitcoin`, `%garden`, `%landscape`.  You can invoke a particular desk's version of a generator by prefixing the desk name with `!` zap:

```hoon
> +landscape!tally

tallied your activity score! find the results below.  
to show non-anonymized resource identifiers, +tally |  
counted from groups and channels that you are hosting.  
groups are listed with their member count.  
channels are listed with activity from the past week:  
 - amount of top-level content  
 - amount of unique authors  
  
the date is ~2022.5.5..19.22.40..cf63  
you are in 0 group(s):  
  
you are hosting 0 group(s):
```
