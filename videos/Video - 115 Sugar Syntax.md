---
uuid: 115
layout: node
title: "Irregular forms, sugar syntax"
tags:
 - "%hoon"
prerequisites:
  - "113"
postrequisites:
  - "120"
  - "175"
  - "201"
  - "215"
  - "250"
objectives:
  - "Identify current known irregular syntax."
  - "Convert between regular and irregular forms of runes to date."
runes: []
irregular:
  - "()"
key_points: []
assessments: []
comments: ""
content: ""
---

#   Sugar Syntax

At this point, we have striven to work with Hoon only using runes, except for a couple of simple cases like using brackets for a cell.

```hoon
> :-  1  2
[1 2]
```

Hoon has a rich repertoire of sugar syntax, or irregular forms that reduce to rune expressions but are more straightforward to compose.  For instance, as we see here, `:-` colhep is commonly written using square brackets, which more intuitively read as cells to a developer.

Another example 
