---
title: "Database Structures"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Learn how Hoon represents structured data for easy lookup."
runes: []
keypoints: []
readings:
  - "https://developers.urbit.org/reference/hoon/stdlib/1b"
  - "https://developers.urbit.org/reference/hoon/stdlib/2i"
  - "https://developers.urbit.org/reference/hoon/stdlib/2o"
  - "https://developers.urbit.org/reference/hoon/stdlib/2m#mynl"
homework: []
mirror: []
video: []
---

#   🖭 `awl3`. Database Structures

Over the course of this and the following lesson, we will build a little database, `%rkyv`, which implements the backend and SQL-like instructions necessary to operate on the stored data.  In this lesson, we will start by examining the `tree` and `map` data structures, then proceed to build a simple database operable by explicit pokes.  In the next lesson, we will examine some database implementations like `urQL` and TomeDB, as well as build a simple grammar with our `%rkyv` database.


##  `tree`

`++tree` is defined as a mold generator which receives a type and produces a logical mold describing a binary [tree](https://en.wikipedia.org/wiki/Tree_%28data_structure%29) of values and left and right elements.  It is recursively defined as:

```hoon
++  tree
  |$  [node]
  $@(~ [n=node l=(tree node) r=(tree node)])
```

(The `[]` around the `spec` for the mold builder appear to be superfluous.)

The `$@` bucpat rune switches on the sample as an atom—if an atom, then `~`, else a recursive subtree.  `$@` bucpat is useful here in producing `~` empty nodes when there is no content in a node.

If we generate this tree:

```hoon
> `(tree @)`[1 [2 ~ ~] ~]
{2 1}
```

then it corresponds in structure to

```
    1
   / \
  2   ~
 / \
~   ~
```

A [binary tree](https://en.wikipedia.org/wiki/Binary_tree) like this allows for flexibility in defining branched storage structures.  Each node can have a value and a left child and a right child.  (Note that this differs from the standard noun binary tree concept, in which there is a value OR a pair of children.)  Trees are preferred where hierarchical data are being represented.  Hoon will use `tree` most notably to define `set`s and `map`s, both of which are also mold generators.

Trees need to support the following operations:

- Enumeration of items
- Searching for items
- Addition or deletion of items
- Pruning or grafting of entire subtrees
- Finding the common ancestor of two nodes

Tree traversal is commonly used to enumerate or search for items, as well as to find common ancestors.

### Example:  Depth-First Search of Tree

Given a `(tree @)`, locate the first time a value occurs in a depth-first search.  A depth-first search (DFS) means that we descend into the left subtree first before moving across to the right subtree.

1. Check the current node for the value.
2. Look left.  If not null, descend left and DFS again.
3. Look right.  If not null, descend right and DFS again.
4. If both null, ascend.

**Translate `tree` address to numeric address**.  Given a value in a `tree`, return the numeric address corresponding to its position as a `(unit @ud)` (or `~` for absent).  This assumes a `(tree @)` and must be modified for other data types.

```hoon
|%
++  search
    |=  [=(tree @) nedl=@]
    ^-  (unit @ud)
    =/  dept  1
    |-  ^-  (unit @ud)
    ~&  >  tree
    ?~  tree  ~
    ?:  =(nedl n.tree)  (some (peg dept 2))
    =/  l  $(tree l.tree, dept (peg dept 6))
    ?~  l
      $(tree r.tree, dept (peg dept 7))
    l
--
```

**Convert a `tree` to a DFS-ordered `list`**.  For instance, this gate will flatten a tree `[1 [2 [3 ~ ~] [4 ~ ~]] [5 [6 ~ ~] ~]]` to the list `~[1 2 3 4 5 6]`.

```hoon
|%
++  is-null  |=(p=@ ?~(p %.y %.n))
++  flatten
  |=  =(tree @)
  ^-  (list @)
  ?~  tree  *(list @)
  =/  l  (skip (flatten l.tree) is-null)
  =/  r  (skip (flatten r.tree) is-null)
  [n.tree (welp l r)]
--
```

### Challenge:  Breadth-First Search of Tree

Modify the DFS algorithm such that the `tree` is converted to a `list` by breadth first; that is, all nodes at a given depth should be included before any at a deeper depth are listed.

### Challenge:  Number Nodes in a Binary Tree

Every noun is a simple binary tree.  A `tree` is actually a bit more complex since at each level it can include its own data as well as children.

Produce a gate which accept a cell of data and produces a cell of the _addresses_ of each value at the same location.

For instance, given the cell

```hoon
[[%a %b] [%c [%d %e]]]
```

this gate should produce the address cell

```
[[4 5] [6 [14 15]]]
```

Similarly, `"Hello Mars!"` should produce `~[2 6 14 30 62 126 254 510 1022 2046 4094]`.


##  `++map` and `++by`

To understand data storage and database behavior, we should start with the simplest key–value store which Urbit supports:  the `map`.  In computer science generally, a map is an association of key–value pairs, or a lookup table.  A lookup table is often structured as a hash table or search tree; here, it is a binary search tree based on the hash of the key.

### `map` structure

`map` is itself a mold builder, accepting two molds as values and producing a type relating them.

The relevant definitions from `/sys/hoon.hoon` are:

```hoon
++  tree
  |$  [node]
  $@(~ [n=node l=(tree node) r=(tree node)])

++  map
  |$  [key value]
  $|  (tree (pair key value))
  |=(a=(tree (pair)) ?:(=(~ a) & ~(apt by a)))
```

You can see that a `map` is a `(tree pair key value)` and thus the actual layout of a map can be obtained as a tree:

```hoon
> =colors `(map @tas @ux)`(my ~[[%red 0xed.0a3f] [%yellow 0xfb.e870] [%green 0x1.a638] [%blue 0x66ff]])
> -:colors
n=[p=%green q=0x1.a638]
> +:colors
[ l=[n=[p=%blue q=0x66ff] l={[p=%red q=0xed.0a3f]} r={}]
  r=[n=[p=%yellow q=0xfb.e870] l={} r={}]
]
> +<:colors
l=[n=[p=%blue q=0x66ff] l={[p=%red q=0xed.0a3f]} r={}]
> +>:colors
r=[n=[p=%yellow q=0xfb.e870] l={} r={}]
> +<-:colors
n=[p=%blue q=0x66ff]
> +<+:colors
[l={[p=%red q=0xed.0a3f]} r={}]
```

is laid out structurally as

```
                          [%green 0x66ff]
                         /               \
           [%blue 0x66ff]                 [%yellow 0xfb.e870]
          /              \               /                   \
  [%red 0xed.0a3f]        ~             ~                     ~
 /                \
~                  ~
```

(This implies that there are many structural trees that could behave as `map`s, on which more in a moment.)

The mold-builder runes involved in the definition of `++map` include:

- `|$` barbuc is a “wet gate” mold builder.  A [wet gate](https://developers.urbit.org/guides/core/hoon-school/R-metals#wet-gates) is a bit more like a macro in that it is more flexible with type—it simply replaces the sample rather than coerces.
- `$|` bucbar is a structure validator, here making sure that we actually have a `(tree (pair key value))` coming out of the gate below.

The validator gate then takes a tree of `(pair)` (the bunt) and asserts that the value is emtpy (`~` is a valid `map`) or that the tree satisfies `++apt:by`, which does the heavy lifting to check correctness.

### `++apt:by`

[`++apt:by`](https://developers.urbit.org/reference/hoon/stdlib/2i#aptby) actually checks the horizontal and vertical ordering of the tree.   There are several valid ways to order nouns in Hoon orthodoxy:

- `++aor` produces alphabetical ordering.
- `++dor` refers to depth ordering.
- `++gor` is mug ordering, or numerically in order by hash.
- `++mor` is doubly-ordered by mug, or `(mug (mug a))`.

Why bother with a `map` instead of a `list`?  The main reason:  `map` lookup times are substantially faster.  In average-case time, a `list` lookup will be $O(n)$ while a `map` lookup will be $O(\log n)$ (assuming a balanced map).  The use of hash ordering on keys (rather than alphabetical) also randomizes the order and tends to balance the tree more naturally.

So `++apt:by` needs to check whether the left subtree at each node is numerically less, by mug order, than the node value, and that the node value is numerically less, by mug order, than the right subtree.  Then it checks recursively on the doubly-ordered mug value.  If all of these are not true, then the tree is unbalanced and not a valid `map` per Hoon's requirements.

```hoon
++  apt
  =<  $
  ~/  %apt
  =|  [l=(unit) r=(unit)]
  |.  ^-  ?
  ?~  a   &
  ?&  ::  check horizontal ordering
      ?~(l & &((gor p.n.a u.l) !=(p.n.a u.l)))
      ?~(r & &((gor u.r p.n.a) !=(u.r p.n.a)))
      ::  check vertical ordering of each subtree
      ?~(l.a & &((mor p.n.a p.n.l.a) !=(p.n.a p.n.l.a) $(a l.a, l `p.n.a)))
      ?~(r.a & &((mor p.n.a p.n.r.a) !=(p.n.a p.n.r.a) $(a r.a, r `p.n.a)))
  ==
```

The reference example produces two `map`s which are almost identical except for one key; this is sufficient to render one of them an invalid `map`.

```hoon
> =a (malt `(list [@tas @])`~[a+1 b+2 c+3 d+4 e+5])

> ~(apt by a)
%.y

> =z ?~(a ~ a(p.n `@tas`%z))

> z
[n=[p=%z q=2] l={[p=%e q=5]} r={[p=%d q=4] [p=%a q=1] [p=%c q=3]}]

> ~(apt by z)
%.n
```

Because the ordering is wrong, the `map` lookup functions in `++by` fail unpredictably:

```hoon
> z
[ n=[p=%z q=2]
  l=[n=[p=%e q=5] l=~ r=~]
  r=[n=[p=%d q=4] l=~ r=[n=[p=%c q=3] l={[p=%a q=1]} r={}]]
]

> (~(got by z) %z)
2

> (~(got by z) %a)
1

> (~(got by z) %c)
3

> (~(got by z) %d)
dojo: hoon expression failed

> (~(got by z) %e)
5

> a
[ n=[p=%b q=2]
  l=[n=[p=%e q=5] l=~ r=~]
  r=[n=[p=%d q=4] l=~ r=[n=[p=%c q=3] l={[p=%a q=1]} r={}]]
]

> (~(got by a) %d)
4
```

### `++get:by`

Next, let's look inside `++get:by` and see why this is.

```hoon
++  get
  ~/  %get
  |*  b=*
  =>  .(b `_?>(?=(^ a) p.n.a)`b)
  |-  ^-  (unit _?>(?=(^ a) q.n.a))
  ?~  a
    ~
  ?:  =(b p.n.a)
    (some q.n.a)
  ?:  (gor b p.n.a)
    $(a l.a)
  $(a r.a)
```

It turns out that `++get:by` uses `++gor` internally to correctly identify the subtree in which the value would be located.  Searching for a key which is not present is useless.

It's easiest to read the logic of `++get:by` from the lower checks upwards.  At the bottom, we see whether the sought-for key exists at a given node, and if not a dispatch to the left or right based on mug order.  If the key is not present when we get to the bottom, then return `~`.  The trap return type is `(unit _?>(?=(^ a) q.n.a))`; in other words, a unit of the type of the value after assertion that there is a key–value pair.

This little statement is rather wild:  ``.(b `_?>(?=(^ a) p.n.a)`b)``.  What it says is to recalculate the current subject by replacing `b` with the unit of the sought-for value, including a type assertion.  (The `` ` `` tic marks are a `^-` kethep fence.)

### `++put:by`

Let's see `++put:by`.

```hoon
++  put
  ~/  %put
  |*  [b=* c=*]
  |-  ^+  a
  ?~  a
    [[b c] ~ ~]
  ?:  =(b p.n.a)
    ?:  =(c q.n.a)
      a
    a(n [b c])
  ?:  (gor b p.n.a)
    =+  d=$(a l.a)
    ?>  ?=(^ d)
    ?:  (mor p.n.a p.n.d)
      a(l d)
    d(r a(l r.d))
  =+  d=$(a r.a)
  ?>  ?=(^ d)
  ?:  (mor p.n.a p.n.d)
    a(r d)
  d(l a(r l.d))
```

This is more complicated because entries will need to be moved based on the inserted key.  Essentially, the code has to handle four cases:

1. No value in current node.  Just insert the key–value pair.
2. The value at the current node matches the current key.  Insert the key–value pair to replace the value.
3. The value of the current node is greater than or less than the current value.  If we're at the bottom, insert a single node of the current node's value and the new value.
4. The value of the current node is greater than or less than the current value.  If we're not at the bottom, dispatch the value recursively into the left or right daughter subtree.

What does insertion look like?  Let's suppose we have the following values in a `(map @tas @t)`:

```
┌───────────────────┐
│ KEY: %alpha       │
│ HASH: 0x1145.072a │
│ VALUE: 'α'        │
└───────────────────┘
┌───────────────────┐
│ KEY: %beta        │
│ HASH: 0x1a5a.d725 │
│ VALUE: 'β'        │
└───────────────────┘
┌───────────────────┐
│ KEY: %gamma       │
│ HASH: 0x766b.d36e │
│ VALUE: 'γ'        │
└───────────────────┘
```

These will insert in this order:

```
> =greek `(map @tas @t)`(my `(list (pair @tas @t))`~[[%alpha 'α'] [%beta 'β'] [%gamma 'γ']])

> greek
[n=[p=%alpha q='α'] l=~ r=[n=[p=%beta q='β'] l={} r={[p=%gamma q='γ']}]]

                             n=[p=%alpha q='α']
                            /                  \
                           ~               [p=%beta q='β']
                                          /               \
                                         ~          [p=%gamma q='γ']
```

Now we wish to add the key–value pair:

```
┌───────────────────┐
│ KEY: %delta       │
│ HASH: 0x7e4c.d602 │
│ VALUE: 'δ'        │
└───────────────────┘
```

By the hash, this will sort after `%gamma`.  Based on our cases above, this looks like #3.  The new tree will be:

```
> (~(put by greek) %delta 'δ')
[ n=[p=%alpha q='α']
  l=~
  r=[n=[p=%beta q='β'] l=~ r=[n=[p=%delta q='δ'] l={[p=%gamma q='γ']} r={}]]
]

                             n=[p=%alpha q='α']
                            /                  \
                           ~               [p=%beta q='β']
                                          /               \
                                         ~          [p=%delta q='δ']
                                                   /                \
                                         [p=%gamma q='γ']            ~
```

Add the key–value pair:

```
┌───────────────────┐
│ KEY: %epsilon     │
│ HASH: 0x41e4.d385 │
│ VALUE: 'ε'        │
└───────────────────┘
```

By the hash, this will sort between `%beta` and `%gamma`.  The new tree will be:

```
> (~(put by (~(put by greek) %delta 'δ')) %epsilon 'ε')
[ n=[p=%alpha q='α']
  l=~
    r
  [ n=[p=%beta q='β']
    l=~
      r
    [ n=[p=%epsilon q='ε']
      l=~
      r=[n=[p=%delta q='δ'] l={[p=%gamma q='γ']} r={}]
    ]
  ]
]

                             n=[p=%alpha q='α']
                            /                  \
                           ~               [p=%beta q='β']
                                          /               \
                                         ~          [p=%epsilon q='ε']
                                                   /                \
                                         [p=%delta q='δ']          ~
                                        /                  \
                              [p=%gamma q='γ']              ~
```

(This tree is in fact becoming somewhat unbalanced, but it's not so deep yet and we trust in the law of large numbers to save us should we continue.)


### `++my`

How does `++my` build a `map`?

```hoon
++  le                                                ::  construct list
  |*  a=(list)
  ^+  =<  $
    |@  ++  $  ?:(*? ~ [i=(snag 0 a) t=$])
    --
  a
++  my                                                ::  construct map
  |*  a=(list (pair))
  =>  .(a ^+((le a) a))
  (~(gas by `(map _p.i.-.a _q.i.-.a)`~) a)
```

`++gas:by` is itself a recursive `++put:by` call, so aside from some tetchy logic to satisfy the typechecker this makes sense.

The old `map` builder, `++malt`, is still available but has been informally deprecated.  Why?

```hoon
++  malt                                                ::  map from list
 |*  a=(list)  
 (molt `(list [p=_-<.a q=_->.a])`a)  
::            
++  molt                                                ::  map from pair list  
 |*  a=(list (pair))  ::  ^-  =,(i.-.a (map _p _q))  
 (~(gas by `(tree [p=_p.i.-.a q=_q.i.-.a])`~) a)
```

For one thing, it's more complicated.  It also doesn't explicitly cast to `map`.  `++my` also does the equivalent of homogenize (`++homo`) the list first.  (~master-morzod recommends just using `++gas:by` directly to build a `map` from a `list`.)


##  Databases

How does a database differ from a map?  Well, the simplest database is just a hash table, which Hoon implements as a `map`.  So in a sense we're already there at the shallow end.  Databases also implement logic over the top for queries and management (what we'll call a database management system or DBMS).

There are several ways to structure a [database](https://en.wikipedia.org/wiki/Database):

1. Navigational DBMS
2. Relational DBMS (SQL)
3. Object–relational DBMS
4. Document-oriented DBMS (NoSQL)

The architecture for a particular application is determined by a balance of representation and querying.  Classically, a database is a [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) program:  Create, Read, Update, Delete.  The most complicated of these in most applications is `Read` since the lookup logic for desired data can grow to be quite involved.  (This is much of the value of SQL, for instance.)

If we want to implement a database in Urbit, we need a few components:

1. Interface (REPL or code, text to action)
2. Command processor (action to event)
3. Database backend (event to data)

(There's our old friend the CLI again!  Altho in practice we'll want an HTTP API and a JSON output.  Input pokes can come in our regular grammar and we'll process them as such.)

In this lesson, we'll conclude by producing the database superstructure and some I/O logic.  Next time, we'll build this out with some query logic.

**WIP logic which we'll elaborate on next time**

**`/sur/rkyv.hoon`**

```hoon
|%
+$  key  @tas
+$  value
  $%  [%xml body=manx]
      [%json body=json]
      [%yaml body=@t]
      [%txt body=@t]
  ==
+$  store  (map key value)
+$  cursor  @ud
+$  action
  $%  [%create =key =value]
      [%retrieve =key]
      [%update =key =value]
      [%destroy =key]
  ==
+$  result
  $%  [%store =store]
      [%value =value]
      [%delete =key]
  ==
--
```

Later on we'll look at how to generate multi-key retrieval actions.  [`+$cursor`](https://cstack.github.io/db_tutorial/parts/part6.html) will form the basis for this.

**`/mar/rkyv/action.hoon`**

```hoon
/-  rkyv
::
|_  axn=action:rkyv
::
++  grad  %noun
++  grow
  |%
  ++  noun  axn
  --
++  grab
  |%
  ++  noun  action:rkyv
  --
--
```

**`/mar/rkyv/result.hoon`**

```hoon
/-  rkyv
::
|_  res=result:rkyv
::
++  grad  %noun
++  grow
  |%
  ++  noun  res
  --
++  grab
  |%
  ++  noun  result:rkyv
  --
--
```

**`/app/rkyv/.hoon`**

```hoon
/-  *rkyv
/+  default-agent, dbug
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0
  $:  [%0 =store]
  ==
+$  card  card:agent:gall
--
%-  agent:dbug
=|  state-0
=*  state  -
^-  agent:gall
|_  =bowl:gall
+*  this     .
    default  ~(. (default-agent this %|) bowl)
++  on-init   on-init:default
++  on-save   !>(state)
++  on-load
  |=  old=vase
  ^-  (quip card _this)
  `this(state !<(state-0 old))
++  on-poke
  |=  [=mark =vase]
  ^-  (quip card _this)
  ?>  =(our src):bowl
  ?>  ?=(%rkyv-action mark)
  =/  act  !<(action vase)
  ?-    -.act
      %create
    :_  this(store (~(put by store) key.act value.act))
    :~  [%give %fact ~[/store] %rkyv-result !>(store)]
        [%give %kick ~[/store] ~]
    ==
  ::
      %retrieve
    :_  this
    :~  [%give %fact ~[/store] %rkyv-result !>(value+(~(get by store) key.act))]
        [%give %kick ~[/store] ~]
    ==
  ::
      %update
    :_  this(store (~(put by store) key.act value.act))
    :~  [%give %fact ~[/store] %rkyv-result !>(value+value.act)]
        [%give %kick ~[/store] ~]
    ==
  ::
      %destroy
    :_  this(store (~(del by store) key.act))
    :~  [%give %fact ~[/store] %rkyv-result !>(delete+key.act)]
        [%give %kick ~[/store] ~]
    ==
  ==
::
++  on-peek
  |=  =path
  ^-  (unit (unit cage))
  ?+  path  (on-peek:default path)
    [%x %store ~]  ``noun+!>(store)
    [%x %key @ ~]  ``noun+!>((~(gut by store) `key`+>-:path %null))
  ==
++  on-arvo   on-arvo:default
++  on-watch
  |=  =path
  ^-  (quip card _this)
  ?+    path  (on-watch:default path)
      [%store ~]
    :_  this
    :~  [%give %fact ~ %rkyv-result !>(store+store)]
    ==
  ::
      [%key @ ~]
    :_  this
    :~  [%give %fact ~ %rkyv-result !>(value+(~(gut by store) `key`+>-:path %null))]
    ==
  ==
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```


##  Exercises

- Analyze `set` and `++in` in the same manner as the `map` discussion.
- Produce a version of `++map` and `++by` (let's call them `++kan` and `++ye`) which sorts the tree based on alphabetically ordered keys.  Implement `++put`, `++get`, and `++apt`.
- Implement [Ted Nelson's ZigZag data structure](https://en.wikipedia.org/wiki/ZigZag_%28software%29) in Hoon.
