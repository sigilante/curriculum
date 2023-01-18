---
uuid: 110
layout: node
title: "Syntax, nouns, auras"
tags:
 - "%hoon"
prerequisites:
  - "100"
  - "103"
postrequisites:
  - "112"
  - "113"
objectives:
  - "Distinguish nouns, cells, and atoms."
  - "Apply auras to transform an atom."
  - "Identify common Hoon molds, such as cells, lists, and tapes."
  - "Annotate Hoon code with comments."
runes:
  - "::"
irregular:
  - "@"
  - "[]"
  - "~[]"
  - "''"
  - "\"\""
key_points: []
assessments: []
comments: ""
content: ""
---

#   Basic Syntax

Hoon programs, like molecules, graphs, and mathematical expressions, consist of values connected by operators.

Hoon values include simple _atoms_, including text, numbers, dates, ship names, and boolean values.  Hoon values can also be _cells_, pairs of two other values.  We call all Hoon values _nouns_.

Hoon operators are called _runes_.  Runes define relationships between nouns much like verbs.  Each rune takes a number of daughter expressions:  these can be more rune expressions, simple atom values, or cell-based structures.  Runes are written using two ASCII characters, such as `?:` wutcol or `:-` colhep.

If you open up any Hoon program, you can learn to see values

(highlight text)

and runes, including irregular forms

(highlight other text)

```hoon
::  |new-desk: creates a minimal desk                                                                 
::
/+  *generators
::
:-  %ask
|=  $:  [now=@da eny=@uvJ bek=beak]
        [=desk ~]    
        [from=$~(%base desk) hard=_|]
    ==
::    
=;  make-new-desk
  ?.  ?&  !hard
          (~(has in .^((set ^desk) %cd (en-beam bek(q %$) /))) desk)
      ==  
    (make-new-desk)
  %+  print    (rap 3 'the desk %' desk ' already exists. overwrite it?' ~)
  %+  prompt   [%& %prompt "overwrite? (y/N) "]
  |=  in=tape
  ?.  |(=("y" in) =("Y" in) =("yes" in))
    no-product
  (make-new-desk)
::
|.  %-  produce
:-  %helm-pass
%^  new-desk:cloy  desk
```

Comments are encouraged to illuminate the reasoning process, but are not formally part of the Hoon source.

(highlight text)

Some Hoon values are text

(highlight text, `''`, `""`, `%`)

and some are numbers.

(highlight numbers)

Others refer to code, like functions defined elsewhere.

(highlight gates and faces)

Even tho Hoon can appear intimidating at first, Hoon School will walk you through the process of learning how to read and understand Hoon code quickly.
