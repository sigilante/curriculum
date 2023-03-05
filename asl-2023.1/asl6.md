---
title: "Production Apps"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Enumerate and identify common error messages."
  - "Run existing unit tests."
  - "Produce a unit test."
  - "Install and distribute software using Grid."
  - "Instrument unit tests for a ⛓️Gall agent."
  - "Produce a desk suitable for distribution (with a docket file)."
  - "Explain elements of a docket file."
  - "Publish a desk using `treaty`."
  - "Set up a continuous integration pipeline to test Gall agents and other published code."
runes: []
keypoints:
  - "Agents can be rigorously tested just like libraries."
  - "Urbit provides direct peer-to-peer software distribution for finished apps."
readings:
  - "https://developers.urbit.org/guides/additional/software-distribution"
  - "https://developers.urbit.org/guides/core/app-school-full-stack/8-desk"
  - "https://developers.urbit.org/guides/additional/sail"
  - "https://developers.urbit.org/guides/core/app-school/7-sur-and-marks#permissions"
  - "https://medium.com/dcspark/writing-robust-hoon-a-guide-to-urbit-unit-testing-82b2631fe20a"
homework:
  - "https://forms.gle/DSuNNVDM72eEctVeA"
---

#   🦭 `asl6`.  Production Apps.
##  App School Live Lesson 6

##  Debugging & Testing

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

### Debugging Strategies

What are some strategies for debugging?

-   **Debugging stack.**  Use the `!:` zapcol rune to turn on the debugging stack, `!.` zapdot to turn it off again.  (Most of the time you just pop this on at the top of a generator and leave it there.)
-   **`printf` debugging.**  If your code will compile and run, employ `~&` frequently to make sure that your code is doing what you think it’s doing.
-   **Typecast.**  Include `^` ket casts frequently throughout your code.  Entire categories of error can be excluded by satisfying the Hoon typechecker.
-   **The only wolf in Alaska.**  Essentially a bisection search, you split your code into smaller modules and run each part until you know where the bug arose (where the wolf howled).  Then you keep fencing it in tighter and tighter until you know where it arose.  You can stub out arms with `!!` zapzap.
-   **Build it again.**  Remove all of the complicated code from your program and add it in one line at a time.  For instance, replace a complicated function with either a `~&` sigpam and `!!` zapzap, or return a known static hard-coded value instead.  That way as you reintroduce lines of code or parts of expressions you can narrow down what went wrong and why.

#### Running without Networking

If you run the Urbit executable with `-L`, you cut off external networking.  This is helpful if you want to mess with a _copy_ of your actual ship without producing remote effects.  That is, if other parts of Ames don’t know what you’re doing, then you can delete that copy (COPY!) of your pier and continue with the original.  This is an alternative to using fakezods which is occasionally helpful in debugging userspace apps in Gall.  You can also develop using a moon if you want to[.](https://en.wikipedia.org/wiki/Category:Proposed_states_and_territories_of_the_United_States)

#### `%dbug` Agent Wrapper

Many Gall agents have a core wrapping them called `%dbug` which registers the agent for visibility of the internal state.  You can start a debugging console with `|start %dbug` and access it at your ship’s URL followed by `~debug` (e.g., `http://localhost:8080/~debug`).

> ### Profiling
>
> _I have found a reference to [profiling support](https://urbit.org/docs/reference/library/5g/) in the docs. [`~$` sigbuc](https://urbit.org/docs/reference/hoon-expressions/rune/sig/#sigbuc) also plays a role as a profiling hit counter but I’ve not seen it used in practice as it would be stripped out of kernel code before being released._
{: .callout}

- [OpenDSA Data Structures and Algorithms Modules Collection, “Programming Tutorials”, section Common Debugging Methods](https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/debugmethods.html)

##  Documenting Code

### Comments

Hoon developers employ several commenting styles, and there are mixed opinions on which is to be preferred, as you'll still see crowded comments in use in recent code.

```hoon
::  Formally, we like comments to have breathing room _beneath_ the comment.
::
++  my-code
  ...
::
::  Sometimes we have breathing room above as well.
::
++  more-code
  ...
+$  alias  type                              :: Crowded comments are common
                                             :: but not preferred.
```

The lack of a multi-line commenting system is I think a flaw in contemporary Hoon, but it's not unique to the language.

- [“Hoon Style Guide”](https://urbit.org/docs/hoon/reference/style), section “General naming style”

#### Code Annotations

Doccords are a system to provide code documentation using comments.  The `#` hax command in Dojo can expose annotations about the type.

```hoon
:: example TODO
```

- [`/lib/deco.hoon`](https://github.com/urbit/urbit/blob/develop/pkg/arvo/lib/deco.hoon)

In a similar vein, the `$+` buclus rune allows you to annotate type so that the `!>` zapgar rune can extract the intended name.

```hoon
TODO
```

#### Style Guide

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


##  Best practices

- Compose `%docs`.
- Make sure your desk is hosted `local` lest you issue an upstream change that you don't intend to propagate.
- `|nuke` removes all state from an agent and stops it, which is helpful when debugging.  (It's also an argument for storing important state in a helper agent rather than the operating vane.)

When we talk about _programming_, we can mean several distinct things: code construction (the way a code is created as an artifact of human reason); coding and debugging (the way a code is actually written); software architecture (the high-level design of a software project); etc.  Each of these requires systematic processes at an enterprise level, and frequently at even an individual coder's level (although aspects become informal and cached in one's brain instead).

There is a balance between code planning, code composition, and code testing which every developer must strike.  Well-designed software requires more work up front, but this can pay off in long-term usability.  By increasing usability, you can increase the effective lifespan of a well-built product into which hundreds or thousands of developer hours have been committed.  (Los Alamos still uses nuclear calculation codes written in the 1970s because these codes have been so well validated.)  The Urbit kernel itself espouses this principle of thoughtful permanence very carefully, and altho much of our userspace work may be more transient, we can still start building for the long term.

##  Software Lifecycle

As you prepare to build an app for release into the wild, consider the lifecycle of your app:

1. Requirements (why you want to build the app)
2. Design (how you will build the app)
3. Implementation (most of what we've talked about in HSL/ASL, actually building the app)
4. Testing (how you know the app works)
5. Deployment (releasing the app)
6. Maintenance (maintaining the changes)
7. Sunsetting (deciding what to do with the project when you're done with it)

### Requirements

Software requirements can be fairly formal or pretty loose.  Most of the software that's been released on Urbit in the past year has been a labor of love:  someone saw or thought of something cool and wanted to make it real.  This is a good place to be for now, but we expect to see more elaborate projects coming out soon which may include interoperability, security, and other requirements.

### Design

We'll talk about app architecture more at the end of this lesson.

### Implementation

Aaaaand this is what you've been doing the whole time.  Clean cup, clean cup, move down!

### Testing

![](https://raw.githubusercontent.com/sigilante/curriculum/master/unit-testing.png)

Testing gives you confidence that code works properly up to some determined standard of behavior.  Regression testing is a variant which means that every time you identify a bug, you compose a test which correctly identifies that bug and include it with the software for all future tests.

As you will recall from Hoon School, you can build `/tests` files which contain operations to evaluate and compare library code to a known target.

Agent testing looks a little different:  you have to manually construct state and then compare the results of operations.  This means that you may have to build and compare results step-by-step.  For instance, the `/tests/app/hark-store` example contains this arm:

```hoon
/=  agent  /app/hark-store
...
|%
++  test-half-open
  =|  run=@ud 
  =^  mov1  agent  
     (~(on-poke agent (bowl run)) %hark-action !>((add-note run)))
  =^  mova  agent
     (~(on-poke agent (bowl run)) %noun !>(%sane))
  =.  run  +(run)
  =^  mov2  agent  
     (~(on-poke agent (bowl run)) %hark-action !>(read-count))
  =^  mov3  agent
     (~(on-poke agent (bowl run)) %noun !>(%sane))
  =/  expected-archive=notification:hark
    [(add *time (mul ~s1 0)) bin ~[(body 0)]] 
  =+  !<(=state on-save:agent)
  =/  actual-archive=notification:hark
    (~(got re archive.state) (add *time ~s1) bin)
  (expect-eq !>(expected-archive) !>(actual-archive))
```

You can see that a series of actions are queued up and passed to the agent instance with `=^` tisket, then compared to an expected state at the end.  (Such expected state can be explicitly constructed in the front matter of the file, or immediately before use, as here.)

It's useful to create an artificial `bowl` for such test files:

```hoon
++ bowl
  |=  run=@ud
  ^-  bowl:gall
  :*  [~zod ~zod %hark-store]
    [~ ~]
    [run `@uvJ`(shax run) (add (mul run ~s1) *time) [~zod %garden ud+run]]
  ==
```

- Take a look at the `%pomodoro` agent from the [dcSpark guide](https://medium.com/dcspark/writing-robust-hoon-a-guide-to-urbit-unit-testing-82b2631fe20a).


#### Resources

-   [dcSpark, “Writing Robust Hoon—A Guide to Urbit Unit Testing”](https://medium.com/dcspark/writing-robust-hoon-a-guide-to-urbit-unit-testing-82b2631fe20a)
-   [M. Heroux, "Verification and Validation in Computing"](https://www.krellinst.org/csgf/conf/2017/video/mheroux)
-   [Software Carpentry, "Defensive Programming"](https://swcarpentry.github.io/python-novice-inflammation/08-defensive/)
-   [Stanford Encyclopedia of Philosophy, "Philosophy of Computer Science", Verification](https://plato.stanford.edu/entries/computer-science/#Veri)

### Deployment

#### Practicalities

From Hoon School Live, you probably know how to make a desk public and discoverable.  We can use the `%docket`/`%treaty` agents to distribute an app in with a better user experience.

You need to include at least four files (and a bunch of support files like `/lib/docket.hoon`, depending on the source desk you branched off of to create the app desk):

- `sys.kelvin` should just contain the current kernel version, e.g. `[%zuse 418]`.
- `desk.ship` should just contain the original publisher, e.g. `~sampel-palnet`.
- `desk.bill` has the list of agents on the desk which will be started upon installation.
- `desk.docket-0` contains summary information for distribution.

  ```hoon
  :~  title+'Hello'
      info+'A simple hello world app.'
      color+0x81.88c9
      image+'https://media.urbit.org/guides/additional/dist/wut.svg'
      base+'hello'
      glob-ames+[~zod 0v0]
      version+[0 0 1]
      website+'https://developers.urbit.org/guides/additional/dist/guide'
      license+'MIT'
  ==
  ```

  Most of this information is straightforward, but the `glob` line can be confusing.  Essentially an app with a front-end needs to specify where that front-end comes from:

  - `%glob-ames` served over Ames (I couldn't find an example).
  - `%glob-http` served over HTTP (e.g. Landscape, `%bitcoin`).
  - `%site` served by Eyre (e.g. `%pals` with Sail).

As you saw when working with the front-end materials in Lesson 4, you can use the Globulator tool to fix the docket file correctly.

Having provided all that information, you can now make your app visible to others for installation:

```hoon
:treaty|publish %hello
```

and they can locate it by searching for your ship.

You may wish to host software from a star or from a moon.  There aren't strong reasons yet to prefer a particular pattern, although I myself am partial to moons for this purpose.

#### Resources

- [Distributing Software](https://developers.urbit.org/guides/additional/software-distribution)
- [App School Full Stack, “Desk”](https://developers.urbit.org/guides/core/app-school-full-stack/8-desk)
- [Sail:  HTML in Hoon](https://developers.urbit.org/guides/additional/sail)

#### Imperatives

Software deployments should include a few standard files:

1.  `README` or `README.md`
2.  `INSTALL` (optional for Urbit)
3.  `CITATION` (optional unless attached to an academic program)
4.  `CHANGELOG` (unless integrated into `README`)
5.  `LICENSE` (typically the [MIT License](https://mit-license.org/))


### Maintenance

Right now, maintenance mainly means making sure that your app stays abreast of any breaking changes in Arvo and keeping an up-to-date `sys.kelvin` version (currently `%418`).

We have a developer newsletter, `[battery payload]`, which will go out on the first of each month.  We will note upcoming breaking changes there.

### Sunsetting

The reality is that you will bear some _de facto_ responsibility for the code projects you have worked on in the past. This means that your initial investment of time spent writing code (which was visible) gets traded over time for an _invisible_ maintenance cost in planning and refactoring and consulting. Most of the time, this invisible burden saps your ability to do productive work downstream, so you need to compose your code and interfaces in such a way that others can assume your role when you leave it.


##  App Architecture

The doctrine of app design, and the relationship of an app to the larger ecosystem, has been evolving fairly quickly in Urbit.  One can envision several possible futures, such as internal “frenemy” competing tools platforms (like R has) or tightly disciplined sets of highly-compatible tools put out by one or more big players that most others use.  Depending on how remote scry and permissioning works, maybe apps won't really have to share primitives beyond the OS at all.

- **Naming**.  Older Gall agents tend to adopt a stricter three-letter word for values, such as `bol=bowl.gall` in the door's sample or `pax=path` in a gate's sample.  Contemporary developers seem to prefer `=bowl:gall` and `=path` instead, skipping matches with `^` ket if necessary.  There's no specific recommendation here, but you should probably pick a lane to maintain readability.

- **State and Endpoints**.  You can scry for internal values using `.^` dotket; these are handled in `++on-peek`.  You should implement a simple permissions check.  You should also make all internal state available to this kind of check, as well as wrapping your agent in the `dbug` wrapper.

- **Helper Cores**.  There are three basic patterns you can use for including helper arms:

  1.  Include the arms directly in the Gall agent core.  This isn't recommended.
  2.  Wrap the arms in a `|^` barket core for immediate evaluation.  This is fine, and you'll see this pattern occasionally in production code.
  3.  Include a separate auxiliary core next to the main Gall core.  This is the most common pattern, and you'll often see a reference to it included in the default definitions.
  4.  Produce a library.  This is most helpful when the helper arms will be useful to several agents in your app.

- **Store/Hook/View**.  For a while, userspace applications were built with an architectural division in three classes ([much like Gaul](https://en.wikipedia.org/wiki/Commentarii_de_Bello_Gallico)).  You see this in Graph Store and related tools:

  1.  **Stores**. Independent local collections of data exposed to other apps. Think of Groups for Landscape.
  2.  **Hooks**. Store manipulations. Think of subscriptions.
  3.  **Views**. User-interface applications. Think of Landscape itself (the browser interface).
  
  -   [Logan Allen, Matt, Matilde Park `~haddef-sigwen`, “Userspace Architecture”](https://docs.google.com/document/d/1hS_UuResG1S4j49_H-aSshoTOROKBnGoJAaRgOipf54/edit)
  
  Today, the recommendation is rather that each app should contain as few agents as possible, while permitting clean division between agent roles.

- **`++abed`/`++abet` Pattern**.  Sometimes agents need to issue a lot of state changes which can lead to awkward `=^` tisket changes to cards so that events resolve in the correct order.  (Cards all happen “at the same time”, meaning before any mutations are applied to the state.)  Rather than produce `(quip card _state)`, you can close over a list of cards and state using a core, then pull the `++abet` arm on that core to produce the new list of cards and state.

  ```hoon
  ++  abet
    ^-  (quip card _state)
    [(flop cards) state]
  ```

  You can see this illustrated in `/app/acme.hoon`, where various arms like `++wake` make calls such as `%-  (slog u.error)  abet` from time to time.  It's also used in [`/sys/gall.hoon`](https://github.com/urbit/urbit/blob/cd10e02b732ad2c410e5b730d2fa2ce133060dd2/pkg/arvo/sys/vane/gall.hoon#L280) with nested cores.

  For instance, imagine a chat app.  Let's have a core that has the state of a particular chat in the door's sample, which you initialize by calling an arm `++abed` to populate the sample.  Then all mutations are carried out and collected, then performed using the door's `++abet` arm.  Normally there is a `++take` arm to receive and process signs.

  You can nest cores and use this pattern to simplify wire management by `area`; e.g. `++mo-abet` and so forth.  When used well, the `++abet` pattern can lead to cleaner code factoring and sequestration of more complex logic.

- **Handling subscriptions**.  While [pubsub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) is an attractive messaging pattern for constructing apps, in practice subscriptions can be a bit flaky and kick a lot.  One way to deal with this contingency within pubsub is to use an update log, which tracks and synchronizes remote values (as in something like Groups).  The `%journal` app uses an ordered `map` (or `mop`) to accomplish something similar.

- **Permissions**.  We have largely ignored any consideration of permissions issues.  In practice, you won't want apps to accept pokes from literally anywhere, so each agent will need to use some proxy for filtering input data requests and pokes.  Fortunately, Urbit ID naturally provides a framework for this without API keys or the like.

  One pattern you can use is to receive any poke, check the source against self and whitelist (or blacklist), then re-issue any approved pokes from your self.  Then you can put a fence over any critical code like this:

  ```hoon
  ?>  =(our.bowl src.bowl)
  ```

  There are other models, like allowing only moons (`team:title`) or having a whitelist (`?>  (~(has in allowed) src.bowl)`).  You can also use other apps as a proxy, such as scrying into Pals or a particular group in Groups:

  ```hoon
  ?>  .^(? %gx /(scot %p our.bowl)/group-store/(scot %da now.bowl)/groups/ship/~bitbet-bolbel/urbit-community/join/(scot %p src.bowl)/noun)
  ```

- [App School, “Structure and Mark Files”, section “Permissions”](https://developers.urbit.org/guides/core/app-school/7-sur-and-marks#permissions)
