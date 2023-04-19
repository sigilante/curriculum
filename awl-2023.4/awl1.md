---
title: "Command Line"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Produce a command-line interface agent including input validation."
runes: []
keypoints: []
readings:
  - "https://developers.urbit.org/guides/core/hoon-school/P-stdlib-io"
  - "https://developers.urbit.org/guides/core/hoon-school/Q2-parsing"
  - "https://developers.urbit.org/guides/additional/parsing"
  - "https://developers.urbit.org/guides/additional/cli-tutorial"
homework: []
mirror: []
video: []
---

#   ✂ `awl1`. Command Line

Command-line interface (CLI) programs are one of the great [primeval](https://www.hackneys.com/docs/in-the-beginning-was-the-command-line.pdf) interfaces for personal computing and client–server computing.  (I omit, of course, punched cards and other early modes of interaction.)  Even today many aspects of deep system configuration are available only to those willing to plumb the depths of their system lit only by the flashing cursor.

While we typically associate the command line with the terminal, other systems can also be thought of as text-based user interfaces:  search engines, voice assistants, PC game console interfaces, and device streams.  Urbit has long provided the Dojo as the main text user interface.  Dojo acts similar to [`bash`](https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29) in terms of permitting access to the file system and a systems language.  Dojo parses for valid input in real time, which can be frustrating for a first-time user, but thus attempts to only allow valid commands to be entered.  Besides acting as a Hoon REPL, the Dojo knows how to interact with system generators (`|` bar for `%hood` generators, `+` lus for `/gen` userspace generators, and `-` hep for `/ted` threads) and pin values with faces for use in subsequent expressions (like Lisp's `set` and derivatives).

Urbit CLI programs are built around two related libraries:

- `%shoe` acts as the backbone for managing CLI agent sessions.
- `%sole` instruments effects (results) arising from `%shoe` programs.

and the capability to take in commands:

- parsing handles converting input text to valid commands for `%sole`.

In this tutorial, we will cover how to parse text and how to build `%shoe`/`%sole` CLI agents.  We will illustrate this by producing a simple reverse Polish notation calculator agent.  This agent will accept values, store them on a stack, and operate on them using arithmetic operators:

```hoon
> 1
[.1]

> 3
[.1 .3]

> -
[.1 .3 -] →
[.2]

> 4
[.2 .4]

> *
[.2 .4 *] →
[.8]

> .
.8
[.8]
```


##  Parsing

Our main curriculum in this section draws verbatim on [“Hoon School:  Text Processing III”](https://developers.urbit.org/guides/core/hoon-school/Q2-parsing) with additions from the [Parsing Text](https://developers.urbit.org/guides/additional/parsing) tutorial.  After reading those, return to this document.

As you can imagine, building a full parser from scratch can become incredibly complicated.  It is common to define a host of intermediate rules which match clauses (such as valid commands) rather than build the entire parsing rule set at once.

For instance, if we would like a rule that matches exactly one of the texts `give`, `list`, or `diff` (useful in the next lesson), we could write rules using `++pose` and `++star` operating on `++jest` for perfect matches:

```hoon
::  ;~(pose (jest 'give') (jest 'list') (jest 'diff'))

> (scan "give" ;~(pose (jest 'give') (jest 'list') (jest 'diff')))
'give'

> (scan "list" ;~(pose (jest 'give') (jest 'list') (jest 'diff')))
'list'

> (scan "mask" ;~(pose (jest 'give') (jest 'list') (jest 'diff')))
{1 4}
syntax error
dojo: hoon expression failed

::  (star ;~(pose (jest 'give') (jest 'list') (jest 'diff')))

> (scan "listgive" (star ;~(pose (jest 'give') (jest 'list') (jest 'diff'))))
[i='list' t=<|give|>]
```

Let's suppose that our overall grammar looks like this:

```
('list' | 'diff' | 'draw') ace path 
```

In this case, we need to define a rule to match one command (which we already have above):

```hoon
++  cmd  ;~(pose (jest 'list') (jest 'diff') (jest 'draw'))
```

Next we'll need to match an `ace`.  This is provided by `hoon.hoon` as `++ace`.

```hoon
> (scan " " ace)
' '

> (scan "$" ;~(pose ace buc))
'$'

> (scan ":" ;~(pose ace buc))
{1 1}
syntax error
dojo: hoon expression failed

> (scan "  " (star ace))
[i=' ' t=<| |>]
```

Finally we need to parse a `path`.  As with `ace`, this is already provided for in the Hoon parser:  `++gash:vast`.  `++gash:vast` actually does more than we want here, however, since it immediately parses the `path` into a Hoon AST.

```hoon
> (scan "/5/6/7" gash:vast)
[ i=[~ [%sand p=%tas q=0]]
  t=[i=[~ [%sand p=%ta q=53]] t=~[[~ [%sand p=%ta q=54]] [~ [%sand p=%ta q=55]]]]
]

> (scan "/foo/bar/baz" gash:vast)
[ i=[~ [%sand p=%tas q=0]]
    t
  [i=[~ [%sand p=%tas q=7.303.014]] t=~[[~ [%sand p=%tas q=7.496.034]] [~ [%sand p=%tas q=8.020.322]]]]
]
```

Instead, we will use what `++gash:vast` uses internally before it `++cook`s the result:  `(more fas limp)` which ultimately expands to `(more fas ;~(plug (star fas) sym:so))`.  (Unfortunately this still yields `@`s instead of `knot`s but we can live with that here.)

```hoon
> (scan "/foo/bar/baz" (more fas ;~(plug (star fas) sym:so)))
[[[i='/' t=<||>] 7.303.014] [i=[~ 7.496.034] t=~[[~ 8.020.322]]]]
```

That first `/` fas is pesky due to the empty string, but we could trim it off by prepending a `plug`:

```hoon
> (scan "/foo/bar/baz" ;~(plug fas (more fas ;~(plug (star fas) sym:so))))
['/' [[~ 7.303.014] [i=[~ 7.496.034] t=~[[~ 8.020.322]]]]]
```

Thus:

```hoon
++  pax  ;~(plug fas (more fas ;~(plug (star fas) sym:so)))
```

However, as is often the case when parsing things that look like Hoon, there is an appropriate simple parser we can use, `++stap:so`.  `++stap:so` parses strings containing `path`s into `path`s and it simplifies out the `unit`s from `++sym:so`.

All together, then, our rule becomes:

```hoon
::  ;~(plug cmd ace stap:so)

> (scan "list /path/to/hoon" ;~(plug cmd ace stap:so))  
['list' ' ' /path/to/hoon]
```

It's ready to pass to `++cook` for handling.  (It'll actually become more complicated than this but it's a start on `awl2`.)

We often wish to attach actions to particular words when they are parsed.  [`++cook`](https://developers.urbit.org/reference/hoon/stdlib/4f#cook) applies a gate to the result of a parser rule and is used to actually transform the results of parsing into actionable nouns for subsequent Hoon expressions.

Given a gate such as

```hoon
/+  pretty-file
|%
++  retrieve-file
  !:  |=  =path
  ^-  cord
  ~&  >  :(weld /=== path)
  .^(cord %cx :(weld /=== path))
--
```

we can apply it to a parsing rule thus:

```hoon
> ((cook |=(=path .^(cord %cx (weld /=== path))) stap:so) [[1 1] "/lib/csv/hoon"])
[ p=[p=1 q=14]  
   q  
 [ ~  
     u  
   [   p  
     '::  Parse CSV files with a known schema, then perform queries on the\0a::  results.\0a::\0a|%\0a+  
+  text\0a  %+  cook\0a    |=  =tape\0a    (crip tape)\0a  ;~  pose\0a    (cook tape soil:vast)\0a    no  
n-quote-text\0a  ==\0a::\0a++  non-quote-text\0a  (star ;~(less com qit))\0a::\0a++  parse\0a  |*  cols=  
(list rule)\0a  %+  ifix\0a    :-  ;~(sfix ;~(less (just `@`10) (star prn)) (just `@`10))\0a    (just `@  
`10)\0a  (more (just `@`10) (parse-line cols))\0a::\0a++  parse-line\0a  |*  cols=(list rule)\0a  ?~  co  
ls\0a    (easy ~)\0a  ?~  t.cols\0a    i.cols\0a  ;~  plug\0a      i.cols\0a      ;~(pfix com $(cols t.c  
ols))\0a  ==\0a::\0a::  inner join\0a::\0a++  join\0a  =/  name-side  (ream \'[left=- right=+]\')\0a  |=  
 [left=(list vase) rite=(list vase) =hoon]\0a  ^-  (list vase)\0a  |-  ^-  (list vase)\0a  =*  left-loo  
p  $\0a  ?~  left\0a    ~\0a  =/  rote  rite\0a  |-  ^-  (list vase)\0a  =*  rite-loop  $\0a  ?~  rite\0  
a    left-loop(left t.left, rite rote)\0a  =/  slopped-row  (slap (slop i.left i.rite) name-side)\0a  =/  
 val  (slap (slop slopped-row !>(..zuse)) hoon)\0a  ?.  =(%& q.val)\0a    rite-loop(rite t.rite)\0a  :-  
 slopped-row\0a  rite-loop(rite t.rite)\0a::\0a::  filter\0a::\0a++  where\0a  |=  [rows=(list vase) =h  
oon]\0a  ^-  (list vase)\0a  %+  skim  rows\0a  |=  =vase\0a  =/  val  (slap vase hoon)\0a  =(%& q.val)\  
0a::\0a::  select\0a::\0a++  select\0a  |=  [=hoon rows=(list vase)]\0a  ^-  (list vase)\0a  %+  turn  r  
ows\0a  |=  =vase\0a  (slap (slop vase !>(..zuse)) hoon)\0a::\0a::  pretty-print rows\0a::\0a++  print-r  
ows\0a  |=  rows=(list vase)\0a  (slog (turn rows sell))\0a--\0a'  
     q=[p=[p=1 q=14] q=""]  
   ]  
 ]  
]
```

Notice how `++cook` modifies the parsing rule, then the gate resulting from slamming `++cook` on its gate and the parsing rule is applied to the `nail`.

### Parsing Arithmetic Expressions

The following generator is a calculator which will consume basic addition and multiplication statements.

**`/gen/expr-parse.hoon`**

```hoon
::  expr-parse: parse arithmetic expressions
::
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

This doesn't rise to the level of a CLI agent, but it points in the right direction.

```hoon
> +expr-parse "3"
3

> +expr-parse "3+3"
6

> +expr-parse "3+3+(2*3)+(4+2)*(4+1)"
42

> +expr-parse "3+3+2*3"
12
```


##  `%shoe`

`%shoe` is responsible to manage attached agent sessions.  It adds a few arms to the standard Gall agent, namely:

- `++command-parser` is the input parser, similar to the work we were carrying out just above.  This parses every input and only permits valid keystrokes (think of Dojo real-time parsing).
- `++tab-list` provides autocompletion options.  We can ignore for now.
- `++on-command` is called whenever a valid command is run.  This produces the actual effects.
- `++can-connect` supports `|link` connexion to the app.
- `++on-connect` provides particular session support when a user connects.  We can ignore for now.
- `++on-disconnect` provides particular session support when a user disconnects.  We can ignore for now.

To get started with text parsers and CLI agents, we need to focus on `++command-parser` and `++on-command`.  But first, the agent's structure and state:


The agent will adopt a two-stage process, wherein a value is put on the stack then the stack is checked for any valid operations.

### `++command-parser`

The input parser can simply accept whole words or single inputs, or parse complex expressions (as Dojo does with Hoon).

This results in a noun of `+$command-type` based on the specific application.  The example `/app/shoe.hoon` agent defines:

```hoon
+$  command
  $?  %demo
      %row
      %table
  ==
```

and later uses this as:

```hoon
  ++  command-parser                                                                            
    |=  =sole-id:shoe
    ^+  |~(nail *(like [? command]))
    %+  stag  &
    (perk %demo %row %table ~)
```

where the unfamiliar parser components are:

- `++stag` adds a label, here `&` pam `TRUE`/`%.y` to indicate that the command should be run immediately when it matches.  (We won't want this below so we will `++stag` a `|` `FALSE`/`%.n`.)
- `++perk` parses a fork in the type.

### `++on-command`

This arm accepts a session ID and a command resulting from `++command-parser`.  It produces a regular `(quip card _this)` so you can modify agent state and produce effects here.


##  `%sole`

`%sole` is responsible for producing effects.  If you want to yield effects to the command line from your CLI agent (which you often do), this is a great place to work.

`%sole-effect`s are head-tagged by time and produce a variety of terminal effects, from text to bells, colors, and other screen effects.

Here is an agent that will accept a single character and produce a line with varying random colors of that character.

**`/app/track7.hoon`**

```hoon
/+  default-agent, dbug, shoe, sole
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0  %0
+$  card  card:agent:shoe
+$  command  @t
--
%-  agent:dbug
=|  state-0
=*  state  -
^-  agent:gall
%-  (agent:shoe command)
^-  (shoe:shoe command)
|_  =bowl:gall
+*  this     .
    default  ~(. (default-agent this %|) bowl)
    leather  ~(. (default:shoe this command) bowl)
++  on-init   on-init:default
++  on-save   !>(state)
++  on-load
  |=  old=vase
  ^-  (quip card _this)
  `this(state !<(state-0 old))
++  on-poke   on-poke:default
++  on-peek   on-peek:default
++  on-arvo   on-arvo:default
++  on-watch  on-watch:default
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
++  command-parser
  |=  =sole-id:shoe
  ^+  |~(nail *(like [? command]))
  (stag & (boss 256 (more gon qit)))
++  on-command
  |=  [=sole-id:shoe =command]
  ^-  (quip card _this)
  :_  this
  ^-  (list card)
  :~  :+  %shoe  ~
  ^-  shoe-effect:shoe
  :-  %sole
  ^-  sole-effect:sole  :-  %klr
  ^-  styx
  =/  idx  0
  =|  fx=styx
  =/  rng  ~(. og eny:bowl)
  |-
  ?:  =(80 idx)  fx
  =^  huer  rng  (rads:rng 256)
  =^  hueg  rng  (rads:rng 256)
  =^  hueb  rng  (rads:rng 256)
  %=  $
    idx  +(idx)
    fx   `styx`(weld fx `styx`~[[[`%br ~ `[r=`@ux`huer g=`@ux`hueg b=`@ux`hueb]] command ~]])
  ==  ==
++  can-connect
  |=  =sole-id:shoe
  ^-  ?
  ?|  =(~zod src.bowl)
      (team:title [our src]:bowl)
  ==
++  on-connect     on-connect:leather
++  on-disconnect  on-disconnect:leather
++  tab-list       tab-list:leather
--
```

- [~lagrev-nocfep, `sigilante/track7`](https://github.com/sigilante/track7)
- [App Guide, “Command-Line Apps”](https://developers.urbit.org/guides/additional/cli-tutorial)


##  Tutorial:  Building a CLI App

We will utilize the basic calculator app logic from the [parsing guide](https://developers.urbit.org/guides/additional/parsing#recursive-parsers) to produce a linked calculator agent `%rpn` supporting the following operators by the appropriate parsers:

- numbers (as `@rs` without `.` dot prefix) (`royl-rs:so`)
- `+` lus, addition (`lus`)
- `-` hep, subtraction (`hep`)
- `*` tar, multiplication (`tar`)
- `/` fas, division (`fas`)
- `.` dot, display top of stack (`dot`)
- `..` dotdot, display entire stack (`(jest '..')`)

We will leave all regular Gall arms as their defaults, but of course poking, subscribing, and peeking should be supported in a full application.

### Agent logic

**`/sur/rpn.hoon`**

We just need to define the expected operators that will show up in the stack.  These are `@t` text constants.

```hoon
|%
+$  op  $?  [%op %add]
            [%op %sub]
            [%op %mul]
            [%op %div]
            [%op %sho]
            [%op %all]
        ==
+$  num  @rs
+$  command  ?(@rs op)
--
```

(`+$command` doesn't really feel like the right name here, but we're pattern-matching with the demo `/app/shoe.hoon`.)

**`/lib/rpn.hoon`**

These are the parsing rules that the CLI agent will use.  We could include these directly in the agent file but we'll post them to a library file.

```hoon
|%
++  num     royl-rs:so
++  op-add  (cook |=(p=@ ?:(=('+' p) op+%add ~)) lus)
++  op-sub  (cook |=(p=@ ?:(=('-' p) op+%sub ~)) hep)
++  op-mul  (cook |=(p=@ ?:(=('*' p) op+%mul ~)) tar)
++  op-div  (cook |=(p=@ ?:(=('/' p) op+%div ~)) fas)
++  op-sho  (cook |=(p=@ ?:(=('.' p) op+%sho ~)) dot)
++  op-all  (cook |=(p=@ ?:(=('..' p) op+%all ~)) (jest '..'))
++  ops     ;~(pose op-add op-sub op-mul op-div op-sho op-all)
--
```

**`/app/rpn.hoon`**

```hoon
++  state-0
  $:  %0
      stack=(list ?(@rs op:rpn))
  ==
```

**`++command-parser`**

We want this arm to wait until `RETURN` is pressed so we `++stag` the value with `|` `FALSE`/`%.n`.

```hoon
++  command-parser
  |=  =sole-id:shoe
  ^+  |~(nail *(like [? command:rpn]))
  %+  stag  |
  (cook command:rpn ;~(pose num:rpnlib ops:rpnlib))
```

**`++on-command`**

This arm pushes values onto the stack, displays the stack, then checks to parse for the result of an operation.

```hoon
++  on-command
  |=  [=sole-id:shoe =command:rpn]
  ^-  (quip card _this)
  =/  old-stack  (weld stack ~[command])
  =/  new-stack  (process:rpnlib old-stack)
  :_  this(stack new-stack)
  :~  [%shoe ~ sole+klr+~[(crip "{<old-stack>} →")]]
      [%shoe ~ sole+klr+~[[[`%br ~ `%g] (crip "{<new-stack>}") ~]]]
  ==
```

For this we add a helper arm to `/lib/rpn.hoon` which takes each entry, makes sure it is a `@rs` atom, and carries out the operation.  (This could probably be made more efficient.)

**`/lib/rpn.hoon`**

```hoon
/-  rpn
:: * * *
++  process
  |=  stack=(list command:rpn)
  ^-  (list command:rpn)
  ~|  "Failure processing operation on stack {<stack>}"
  ?~  stack  !!
  ?-    `command:rpn`(snag 0 (flop stack))
      [%op %add]
    =/  augend        ;;(@rs `command:rpn`(snag 1 (flop stack)))
    =/  addend        ;;(@rs `command:rpn`(snag 2 (flop stack)))
    (flop (weld ~[(add:rs augend addend)] (slag 3 (flop stack))))
    ::
      [%op %sub]
    =/  minuend       ;;(@rs `command:rpn`(snag 1 (flop stack)))
    =/  subtrahend    ;;(@rs `command:rpn`(snag 2 (flop stack)))
    (flop (weld ~[(sub:rs minuend subtrahend)] (slag 3 (flop stack))))
    ::
      [%op %mul]
    =/  multiplicand  ;;(@rs `command:rpn`(snag 1 (flop stack)))
    =/  multiplier    ;;(@rs `command:rpn`(snag 2 (flop stack)))
    (flop (weld ~[(mul:rs multiplicand multiplier)] (slag 3 (flop stack))))
    ::
      [%op %div]
    =/  numerator     ;;(@rs `command:rpn`(snag 1 (flop stack)))
    =/  denominator   ;;(@rs `command:rpn`(snag 2 (flop stack)))
    (flop (weld ~[(div:rs numerator denominator)] (slag 3 (flop stack))))
    ::
      [%op %sho]
    ~&  >  "{<(snag 1 (flop stack))>}"
    (flop (slag 1 (flop stack)))
    ::
      [%op %all]
    ~&  >  "{<stack>}"
    (flop (slag 1 (flop stack)))
    ::
      @rs
    stack
  ==
```

(Edit:  it looks like `'..'` isn't picking up properly in this version.)

### Linking

After a `%sole` agent has been `|install`ed, it should be registered for Dojo to cycle input to it using `|link`.

```hoon
|link %rpn
```

Now `Ctrl`+`X` allows you to switch to that app and evaluate expressions using it.

```hoon
gall: booted %rpn
> 50
~ →
~[.50]

> 25
~[.50] →
~[.50 .25]

> -
~[.50 .25] →
~[.-25]

> 5
~[.-25] →
~[.-25 .5]

> /
~[.-25 .5] →
~[.-0.19999999]

> 5
~[.-0.19999999] →
~[.-0.19999999 .5]

> *
~[.-0.19999999 .5] →
~[.-0.99999994]

> 1
~[.-0.99999994] →
~[.-0.99999994 .1]

> /
~[.-0.99999994 .1] →
~[.-1]
```

- [~lagrev-nocfep, `sigilante/rpn`](https://github.com/sigilante/rpn)


##  Exercises

- Extend the calculator app to support modulus as `%` cen.
- Extend the calculator app so it instead operates on `@rd` values.  Either use `++cook` to automatically convert the input values from a `1.23`-style input to the `.~1.23` `@rd` style or build a different input parser from the entries in `++royl:so`.
- Extend the calculator app so that it can support named variables (using `@tas`) with `=` tis.  What new data structure do you need?  For convenience, expose the result of the last operation as `ans` (a feature of TI graphing calculators and MATLAB, among other programs).
- The calculator app stack isn't really a proper CS stack with push and pop operations.  Refactor it to use such a type.
- **Challenge**.  Produce a tic-tac-toe CLI agent which allows two people to play a game, including detecting the win condition.
