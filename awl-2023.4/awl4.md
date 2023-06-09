---
title: "Database Operators"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Examine several database implementations in Hoon."
runes: []
keypoints: []
readings: []
homework: []
mirror: "https://github.com/sigilante/curriculum/blob/master/awl-2023.4/awl4.md"
video: "https://youtu.be/5O_FuNNaBSo"
---

#   🖴 `awl4`. Database Operators

Over the course of the previous lesson and this one, we are building a little database, `%rkyv`, which implements the backend and SQL-like instructions necessary to operate on the stored data.  In the last lesson, we examined the `map` and `tree` data structures, then built a database operable by explicit pokes.  In this lesson, we will examine three instances of Urbit databases, TomeDB, urQL, and lineDB.  We will also expand `%rkyv` into a simple database with a SQL-like grammar.


##  TomeDB

- https://github.com/holium/tome-db

~larryx-woldyr has written TomeDB as an Urbit-based database that supports a complete external interface for JavaScript apps.

> TomeDB is an Urbit database and JavaScript client package with native permissioning and subscription support.  With TomeDB, developers can build full-stack Urbit applications entirely in JavaScript (no Hoon).  Tome currently supports multiple storage types, including key-value, log, and feed.  ([Holium, TomeDB](https://holium.gitbook.io/tomedb/))

Follow the [setup instructions](https://docs.holium.com/tomedb/quick-start/) for basic usage.  Then analyze the app's behavior using our standard `/sur`, `/lib`, `/app` approach.

Some points about TomeDB:

1. TomeDB uses the [nested core design pattern](https://developers.urbit.org/blog/nested-core-pattern).  If you haven't seen this before, the shortest explanation is that it uses a helper outer core to build sets of state changes then implement them all at once through their `++abet` arm.

2. TomeDB accepts an incoming `(pole knot)` instead of a `wire`.  These are structurally the same, but `(pole knot)` makes it easier to label components of an incoming `(list knot)` with faces.

    Compare this code from a different agent, which shows that `(pole knot)` strips the `list` faces so you can add your own with `?=` wuttis:

    ```hoon
    ++  on-peek
      |=  =(pole knot)
      ^-  (unit (unit cage))
      ?+    pole  (on-peek:def pole)
      ::  desk peek
      ::
          [%x desk=@ ~]
        ``noun+!>((~(get by store) (slav %tas desk.pole)))
      ==
    ```

3.  TomeDB rigorously includes error traces with `~|` sigbar for highly differentiated crash feedback.

4.  `++fe-perm` handles permission levels and is worth a perusal.


##  urQL

- https://github.com/jackfoxy/urQL

~nomryg-nilref has described urQL as a relational database language and reference implementation that's more fundamental than SQL.

As of this writing, urQL is incomplete, with the parser being close to complete.


##  LineDB

- https://github.com/uqbar-dao/linedb

LineDB is a hybrid userspace/kernelspace file management system by ~dachus-tiprel and ~hosted-ladrun.

> `%linedb` is a Git-like VCS that lives in userspace.  It includes a build system, `%uqbuild`, that will soon accept custom build languages (define your own parser and gate to create Nock out of that parsed Hoon; we'll be using this for Uqbar smart contracts, but you could imagine defining new runes, new Ford-like runes, even new languages—the sky is the limit).  It has no marks.  It can interface with Clay.

LineDB is not yet annotated but you can tell the sorts of Git-like operations it supports (or prospectively supports) by examining the paths and especially the `/lib` file.


##  `%rkyv` Database

### Batch Operations

We upgrade `%rkyv` to support a basic search and retrieval syntax as well as batch operations.

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
+$  cursor  (unit @ud)
+$  action
  $%  [%create =key =value]
      [%retrieve =key]
      [%update =key =value]
      [%destroy =key]
  ==
+$  batch
  $%  [%create-many =(list (pair key value))]
      [%retrieve-by-head =term]
      [%retrieve-by-value =cord]
      [%update-many =(list (pair key value))]
  ==
+$  result
  $%  [%store =store]
      [%value =value]
      [%delete =key]
      [%answer =(set key)]
      [%values =(set (pair key value))]
  ==
--
```

We create four batch operations which are worthy of closer examination:

1. `%create-many` is used to take a list of key-value pairs appropriate to the database and insert them _en masse_.
2. `%retrieve-by-head` allows us to batch-retrieve a sorted subset of keys based on the head of the key.  (For instance, given keys of the form `%gen-1`, `%gen-2`, `%exo-1`, and so forth, we could `%retrieve-by-head` on `%gen` to get all of the Genesis keys.)
3. `%retrieve-by=value` will search the text of each entry for the target string and return a collection of matching key–value pairs.
4. `%update-many` like `%create-many` allows us to batch replacements in the database.  (Actually it'll be functionally pretty much the same operation but you could imagine permission-based differentiation, for instance.)

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

**`/mar/rkyv/batch.hoon`**

```hoon
/-  rkyv
::
|_  bat=batch:rkyv
::
++  grad  %noun
++  grow
  |%
  ++  noun  bat
  --
++  grab
  |%
  ++  noun  batch:rkyv
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

**`/lib/rkyv/.hoon`**

```hoon
/-  *rkyv
|%
++  find-by-value
  |=  [=store =cord]
  ^-  (set (pair key value))
  =|  result=(set (pair key value))
  =/  values  ~(tap by store)
  |-
  ?~  values  result
  =/  key     -:i.values
  =/  search  (find-in-txt +:i.values cord)
  ?~  search
    $(values t.values, result (~(put in result) [key (need search)]))
  $(values t.values)
++  find-in-txt
  |=  [=value =cord]
  ^-  cursor
  ?-    -.value
      %txt
    =/  nedl=tape  (trip cord)
    =/  hstk=tape  (trip body.value)
    `cursor`(find nedl hstk)
  ::
      %yaml
    =/  nedl=tape  (trip cord)
    =/  hstk=tape  (trip body.value)
    `cursor`(find nedl hstk)
  ::
      %xml
    *cursor
  ::
      %json
    *cursor
  ==
--
```

**`/app/rkyv/.hoon`**

```hoon
/-  *rkyv
/+  default-agent, dbug, *rkyv
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
  ?+    mark  ~|(%invalid-poke (on-poke:default))
      %rkyv-action
    =/  act  !<(action vase)
    ?-    -.act
        %create
      =/  new-store  (~(put by store) key.act value.act)
      :_  this(store new-store)
      :~  [%give %fact ~[/store] %rkyv-result !>(new-store)]
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
      =/  new-store  (~(put by store) key.act value.act)
      :_  this(store new-store)
      :~  [%give %fact ~[/store] %rkyv-result !>(value+value.act)]
          [%give %kick ~[/store] ~]
      ==
    ::
        %destroy
      =/  new-store  (~(del by store) key.act)
      :_  this(store new-store)
      :~  [%give %fact ~[/store] %rkyv-result !>(delete+key.act)]
          [%give %kick ~[/store] ~]
      ==
    ==  ::  %rkyv-action
  ::
      %rkyv-batch
    =/  bat  !<(batch vase)
    ?-    -.bat
        %create-many
      ::  Insert a list of key-value pairs.
      =/  new-store  (~(uni by store) (~(gas by *^store) list:bat))
      :_  this(store new-store)
      :~  [%give %fact ~[/store] %rkyv-result !>(store+new-store)]
          [%give %kick ~[/store] ~]
      ==
    ::
        %retrieve-by-head
      |^
      =/  keys  (scan-keys store term:bat)
      :_  this
      :~  [%give %fact ~[/store] %rkyv-result !>(answer+keys)]
          [%give %kick ~[/store] ~]
      ==
      ++  scan-keys
        |=  [=^store =term]
        ^-  (set key)
        =/  term  (trip term)
        =/  keys  ~(tap in ~(key by store))
        =/  len  (lent term)
        =|  leys=(set key)
        |-
        ?~  keys  leys
        =/  ley  (scag len (trip i.keys))
        ?:  =(term ley)
          $(keys t.keys, leys (~(put in leys) `key`(crip ley)))
        $(keys t.keys)
      --
    ::
        %retrieve-by-value
      =/  values  (find-by-value store cord.bat)
      :_  this
      :~  [%give %fact ~[/store] %rkyv-result !>(values+values)]
          [%give %kick ~[/store] ~]
      ==
    ::
        %update-many
      =/  new-store  (~(uni by store) (~(gas by *^store) list:bat))
      :_  this(store new-store)
      :~  [%give %fact ~[/store] %rkyv-result !>(store+new-store)]
          [%give %kick ~[/store] ~]
      ==
    ==  ::  %rkyv-batch
  ==  ::  mark
::
++  on-peek
  |=  =(pole knot)
  ^-  (unit (unit cage))
  ?+  pole  ~|(%invalid-scry-path (on-peek:default pole))
    [%x %store ~]  ``noun+!>(store)
    [%x %key key=@ ~]  ``noun+!>((~(gut by store) key:pole %null))
    [%x %value value=@ ~]  ``rkyv-result+!>(values+(find-by-value store value:pole))
    [%x %value %txt value=@ ~]  ``noun+!>((find-by-value store value:pole))
  ==
++  on-arvo   on-arvo:default
++  on-watch
  |=  =(pole knot)
  ^-  (quip card _this)
  ?+    pole  ~|(%invalid-watch-path (on-watch:default pole))
      [%store ~]
    :_  this
    :~  [%give %fact ~ %rkyv-result !>(store+store)]
    ==
  ::
      [%key key=@ ~]
    :_  this
    :~  [%give %fact ~ %rkyv-result !>(value+(~(gut by store) key:pole %$))]
    ==
  ==
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

Some points:

1.  `~|` sigbar logging is used for basic error handling.  We could also build [formatted text output](https://developers.urbit.org/guides/core/hoon-school/P-stdlib-io#formatted-text).
2. `%rkyv` as written does not handle `%json` or `%xml` searches by value.  This would be a good exercise for you to write.
3. There are not currently any client applications to use the subscriptions so these have not been checked.

### Example:  Load and Query Documents

This generator can be used to load data from a collection of files into the database.  It will work recursively with a folder as well.  The source folder (in this case) is a collection of the form:

```

```

The generator:

```hoon
:rkyv|load /=data=/kjv
```

**`/gen/load.hoon`**

```hoon
/-  *rkyv
:-  %say
|=  [* [=path ~] *]
:-  %rkyv-batch
:-  %create-many
|^
?~  path  !!
=/  files   .^((list ^path) %ct path)
=/  paths   (turn files |=(file=^path `^path`:(weld ~[&1:path] ~[&2:path] ~[&3:path] file)))
=/  values  `(list value)`(turn paths path-to-file)
=/  keys    `(list key)`(strip-keys files)
`(list (pair key value))`(zip keys values)
++  path-to-term
  |=  =^path
  ^-  @tas
  =|  =tape
  |-
  ?~  path  (crip (scag (sub (lent tape) 6) tape))
  $(path t.path, tape :(weld tape (trip i.path) "-"))
++  path-to-file
  |=  =^path
  ^-  value
  :-  %txt
  (of-wain:format .^(wain %cx path))
++  zip
  |=  [lhs=(list term) rhs=(list value)]
  ^-  (list (pair key value))
  =|  kv=(list (pair key value))
  |-  ^-  (list (pair key value))
  ?~  lhs  (flop kv)
  ?~  rhs  (flop kv)
  $(lhs t.lhs, rhs t.rhs, kv [[i.lhs i.rhs] kv])
++  strip-keys
  |=  =(list ^path)
  ^-  (^list key)
  =|  keys=(^list key)
  |-
  ?~  list  (flop keys)
  =/  key  `term`(snag (dec (dec (lent i.list))) i.list)
  $(list t.list, keys [key keys])
--
```

With that complete, we can either query at the `%rkyv` command line or using a poke generator at the Dojo prompt.

```hoon
> .^(cord %gx /=rkyv=/key/genesis-1-1/txt/noun)
'1:1  In the beginning God created the heaven and the earth.'

> +data!verse 'Genesis 1:1'
'1:1  In the beginning God created the heaven and the earth.'
```

The poke generator:

**`/gen/verse.hoon`** (on desk `%data`)

```hoon
=<
:-  %say
|=  [[* * =beak] [arg=cord ~] *]
:-  %noun
=/  beak  `path`/(@ta (scot %p -:beak))/rkyv/(@ta (scot %da +>+:beak))
=/  tape  (trip arg)
=/  bkidx  (sub (lent tape) (need (find " " (flop tape))))
=/  verse  (slag bkidx tape)
=/  vsidx  (need (find ":" verse))
=/  verse  (snap verse vsidx '-')
=/  title  (~(got by books) (crip (scag (dec bkidx) tape)))
=/  ref    `@tas`(crip :(weld (trip title) "-" verse))
=/  pax    :(weld `path`beak /key `path`~[ref] /txt/noun)
.^(cord %gx pax)
|%
++  books
  ^-  (map @t @tas)
  %-  my
  ^-  (list (pair @t @tas))
  :~  :-  'Genesis'  %genesis
      :-  'Exodus'  %exodus
      :-  'Leviticus'  %leviticus
      :-  'Numbers'  %numbers
      :-  'Deuteronomy'  %deuteronomy
      :-  'Joshua'  %joshua
      :-  'Judges'  %judges
      :-  'Ruth'  %ruth
      :-  '1 Samuel'  %samuel-1
      :-  '2 Samuel'  %samuel-2
      :-  '1 Kings'  %kings-1
      :-  '2 Kings'  %kings-2
      :-  '1 Chronicles'  %chronicles-1
      :-  '2 Chronicles'  %chronicles-2
      :-  'Ezra'  %ezra
      :-  'Nehemiah'  %nehemiah
      :-  'Esther'  %esther
      :-  'Job'  %job
      :-  'Psalms'  %psalms
      :-  'Proverbs'  %proverbs
      :-  'Ecclesiastes'  %ecclesiastes
      :-  'Song of Solomon'  %song-of-solomon
      :-  'Isaiah'  %isaiah
      :-  'Jeremiah'  %jeremiah
      :-  'Lamentations'  %lamentations
      :-  'Ezekiel'  %ezekiel
      :-  'Daniel'  %daniel
      :-  'Hosea'  %hosea
      :-  'Joel'  %joel
      :-  'Amos'  %amos
      :-  'Obadiah'  %obadiah
      :-  'Jonah'  %jonah
      :-  'Micah'  %micah
      :-  'Nahum'  %nahum
      :-  'Habakkuk'  %habakkuk
      :-  'Zephaniah'  %zephaniah
      :-  'Haggai'  %haggai
      :-  'Zechariah'  %zechariah
      :-  'Malachi'  %malachi
      :-  'Matthew'  %matthew
      :-  'Mark'  %mark
      :-  'Luke'  %luke
      :-  'John'  %john
      :-  'Acts'  %acts
      :-  'Romans'  %romans
      :-  '1 Corinthians'  %corinthians-1
      :-  '2 Corinthians'  %corinthians-2
      :-  'Galatians'  %galatians
      :-  'Ephesians'  %ephesians
      :-  'Philippians'  %philippians
      :-  'Colossians'  %colossians
      :-  '1 Thessalonians'  %thessalonians-1
      :-  '2 Thessalonians'  %thessalonians-2
      :-  '1 Timothy'  %timothy-1
      :-  '2 Timothy'  %timothy-2
      :-  'Titus'  %titus
      :-  'Philemon'  %philemon
      :-  'Hebrews'  %hebrews
      :-  'James'  %james
      :-  '1 Peter'  %peter-1
      :-  '2 Peter'  %peter-2
      :-  '1 John'  %john-1
      :-  '2 John'  %john-2
      :-  '3 John'  %john-3
      :-  'Jude'  %jude
      :-  'Revelation'  %revelation
  ==
--
```

### Retrieval Grammar

**(incomplete section)**

In [SQL terms](https://en.wikipedia.org/wiki/SQL_syntax), a basic query would look something like this:

```sql
SELECT * FROM table WHERE name = 'Genesis';
```

Since we only have one “table” (`store`), we don't need the `FROM` clause.  We also don't calculate derivative quantities, so we're stuck with just the key or something systematically available in the same place every time.  (This is a great extension to make, by the by.)  So our query statement will end up more like this:

```sql
SELECT * WHERE genesis IN key
```

which should batch-select all documents with the clause `%genesis` in the key.  (As we have keys now, we see `%genesis-1-1` and so forth.)

We don't have any more grammar right now, so we'll have a pretty minimal command parser:

```hoon
|%
++  par-select  (jest 'SELECT')
++  par-where   (jest 'WHERE')
++  par-in      (jest 'IN')
++  par-statement  ;~(plug par-select ace tar ace par-where ace sym:so par-in sym-so)

--

|%
++  par-list  ;~(plug (jest 'list') ace stap)
++  par-diff  ;~(plug (jest 'diff') ace stap ace dem:ag ace dem:ag)
++  par-draw  ;~(plug (jest 'draw') ace stap)
++  par-span  ;~(plug (jest 'span') ace stap ace sym:so)
++  par-name  ;~(plug (jest 'name') ace stap ace sym:so)
++  par       ;~(pose par-list par-diff par-draw par-span par-name)
--
```

If we wanted to add some variety to the statements, what could we do?  The easiest thing is to allow more variety for `WHERE` statements, like `SELECT * WHERE length > 100` or `SELECT * WHERE chapter = 2`.  An optional `ORDER BY` suffix would also be straightforward.


##  The `++abet` Pattern

**(incomplete section—let's finish together if we have time)**

The logic of `%rkyv` compound operations is ripe for use with the [`++abet` nested core pattern](https://developers.urbit.org/blog/nested-core-pattern).  Let's refactor the agent to use it.

  > Once you are comfortable thinking in terms of cores and doors, the nested core pattern is a natural evolution to a more abstract and powerful viewpoint. Just as a door generalizes certain aspects of a gate to a more general usage, the nested core pattern serves to generalize the door by effectively providing a higher-level script for operations.

**`/app/rkyv.hoon`**

```hoon
TODO
```


##  Exercises

- Implement an alias system for `%rkyv`.  This would involve adding a new type of `+$value`, `[%alias =key]`, to allow redirection to values (i.e. multiple keys per value).
- Give the database a chatbot agent so it can be used in Talk or Pongo.
- Calculate secondary qualities (such as length) so that `WHERE` gives more options, like `length > 100`.
- Implement [Conor Stack's Little Database](https://cstack.github.io/db_tutorial/) in Urbit.
- Implement a [Git server](https://urbit.org/grants/git-on-clay) in Urbit.
