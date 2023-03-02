---
title: "Threads"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Explain the utility of threads."
  - "Use 🕷️Spider to dispatch and manage threads."
runes:
  - "`!<`"
  - "`;<`"
keypoints:
  - "🕷️Spider threads are useful for transient or likely-to-fail processes."
readings:
  - "https://developers.urbit.org/guides/additional/threads/fundamentals"
  - "https://developers.urbit.org/reference/arvo/threads/examples/child-thread"
  - "https://developers.urbit.org/reference/arvo/threads/gall/start-thread"
  - "https://developers.urbit.org/reference/arvo/threads/overview"
homework:
  - "https://forms.gle/jAhGoXpVapUWf8UY7"
mirror: "https://github.com/sigilante/curriculum/blob/master/asl-2023.1/asl5.md"
video: "https://youtu.be/h2eY5ONMAsA"
---

#   🕷️ `asl5`.  Threads.
##  App School Live Lesson 5

##  Transient Processes

- App Workshop Live has been moved up to April 12.
  - https://developers.urbit.org/courses/awl

All Urbit code occupies one of these categories:

-   Runtime (Nock interpreter, persistence engine, I/O drivers, jets)
-   Kernel vanes (managed by Arvo)
-   Userspace agents (managed by `%gall`, permanent state)
-   Userspace threads (managed by Spider or `%khan`, transient state)

A thread is a function which takes arguments and produces a result.  Unlike a gate, it is not a pure function:  it can perform input and output, and it may fail.

An agent is permanent and bulletproof.  All state transitions are defined, and each action it performs is a transaction.  Code upgrades preserve existing state.

However, an agent can have trouble with complex input and output.  Since each state transition must be explicitly handled, the complexity of an agent explodes with the amount of I/O it handles.  At best, this results in long and complex code; at worst, unexpected states are mishandled, corrupting permanent state.

A thread's strength is that it can easily perform complex I/O operations.  It uses what's often called the [IO monad](https://urbit.org/blog/io-in-hoon/) (plus the exception monad) to provide a natural framework for I/O.

A thread's weakness is its impermanence and liability to fail unexpectedly.  In most of its intermediate states, it expects only a small number of events (usually one), so if it receives anything it didn't expect, it fails.  When code is upgraded, it's impossible to upgrade a running thread, so it fails.

If you want permanence and persistence, use an agent.  If the agent needs a complex sequence of I/O operations, reduce the sequence to a single operation (from the point of view of the agent) by writing a thread to handle everything.  That way, the agent's state only changes in response to the success of the thread, and an I/O failure never leads to partial state changes.

You have already used threads in the Dojo:  anything prefixed with a `-` hep, like `-test`, is a thread.  In this lesson, we need to learn how to a thread works, how to compose a thread, and how to invoke a thread from inside a Gall agent.

##  How Threads Work

Threads can be defined in a separate file in `/ted` or inline within an agent (e.g. as an arm or simply an expression).

As of this writing, threads can be invoked using Gall's `%spider` agent or via the more recent Khan vane (`%k`).  You will see both in this document, altho we will start with the older `%spider` approach.

Let's crack a thread open and see what one looks like up front.  `/ted/time.hoon`, or `-time`, is used to time an event; it accepts a relative time to wait and returns the actual time waited (which should be close unless some other event intervenes, like a system shutdown).

**`/ted/time.hoon`**:

```hoon
/-  spider
/+  strandio
=,  strand=strand:spider
^-  thread:spider
|=  arg=vase
=/  m  (strand ,vase)
^-  form:m
=+  !<([~ arg=@dr] arg)
;<  now-1=@da  bind:m  get-time:strandio
;<  ~          bind:m  (sleep:strandio arg)
;<  now-2=@da  bind:m  get-time:strandio
(pure:m !>(`@dr`(sub now-2 now-1)))
```

Line by line:

```hoon
/-  spider
/+  strandio
=,  strand=strand:spider
```

Boilerplate:  load the `spider` structure file, load the `strandio` helper library for I/O operations, and rename the `strand` so it's easier to refer to.

```hoon
^-  thread:spider
|=  arg=vase
=/  m  (strand ,vase)
^-  form:m
```

`/sur/spider/hoon` defines a thread as `+$  thread  $-(vase _*form:(strand ,vase))`; that is, a gate which takes a `vase` and returns the `form` of a `strand` that produces a `vase`.  In other words, the thread doesn't just produce a result, it actually produces a strand that takes input and produces output from which a result can be extracted.  (That's what `form` accomplishes here.)

It works like this:

![thread diagram](https://storage.googleapis.com/media.urbit.org/site/thread-diagram.png)

Threads typically do a bunch of I/O so one can't just immediately produce a result and end. Instead the strand will get some input, produce output, get some new input, produce new output, and so forth, until it eventually produces a `%done` with the actual final result.

```hoon
=+  !<([~ arg=@dr] arg)
;<  now-1=@da  bind:m  get-time:strandio
;<  ~          bind:m  (sleep:strandio arg)
;<  now-2=@da  bind:m  get-time:strandio
(pure:m !>(`@dr`(sub now-2 now-1)))
```

We encounter two new runes

- [`!<` zapgal](https://developers.urbit.org/reference/hoon/rune/zap#-zapgal) extracts a `vase` to a given mold if the type nests properly.  Here we use it because we need to get the value back out of the `vase` in a usable form.  Note as well that Dojo unitizes the argument it receives.  (`!<` zapgal operates on the type, while `;;` micmic operates on the value.)  It's the opposite of `!>` zapgar.
- [`;<` micgal](https://developers.urbit.org/reference/hoon/rune/mic#-micgal) is designed to build pipelines of dependent clauses, much like `;~` micsig for parsers and unit tests.  Basically, `;<` micgal lets you sequence two expressions; here the first two arguments are a mold and the `bind` gate, then the first expression to complete and the second.  `/ted/time.hoon` sequences three `;<` micgal expressions together because it is explicitly timing an interval

We extract the current time using `++get-time:strandio` (look it up, it's even simpler than a `%behn` call), then wait an interval (which does use `%behn`) and grab the time again.  The final result is a `vase` of the time delta wrapped in `pure`.`

- How could you alter `/ted/time.hoon` to just use `now`?

There are three important arms that we've run into here, all belonging to the `strand`:

-   `form` - the mold of the strand, the specialized type it will produce—for a thread, always `(strand ,vase)`
-   `pure` - produces a strand that does nothing except return a value (i.e., no I/O)
-   `bind` - monadic bind, like `then` in javascript promises

```hoon
> -time ~s1
~s10..002d
```

If you use a longer time, like `~s5`, then any commands you type in the Dojo while the thread is waiting will show `%dy-edit-busy`.  This means that the Dojo is blocking on waiting for execution.  If you get stuck in a situation like this, press `⌫` to cancel the thread.


##  Composing a Thread

A very simple thread:

```hoon
/-  spider
/+  strandio
=,  strand=strand:spider
^-  thread:spider
|=  arg=vase
=/  m  (strand ,vase)
^-  form:m
(pure:m arg)
```

Save and run this.  Any surprises?  (The dojo wraps arguments as a vase so that's why it's `[~ 'foo']` rather than just `foo`.)

Any nontrivial thread will need to `bind` values for deferred results.  `bind` takes two gates as arguments; it calls the first function and if it succeeds, it calls the second with the result of the first as its sample.

For the most part when you get started, you can treat the above (and `;<` micgal) as boilerplate that you'll swap out your processing pieces for.  For acquiring and using data, the `/lib/strandio.hoon` library is invaluable.

Let's write a thread that fetches a value from a public API.  This thread accepts as argument the name of a Pokémon and retrieves related information from [the Pokédex API](https://pokeapi.co/).

**`/ted/pokedex.hoon`**

```hoon
/-  spider
=,  strand=strand:spider
^-  thread:spider
|=  arg=vase
=/  m  (strand ,vase)
^-  form:m
=+  !<([~ arg=@t] arg)
=/  base-url  "https://pokeapi.co/api/v2/pokemon/"
=/  url  (weld base-url (trip arg))
;<  pokeinfo=json  bind:m  (fetch-json:strandio url)
(pure:m !>(pokeinfo))
```

This returns a raw JSON, which of course will need to be parsed and reparsed to be useful.  But it reduces the complex I/O network request to a single line in a calling agent.  (Guess what your homework will be!)

```hoon
> -pokedex %raichu
[ %o  
   p  
 { [p='base_experience' q=[%n p=~.243]]  
   [ p='forms'  
       q  
     [ %a  
         p  
       ~[  
         [ %o  
             p  
           { [p='url' q=[%s p='https://pokeapi.co/api/v2/pokemon-form/26/']]  
             [p='name' q=[%s p='raichu']]
...
```


##  Calling a Thread

### From a `/ted` File

As we pointed out earlier, the Dojo is instrumented to invoke threads using the `-` hep notation:

```hoon
> -test ~[/===/tests]
```

This syntax works for the `%base` desk, but threads on other desks will need to include the desk in the command:  `-sandbox!call`.

Within an agent, a thread will be called and its result subscribed to.  This looks like a pair of cards passed to Spider with whatever appropriate information:

```hoon
=/  tid  `@ta`(cat 3 'thread_' (scot %uv (sham eny.bowl)))
=/  ta-now  `@ta`(scot %da now.bowl)
=/  start-args  [~ `tid byk.bowl(r da+now.bowl) p.q.vase !>(q.q.vase)]
:_  this
:~  [%pass /thread/[ta-now] %agent [our.bowl %spider] %watch /thread-result/[tid]]
    [%pass /thread/[ta-now] %agent [our.bowl %spider] %poke %spider-start !>(start-args)]
==
```

(Thread IDs should be unique.)

When the thread returns, the value will come in via the subscription in the `++on-agent` arm as a `%fact` of `cage` `%thread-done` (if successful) or `%thread-fail` (if not).

There's a pretty good guide to all of this in the Thread Guide that is worth working through in detail.  The docs also cover child threads, or threads spawned by threads.

- When you're feeling bold, have a gander at `/ted/test.hoon`.

### Inline

The alternative to Spider is the new `%khan` vane, which can launch threads directly.

```hoon
:*  %pass
    /path-name        ::  path
    %arvo  %k  %fard  ::  Arvo vane and %khan mode
    %namespace        ::  namespace
    %thread-name      ::  /ted/thread-name.hoon
    %noun             ::  mark (always %noun for now)
    !>  :*            ::  thread arguments:
      bowl            ::    bowl (entropy etc.)
      other-info      ::    other arguments for thread
    ==
==
```

Such a thread looks normal, based on what we've done above.  Results come in via `++on-arvo` instead of via `++on-agent`, however.

```hoon
++  on-arvo
  |=  [=wire =sign-arvo]
  ^-  (quip card _this)
  ?+  wire  (on-arvo:default wire sign-arvo)
      [%thread-name ~]
    `this
  ==
```

A Khan thread invocation is similar to a Gall `%spider` thread.  Cards to invoke `-azimuth-load` look like this in the two lingos:

```hoon
::  Khan
[%pass /al %arvo %k %fard %base %azimuth-load %noun !>(~)]

::  Gall/Spider
[%pass /thread/azimuth-load %agent [our.bowl %spider] %watch /thread-result/[tid]]
[%pass /thread/azimuth-load %agent [our.bowl %spider] %poke %spider-start !>(~)]
```

The above invocation relies on a thread already having been defined in `/ted`.  We can also define a thread inline and invoke it with Khan:

```hoon
=/  shed
  =/  m  (strand ,vase)
  ;<  ~  bind:m  (poke:strandio [our %hood] %helm-hi !>('hi'))
  ;<  ~  bind:m  (poke:strandio [our %hood] %helm-hi !>('there'))
  (pure:m !>("product"))
[%pass /wire %arvo %k %lard %base shed]
```

A Khan task can be one of:

- `%fard` is an in-Arvo thread (like a regular Gall call) from `/ted`.
- `%fyrd` is a thread invocation from outside of Arvo (i.e. the runtime).
- `%lard` uses an inline thread definition.


##  Working with `strandio`

`/lib/strandio.hoon` provides common utility services for threads.  For instance, `++fetch-json` automatically unwraps JSON returned by a `GET` request to a given URL.

```sh
curl --location --request GET "https://sampledataapi.com/API/getcategory"
```

```hoon
(fetch-json:strandio 'https://sampledataapi.com/API/getcategory')
(fetch-cord:strandio 'https://sampledataapi.com/API/getcategory')
```

- Interpret `/ted/code` (`-code`).

    ```hoon
    /-  spider                                                                                            
    /+  strandio
    =,  strand=strand:spider
    ^-  thread:spider
    |=  arg=vase
    =/  m  (strand ,vase)
    ^-  form:m
    ;<  =bowl:spider  bind:m  get-bowl:strandio
    ;<  code=@p  bind:m  (scry:strandio @p /j/code/(scot %p our.bowl))
    %-  pure:m
    !>  ^-  tape
    %+  slag  1
    (scow %p code)
    ```


##  Resources

- [Thread Guide, “Fundamentals”](https://developers.urbit.org/guides/additional/threads/fundamentals)
- [Thread Guide, “Child Thread”](https://developers.urbit.org/reference/arvo/threads/examples/child-thread)
- [Thread Guide, “Gall:  Start Thread”](https://developers.urbit.org/reference/arvo/threads/gall/start-thread)
- [Arvo Reference, “Threads”](https://developers.urbit.org/reference/arvo/threads/overview)
