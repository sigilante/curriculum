---
uuid: 183
layout: node
title: "Sets, maps, jars, jugs"
tags:
 - "%hoon"
prerequisites:
  - "150"
postrequisites:
  - "233"
  - "263"
  - "283"
  - "284"
  - "333"
objectives:
  - "Identify units, sets, maps, and compound structures like jars and jugs."
  - "Explain why units and vases are necessary."
  - "Use helper arms and syntax:  `` ` ``, `biff`, `some`, etc."
runes: []
irregular: []
key_points: []
assessments: []
comments: |
    "<!-- 2a -->"
content: ""
---

#   Units

A `+$unit` is a type employed to distinguish an empty response from no response.  This lesson covers how to construct and interact with `unit`s ahead of using them in earnest when discussing `map`s and `set`s.

Suppose we need to retrieve a value from a data collection.  If the value is zero, you should receive a zero in return.  But if the value is not present, what should happen?  One option is to crash, but this would be a disruptive design pattern.  Instead, Hoon prefers to return either a bare null value (if the value is absent) or a cell with null head (if the value is present).

A `unit` can be built using either the special `` ` `` tic notation or `++some`:

```hoon
> `%mars
[~ %mars]

> (some %mars)
[~ %mars]
```

`++need` reduces a `unit` to its bare associated value, or its tail.  If a `unit` has been returned as null, then `++need` will crash.

```hoon
> (need `%mars)
%mars

> (need ~)
dojo: hoon expression failed
```

Some tools like `++biff` and `++bind` allow functions which do not recognize `unit`s to seamlessly be applied to or produce `unit`s.

```hoon
> (bind )
```

Unit logic allows you to compose more agile code when using `map`s, `set`s, and other compound data structures.  In addition, `unit`s result from many kinds of network and agent operations which may be liable to failure.

---

#   Maps and Sets

Cores can be composed with varying degrees of complexity and nesting.  Let's examine how `+$map`s and `+$set`s instrument cores to serve as accessible persistent data structures.

A `map` is a pattern from a key to a value.  Like a dictionary or an index, we can use a `map` to associate data to a lookup key.  Essentially it scans for a particular key, then returns the data associated with that key (which may be any noun).

We can build a `map` from a list of pairs of keys and values with `++malt`.  A `map` doesn't have an order, so the elements may appear in any order depending on how the `map` was built.

```hoon
> =greek (malt `(list (pair @tas @t))`~[[%alpha 'α'] [%beta 'β'] [%gamma 'γ'] [%delta 'δ']])

> greek
[n=[p=p=%alpha q=q='α'] l={} r={[p=p=%beta q=q='β'] [p=p=%gamma q=q='γ'] [p=p=%delta q=q='δ']}]
```

`+$map` operations are provided by the `++by` core.

We can use `++put:by` to insert a new key into the `map`.  Since Hoon as a functional programming language represents all values as immutable, to modify a `map` we actually make a copy with the change.

```hoon
> (~(put by greek) [%epsilon 'ε'])
[ n=[p=p=%alpha q=q='α']
  l=~
    r
  [n=[p=p=%beta q=q='β'] l={} r={[p=p=%epsilon q=q='ε'] [p=p=%gamma q=q='γ'] [p=p=%delta q=q='δ']}]
]

> greek
[n=[p=p=%alpha q=q='α'] l={} r={[p=p=%beta q=q='β'] [p=p=%gamma q=q='γ'] [p=p=%delta q=q='δ']}]

> =greek (~(put by greek) [%epsilon 'ε'])

> greek
[ n=[p=p=%alpha q=q='α']
  l=~
    r
  [n=[p=p=%beta q=q='β'] l={} r={[p=p=%epsilon q=q='ε'] [p=p=%gamma q=q='γ'] [p=p=%delta q=q='δ']}]
]
```

Other operations allow us to look up values, as with `++get:by` (which returns a `unit`) and `++got:by` (which doesn't):

```hoon
> (~(get by greek) %alpha)
[~ q='α']

> (~(got by greek) %alpha)
q='α'
```

We can delete elements with `+del:by`:

```hoon
> =greek (~(put by greek) [%digamma 'Ϝ'])

> (~(get by greek) %digamma)
[~ q='Ϝ']

> =greek (~(del by greek) %digamma)
> greek
[ n=[p=p=%alpha q=q='α']
  l=~
    r
  [ n=[p=p=%beta q=q='β']
    l=~
    r=[n=[p=p=%epsilon q=q='ε'] l=~ r=[n=[p=p=%delta q=q='δ'] l={[p=p=%gamma q=q='γ']} r={}]]
  ]
]
```

Membership of a value can be checked using `++has:by` and the appropriate key:

```hoon
> (~(has by greek) %delta)
%.y

> (~(get by greek) %delta)
[~ q='δ']
```

Convenience functions also let us extract the list of keys with `++key:by`; the values with `++val:by`; and the pairs as a `list` with `++tap:by`.

```hoon
> ~(key by greek)
{p=%alpha p=%beta p=%epsilon p=%gamma p=%delta}

> ~(val by greek)
~[q='δ' q='γ' q='ε' q='β' q='α']

> ~(tap by greek)
~[
  [p=p=%delta q=q='δ']
  [p=p=%gamma q=q='γ']
  [p=p=%epsilon q=q='ε']
  [p=p=%beta q=q='β']
  [p=p=%alpha q=q='α']
]
```
Finally, a function can be applied across every element of a `map` using `++run:by`:

```hoon
> (~(run by greek) trip)
{ [p=p=%alpha q="α"]
  [p=p=%beta q="β"]
  [p=p=%epsilon q="ε"]
  [p=p=%digamma q="Ϝ"]
  [p=p=%gamma q="γ"]
  [p=p=%delta q="δ"]
}
```

---

In contrast to `map`s, `set`s are unordered containers without keys, containing only values.

A `set` is simply built from the unique elements of a `list`:

```hoon
> =nexus (silt `(list @tas)`~[%batty %pris %leon %zhora %zhora])

> nexus
[n=%leon l={%zhora %pris} r={%batty}]
```

`+$set` operations are provided by the `++in` core.

We can use `++put:in` to insert a new value into the `set`.  As with a `map`, we have to replace the `set` with a mutated copy.

```hoon
> (~(put in nexus) %rachael)
[n=%leon l=[n=%zhora l={} r={%pris}] r=[n=%rachael l={} r={%batty}]]

> nexus
[n=%leon l={%zhora %pris} r={%batty}]

> =nexus (~(put in nexus) %rachael)

> nexus
[n=%leon l=[n=%zhora l={} r={%pris}] r=[n=%rachael l={} r={%batty}]]
```

We check `set` membership with `++has:in`:

```hoon
> (~(has in nexus) %batty)
%.y

> (~(has in nexus) %deckard)
%.n
```

We delete elements with `+del:in`:

```hoon
> (~(del in nexus) %rachael)
[n=%leon l=[n=%zhora l=~ r=[n=%pris l={} r={}]] r=[n=%batty l=~ r=~]]

> nexus
[n=%leon l=[n=%zhora l={} r={%pris}] r=[n=%rachael l={} r={%batty}]]

> =nexus (~(del in nexus) %rachael)

> nexus
[n=%leon l=[n=%zhora l=~ r=[n=%pris l={} r={}]] r=[n=%batty l=~ r=~]]
```

Auxiliary functions let us conver the `set` back to a `list` with `++tap:in`: 

```hoon
> ~(tap in nexus)
~[%batty %leon %pris %zhora]
```

Finally, a function can be applied across every element of a `set` using `++run:in`:

```hoon
> (~(run in nexus) trip)
{"zhora" "batty" "leon" "pris"}
```
