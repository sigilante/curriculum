---
title: "Passing Data"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Describe and produce a structure file."
  - "Diagram how marks convert nouns."
  - "Explain the use of the `++grab`, `++grow`, and `++grad` arms."
  - "Produce a simple mark."
  - "Parse JSON input."
  - "Construct a JSON reparser."
  - "Convert JSON to other formats with a mark."
  - "Retrieve particular values from a JSON input."
runes:
  - "`/*`"
  - "`;;`"
keypoints:
  - "⛓️Gall agents can communicate via validated data structures using marks."
  - "JSON processing requires parsing and reparsing to become available to Hoon."
readings:
  - "https://developers.urbit.org/guides/core/app-school/7-sur-and-marks"
  - "https://developers.urbit.org/guides/core/app-school-full-stack/3-json"
  - "https://developers.urbit.org/guides/additional/json-guide"
homework:
  - "https://forms.gle/sKk9EeWN2iopud7GA"
---

#   🐝 `lesson3`.  Passing Data.
##  App School Live Lesson 3

As we saw last week, many Gall agents consist of at least three files:  the `/app` agent engine, a `/sur` structure file, and one or more `/mar/agent-name` mark files.

What exactly are the support files and what do they expect?


##  Structure Files

Most agents require a shared set of type definitions.  Some of these are simple aliases, such as `+$  url  @t` or `+$  who  @p`; these may not even have any validation on them, as `url`.  Others are cores which will be commonly used, such as `+$  friends  (set who)`.  Pokes are very commonly restricted and validated using a set of `term` constants nested under a blanket action such as `action` or `update` or `request`.  (These frequently correspond to the mark files.)

For instance, the `%todo` app used the following file:

**`/sur/todo.hoon`**

```hoon
|%
+$  id  @
+$  name  @t
+$  task  [=name done=?]
+$  tasks  (map id task)
+$  action
  $%  [%add =name]
      [%del =id]
      [%toggle =id]
      [%rename =id =name]
  ==
+$  update
  $%  [%add =id =name]
      [%del =id]
      [%toggle =id]
      [%rename =id =name]
      [%initial =tasks]
  ==
--
```

In this case, `action`s correspond to `%todo` agent poke events, while `update`s correspond to the `%todo-watcher` agent events.

Gall doesn't coerce you to use this structure, but head-tagged poke types are a very common and very clear pattern we recommend you use throughout.  (Notably, `%delta-follower` in the previous lesson did _not_ use such a handler for the `%sub`/`%unsub` actions.)

You've seen marks some beforehand; here we only briefly comment on their major features.

**`/mar/todo/action.hoon`**

```hoon
/-  todo:
|_  =action:todo
++  grab
  |%
  ++  noun  action:todo
  --
++  grow
  |%
  ++  noun  action
  --
++  grad  %noun
--
```

Most marks are fairly simple—they either delegate their validation role directly to the marks defined in the structure file, or they defer to the built-in types (which are often rather involved).

-   `++grab`: This handles conversion methods _to_ our mark. It contains a core with arm names corresponding to other marks. In this case, it can only convert from a `noun` mark, so that's the core's only arm. The `noun` arm simply calls the `action` structure from our structure library. This is called "clamming" or "molding" - when some noun comes in, it gets called like `(action:todo [some-noun])` - producing data of the `action` type if it nests, and crashing otherwise.
-   `++grow`: This handles conversion methods _from_ our mark. Like `grab`, it contains a core with arm names corresponding to other marks. Here we've also only added an arm for a `%noun` mark. In this case, `action` data will come in as the sample of our door, and the `noun` arm simply returns it, since it's already a noun (as everything is in Hoon).
-   `++grad`: This is the revision control arm, and as you can see we've simply delegated it to the `%noun` mark.

Mark files are commonly referred to by their path as a `term` constant—in this case, `%todo-action` would be interpreted by Gall as referring to this mark.

As you'll see soon, adding `json` arms to your mark will allow you greater flexibility in preparation for communicating with a front-end.


##  Receiving JSON Data

[JSON (JavaScript Object Notation_](https://en.wikipedia.org/wiki/JSON) is a data format very commonly used by platforms and languages to communicate structured data.

A JSON file is organized into lists (arrays) and maps (objects) of basic values:  numbers, strings, booleans, `null`, and lists and maps again.  Whitespace is ignored outside of strings.  JSON is designed to be a low-overhead representation, and has achieved prominence similar to that of XML in the 00s.

```json
{
  "red": "#f44336",
  "pink": "#e91e63",
  "purple": "#9c27b0",
  "deeppurple": "#673ab7",
  "indigo": "#3f51b5",
  "blue": "#2196f3",
  "lightblue": "#03a9f4",
  "cyan": "#00bcd4",
  "teal": "#009688",
  "green": "#4caf50",
  "lightgreen": "#8bc34a",
  "lime": "#cddc39",
  "yellow": "#ffeb3b",
  "amber": "#ffc107",
  "orange": "#ff9800",
  "deeporange": "#ff5722",
  "brown": "#795548",
  "grey": "#9e9e9e",
  "black": "#000000",
  "white": "#ffffff",
}
```


Hoon internally represents JSON values not as plain text strings but as structured data:

```hoon
+$  json                    ::  normal json value
  $@  ~                     ::  null
  $%  [%a p=(list json)]    ::  array
      [%b p=?]              ::  boolean
      [%o p=(map @t json)]  ::  object
      [%n p=@ta]            ::  number
      [%s p=@t]             ::  string
  ==                        ::
```

So the equivalent to the above string

```hoon
[ ~  
 [ %o  
     p  
   { [p='lightblue' q=[%s p='#03a9f4']]  
     [p='purple' q=[%s p='#9c27b0']]  
     [p='black' q=[%s p='#000000']]  
     [p='red' q=[%s p='#f44336']]  
     [p='indigo' q=[%s p='#3f51b5']]  
     [p='cyan' q=[%s p='#00bcd4']]  
     [p='lime' q=[%s p='#cddc39']]  
     [p='amber' q=[%s p='#ffc107']]  
     [p='blue' q=[%s p='#2196f3']]  
     [p='deeporange' q=[%s p='#ff5722']]  
     [p='green' q=[%s p='#4caf50']]  
     [p='pink' q=[%s p='#e91e63']]  
     [p='lightgreen' q=[%s p='#8bc34a']]  
     [p='brown' q=[%s p='#795548']]  
     [p='white' q=[%s p='#ffffff']]  
     [p='yellow' q=[%s p='#ffeb3b']]  
     [p='orange' q=[%s p='#ff9800']]  
     [p='teal' q=[%s p='#009688']]  
     [p='grey' q=[%s p='#9e9e9e']]  
     [p='deeppurple' q=[%s p='#673ab7']]  
   }  
 ]  
]
```

This is one of the places where Hoon may shock you just a tiny a bit.  It's actually not terribly uncommon for languages to have their own internal representations of data languages like HTML and XML (e.g. Hoon's Sail; Clojure's Hiccup).  What this does is decouple your thinking about what a JSON examples means from how it is written.  All information is retained:  it is simply the representation that has changed.  (However, since JSON ignores whitespace, a round trip through Hoon may not produce the exact same text layout of the JSON data.)

Anyway, notice that the above is a `unit`, then an object (map) of string–string pairs.  Every cell is head-tagged with the JSON type.

A JSON must be processed twice:

1. First the JSON is parsed from text (`@t` `cord`) into a tagged cell representation `+$json` using `++dejs:html`.
2. Then the parsed JSON is sent through a custom-built reparser to retrieve particular values.

There are also a number of handlers for converting to and from `+$json`.

![](https://media.urbit.org/docs/json-diagram.svg)

### Parsing JSON

JSON input arrives as a `cord` from a source like Eyre.  Having received the text, we need to convert it from that representation to the `+$json` structure.  We'll look at a couple:  first, a highly-nested example from the [official JSON docs](https://www.json.org/example.html).

**Incoming JSON**

```json
{
  "glossary": {
    "title": "example glossary",
    "GlossDiv": {
      "title": "S",
      "GlossList": {
        "GlossEntry": {
          "ID": "SGML",
          "SortAs": "SGML",
          "GlossTerm": "Standard Generalized Markup Language",
          "Acronym": "SGML",
          "Abbrev": "ISO 8879:1986",
          "GlossDef": {
            "para": "A meta-markup language, used to create markup languages such as DocBook.",
            "GlossSeeAlso": ["GML", "XML"]
          },
        "GlossSee": "markup"
        }
      }
    }
  }
}
```

At the Dojo prompt, it is more convenient to work with the same JSON as a single-line `cord` in single quotes `'` soq:

```json
{ "glossary": { "title": "example glossary", "GlossDiv": { "title": "S", "GlossList": { "GlossEntry": { "ID": "SGML", "SortAs": "SGML", "GlossTerm": "Standard Generalized Markup Language", "Acronym": "SGML", "Abbrev": "ISO 8879:1986", "GlossDef": { "para": "A meta-markup language, used to create markup languages such as DocBook.", "GlossSeeAlso": ["GML", "XML"] }, "GlossSee": "markup" } } } } }
```

**Processing code**

```hoon
[ ~
  [ %o
      p
    { [ p='glossary'
          q
        [ %o
            p
          { [p='title' q=[%s p='example glossary']]
            [ p='GlossDiv'
                q
              [ %o
                  p
                { [ p='GlossList'
                      q
                    [ %o
                        p
                      { [ p='GlossEntry'
                            q
                          [ %o
                              p
                            { [p='GlossSee' q=[%s p='markup']]
                              [p='ID' q=[%s p='SGML']]
                              [ p='GlossDef'
                                  q
                                [ %o
                                    p
                                  { [ p='para'
                                        q
                                      [ %s
                                          p
                                        'A meta-markup language, used to create markup languages such as DocBook.'
                                      ]
                                    ]
                                    [p='GlossSeeAlso' q=[%a p=~[[%s p='GML'] [%s p='XML']]]]
                                  }
                                ]
                              ]
                              [p='SortAs' q=[%s p='SGML']]
                              [p='GlossTerm' q=[%s p='Standard Generalized Markup Language']]
                              [p='Abbrev' q=[%s p='ISO 8879:1986']]
                              [p='Acronym' q=[%s p='SGML']]
                            }
                          ]
                        ]
                      }
                    ]
                  ]
                  [p='title' q=[%s p='S']]
                }
              ]
            ]
          }
        ]
      ]
    }
  ]
]
```

That one shows the Hoon cell structure clearly, but all of the values are strings still so it's not as interesting mechanically.  Let's look at a JSON with mixed values:


**Incoming JSON**

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "isAlive": true,
  "age": 27,
  "address": {
    "streetAddress": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postalCode": "10021-3100"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "212 555-1234"
    },
    {
      "type": "office",
      "number": "646 555-4567"
    }
  ],
  "children": [
      "Catherine",
      "Thomas",
      "Trevor"
  ],
  "spouse": null
}
```

At the Dojo prompt, it is more convenient to work with the same JSON as a single-line `cord` in single quotes `'` soq:

```json
{ "firstName": "John", "lastName": "Smith", "isAlive": true, "age": 27, "address": { "streetAddress": "21 2nd Street", "city": "New York", "state": "NY", "postalCode": "10021-3100" }, "phoneNumbers": [ { "type": "home", "number": "212 555-1234" }, { "type": "office", "number": "646 555-4567" } ], "children": [ "Catherine", "Thomas", "Trevor" ], "spouse": null}
```

**Processing code**

```hoon
> (de-json:html '{ "firstName": "John", "lastName": "Smith", "isAlive": true, "age": 27, "address": { "streetAddress": "21 2nd Street", "city": "New York", "state": "NY", "postalCode": "10021-3100" }, "phoneNumbers": [ { "type": "home", "number": "212 555-1234" }, { "type": "office", "number": "646 555-4567" } ], "children": [ "Catherine", "Thomas", "Trevor" ], "spouse": null}')
[ ~
  [ %o
      p
    { [p='firstName' q=[%s p='John']]
      [p='lastName' q=[%s p='Smith']]
      [p='children' q=[%a p=~[[%s p='Catherine'] [%s p='Thomas'] [%s p='Trevor']]]]
      [ p='address'
          q
        [ %o
            p
          { [p='postalCode' q=[%s p='10021-3100']]
            [p='streetAddress' q=[%s p='21 2nd Street']]
            [p='city' q=[%s p='New York']]
            [p='state' q=[%s p='NY']]
          }
        ]
      ]
      [ p='phoneNumbers'
          q
        [ %a
            p
          ~[
            [%o p={[p='type' q=[%s p='home']] [p='number' q=[%s p='212 555-1234']]}]
            [%o p={[p='type' q=[%s p='office']] [p='number' q=[%s p='646 555-4567']]}]
          ]
        ]
      ]
      [p='spouse' q=~]
      [p='isAlive' q=[%b p=%.y]]
      [p='age' q=[%n p=~.27]]
    }
  ]
]
```

- `++de-json:html` returns a `unit` of the result, because a failure to parse will result in `~` null.
- Most of the values are still strings, but note at the end that `spouse` is `null`; `isAlive` is a boolean in loobean clothes; and `age` is a number as a `knot`.
- The `%n` number type is a `@ta` rather than something like a `@ud` that you might expect. This is because JSON's number type may be either an integer or floating point, so it's left as a `knot` which can then be parsed to a `@ud` or `@rd` with the appropriate [`+dejs:format`](https://developers.urbit.org/reference/hoon/zuse/2d_6) function.

### Reparsing JSON

The naïve way to extricate relevant information is to use faces or lark notation to find the value you're looking for.  Sometimes this is helpful particularly at the command line while you're figuring out the shape of the data, but in production code you should write a reparser gate.

Using wing notation, you can grab a particular value out.  This is brittle, tends to run afoul of `find-fork`, and can get the wrong type out after all that work.

```hoon
:: having defined the above as `val` and trying to extract 'isAlive'’s value

> +>+>+>->:val  
q=[%b p=%.y]  

> +>+>+>->+:val  
p=''
```

A reparser is built to locate and return the values from the `+$json` data structure as Hoon-legible values.  To build a reparser does require you to have thought carefully about the kinds of values you expect (e.g. integer or floating-point numbers).

For instance, a gate to reparse a flatter JSON example into a set of usable values could look like this:

**Incoming JSON**

```json
{
  "name": ["Jon", "Johnson", "of Wisconsin"],
  "member": true,
  "dues": 123
}
```

```hoon
> %-  (ot ~[])
```

**Reparser**

```hoon
=,  dejs:format
%-  ot
:~
  [%name (at ~[so so so])]
  [%member bo]
  [%dues ni]
==
```

In use:

```hoon
> =js %-  need  %-  de-json:html
  '''
  {
    "name": ["Jon", "Johnson", "of Wisconsin"],
    "member": true,
    "dues": 123
  }
  '''

> js
[ %o
    p
  { [p='dues' q=[%n p=~.123]]
    [p='member' q=[%b p=%.y]]
    [p='name' q=[%a p=~[[%s p='Jon'] [%s p='Johnson'] [%s p='of Wisconsin']]]]
  }
]

> =reparser =,  dejs:format
%-  ot
:~
  [%name (at ~[so so so])]
  [%member bo]
  [%dues ni]
==

> (reparser js)
[['Jon' 'Johnson' 'of Wisconsin'] %.y 123]
```

What's going on?  The `++dejs:format` core provisions many functions designed to ingest `+$json` strings and turn them into something useful.  These two-letter-designated functions nest to describe the overall structure of the JSON, then extricate the values as head-tagged cells with the correct Hoon type.  (`=,` tiscom strips the namespace off of the two-letter JSON parser gates for convenience.)

We can touch on some useful families of `++dejs` functions in brief, but because there's so many, in practice you'll need to look through the [`++dejs` reference](https://developers.urbit.org/reference/hoon/zuse/2d_6) to find the correct functions for your use case.

#### Number functions

-   `++ne` - decode a number to a `@rd`.
-   `++ni` - decode a number to a `@ud`.
-   `++no` - decode a number to a `@ta`.
-   `++nu` - decode a hexadecimal string to a `@ux`.

For example:

> (ni:dejs:format n+'123')

123

#### String functions

-   `++sa` - decode a string to a `tape`.
-   `++sd` - decode a string containing a `@da` aura date value to a `@da`.
-   `++se` - decode a string containing the specified aura to that aura.
-   `++so` - decode a string to a `@t`.
-   `++su` - decode a string by parsing it with the given [parsing rule](https://developers.urbit.org/reference/hoon/stdlib/4f).

#### Array functions

`++ar`, `++as`, and `++at` decode a `$json` array to a `list`, `set`, and n-tuple respectively. These gates take other `++dejs` functions as an argument, producing a new gate that will then take the `$json` array. For example:

```hoon
> ((ar so):dejs:format a+[s+'foo' s+'bar' s+'baz' ~])
<|foo bar baz|>
```

Notice that `++so` is given as the argument to `++ar`. `++so` is a `++dejs` function that decodes a `$json` string to a `cord`. The gate resulting from `(ar so)` is then called with a `$json` array as its argument, and its product is a `(list @t)` of the elements of the array.

Many `++dejs` functions take other `++dejs` functions as their arguments. A complex nested `$json` decoding function can be built up in this manner.

#### Object functions

-   `++of` - decode an object containing a single key-value pair to a head-tagged cell.
-   `++ot` - decode an object to a n-tuple.
-   `++ou` - decode an object to an n-tuple, replacing optional missing values with a given value.
-   `++oj` - decode an object of arrays to a `jug`.
-   `++om` - decode an object to a `map`.
-   `++op` - decode an object to a `map`, and also parse the object keys with a [parsing rule](https://developers.urbit.org/reference/hoon/stdlib/4f).

#### Errors

If you attempt to parse a key using an invalid decoder/value pair, the error will gently nudge you towards what's wrong.

```hoon
> =reparser-wrong =,  dejs:format
  %-  ot
  :~
    [%name (at ~[so so so])]
    [%member du]                     :: ← changed to wrong type
    [%dues ni]
  ==

> (reparser-wrong js)
[%key 'member']
```

A similar result will happen if a key isn't recognized.

Mixed-case names require you to revert from `term`-constant head tags to `@t` head tags:

```hoon
> =js %-  need  %-  de-json:html  '{ "firstName": "John", "lastName": "Smith", "isAlive": true, "age": 27, "address": { "streetAddress": "21 2nd Street", "city": "New York", "state": "NY", "postalCode": "10021-3100" }, "phoneNumbers": [ { "type": "home", "number": "212 555-1234" }, { "type": "office", "number": "646 555-4567" } ], "children": [ "Catherine", "Thomas", "Trevor" ], "spouse": null}'

> =reparser =,  dejs:format
  %-  ot
  :~
    ['firstName' so]
    [%age ni]
    [%address (ot ~[['streetAddress' so] [%city so] [%state so]])]
  ==

> (reparser js)  
['John' 27 '21 2nd Street' 'New York' 'NY']
```

Notice that the reparser values do not have to be exhaustive.

`++dejs:format` functions crash on failure.  `++dejs-soft:format` functions instead return `~` null on failure to parse.

```hoon
> =reparser =,  dejs-soft:format
  %-  ot
  :~
   ['firstname' so]                  :: ← lower-case when should be upper-case
   [%age ni]
   [%address (ot ~[['streetAddress' so] [%city so] [%state so]])]
  ==

> (reparser js)
~
```

#### When to Parse and Reparse Explicitly

Sometimes an agent's interactions with a web interface are totally distinct from its interactions with other agents. If so, the agent could just have separate scry endpoints, poke handlers, etc, that directly deal with `+$json` data with a `%json` mark. In such a case, you can include `+$json` encoding/decoding functions directly in the agent or associated libraries, using the general techniques demonstrated in the [+$json encoding and decoding example](https://developers.urbit.org/guides/additional/json-guide#json-encoding-and-decoding-example) section below.

If, on the other hand, you want a unified interface (whether interacting with a web client or within Urbit), a different approach is necessary. Rather than taking or producing either `%noun` or `%json` marked data, custom `mark` files can be created which specify conversion methods for both `%noun` and `%json` marked data.

With this approach, an agent would take and/or produce data with some `mark` like `%my-custom-mark`. Then, when the agent must interact with a web client, the webserver vane Eyre can automatically convert `%my-custom-mark` to `%json` or vice versa. This way the agent only ever has to handle the `%my-custom-mark` data. This approach is used by `%graph-store` with its `%graph-update-2` mark, for example, and a number of other agents.


##  Receiving Data Through Marks

We have previously used marks three ways:

1.  Directly as file type handlers.  (`+cat /===/gen/tally/hoon`)
2.  For poke and peek types.  (`&noun`/`%noun`)
3.  As data validators inside of agents.  (`%charlie-action`)

We are now going to use them to explicitly convert and handle data.  Ultimately, we are looking at building a data flow like this:

![](https://media.urbit.org/guides/core/app-school-full-stack-guide/eyre-mark-flow-diagram.svg)

This pattern works well for structured data coming through Eyre, which is what most front-end data will be.  It will save us explicitly parsing and reparsing JSON data inside of our agent or a helper core.

### Loading Files with a Mark

The [`/*` fastar](https://developers.urbit.org/reference/hoon/rune/fas#-fastar) rune supports importing a file at a given path via the specified mark.

```hoon
/*  help-text  %txt  /gen/hood/fuse/help/txt
```

The `txt` mark delegates its `++grab` functions to `wain`, a `(list cord)`.

### Produce a JSON-Compatible Mark

In order to handle the `json` mark, we need a `+$json`-compatible conversion arm in our mark.

Let's take `%delta` from the previous lesson and update it.  Since only the `%delta-action` and `%delta-update` marks are changing, we'll actually leave it as the same agent rather than upgrade to `%echo` now.

Examine the `++grab` and `++grow` arms carefully:  they allow `%delta` to receive pokes as JSON instances, and to update subscribers using JSON.

**`/mar/delta/action.hoon`**

```hoon
/-  *delta
|_  act=action
++  grow
  |%
  ++  noun  act
  --
++  grab
  |%
  ++  noun  action
  ++  json
    =,  dejs:format
    |=  jon=json
    ^-  action
    %.  jon
    %-  of
    :~  [%push (ot ~[target+(se %p) value+ni])]
        [%pop (se %p)]
    ==
  --
++  grad  %noun
--
```

This one is fairly straightforward:  it's mostly a matter of getting the `%target` and the `%value` out of the JSON using tools similar to what we saw above.

**`/mar/delta/update.hoon`**

```hoon
/-  *delta
|_  upd=update
++  grow
  |%
  ++  noun  upd
  ++  json
    =,  enjs:format
    ^-  ^json
    ?-    -.upd
      %pop   (frond 'pop' s+(scot %p target.upd))
      %init  (frond 'init' a+(turn values.upd numb))
      %push  %+  frond  'push'
             %-  pairs
             :~  ['target' s+(scot %p target.upd)]
                 ['value' (numb value.upd)]
    ==       ==
  --
++  grab
  |%
  ++  noun  update
  --
++  grad  %noun
--
```

This one looks a little different:  we skipped over the details of producing `+$json` instances from raw values.  Notice in particular the use of [`++frond`](https://developers.urbit.org/reference/hoon/zuse/2d_1-5#frondenjsformat) and [`++pairs`](https://developers.urbit.org/reference/hoon/zuse/2d_1-5#pairsenjsformat), which produce objects containing key–value pairs.  (`++frond` is singular `++pairs`.)  We also `++scot` values to make them into `cord`s.

Next week, we will see how to connect Eyre to the front-end and carry out operations using something like this mark.


##  Normalizing Nouns

There are some limitations on the data which can be passed from ship to ship.  We send nouns and then need to recover type information.  The [`;;` micmic](https://developers.urbit.org/reference/hoon/rune/mic#-micmic) rune applies a mold and asserts that the action succeeds.

When one agent pokes another with a cage over the network, Gall looks up the mark and applies the [`;;` micmic](https://developers.urbit.org/reference/hoon/rune/mic#-micmic) rune to normalize the type before passing the result to the `++on-poke` arm.  However, poking with `%noun` applies `;;(* data)`, thereby erasing all type information.

You'll see some agents that deal in data which use `;;` micmic to assert the structural match.  This is more flexible in some ways than `^-` kethep because the data can include more complicated ehad-tagged terms, but it also ignores aura data:

```hoon
> ;;(@ud 5)
5

> ;;(@ud .5)
1.084.227.584
```

`;;` micmic can be helpful for validating parsing:

```hoon
> (scan "m15.s15" crub:so)  
[p=~.dr q=16.878.770.827.444.239.728.640]

> ;;([%dr @dr] (scan "m15.s15" crub:so))
[%dr ~m15.s15]
```


##  Debugging Vases and Cages

If you are debugging and need to print typed information, you should be careful not to print vases or cages directly.  There is a significant chance that they include the entire kernel.  Instead, use [`++sell`](https://developers.urbit.org/reference/hoon/stdlib/5c#sell) to convert the vase to a `tank` or [`++text`](https://developers.urbit.org/reference/hoon/stdlib/5c#text) to convert the vase to a `tape`.


##  Resources:

- [App School, “7. Structures and Marks”](https://developers.urbit.org/guides/core/app-school/7-sur-and-marks)
- [App School Full-Stack, “3. JSON”](https://developers.urbit.org/guides/core/app-school-full-stack/3-json)
- [Additional Guides, “Working With JSON”](https://developers.urbit.org/guides/additional/json-guide)
