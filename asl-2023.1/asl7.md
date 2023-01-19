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

#   🦏 `lesson7`.  Design Patterns.
##  App School Live Lesson 7

This lesson aims to upgrade your app development skills to a more professional plane by identifying and employing specific design patterns.  We will highlight:

1. Using generators to wrap pokes.
2. Using libraries (both system and third-party) to simplify processing.
3. Using the nested core `+abet` design pattern.

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

https://developers.urbit.org/guides/additional/app-workbook/ahoy#gen-generator-files

### Aside:  `%dbug`

What is `%dbug` doing?  How does it work?
TODO

##  Useful Libraries

As Urbit is a personal server, many operations you'll carry out involve processing incoming or outgoing data.  Several libraries have been developed to facilitate server actions.  Once you know the facility of a particular library, you can treat calls to it as boilerplate.

### `/lib/server.hoon`

Server is a system library which facilitates

### `/lib/rudder.hoon`

Rudder is a third-party library developed by ~palfun-foslup.

### `/lib/schooner.hoon`

Schooner is a third-party library developed by Quartus.

### `/lib/gossip.hoon` ???

default-agent

Besides server actions, there are other ways to configure an Urbit ship or running process.

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

`/lib/agentio` considered harmful:  or at least too much work to actually be worthwhile in constructing cards.

##  Nested Cores

- TODO:  engine pattern

o `|nuke %docs, =desk %.y` and the `|install ~pocwet %docs` ?
