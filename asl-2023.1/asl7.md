---
title: "Design Patterns"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Use helpful libraries to facilitate coding."
  - "Employ the nested core design pattern in a Gall app."
runes: []
keypoints:
  - "Nested cores "
readings: []
homework:
  - "https://forms.gle/pV4mQyLiLiimCNVv6"
---

#   🦏 `asl7`.  Design Patterns.
##  App School Live Lesson 7

This lesson aims to upgrade your app development skills to a more professional plane by identifying and employing specific design patterns.  We will highlight:

0. A schema for mark and structure naming.
1. Proper upgrade protocol.
2. Using generators to wrap pokes.
3. Using libraries (both system and third-party) to simplify processing.


##  Mark/Structure Naming

Marks serve two primary roles in the Urbit ecology:

1. They serve as structure types and transformation rules for arbitrary nouns.
2. They serve as markers for 

Marks are often used in `cage`s, or `(pair mark vase)`, which allow us to transmit typed data between agents and ships.

A general pattern of mark names has emerged which favors `%agent-action` for ship-to-ship events, particularly pokes, and `%agent-update` for client-to-ship events.  `%agent-effect` is also in use for subscriber updates.

![](https://storage.googleapis.com/media.urbit.org/developers/vert-horz.svg)

In general, I counsel those two names for your basic work, and a system of six-letter words for other agent marks:  e.g., `inform`, `gossip`, `result`, `impact`, `change`, `impose`.  This yields a quick idiom that's easily recognizable (much like four-letter words in various parts of the system) and 

- [App Workbook, `%flap`](https://developers.urbit.org/guides/additional/app-workbook/flap)


##  State Upgrades

A state upgrade describes a transition rule from a current agent state to a new agent state.  This step can include adding or removing variables from the state, so the former state mold may not fit into the new state mold.

A basic state update takes the state matching the old state mold, modifies any values, and produces something meeting the new state mold.

From `/app/settings-store.hoon`:

```hoon
|%
+$  card  card:agent:gall
+$  versioned-state
  $%  state-0
      state-1
      state-2
  ==
+$  state-0  [%0 settings=settings-0]
+$  state-1  [%1 settings=settings-1]
+$  state-2  [%2 =settings]
--
::  ...
|%
++  on-load
  |=  =old=vase
  ^-  (quip card _this)
  =/  old  !<(versioned-state old-vase)
  |-
  ?-  -.old
    %0  $(old [%1 +.old])
    %1  $(old [%2 (~(put by *^settings) %landscape settings.old)])
    %2  `this(state old)
  ==
:: ...
--
```

One could define an upgrade path from each former state to the current state, eventually ballooning the number of transition definitions to $\sum_{n} i$.  For this reason, we prefer to go one at a time in `++on-load`.

(Incidentally, I slightly favor names for versions, e.g. `%zero` instead of `%0`, but it's no big deal either way.)


##  Generators

Don't poke explicitly at the command line:  build generators to organize the command.

It is better to structure your CLI experience around using generators:  easier to remember and write.  But agent generators can also be called via Eyre.

Agent-specific generator files can be much cleaner than manual poke logic:

```hoon
:ahoy|add-watch ~sampel-palnet ~h2
```

is the equivalent of

```hoon
:ahoy &ahoy-command [%add-watch ~sampel-palnet ~h2]
```

but allows the mark to be omitted and simplifies the cell syntax somewhat.

### Exercise:  Hood Generators

Examine the generators in `/gen/hood` to see how they wrap more complex pokes.

- [App Workbook, `%ahoy`](https://developers.urbit.org/guides/additional/app-workbook/ahoy#gen-generator-files)

### Aside:  `%dbug`

What is `%dbug` doing?  How does it work?  Look at [how the generators work](https://developers.urbit.org/guides/additional/app-workbook/dbug#how-the-generator-works) now.

We'll do more with agent wrappers in App Workshop Live.

- [App Workbook, `%dbug`](https://developers.urbit.org/guides/additional/app-workbook/dbug)


##  Useful Libraries

As Urbit is a personal server, many operations you'll carry out involve processing incoming or outgoing data.  Several libraries have been developed to facilitate server actions.  Once you know the facility of a particular library, you can treat calls to it as boilerplate.

### `/lib/server.hoon`

Server is a system library which offers Eyre-compatible wrappers for receive types and a send types, as well as common actions like requiring authentication (`+code`).



Perhaps the most common arm you will use is `++give-simple-payload`, which sends cards of `+$http-response-header` (an Eyre type consisting of `$`) with 

```hoon
++  give-simple-payload
  |=  [eyre-id=@ta =simple-payload:http]
  ^-  (list card:agent:gall)
  =/  header-cage
    [%http-response-header !>(response-header.simple-payload)]
  =/  data-cage
    [%http-response-data !>(data.simple-payload)]
  :~  [%give %fact ~[/http-response/[eyre-id]] header-cage]
      [%give %fact ~[/http-response/[eyre-id]] data-cage]
      [%give %kick ~[/http-response/[eyre-id]] ~]
  ==
```

`server` also provide [basic MIME type response headers](https://www.iana.org/assignments/media-types/media-types.xhtml), such as `image/png`:

```hoon
++  png-response
  =|  cache=?
  |=  =octs
  ^-  simple-payload:http
  :_  `octs
  [200 [['content-type' 'image/png'] ?:(cache [max-1-wk ~] ~)]]
```

### `/lib/schooner.hoon`

[Schooner](https://github.com/dalten-collective/schooner/) is a third-party library developed by Quartus.  Like `server`, it mainly provides wrappers for HTTP responses with the proper MIME `content-type` header information, and otherwise intends to simplify HTTP handling beyond `server`'s affordances.

You can see `schooner` in action in `%feature` and in `%flap`.

### `/lib/rudder.hoon`

[Rudder](https://github.com/Fang-/suite/blob/master/lib/rudder.hoon) is a third-party library developed by ~palfun-foslup.  `rudder` particularly facilitates Sail-based webpages (altho not exclusively since Sail is HTML).

Basically, three door arm builders produce page views:

- `++build` is for `GET` requests and produces a `+$reply` (`%page` or other server code results).
- `++argue` is for `POST` requests and produces a command (which may update the view).
- `++final` is called after `POST` requests to produce the updated view as a `+$reply`.

You can see `rudder` in action in `%pals`, in `%ahoy`, and in the legacy version of `%beacon`.

### `/app/settings-store.hoon`

`%settings-store` provides a way of setting system-wide values.  For instance, if we were using [`%l10n`](https://github.com/sigilante/l10n) to support multiple languages in our app, we could set a system-wide value `%language-default` with value `%en-us-latn` to prefer U.S. English with a Latin script.

`%settings-store` is an agent which maintains a data structure `(mip desk key bucket)` allowing you to look up per-desk entries.

```hoon
[%put-bucket desk=%base key=%language bucket={%default: %en-us-latn}]
```

Your agent would subscribe to the path

```hoon
/entry/base/language-default
```

The clunky part about `%setting-store` is that it is built for JSON operations.

As a tentative replacement for `%settings-store` for in-Urbit applications, consider [`%global-store`](https://github.com/sigilante/global-store), which I hope to get into the base distribution soon.


##  Miscellaneous Points

- `/lib/agentio` considered harmful:  or at least too much work to actually be worthwhile in constructing cards.
- When developing on a desk, it is useful to reset an agent sometimes in order to call `++on-init` again.  Currently that procedure looks like this:

  ```hoon
  > |nuke %agent, =desk %.y
  > |rein %desk [& %agent]
  ```

- Opportunities lecture next week.
