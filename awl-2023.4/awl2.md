---
title: "Command Line"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Produce a command-line agent to interact with Clay entities."
runes: []
keypoints: []
readings:
  - "https://developers.urbit.org/reference/arvo/clay/clay"
  - "https://developers.urbit.org/reference/arvo/clay/architecture"
homework: []
mirror: "https://github.com/sigilante/curriculum/blob/master/awl-2023.4/awl2.md"
video: "https://youtu.be/3zTO3AQZO-8"
---

#   🖪 `awl2`. Filesystem

Our objective in this lesson is to leverage our mastery of CLI tooling and the capabilities of Clay to produce a minimalist version control interface.

In this lesson, we will examine how Clay works, build a CLI agent, calculate diffs, produce styled text output, and put these ideas together into a simple version control tool.


##  Clay

[Clay](https://developers.urbit.org/reference/arvo/clay/clay) serves as Urbit's filesystem.  Clay has three main responsibilities:

1. Manage desks and files, in particular file builds.
2. Provision marks, a system of noun transformation.
3. Handle over-the-air system upgrades (desk merges).

In order to build on top of Clay's capabilities as a version-controlled filesystem, we have to first understand something of what Clay is capable of doing and how it works.  We will elide complex operations like desk merging and file building for the current lesson, instead focusing on data structures, individual file reads, marks, and scries.

### Desks and files

Clay's data structures are pretty complicated, so let's sketch out a 10,000' view of the necessary parts.  At the highest level, Clay maintains vane state as a `+$raft`, a data structure primarily aimed at serving as a file database and managing subscriptions and permissions:

**`/sys/vane/clay.hoon`**

```hoon
::
::  Formal vane state.
::
::  --  `rom` is our domestic state.
::  --  `hoy` is a collection of foreign ships where we know something about
::      their clay.
::  --  `ran` is the object store.
::
+$  raft                                                ::  filesystem
  $:  rom=room                                          ::  domestic
      hoy=(map ship rung)                               ::  foreign
      ran=rang                                          ::  hashes
      ...
  ==                                                    ::
```

`+$raft` is the primary data structure for the filesystem; we note in particular `rom`, domestic files; `hoy`, foreign files; and `ran`, hashes; along with some miscellaneous elements lke mount points.

Our domestic filestore (in `+$room`) is a `(map desk dojo)` or collection of desk states organized by desk labels (`+$desk` is merely `@tas`).  The desk state is:

**`/sys/arvo.hoon`**

```hoon
::
::  Domestic desk state.
::
::  Includes subscriber list, dome (desk content), possible commit state (for
::  local changes), possible merge state (for incoming merges), and permissions.
::
+$  dojo
  $:  qyx=cult                                          ::  subscribers
      dom=dome                                          ::  desk state
      per=regs                                          ::  read perms per path
      pew=regs                                          ::  write perms per path
      fiz=melt                                          ::  state for mega merges
  ==
```

Right now we mainly care about the desk state:

**`/sys/lull.hoon`**

```hoon
::
::  Desk state.
::
::  Includes a checked-out ankh with current content, most recent version, map
::  of all version numbers to commit hashes (commits are in hut.rang), and map
::  of labels to version numbers.
::
::  `mim` is a cache of the content in the directories that are mounted
::  to unix.  Often, we convert to/from mime without anything really
::  having changed; this lets us short-circuit that in some cases.
::  Whenever you give an `%ergo`, you must update this.
::
+$  dome
  $:  let=aeon                                        ::  top id
      hit=(map aeon tako)                             ::  versions by id
      lab=(map @tas aeon)                             ::  labels
      tom=(map tako norm)                             ::  tomb policies
      nor=norm                                        ::  default policy
      mim=(map path mime)                             ::  mime cache
      fod=flue                                        ::  ford cache
      wic=(map weft yoki)                             ::  commit-in-waiting
      liv=zest                                        ::  running agents
      ren=rein                                        ::  force agents on/off
  ==                                                  ::
```

and in particular those `tako`s, which we'll use to look up files in a bit.

In a sense, the actual file database of Clay is a `(map lobe page)`, or a map from the hash of a raw file to the file itself as a `cask` or pair of mark and data (any mold, very general).  This is derived from the top-level `+$raft` via `+$rang`, which contains the data as `(map lobe page)`.  (Because this data repository is stored above the desk level, files can be stored singly with multiple references to the data from different desks.)

```hoon
+$  lobe  @uvI                    ::  /sys/lull
+$  page  (cask)                  ::  /sys/arvo
?=  lat  (map lobe page)          ::  /sys/lull
```

This also explains why you have to have a mark defined in `/mar` in order to include a file on a desk:  otherwise the `cask` cannot resolve.  It works here because the resolution of the `cask` takes place on a specific desk, and here is more of just a label for deferred use later.

We normally access file data through a `path`.  The `path` to a file is a convention that nods to Unix but also generally works to access resources organized hierarchically.  The `path` is actually resolved through the whimsically-named `+$yaki` data structure for a commit, which contains the `(map path lobe)` that allows files to be resolved from their `path` to their `lobe` to their `page`.

```hoon
+$  yaki                                              ::  commit
  $:  p=(list tako)                                   ::  parents
      q=(map path lobe)                               ::  namespace
      r=tako                                          ::  self-reference
      t=@da                                           ::  date
  ==                                                  ::
```

(Phew, that's a bit of a journey.)

If we want to access the contents of a file directly, we use a scry into Clay's namespace, typically with a `%x` care:

```hoon
> .^(@t %cx %/gen/cat/hoon)  
'::  ConCATenate file listings\0a::\0a::::  /hoon/cat/gen\0a  ::\0a/?    310\0a/  
+    pretty-file, show-dir\0a::\0a::::\0a  ::\0a:-  %say\0a|=  [^ [arg=(list pat  
h)] vane=?(%g %c)]\0a=-  tang+(flop `tang`(zing -))\0a%+  turn  arg\0a|=  pax=pa  
th\0a^-  tang\0a=+  ark=.^(arch (cat 3 vane %y) pax)\0a?^  fil.ark\0a  ?:  =(%sc  
hed -:(flop pax))\0a    [>.^((map @da cord) (cat 3 vane %x) pax)<]~\0a  [leaf+(s  
pud pax) (pretty-file .^(noun (cat 3 vane %x) pax))]\0a?-     dir.ark             
                              ::  handle ambiguity\0a    ~\0a  [rose+[" " `~]^~  
[leaf+"~" (smyt pax)]]~\0a::\0a    [[@t ~] ~ ~]\0a  $(pax (welp pax /[p.n.dir.ar  
k]))\0a::\0a    *\0a  =-  [palm+[": " ``~]^-]~\0a  :~  rose+[" " `~]^~[leaf+"*"  
(smyt pax)]\0a      `tank`(show-dir vane pax dir.ark)\0a  ==\0a==\0a'
```

At the current time, Clay only stores entire files (or tombstones); the diff storage was removed since it was proving unnecessary in practice.  We will reconstruct diff capabilities later in this tutorial.

- [~wicdev-wisryt, “Clay Technical Walkthrough”](https://www.youtube.com/playlist?list=PL8h4Lku3qajB3GUIO7rxFGLNaiNWqUHoQ) (somewhat outdated)

### Marks and noun transformation

![](https://www.serebii.net/potw-xy/evolution/Machamp.png)

Given file data, how can we access it or transform it?  Let's imagine Urbit's data type scheme as having three levels:

1. **Molds** are gates that validate a given input type.  Atom auras and basic `+$` lusbuc type arms behave this way.
2. **Vases** are a pair of type and data:  that is, a cell whose head is a Hoon-recognized type (or alias if `$+` buclus was used) and whose tail is the corresponding data as a noun.  We use vases frequently in data transmission since we can send the noun safely then reconstruct it when needed.
3. **Marks** are more complicated rules for transforming nouns, such as a structured `%html` file to a `%txt` file (or `(list cord)`).  They may be lossy, since the noun transformation rule's output may not carry the same information as the input.

Most of the time, we let Gall and the other vanes handle mark transformation for us invisibly:  if we have defined a `++json:grab` arm in our mark file for instance then then conversion should just happen when we receive a value from the browser client session.

But if we're going to build a VCS CLI agent, then we may want the ability to manually convert between mark types.  What would that look like?

Urbit's mark system supports dynamic marks, which handle vases of data, and static marks which are just for values.  Here we'll use static mark conversion gates.

To convert from JSON to text, we use a `%f` care and appropriate mark names:

```hoon
> =json-to-txt .^($-(json wain) %cf /===/json/txt)

> (json-to-txt (need (de-json:html '{"message":"Hello Mars!"}')))
<|{"message":"Hello Mars!"}|>
```

Since the scry is passed through an appropriate gate, we use [`$-` buchep](https://developers.urbit.org/reference/hoon/rune/buc#--buchep) to build an input/output gate.  Furthermore, the mark must supply the appropriate `++grab` arm:

**`/mar/json.hoon`**

```hoon
++  grow                                                ::  convert to
  |%
  ++  mime  [/application/json (as-octs:mimes -:txt)]   ::  convert to %mime
  ++  txt   [(en:json jon)]~
  --
```

Other ways of building mark conversion cores can provide a lot of power, but that's overkill for our current needs.

Finally, note that `++mime:grow` is highly recommended:

> When you `|commit` a file to a `desk` mounted to Unix, Clay will receive the data as a `%mime` `mark`, and then convert it to the `mark` matching the file extension. It will perform the same operation in reverse when mounting a `desk` to Unix. For this reason, any `mark` you wish to be able to access from the Unix filesystem should have `%mime` conversion routines. In certain cases (such as the scry interface), Eyre will also need to convert your `mark` to a `%mime` in order to encode it in an HTTP response, so you may require a `+mime` arm for that reason as well.

- [Urbit Docs, “Clay:  Marks:  Overview”](https://developers.urbit.org/reference/arvo/clay/marks/marks)
- [Urbit Docs, “Clay:  Marks:  Using Marks”](https://developers.urbit.org/reference/arvo/clay/marks/using-marks)


##  VCS

### Clay Guarantees

From the perspective of a version control system, what does Clay have to offer?  Clay makes three guarantees:

1. **Referential transparency.**  "A request must always yield the same result for all time."  The exception to this is tombstoning, since a resource can become unavailable subsequently to its publication.  Note that because of this, we have built-in versioning.

2. **Typed data.**  Marks allow us to access and convert between data types, rather like MIME types.  Ultimately all data are stored as nouns with type metadata attached via the `cask`.

3. **Globally addressable file system.**  Entailed with referential transparency is the fact that every version of a file can be uniquely referred to using the `beak`.

    Conventionally we obtain an example `beak` from the `/===` convention at the Dojo prompt, where we see that it consists of the ship, the desk, and the timestamp.
    
    ```hoon
    > /===
    [~.~zod ~.base ~.~2023.3.2..21.22.46..234d ~]
    ```
    
    That third element, here the timestamp, is actually a type union called a `case`.  We can refer to a file by the timestamp, meaning the last modification before the current time; by a label; by a revision number; or by a hash.

    **`/sys/arvo.hoon`**

    ```hoon
    +$  case
      $%  ::  %da:  date
          ::  %tas: label
          ::  %ud:  sequence
          ::  %uv:  hash
          ::
          [%da p=@da]
          [%tas p=@tas]
          [%ud p=@ud]
          [%uv p=@uv]
      ==
    ```

    The revision number is displayed when `|commit` is used to modify a file, e.g.
    
    ```hoon
    > |commit %base
    >=
    + /~zod/base/2/gen/fib/hoon
    ```

    We can access a file using any of these; here, we use the timestamp `now` and then a revision number.

    ```hoon
    > .^(@t %cx /===/gen/fib/hoon)
    '|=  n=@ud\0a^-  @ud\0a?:  =(n 1)  1\0a?:  =(n 2)  1\0a(add $(n (dec n)) $(n (dec (dec n))))\0a\0a'
    
    > .^(@t %cx /(scot %p our)/base/2/gen/fib/hoon)
    '|=  n=@ud\0a^-  @ud\0a?:  =(n 1)  1\0a?:  =(n 2)  1\0a(add $(n (dec n)) $(n (dec (dec n))))\0a\0a'
    ```

    (Incidentally, the part of the path after the `beak` is called the `spur`.)

- [Hoon docs, “Clay Architecture:  Revision Control”](https://developers.urbit.org/reference/arvo/clay/architecture#revision-control)

### `%prat`

In this lesson, we will specify a CLI version control system to:

1. Produce the current version of a document.
2. Maintain a history of the document, typically as a series of diffs, or changes.
3. Calculate the net changes between two revision points.
4. Produce the file at a particular revision point in its history.
5. Convert the file between marks.

With Clay, we can get #1 and #4 for free.  Calculating the diffs will require us to do more calculation.

Since as Linus Torvalds jokes that [he names all his software projects after himself](https://www.computerworld.com/article/2810180/after-controversy--torvalds-begins-work-on--git-.html), we will call our minimalist VCS implementation [`%prat`](https://en.wiktionary.org/wiki/pratfall#English).  We expect operations to be carried out at the `%prat` CLI or equivalently using the Dojo prompt and `%prat`-specific generators.

```hoon
prat> draw /===/dais/test/txt
dojo> :prat +draw /===/rug/test/txt
```

To start, we will define a few CLI actions.  These will correspond to pokes and generators.  `%prat` will overlay Clay so no `git init` equivalent is needed:  every desk can validly work with `%prat`.  Similarly, no `git add` or `git commit` equivalents are needed, unless we decide to start using the Clay tagging mechanism.

- `draw` will `+cat` the value of the `%prat` resource.
- `list` will show the history of a resource in `%prat` (`git log`).
- `diff` will show the calculated difference between two times in the history of a `%prat` resource (`git diff`).
- `span` will attempt to convert the data from its native mark to another (no Git equivalent as Git is not typed).
- `name` will label a given commit (`git tag`, sort of).

Since Clay is a typed and timestamped file system, we don't need to worry about maintaining that information separately.

#### Data Structures

In a typical version control system, we would have to specify data structures like [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) which allow us to track individual file and branch history.  Clay offers userspace this for free—obviously internally it has its own representations, but they can be largely treated as invisible to us.

That said, it's worth taking a quick look at how [Clay](https://developers.urbit.org/reference/arvo/clay/architecture) actually stores files.  Fundamentally, a file is a delimited collection of bytes on disk.  Urbit represents these as a noun, like everything else.  Marks (among other roles) act as "file types", handlers that show how the file data "prefers" to be accessed.  Clay stores a table of `path`s and a hash of the associated data (along with commit metadata and other details).  So ultimately a Clay file is conceptually accessed via a `path`, but really is stored independently of that `path` in memory layout.  (This is also how Clay can deduplicate files such as libraries which may be present on more than one desk.)

`%prat` only needs to query Clay data to carry out its calculations over files.

`%prat` will recognizes only one kind of event mark:  `%prat-action` (to poke or use the agent).  At the current time, `%prat` doesn't talk to any other agents so no effect or update mark is necessary.

**`/sur/prat.hoon`**

```hoon
|%
+$  action
  $%  [%list pax=path]
      [%diff pax=path v1=@ud v2=@ud]
      [%draw =path]
      [%span =path to-mark=term]
      [%name =path label=term]
  ==
--
```

**`/mar/prat/action.hoon`**

```hoon
/-  prat
|_  =action:prat
++  grab
  |%
  ++  noun  action:prat
  --
++  grow
  |%
  ++  noun  action
  --
++  grad  %noun
--
```

#### CLI Logic

We need to write a parser which can handle the following commands:

- `draw <path>` will `+cat` the value of the `%prat` resource.
- `list <path>` should list the previous versions of a file at a given path.
- `diff <path> <version> <version>` should show the diff (see below) of two versions of the file.  (Just numbers for now.)
- `span <path> <to-mark>` will attempt to convert the data from its native mark to another.
- `name <path> <label>` will add a `@tas` label to the commit in Clay.

There is no equivalent `prat` command for `git init` or `git clone` (since these are handled by the desk mechanism of Clay), or for `git add` (since all files in a desk are monitored).  It's worth thinking about commit messages tho—Clay does technically support some metadata but it largely hasn't been used yet (see Exercises below).

From `awl1`, we know that a similar rule can be constructed using components like these:

```hoon
++  cmd  ;~(pose (jest 'list') (jest 'diff') (jest 'draw'))
```

Since `diff` wants two `path`s instead of one, we'll actually need to construct a more complex set of rules:

```hoon
|%
++  par-list  ;~(plug (jest 'list') ace stap)
++  par-diff  ;~(plug (jest 'diff') ace stap ace dem:ag ace dem:ag)
++  par-draw  ;~(plug (jest 'draw') ace stap)
++  par-span  ;~(plug (jest 'span') ace stap ace sym:so)
++  par-name  ;~(plug (jest 'name') ace stap ace sym:so)
++  par       ;~(pose par-list par-diff par-draw par-span par-name)
--
```

We're not throwing away extraneous values in the current version, but it extricates what we want so we can build proper expressions:

```hoon
> (scan "etch /hello/mars label-me" par-etch)
[ 'etch'
  ' '
  [[[i='/' t=<||>] 478.560.413.032] [i=[~ 1.936.875.885] t=~]]
  ' '
  7.308.547.713.872.847.212
]
```

On this basis, we can `++cook` results to produce actions for our agent.  For instance, given the rules above, we can construct handler gates for our overall command parser:

```hoon
/-  prat
|%
++  par-list  ;~(plug (jest 'list') ace stap)
++  par-diff  ;~(plug (jest 'diff') ace stap ace dem:ag ace dem:ag)
++  par-draw  ;~(plug (jest 'draw') ace stap)
++  par-span  ;~(plug (jest 'span') ace stap ace sym:so)
++  par-name  ;~(plug (jest 'name') ace stap ace sym:so)
++  par       ;~(pose par-list par-diff par-draw par-span par-name)
++  cmd-list
  %+  cook
  |=  [p=cord q=cord r=path]
  ^-  action:prat
  list+r
  par-list
++  cmd-diff
  %+  cook
  |=  [p=cord q=cord r=path s=cord t=@ud u=cord v=@ud]
  ^-  action:prat
  diff+[r t v]
  par-diff
++  cmd-draw
  %+  cook
  |=  [p=cord q=cord r=path]
  ^-  action:prat
  draw+r
  par-draw
++  cmd-span
  %+  cook
  |=  [p=cord q=cord r=path s=cord t=term]
  ^-  action:prat
  span+[r t]
  par-span
++  cmd-name
  %+  cook
  |=  [p=cord q=cord r=path s=cord t=term]
  ^-  action:prat
  name+[r t]
  par-etch
++  parser  ;~(pose cmd-list cmd-diff cmd-draw cmd-span cmd-name)
--
```

#### `draw`

- `draw <path>` will `+cat` the value of the `%prat` resource.

This is simply a scry wrapper.

```hoon
++  draw-file
  |=  =path
  ^-  wain
  %-  to-wain:format
  .^(@t %cx path)
```

At this point, it's worth thinking about whether we want the user to specify the whole `path` or to just associate `%prat` with a particular desk, but we'll punt on that question and just require the entire `path` to be specified.

#### `diff`

- `diff <path> <version> <version>` should show the diff of two versions of the file.

A [diff](https://en.wikipedia.org/wiki/Diff) is a data comparison showing the differences between two data structures, typically files.  The basic diff algorithm uses the concept of a [_longest common subsequence_](https://rosettacode.org/wiki/Longest_common_subsequence) (LCS), typically over lines.  (We will retain operations over lines for simplicity of output, but there could be good reasons for analyzing per character instead.  It's more difficult to display such an analysis intelligibly.)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Nubio_Diff_Screenshot3.png/330px-Nubio_Diff_Screenshot3.png)

Here the longest common subsequence is `this is changed` and other text represents deletions or interpolations.

Clay has stored diffs in the past, but the current version stores entire files.  Thus we will manually implement file diffs in userspace for `prat` so we can examine one version of the LCS algorithm.

##### An LCS Algorithm

Our proof-of-concept algorithm will not be the most efficient solution.

1. Retrieve each base text (there should be two).  (Convert `cord` to `tape` using `++crip`.)
2. Break into constituent units (here, lines).  (In Hoon, we will have a `(list tape)` or a `wall`.)
3. Recursively check if we are at the end of either sequence; if so, return nothing (to add).
4. Otherwise, if the first elements match, append the head to the LCS and continue to calculate at #3.
5. If the first elements don't match, then we try both possible sequences from this point forward at #3.

**`/lib/diff.hoon`**

```hoon
|%
++  linebreak
  |=  =tape
  ^-  wall
  =/  lines  *wall
  |-  ^-  wall
  =/  idx  (find "\0a" tape)
  ?~  idx  (snoc lines tape)
  $(lines (snoc lines (scag (need idx) tape)), tape (slag +((need idx)) tape))
++  lcs
  ::  bit of a joke:  X-tudo is a cheeseburger w/ everything in Brazil
  |=  [xtudo=wall ytudo=wall]
  ^-  wall
  ::  if no lines left, return
  ?~  xtudo   *wall
  ?~  ytudo   *wall
  ::  final result
  =/  lcs  *wall
  ::|-  ^-  wall
  =/  xhead=tape   -:(scag 1 `wall`xtudo)
  =/  yhead=tape   -:(scag 1 `wall`ytudo)
  =/  xtail=wall   (slag 1 `wall`xtudo)
  =/  ytail=wall   (slag 1 `wall`ytudo)
  ?:  =(xhead yhead)
    (weld ~[xhead] $(xtudo xtail, ytudo ytail))
  =/  xhead-ytail  $(ytudo ytail)
  =/  yhead-xtail  $(xtudo xtail)
  ?:  (gth (lent xhead-ytail) (lent yhead-xtail))
    xhead-ytail
  yhead-xtail
--
```

**`/tests/lib/diff.hoon`**

You can run these unit tests with `-test /=diff=/tests/lib`.

```hoon
/+  *test, *diff
|%
++  test-single-line
  ;:  weld
  %+  expect-eq
    !>  `wall`~["Hello"]
    !>  (lcs (linebreak "Hello") (linebreak "Hello\0aMars!"))
  %+  expect-eq
    !>  `wall`~["Hello"]
    !>  (lcs (linebreak "Hello\0aMars!") (linebreak "Hello"))
  %+  expect-eq
    !>  `wall`~["Mars!"]
    !>  (lcs (linebreak "Hello\0aMars!") (linebreak "Mars!"))
  ==
++  test-double-lines
  ;:  weld
  %+  expect-eq
    !>  `wall`~["Hello"]
    !>  (lcs (linebreak "Hello\0aMars!") (linebreak "Hello\0aworld!"))
  %+  expect-eq
    !>  `wall`~["Mars!"]
    !>  (lcs (linebreak "Hello\0aMars!") (linebreak "Hola\0aMars!"))
  ==
++  test-many-lines
  ;:  weld
  %+  expect-eq
    !>  `wall`~["Hello" "Welcome" ""]
    !>  (lcs (linebreak "Hello\0aMars!\0aWelcome\0ahome.\0a\0a") (linebreak "Hello\0aworld!\0aWelcome\0aback.\0a"))
  %+  expect-eq
    !>  `wall`~["Hello" "Welcome"]
    !>  (lcs (linebreak "Hello\0aMars!\0aWelcome\0ahome.") (linebreak "Hello\0aworld!\0aWelcome\0aback."))
  ==
++  test-hanging-newline
  ;:  weld
  %+  expect-eq
    !>  `wall`~["Hello"]
    !>  (lcs (linebreak "Hello") (linebreak "Hello\0a"))
  ==
++  test-leading-newline
  ;:  weld
  %+  expect-eq
    !>  `wall`~["Hello"]
    !>  (lcs (linebreak "\0aHello") (linebreak "Hello"))
  ==
--
```

##### A Diff Algorithm from LCS

Given the above code, we can load two files and compare their differences.  That will require new arms to show the deletions and additions for each side.  We'll add these to `/lib/diff.hoon`.  We will use an ordered `map`, or `mop`, based on the list index in the `wall`.  The index will be the row index for each row in the left-hand entry or right-hand entry, and one of `?(%d %a %$)` for deleted/added/same.  (We could make a more complicated data structure, but let's save that for the database lessons.)

**Additions to `/lib/diff.hoon`**

```hoon
+$  op  ?(%d %a %$)
++  left-hand   :: deletions
  |=  [x=wall lcs=wall]
  =|  lines=((mop @ud op) gth)
  =/  on  ((on @ud op) gth)
  =/  idx  0
  =/  ids  0
  |-  ^+  lines
  ?:  =((lent x) idx)  lines
  ?:  =((snag idx x) (snag ids lcs))
    :: same in both
    $(idx +(idx), ids +(ids), lines (put:on lines idx %$))
  :: not found in lcs
  $(idx +(idx), lines (put:on lines idx %d))
++  right-hand  ::  additions
  |=  [lcs=wall y=wall]
  =|  lines=((mop @ud op) gth)
  =/  on  ((on @ud op) gth)
  =/  idy  0
  =/  ids  0
  |-  ^+  lines
  ?:  =((lent y) idy)  lines
  ?:  =((snag idy y) (snag ids lcs))
    :: same in both
    $(idy +(idy), ids +(ids), lines (put:on lines idy %$))
  :: not found in lcs
  $(idy +(idy), lines (put:on lines idy %a))
```

**Additions to `/tests/lib/diff.hoon`**

```hoon
++  test-lhs
  ;:  weld
  %+  expect-eq
    !>  (gas:((on @ud op) gth) *((mop @ud op) gth) ~[[2 %$] [1 %d] [0 %$]])
     !>  (left-hand `wall`~["Hello" "new" "world!"] `wall`~["Hello" "world!"])
   ==
 ++  test-rhs
   ;:  weld
   %+  expect-eq
     !>  (gas:((on @ud op) gth) *((mop @ud op) gth) ~[[2 %$] [1 %a] [0 %$]])
     !>  (right-hand `wall`~["Hello" "world!"] `wall`~["Hello" "new" "world!"])
  ==
```

We still don't have a great way to display this information yet.  (See the exercises.)

- [`sigilante/diff`](https://github.com/sigilante/diff)

#### Back to `diff`

Now that we can diff two files, let's look at our `%prat` functionality:

```hoon
|=  [pal=path par=path]
^-  wall
=/  lhs  ~(ram re .^(%txt %cx pal))
=/  rhs  ~(ram re .^(%txt %cx par))
(lcs:diff lhs rhs)
```

(Notice that we have [formatted text](https://developers.urbit.org/guides/core/hoon-school/P-stdlib-io#formatted-text) in our output here.  This can be converted to a `tape` using `~(ram re my-tank)`.)

Let's use `wain`s as our final output.  Modify that gate to instead return a `wain` (list of `cord`s rather than `tape`s).

```hoon
++  wall-to-wain
  |=  =wall
  ^-  wain
  =|  =wain
  |-
  ?~  wall  wain
  $(wall t.wall, wain (snoc wain (crip i.wall)))
++  wain-to-wall
  |=  =wain
  ^-  wall
  =|  =wall
  |-
  ?~  wain  wall
  $(wain t.wain, wall (snoc wall (trip i.wain)))
++  diff-files
  |=  [pal=path par=path]
  ^-  wain
  %-  turn  :_  crip
  =/  lhs  ~(ram re .^(%txt %cx pal))
  =/  rhs  ~(ram re .^(%txt %cx par))
  (lcs:diff lhs rhs)
```

#### `list`

- `list <path>` should list the previous versions of a file at a given path.

The naïve version of this code will simply pull the file at every revision number for the desk.  We can use a `%w` care or a `%s` to infer this information, since both give us current revision numbers (for the file and for the desk, respectively):

```hoon
> .^(cass:clay %cs /(scot %p our)/base/1/late)
[ud=2 da=~2023.5.8..22.47.02..fc7b]

> .^(cass:clay %cw /===/gen/cat/hoon)
[ud=1 da=~2023.4.28..18.23.34..09d4]

> +cat /==/(scot %ud 1)/gen/cat/hoon
/~zod/base/2/gen/cat/hoon
::  ConCATenate file listings
::  * * *
==
```

If we wanted to do this really properly, we would then check the diff of each revision number and only report the changed ones; for the time being, we will simply print all of them.

This yields:

```hoon
++  list-revisions
  |=  =path
  ^-  wain
  %-  wall-to-wain
  =/  max=@ud  ud:.^(cass:clay %cw path)
  =/  idx  1
  =|  =wall
  |-
  ?:  =(max idx)  wall
  =/  pax  `^path`:(weld (scag 2 `^path`path) `^path`~[(scot %ud idx)] (slag 3 path))
  $(idx +(idx), wall (snoc wall (trip .^(@t %cx pax))))
```

#### `span`

- `span <path> <to-mark>` will convert the file from one mark to another.

Given a file path—presumptively the most recent—and a target mark, convert between them.  This requires us to build a mark conversion gate, then apply it and yield the output noun.

(**WIP** this one is a bit of a stinker and I may have bitten off more than I can chew)

```hoon
++  span-marks
  |=  [=path to=@ta]
  =/  from  (rear path)
  .^($-(from to) %cf path)
```


> Now, changing gears: Can I dynamically load a mark from disk at runtime? That is, given a `term` which is the name of a mark file (but not the type like `json` or `wain`), can I grab the appropriate mark type?  TODO

```
;;(mold %json)
p:$:vale:.^(dais:clay cb+/=base=/json)
```

#### `name`

- `name <path> <label>` will add a `@tas` label to the commit in Clay.

A Clay `+$case` can be one of an `aeon` number, a `term` label, a timestamp, or a `@uv` hash.  Altho there are not yet affordances built to take much advantage of labels, let's start to change that.

There is an existing `|label` generator we can use as a reference for how this will work:

```hoon
> |label %base %tag-20230504
labeled /~zod/base/tag-20230504

> +cat /~zod/base/tag-20230504/gen/ls/hoon
/~zod/base/tag-20230504/gen/ls/hoon
::  LiSt directory subnodes
::
::::  /hoon/ls/gen
  ::
/?    310
/+    show-dir
::
::::
  ::
~&  %
:-  %say
|=  [^ [arg=path ~] vane=?(%g %c)]
=+  lon=.^(arch (cat 3 vane %y) arg)
tang+[?~(dir.lon leaf+"~" (show-dir vane arg dir.lon))]~
```

Our version will pass a card for the agent to use:

```hoon
++  name-commit-card
  |=  [=path label=@tas]
  ^-  card
  |^
  [%pass /prat %arvo %c [%info [(get-desk path) %| label (get-aeon path)]]]
  ++  get-desk
    |=  =^path
    ^-  @ta
    (snag 1 path)
  ++  get-aeon
    |=  =^path
    ^-  @ta
    (snag 2 path)
  --
```

Of course, we still don't have a way to _use_ such labels yet, but building this sort of affordance will enable that usage later on.  There is a system for tagging commit messages—see Story, described below—which could open up some possibilities.

#### Agent Logic

`%prat` need maintain no state since Clay does that for it.  It will, however, have to handle pokes and `%shoe` cards.

**`/app/prat.hoon`**

```hoon {% mode="collapse", copy="true" %}
/-  prat
/+  default-agent, dbug, pratlib=prat, shoe, sole
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0  %0
+$  card  card:agent:shoe
--
%-  agent:dbug
=|  state-0
=*  state  -
^-  agent:gall
%-  (agent:shoe action:prat)
^-  (shoe:shoe action:prat)
|_  =bowl:gall
+*  this     .
    default  ~(. (default-agent this %|) bowl)
    leather  ~(. (default:shoe this action:prat) bowl)
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
  ^+  |~(nail *(like [? action:prat]))
  %+  stag  |
  parser:pratlib
++  on-command
  |=  [=sole-id:shoe =action:prat]
  ^-  (quip card _this)
  ?-    action
      [%draw *]
    =/  =tape  (draw-file:pratlib path:action)
    :_  this
    :~  [%shoe ~ sole+klr+~[(crip ~(ram re leaf+tape))]]
    ==
      [%list *]
    =/  =tape  (list-revisions:pratlib path:action)
    :_  this
    :~  [%shoe ~ sole+klr+~[(crip ~(ram re leaf+tape))]]
    ==
      [%diff *]
    =/  =tape  (diff-files:pratlib path:action v1:action v2:action)
    :_  this
    :~  [%shoe ~ sole+klr+~[(crip ~(ram re leaf+tape))]]
    ==
      [%span *]
    :_  this
    :~  [%shoe ~ sole+klr+~[(crip "{<action>}")]]
    ==
      [%name *]
    `this
    :::_  this
    :::~  (name-commit-card:pratlib path:action label:action)
    ::==
  ==
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

The agent's `++command-parser` arm is pretty generic:

```hoon
++  command-parser
  |=  =sole-id:shoe
  ^+  |~(nail *(like [? action:prat]))
  %+  stag  |
  parser:pratlib
```

Notice that we don't have to `++cook` the parser here to get a `+$action:prat`, since we already did that in the library.

The `++on-command` arm will utilize our libraries from just above:

```hoon
++  on-command
```

#### Pokes

TODO:  No pokes yet, but should be straightforward.

#### Generators

TODO:  I didn't get to make these since I hadn't made pokes yet.

#### Testing

We need to create a desk which contains only the files sufficient for the marks to work and has a history for a single file with subsequent changes.

```hoon
> |new-desk %cinema

> |mount %cinema
```

Create the following file and `|commit %cinema` in between altering the file for each version.  This will create a version history of `/films.txt` which exhibits several possible interesting diffs.

**`/films.txt`** Version 1:

```hoon
Films by Wes Anderson
```

**`/films.txt`** Version 2:

```hoon
Films by Wes Anderson
Rushmore
```

**`/films.txt`** Version 3:

```hoon
Films by Wes Anderson
Rushmore
Midnight Kingdom
```

**`/films.txt`** Version 4:

```hoon
Films by Wes Anderson
2001:  A Space Odyssey
Rushmore
Midnight Kingdom
```

**`/films.txt`** Version 5:

```hoon
Films by Wes Anderson
Rushmore
Midnight Kingdom
```

Given this file history, you should be able to verify that `list`, `diff`, `draw`, and `span` all behave appropriately.  (Test `span` with e.g. the `%noun` mark.)  You'll need to `|link %prat` to access it via the command line.  `%prat` is running from the `%prat` desk still but can see all desks on your filesystem.


##  Story

Story is a set of generators to produce Clay commit messages.  The actual messages are stored in a file in Clay, effectively using a Clay as a database.  The generators are instrumented through `%hood`/`%helm` so they can pass notes to Arvo.

```hoon
> |new-desk %tale

> |mount %tale

> |cp /===/mar/story/hoon /=tale=/mar/story/hoon
+ /~zod/tale/2/mar/story/hoon

> |cp /===/sur/story/hoon /=tale=/sur/story/hoon
+ /~zod/tale/3/lib/story/hoon

> |cp /===/lib/story/hoon /=tale=/lib/story/hoon
+ /~zod/tale/4/lib/story/hoon

> |story-init, =desk %tale
+ /~zod/tale/5/story

> +story-read, =desk %tale

> |story-write 'Short message' 'Long descriptive message', =desk %tale
: /~zod/tale/6/story

> +story-read, =desk %tale
commit: 0vn.l7i50.emt3e.79vbv.tjuv6.ftaqk.pos61.iqa5q.j0jq4.7mn92.vjssn
Short message

Long descriptive message
```

Story is supported in `%base`, but you'll need to make the mark available on the target desk as done here.


##  `%linedb`

Uqbar has produced [`%linedb`](https://github.com/uqbar-dao/linedb), a command-line file manager in Urbit.  Alas, there is no external documentation yet so you'll need to shake someone down to find out more.


##  Exercises

- Produce a prettyprinter for diffs as produced by `/lib/diff.hoon`.  Conventionally, diffs are shown line-by-line with `+`/`-` in the left margin and each line listed in order.  This will require creating a union of the left-hand and right-hand diffs.

  It's also helpful to employ some color here.  `/sys/lull` defines `+$styx` styled text type include text colors.  It can be used with `%sole-effect`s to highlight characters.  `/lib/dprint` contains examples of how to approach this, as does [`%track7`](https://github.com/sigilante/track7).

  Print the deletions in red (`%r`) and the additions in green (`%g`).

- Extend `%prat` to support diffs across desks (`link`).  (Easy)
- Extend `%prat` to maintain commit messages (`etch` as modification of `name` with a Story message as well).  (Medium)
- Extend `%prat` to support `|commit` from the host filesystem (`load`).  (Medium)
- Extend `%prat` to support remote repos (unspecified).  (Hard, but not _too_ hard)

  If all `%prat` commands were implemented, then the full set of commands would include:
  
  - `list`
  - `diff`
  - `draw`
  - `span`
  - `name`
  - `etch`
  - `link`
  - `load`

- Instead of `%prat`, implement [Gitlet](http://gitlet.maryrosecook.com/), a minimalist Git about a thousand lines long in JavaScript, in Hoon using Clay.  (Very hard)

  Use the Git-style commands:
  - `init`
  - `add`
  - `commit`
  - `remote`
  - `fetch`
  - `merge`
  - `branch`
  - `checkout`
  - `push`

  You should be able to use some of the logic of `%prat` in this implementation.
