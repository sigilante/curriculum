---
title: "A Simple Agent"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Describe how Gall instruments an agent using standard arms."
  - "Produce a minimal working example of an agent."
runes: []
keypoints:
  - "Produce a minimalist ⛓️Gall agent."
  - "Employ the `default-agent` library."
  - "Employ the `%dbug` agent wrapper."
readings:
  - "https://developers.urbit.org/guides/core/app-school/2-agent"
  - "https://developers.urbit.org/guides/core/app-school/3-imports-and-aliases"
  - "https://developers.urbit.org/guides/core/app-school/4-lifecycle"
homework: "https://forms.gle/upKZoSe89XZAebou5"
mirror: "https://github.com/sigilante/curriculum/blob/master/asl-2023.1/asl0.md"
video: "https://youtu.be/3_HmMUOPZGg"
---

#   🦀 `lesson0`.  A Simple Agent.
##  App School Live Lesson 0

Some setup preliminaries:

- https://github.com/TheCombineDAO/vial
- https://developers.urbit.org/guides/core/environment

I have made two changes to this edition of App School Live:

1. There is an additional lesson which covers using more advanced code patterns.
2. I am requiring only seven of the eight homeworks be completed to be considered a finisher.

Homework has a soft deadline ten days after the lesson (so the second Saturday) and a hard deadline on March 25.  The soft deadline allows us to batch grading for feedback in a timely manner.

---

(train analogy:  hand car, hi-rail truck, locomotive)

Any operating system must define an expected way to load and execute programs.  For instance, the Unix/Linux platforms define an [`ELF` object format](https://www.linuxjournal.com/article/1060) which specifies where in the file the dynamic linker (library loader) is located, then loads and launches the main application process.  The Java Virtual Machine, used by Java, Java applets, Kotlin, and Clojure, specifies a [`JAR` pacakge file](https://en.wikipedia.org/wiki/JAR_%28file_format%29) with a manifest file to specify where the bytecode for the actual main application process is located.

Urbit's operating system, Arvo, is an event handler and dispatcher.  It provides a userspace app framework called Gall which requires a standard application interface and in return gives you access to a rich operating environment, state management, and peer-to-peer software distribution.

We will use “agent” and “app” interchangeably, although there are some subtle differences:  an app would likely be the entire desk you are distributing while an agent is a single process on that desk.

Since everything in Urbit is a noun, and everything nontrivial is a core (cell of `[battery payload]`), we can infer that a Gall agent is both a noun (code and data are interchangeable) and a core.  More particularly, a Gall agent is a door with ten definite arms that are invoked by Arvo upon specific system events.  The Gall agent sample is a `bowl`, or collection of standard system information like that given to a `%say` generator.

### A Minimal Working Agent

Let's create the simplest possible Gall agent:

**`/app/alfa.hoon`**:

```hoon
|_  =bowl:gall
++  on-init   `..on-init
++  on-save   !>(~)
++  on-load   |=(vase `..on-init)
++  on-poke   |=(cage !!)
++  on-watch  |=(path !!)
++  on-leave  |=(path `..on-init)
++  on-peek   |=(path ~)
++  on-agent  |=([wire sign:agent:gall] !!)
++  on-arvo   |=([wire sign-arvo] !!)
++  on-fail   |=([term tang] `..on-init)
--
```

- What elements do you recognize here?
- Which elements do you not recognize?

The big ones include:

- `vase` is a pair of type and value, as produced by `!>` zapgar.  "Structurally, it's a pair of an explicit reification of a type and an untyped noun. This lets us represent a value which has a type that isn't known at compile time."
- `cage` is a pair of mark and vase.  "A mark is a textual tag that should correspond to the particular dynamic type in the vase."
- `path` is a list of `@ta` knots.  It serves as an identifier for resource locations.
- `wire` is an alias of `path` which acts as a unique identifier for a request.
- `` `..on-init`` is a `unit` of the parent core of `++on-init`:  or in other words the agent door itself.
- `sign` and `sign-arvo` are incoming events (in response to a standing request for data).

Minor ones may include:

- `term` is an alias of `@tas`, a text atom.
- `tang` is a formatted print structure.

### Desk Setup

We should work in a new clean fakeship.  Build one using the [developer pill](https://developers.urbit.org/blog/dev-pill).

```sh
$ urbit -B dev-latest.pill -F zod
$ urbit dock zod
$ ./zod/.run
```

This time, however, let's create a new desk:

```hoon
> |merge %alfa our %base

> |mount %alfa
```

```sh
$ cd zod/alfa
$ echo "~[%alfa]" > desk.bill
```

and save the above file to `alfa/app/alfa.hoon`.

```hoon
> |commit %alfa

> |install our %alfa
```

We will use this pattern again and again when creating new agents.

However, this agent is blind and mute:  it can receive and respond to nothing sensible.  For instance, if we attempt to poke the agent, the `++on-poke` arm simply registers a failure to process information (`!!` zapzap, crash).

```hoon
> :alfa &noun %~
/sys/vane/gall/hoon:<[1.372 9].[1.372 37]>
/app/alfa/hoon:<[5 23].[5 25]>
dojo: app poke failed
```

#### Commentary

Line by line:

```hoon
|_  =bowl:gall
...
--
```

A Gall agent is a particular kind of core called a _door_.  The main thing to know is that we can provide the `bowl`, which is a data structure containing the attested ship identity, the timestamp, entropy for randomness, and some other system information.

```hoon
++  bowl              ::  standard app state
  $:  $:  our=ship    ::  host ship
          src=ship    ::  guest ship
          dap=term    ::  agent name
      ==              ::
      $:  wex=boat    ::  outgoing subscriptions
          sup=bitt    ::  incoming subscriptions
      ==              ::
      $:  act=@ud     ::  change number
          eny=@uvJ    ::  entropy
          now=@da     ::  current time
          byk=beak    ::  load source
  ==  ==
```

Without elaborating on what these all mean today, you can see the kinds of data provided to the agent core.

```hoon
++  on-init   `..on-init
```

The `++on-init` arm returns the whole agent (the parent of the current arm) prepended with a `~` sig null value.

```hoon
++  on-save   !>(~)
++  on-load   |=(vase `..on-init)
```

The `++on-save` and `++on-load` arms are used to pack the agent's state ahead of an upgrade, and then to unpack and possibly update the structure of the agent's state after the upgrade.

```hoon
++  on-poke   |=(cage !!)
++  on-peek   |=(path ~)
```

A poke is a one-off message, like a data status request.  Pokes initiate some kind of well-defined action by the agent, often either triggering an event or requesting a data return of some kind.  Pokes are useful as single-instance requests.

A peek represents a direct look into the agent state.  A peek (or “scry”) can't change anything in the state, but it's a quick way to directly get information.

```hoon
++  on-watch  |=(path !!)
++  on-leave  |=(path `..on-init)
```

Gall agents utilize a dataflow computing model, wherein changes in state are indicated to subscribers who then modify or react in turn to the flow of data arriving from this agent.  A subscription is a data-reactive standing request for changes.  For instance, one can watch a database agent for any changes to the database.  Whenever a change occurs, the agent notifies all subscribers, who then act as they should in the event of a message being received (e.g. from a particular ship).  Subscriptions are probably the most complicated part of writing agents, so we'll spend some time in a moment looking at them in more detail.

`++on-watch` registers a new subscriber.  `++on-leave` registers a dropped subscriber.

```hoon
++  on-agent  |=([wire sign:agent:gall] !!)
++  on-arvo   |=([wire sign-arvo] !!)
++  on-fail   |=([term tang] `..on-init)
--
```

These three arms deal with system events.  The `++on-agent` and `++on-fail` arms are called in certain circumstances (i.e. as an update to a subscription to another agent or cleanup after a `%poke` crash). We can leave them as boilerplate for now.

The `++on-arvo` arm handles information passed back from the Arvo operating function (or system kernel).  For instance, if we set a timer for an event, the wake-up call will be handled here.

None of these have specified the return type, so it is as yet unclear what they are doing.  Let's talk about agents some first.

### Agent as State Machine

Circling back around, what is an agent supposed to do?  Well, what is a regular program supposed to do?

> An agent is a piece of software that is primarily focused on maintaining and distributing a piece of state with a defined structure. It exposes an interface that lets programs read, subscribe to, and manipulate the state. Every event happens in an atomic transaction, so the state is never inconsistent. Since the state is permanent, when the agent is upgraded with a change to the structure of the state, the developer provides a migration function from the old state type to the new state type.
>
> It's not too far off to think of an agent as simply a database with developer-defined logic. But an agent is significantly less constrained than a database. Databases are usually tightly constrained in one or more ways because they need to provide certain guarantees (like atomicity) or optimizations (like indexes). Urbit is a single-level store, so atomicity comes for free.
>
> On the other hand, an agent is also a lot like what many systems call a "service". An agent is permanent and addressable -- a running program can talk to an agent just by naming it. An agent can perform IO, unlike most databases. This is a critical part of an agent: it performs IO along the same transaction boundaries as changes to its state, so if an effect happens, you know that the associated state change has happened.
>
> But the best way to think about an agent is as a state machine. Like a state machine, any input could happen at any time, and it must react coherently to that input. Ouput (effects) and the next state of the machine are both pure functions of the previous state and the input event. Of course, it's important to ensure there isn't an order of events that could cause your agent to enter an inconsistent state.
>
> We often think of state machines as finite state machines, but of course in this instance, the state is not actually finite (though it should be definable in a regular recursive data type).

### A Second Agent

Let's upgrade to something that looks more like a complete Gall agent.

**`/app/bravo.hoon`**

```hoon
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
+*  this      .
    default   ~(. (default-agent this %|) bowl)
++  on-init
  ^-  (quip card _this)
  ~&  >  '%bravo initialized successfully'
  =.  state  [%0 *(list @)]
  `this
++  on-save   on-save:default
++  on-load   on-load:default
++  on-poke   on-poke:default
++  on-arvo   on-arvo:default
++  on-watch  on-watch:default
++  on-leave  on-leave:default
++  on-peek   on-peek:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

```hoon
> |merge %bravo our %base

> |mount %bravo
```

```sh
$ cd zod/bravo
$ echo "~[%bravo]" > desk.bill
```

and save the above file to `bravo/app/bravo.hoon`.

```hoon
> |commit %bravo

> |install our %bravo
```

This agent still does nothing, but now it does nothing in a more sophisticated way.  It also stores a list of values as internal state, although we can't change it yet.

Line-by-line again, only looking at the new parts:

```hoon
/+  default-agent, dbug
```

The first line imports two libraries:
- `/lib/default-agent` provides some standard arms we can use as placeholders for parts of the agent we don't want or need to create.
- `/lib/dbug` allows us to directly peek inside the agent and grab its state.

```hoon
|%
+$  versioned-state
  $%  state-0
  ==
::
+$  state-0
  $:  [%0 values=(list @)]
  ==
+$  card  card:agent:gall
--
```

We then create a `|%` barcen core which defines some molds or types we'll need later.  Most saliently, every real Gall agent has a versioned state which allows you to define upgrade paths for subsequent releases.  Here we call the particular version `+$state-0`; it contains only a list of atoms we can use for any purpose.  We also commonly alias the Gall message `card` for easier reference.

```hoon
%-  agent:dbug
=|  state-0
=*  state  -
^-  agent:gall
```

We wrap the whole core in the `%dbug` agent so we can peek at the state directly, then we give a face to the state as `state-0` and return something that fits the Gall agent mold.

```hoon
|_  =bowl:gall
+*  this      .
    default   ~(. (default-agent this %|) bowl)
::
++  on-init
  ^-  (quip card _this)
  ~&  >  '%bravo initialized successfully'
  =.  state  [%0 *(list @)]
  `this
++  on-save   on-save:default
++  on-load   on-load:default
++  on-poke   on-poke:default
++  on-arvo   on-arvo:default
++  on-watch  on-watch:default
++  on-leave  on-leave:default
++  on-peek   on-peek:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

Finally we have our main agent again, the rest being helpful boilerplate.  Most of the lines have been explicitly replaced with the `/lib/default` version of the arms, which is a completely satisfactory solution to pass and do nothing.

- Examine `/lib/default-agent/hoon`.

Some points of interest now are the aliases we pin and the initialization.

1. We pin `this` to refer to the current agent subject, and `default` to refer to the library.  Commonly we may also refer to a helper core which will sit beside the agent and provide a cleaner way to process data.
2. We then initialize the state with the bunt, or empty value, of `(list @)` and return the unit of that state as before.  We also emit a side effect message indicating that the agent `++on-init` arm has successfully completed.  Notice that the return type of this and most arms is a `(quip card _this)`.  For the most part you can crib from existing code examples rather than needing to deeply parse the mold here.
3. Note that the cores are not manually composed using `=<` tisgal or `=>` tisgar.  In fact, Gall agents are wrapped with `=~` tissig to automatically compose all cores together.  I must admit, however, that seeing side-by-side cores always leaves me a bit unsettled!

If we run this agent, we can see it initialize successfully, but we can't interact with it yet.  The docket file warning has to do with registration for release and we can ignore it for now.

```hoon
> |commit %bravo
+ /~zod/bravo/3/app/bravo/hoon

> |install our %bravo
kiln: installing %bravo locally
gall: installing %bravo
>   '%bravo initialized successfully'
[%docket %no-docket-file-for %bravo]

> :bravo +dbug
>   ~
```

##  Looking Ahead

Over the next few lessons, we will learn about Arvo system services—the vanes, like Clay and Eyre—and how to hook up more sophisticated agent logic to a proper front-end.  The ultimate goal of App School Live is for you to be able to write and distribute production-quality apps.  Mostly this means getting the back-end logic and the connection logic correct, deferring front-end design to the particular needs you'll have when designing and producing apps.

##  Resources

- [App School, “2. The Agent Core”](https://developers.urbit.org/guides/core/app-school/2-agent)
- [App School, “3. Imports and Aliases”](https://developers.urbit.org/guides/core/app-school/3-imports-and-aliases)
- [App School, “4. Lifecycle”](https://developers.urbit.org/guides/core/app-school/4-lifecycle)
