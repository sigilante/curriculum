---
uuid: 140
layout: node
title: "Lists, trees"
tags:
 - "%stdlib"
prerequisites:
  - "135"
postrequisites:
  - "145"
objectives:
  - "Use lists to organize data."
  - "Convert between kinds of lists (e.g. tapes)."
  - "Diagram lists as binary trees."
  - "Operate on list elements using `snag`, `find`, `weld`, etc."
runes: []
irregular:
  - "~[]"
key_points: []
assessments: []
comments: ""
content: ""
---

#   Lists

A list is the simplest way of organizing a flexible number of values.  The values in a list have an order, or a numerical index, and the list ends with Hoon's `~` sig null value.  To make a list, you can use the special `~[]` sig-bracket notation along with a list type.

```hoon
> =my-list `(list @ud)`~[1 2 3 4 5]
~[1 2 3 4 5]
```

Lists of atoms will convert all members to the same aura or type.

The head of a list is marked with the face `i` and the tail of the list marked with `t`.  There are a variety of list-related helper functions, such as `++snag` which retrieves the element at a given list index counting from zero.

```hoon
> (snag 3 my-list)
4
```

Since lists are composed of rightwards-branching nested tuples, the tree address of each subsequent element is equal to a power of two minus two:

```hoon
> =my-list `(list @ud)`~[1 2 3]

> +2:my-list
i=1

> +6:my-list
i=2

> +14:my-list
i=3

> +15:my-list
t=~
```

Perhaps confusingly, a Hoon list is not just structurally defined.  You can have a null-terminated tuple that some list functions will accept without questions, but for others you will need to explicitly cast it as a list first.  The best practice is to cast as a list frequently since this introduces no runtime overhead in your code.

```hoon
> (snag 3 ~[1 2 3 4 5])
mull-grow
-need.[i=@ud t=%~]
-have.%~
nest-fail
dojo: hoon expression failed
```

You can also use `++limo` to produce a list:

```hoon
> (limo ~[1 2 3 4 5])
[i=1 t=[i=2 t=[i=3 t=[i=4 t=[i=5 t=~]]]]]

> (snag 3 (limo ~[1 2 3 4 5]))
4
```

After cells, lists serve as the next most common data container in Hoon, and there is a rune, `:~` colsig, dedicated to building null-terminated tuples easily converted to regular lists.

```hoon
> :~(1 2 3 4 5)
[1 2 3 4 5 ~]

> `(list @)`:~(1 2 3 4 5)
~[1 2 3 4 5]
```
