---
title: "Agents"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Produce an agent which accepts and emits pokes and peeks."
  - "Produce an agent which accepts and handles subscriptions for a dataflow-reactive process."
runes: []
keypoints:
  - "A ⛓️Gall agent acts as a back-end persistent server process if it doesn't have a front-end interface."
  - "Agents communicate using `card`s."
  - "Pokes and peeks are for one-off checks; subscriptions are for monitoring and responding to changes in upstream agent data."
readings:
  - "https://developers.urbit.org/guides/core/app-school/5-cards"
  - "https://developers.urbit.org/guides/core/app-school/6-pokes"
  - "https://developers.urbit.org/guides/core/app-school/8-subscriptions"
  - "https://developers.urbit.org/guides/core/app-school/10-scry"
homework:
  - "https://forms.gle/8VcUbce1Dcca2qnBA"
---

#   🐢 `lesson2`.  Agents.
##  App School Live Lesson 2

Most agent arms produce the same two things:  `(quip card _this)`, a list of effects to be emitted, and a new version of the agent itself, typically with an updated state. It thus behaves much like a state machine, performing the function `(events, old-state) => (effects, new-state)`.  This allows Gall agents to alter their own state as events occur.

Reactive computing describes a model wherein dependent values are updated as upstream values change.  For instance, in most programming languages a statement like `c = b + a` would assign `c` once and never change it even if `b` or `a` changed.  But a spreadsheet _would_ change `c` if either of its upstream components changed.  While Hoon is not data-reactive to this extent, it does prefer a subscription model wherein rather than actively requesting data through pokes and peeks (scries), data changes are pushed to a subscriber channel and subscribers are thereby notified (rather like a highly customizable RSS feed).

In this lesson, we will consider how agents communicate, then examine how pokes and peeks work for Gall agents.  Finally we will start working with subscriptions.


##  Cards

Vanes communicate using `moves`s, while Gall agents communicate using `card`s.  Most Gall agent arms result in `(quip card _this)` or similar; essentially, the list of new `card`s to process and the altered agent door.  A `card` is converted into a `move` by Gall behind the scenes when necessary.  A `move` has a bit more information than a `card` so that Arvo can track the call stack and the return path from the vane invoked.

Formally, a `card:agent:gall` is a `(wind note gift)`:  unfolded, either of two things:

```hoon
[%pass wire note]
[%give gift]
```

The type of the first field in a `%pass` card is a `wire`. A `wire` is just a list of `@ta`, with a syntax of `/foo/bar/baz`. When you `%pass` something to an agent or vane, the response will come back on the `wire` you specify here. Your agent can then check the `wire` and maybe do different things depending on its content. The [`wire`](https://developers.urbit.org/guides/core/app-school/types#wire) type is covered in the [types reference](https://developers.urbit.org/guides/core/app-school/types). We'll show how `wire`s are practically used later on.

The `note` is either:

```hoon
[%agent [=ship name=term] =task]
[%arvo note-arvo]
```

`%agent` `note`s are intended for other Gall agents, while `%arvo` `note`s are vane requests.  Above we carried these out with scries and cares:  here we will briefly examine them as `card`s.

![](https://media.urbit.org/guides/core/app-school/arvo-cards.svg)

On the other hand, if you `%give` a `gift`, then it can be one of four things:

```hoon
+$  gift
  $%  [%fact paths=(list path) =cage]
      [%kick paths=(list path) ship=(unit ship)]
      [%watch-ack p=(unit tang)]
      [%poke-ack p=(unit tang)]
  ==
```

Altogether:

![](https://media.urbit.org/guides/core/app-school/card-diagram.svg)


##  Pokes and Peeks

A poke is a message to an agent.  A poke requires a mark (or validated data type) and some data.  For instance, we could poke `%alfa` with the `noun` mark and the null value `~`.  Since `%alfa` has no handler code in its `++on-poke`, it is unable to do anything useful with the poke.

```hoon
> :alfa &noun ~
/sys/vane/gall/hoon:<[1.372 9].[1.372 37]>
/app/alfa/hoon:<[5 23].[5 25]>
dojo: app poke failed
```

A peek is a scry.  It is carried out with `.^` dotket.  The full description for a peek or scry permits any vane to be scried.  Gall agents use the `%gx` care to scry each other for information.

![](https://storage.googleapis.com/media.urbit.org/docs/arvo/scry-diagram-v2.svg)

A scry into `%alfa` could take the form:

```hoon
.^(@ %gx /=alfa=/test/noun)
```

but this sort of request will always fail since `%alfa` doesn't handle scries either.  Most commonly the mark at the end of the path is `noun` and any transformation is taken care of by the mold type at the beginning.

### Example Agent

The next agent we'll take a look at will allow two ships to poke each other and peek at state.  Each agent will maintain a list of numbers, but allow other agents to append numbers to the list (or pop them off).  (We won't filter for agent permissions right now, which would be critical for a real-world application.)

We will introduce marks at this point as well.  Marks serve the same role as file types:  they mark a set of data as having a particular structure.  They are like molds, but they include transformation rules as well, like how to turn an HTML data blob into a plaintext data blob.  Pokes are constrained to match the data structure indicated by the appropriate mark, then handled first by type then content.

To this end, we need three files:

- `/app/charlie.hoon` contains the main agent logic.
- `/sur/charlie.hoon` contains the permitted actions as a mold.
- `/mar/charlie/action.hoon` contains the mark for the actions.

Most agents will have these three files or similar analogues.

**`/app/charlie.hoon`**

```hoon
/-  *charlie
/+  default-agent, dbug
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0
  $:  [%0 values=(list @)]
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
  ?>  ?=(%charlie-action mark)
  =/  act  !<(action vase)
  ?-    -.act
      %push
    ?:  =(our.bowl target.act)
      `this(values [value.act values])
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %charlie] %poke mark vase]~
  ::
      %pop
    ?:  =(our.bowl target.act)
      `this(values ?~(values ~ t.values))
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %charlie] %poke mark vase]~
  ==
::
++  on-peek
  |=  =path
  ^-  (unit (unit cage))
  ?+  path  (on-peek:default path)
    [%x %values ~]  ``noun+!>(values)
  ==
++  on-arvo   on-arvo:default
++  on-watch  on-watch:default
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

**`/sur/charlie.hoon`**

```hoon
|%
+$  action
  $%  [%push target=@p value=@]
      [%pop target=@p]
  ==
--
```

**`/mar/charlie/action.hoon`**

```hoon
/-  *charlie
|_  act=action
++  grow
  |%
  ++  noun  act
  --
++  grab
  |%
  ++  noun  action
  --
++  grad  %noun
--
```

Set up the desk as usual:

```hoon
> |merge %charlie our %base

> |mount %charlie
```

```sh
$ cd zod/charlie
$ echo "~[%charlie]" > desk.bill
```

and save the above files to `charlie/`.

```hoon
> |commit %charlie

> |install our %charlie
```

Once that's launching correctly, two fakeships on the same local machine running `%charlie` can poke each other.  (The next ship after ~zod is ~nec; start that one or any other ship on the same local machine and install `%charlie` there as well.)

```hoon
::  Pokes should pass through the action mark.
:charlie &charlie-action [%push ~zod 100]
:charlie &charlie-action [%push ~nec 50]
:charlie &charlie-action [%pop ~zod]
:charlie &charlie-action [%pop ~nec]

::  Peeks need the return value specified.
.^((list @) %gx /=charlie=/values/noun)
```

Pokes pass through the action mark, which validates that they match the correct structure.  Here we provide them very explicitly at the command line, but we'll be able to trigger them using Javascript from a client session.

Peeks or scries are done using the Nock command `.^` dotket.  You have to specify the mold of the return type, the `%gx` care, and the path that the peek takes place on.  These are convenient but we'll prefer pokes for most one-off actions.

Because Urbit is a functional programming language with no side effects, to modify the state of an agent we have to replace the agent with appropriate changes made.  The Gall platform takes care of much of this for us, but we have to explicitly return a modified `this`, and sometimes getting the state back out can be a bit tricky until you get the hang of the type system's expectations.


##  Subscriptions

The basic unit of a subscription is the _path_.  An agent will typically define a number of subscription paths in its `++on-watch` arm, and other local or remote agents can subscribe to those paths.  The agent will then send out updates called `%fact`s on one or more of its paths, and _all_ subscribers to those paths will receive them.  An agent cannot send out updates to specific subscribers, it can only target a paths.  An agent can kick subscribers from its paths, and subscribers can unsubscribe from any paths.  Paths can be static or dynamic.

Agents talk to each other by means of `card`s, which are messages requesting or replying to other agents or parts of Arvo.  We'll introduce that mechanism for agents to talk to each other here as well.  For this agent, we will retain the peek/poke behavior from before and introduce a new subscriber behavior, wherein every follower is notified when the stack `values` changes.  (We don't have to track this manually, as Gall will do it for us.)  We'll build a separate `delta-follower` agent as well which will listen for subscription updates, but won't store any state itself.

**`/app/delta.hoon`**

```hoon
/-  *delta
/+  default-agent, dbug
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0
  $:  [%0 values=(list @)]
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
  ?>  ?=(%delta-action mark)
  =/  act  !<(action vase)
  ?-    -.act
      %push
    ?:  =(our.bowl target.act)
      :_  this(values [value.act values])
      [%give %fact ~[/values] %delta-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %delta] %poke mark vase]~
  ::
      %pop
    ?:  =(our.bowl target.act)
      :_  this(values ?~(values ~ t.values))
      [%give %fact ~[/values] %delta-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %delta] %poke mark vase]~
  ==
::
++  on-peek
  |=  =path
  ^-  (unit (unit cage))
  ?+  path  (on-peek:default path)
    [%x %values ~]  ``noun+!>(values)
  ==
++  on-watch
  |=  =path
  ^-  (quip card _this)
  ?>  ?=([%values ~] path)
  :_  this
  [%give %fact ~ %delta-update !>(`update`[%init values])]~
++  on-arvo   on-arvo:default
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

**`/sur/delta.hoon`**

```hoon
|%
+$  action
  $%  [%push target=@p value=@]
      [%pop target=@p]
  ==
+$  update
  $%  [%init values=(list @)]
      action
  ==
--
```

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
  --
++  grad  %noun
--
```

**`/mar/delta/update.hoon`**

```hoon
/-  *delta
|_  upd=update
++  grow
  |%
  ++  noun  upd
  --
++  grab
  |%
  ++  noun  update
  --
++  grad  %noun
--
```

**`/app/delta-follower.hoon`**

```hoon
/-  *delta
/+  default-agent, dbug
|%
+$  card  card:agent:gall
--
%-  agent:dbug
^-  agent:gall
|_  =bowl:gall
+*  this     .
    default  ~(. (default-agent this %|) bowl)
++  on-poke
  |=  [=mark =vase]
  ^-  (quip card _this)
  ?>  ?=(%noun mark)
  =/  action  !<(?([%sub =@p] [%unsub =@p]) vase)
  ?-    -.action
      %sub
    :_  this
    [%pass /values-wire %agent [p.action %delta] %watch /values]~
  ::
      %unsub
    :_  this
    [%pass /values-wire %agent [p.action %delta] %leave ~]~
  ==
::
++  on-agent
  |=  [=wire =sign:agent:gall]
  ^-  (quip card _this)
  ?>  ?=([%values-wire ~] wire)
  ?+    -.sign  (on-agent:default wire sign)
      %watch-ack
    ?~  p.sign
      ((slog '%delta-follower: subscribe succeeded!' ~) `this)
    ((slog '%delta-follower: subscribe failed!' ~) `this)
  ::
      %kick
    %-  (slog '%delta-follower: Got kick, resubscribing...' ~)
    :_  this
    [%pass /values-wire %agent [src.bowl %delta] %watch /values]~
  ::
    %fact
    ~&  >>  fact+p.cage.sign
    ?>  ?=(%delta-update p.cage.sign)
    ~&  >>  !<(update q.cage.sign)
    `this
  ==
++  on-watch  on-watch:default
++  on-peek   on-peek:default
++  on-init   on-init:default
++  on-save   on-save:default
++  on-load   on-load:default
++  on-arvo   on-arvo:default
++  on-leave  on-leave:default
++  on-fail   on-fail:default
--
```

Mount and make this desk as usual:

```hoon
> |merge %delta our %base

> |mount %delta
```

```sh
$ cd zod/delta
$ echo "~[%delta %delta-follower]" > desk.bill
```

and save the above file to `delta/app/delta.hoon`.

```hoon
> |commit %delta

> |install our %delta
```

You can interact with `%delta` the same way as `%charlie`, but you can also subscribe to updates in `%delta` with `%delta-follower`.

```hoon
> :delta &delta-action [%push ~zod 30.000]

> :delta-follower [%sub ~zod]
>=
%delta-follower: subscribe succeeded!
>>  [%fact %delta-update]
>>  [%init values=~[30.000]]

> :delta &delta-action [%push ~zod 10.000]
>=
>>  [%fact %delta-update]
>>  [%push target=~zod value=10.000]
```

The main thing to note is the use of `%fact` cards.  These are messages sent to all subscribers by the originator.  A subscriber subscribes to a `path` (which depends on the thing it is subscribing to) with a `wire` (which is a unique ID local to the subscriber).

One aside on handling pokes and subscriptions:  “Route on wire before sign, never sign before wire.”  That is, the path you subscribed on should be the basis for decision making, then the internal details.

So much for basic Gall agents.  You can implement anything you like using them, but right now you are limited to command-line interactions for the user interface.  Lesson 3 will focus on ingesting and processing data, then we will build out a front-end interface in Lesson 4.


##  Resources

- [App School, “5. Cards”](https://developers.urbit.org/guides/core/app-school/5-cards)
- [App School, “6. Pokes”](https://developers.urbit.org/guides/core/app-school/6-pokes)
- [App School, “8. Subscriptions”](https://developers.urbit.org/guides/core/app-school/8-subscriptions)
- [App School, “10. Scries”](https://developers.urbit.org/guides/core/app-school/10-scry)
