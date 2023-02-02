---
title: "Arvo Services"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Explain Arvo as a 🗃️state machine at the end of an 📬event log."
  - "Explain ❄️Kelvin versioning and identify the system components that require this approach."
  - "Explain the services 📻Ames provides to the system."
  - "Diagram the architecture of 📻Ames as a network."
  - "Explain the services ⏱️Behn provides to the system."
  - "Explain the services 📙Clay provides to the system."
  - "Identify key 📙Clay artifacts:  desks, marks, etc."
  - "Explain the services ⌨️Dill provides to the system."
  - "Explain the services 🌬️Eyre provides to the system."
  - "Explain the services ⛓️Gall provides to the system."
  - "Explain the services 🌺Iris provides to the system."
  - "Explain the services 🔑Jael provides to the system."
  - "Enumerate the secrets 🔑Jael tracks."
  - "Explain the services 🕸️Khan provides to the system."
runes:
  - "`/?`"
  - "`!?`"
  - "`.^`"
keypoints:
  - "Arvo acts as an event handler and maintains system state."
  - "Each vane provides a necessary systemwide accommodation."
  - "Kelvin versioning runes `/?` and `!?` allow you to pin a version number or require a version number."
readings:
  - "https://developers.urbit.org/guides/core/app-school/1-arvo"
  - "https://developers.urbit.org/guides/core/app-school/9-vanes"
  - "https://developers.urbit.org/reference/arvo/overview"
homework:
  - "https://forms.gle/vmoNLmLPrY6EFfs49"
mirror: "https://github.com/sigilante/curriculum/blob/master/asl-2023.1/asl1.md"
video: []
---

#   🦦 `asl1`.  Arvo Services.
##  App School Live Lesson 1

##  Arvo

Arvo is the Urbit OS and kernel which is written in Hoon, compiled to Nock, and executed by the runtime environment and virtual machine Vere. Arvo has currently nine kernel modules called vanes.

### 🗃️State Machine

Arvo itself has its own small codebase in /sys/arvo.hoon which primarily implements the transition function `(State, Event) -> (State, Effects)` for events injected by the runtime. It also handles inter-vane messaging, the scry system, and a couple of other things. Most of the heavy lifting is done by the vanes themselves - Arvo itself typically just routes events to the relevant vanes.

Each vane has its own state. Gall's state contains the agents it's managing, Clay's state contains all the desks and their files, Jael's state contains all its PKI data, etc. All the vanes and their states live in Arvo's state, so Arvo's state ultimately contains the entire OS and its data.

### 📬Event Log

Arvo's state is the end result of the events which have operated on it.  The formal state of an Arvo instance is an event history, as a linked list of nouns from first to last. The history starts with a bootstrap sequence that delivers Arvo itself, first as an inscrutable kernel, then as the self-compiling source for that kernel. After booting, we break symmetry by delivering identity and entropy. The rest of the log is actual input.

The formal state of an Arvo instance is an event history, as a linked list of nouns from first to last. The history starts with a bootstrap sequence that delivers Arvo itself, first as an inscrutable kernel, then as the self-compiling source for that kernel. After booting, we break symmetry by delivering identity and entropy. The rest of the log is actual input.  (The event log itself isn't in Arvo; it's stored by the runtime.)

### 🪆 Events

For Arvo, an event is an entry in the log (which feels rather circular BUT bear with me).  An event can consist of an arbitrary number of `move`s, which are “kernel-level actions”.  We'll examine those below.  Events have some nice guarantees, such as that they are _atomic_ and _consistent_, among others:

- **Atomic**:  When an event occurs in Arvo, e.g. the kernel is poked, the effects of an event are computed, the event is persisted by writing it to the event log, and only then are the actual effects applied.
- **Consistent**:  Every possible update to the database puts it into another valid state.

> Arvo handles nondeterminism in an interesting way.  Deciding whether or not to halt a computation that could potentially last forever becomes a heuristic decision that is akin to dropping a packet.  Thus it behooves one to think of Arvo as being a stateful packet transceiver rather than an ordinary computer—events are never guaranteed to complete, even if one can prove that the computation would eventually terminate.

The Arvo causal stack is called a `duct`. This is represented simply as a list of paths, where each path represents a step in the causal chain. The first element in the path is the first letter of whichever vane handled that step in the computation, or the empty span for Unix (the host OS, which must be used at some point for terminal events, network communications, etc.).

Arvo is designed to avoid the usual state of complex event networks: event spaghetti. We keep track of every event's cause so that we have a clear causal chain for every computation. At the bottom of every chain is a Unix I/O event, such as a network request, terminal input, file sync, or timer event. We push every step in the path the request takes onto the chain until we get to the terminal cause of the computation. Then we use this causal stack to route results back to the caller.

If `duct`s are a call stack, then how do we make calls and produce results? Arvo processes `move`s which are a combination of message data and metadata. There are four types of `move`s:  `%pass`, `%give`, `%slip`, and `%unix`.  Almost everything you will deal with is either a `note` (result of `%pass`) or a `$gift` (result of `%give`).

- [“Arvo Overview”](https://developers.urbit.org/reference/arvo/overview)

### ❄️Kelvin Versioning

> When we see a system that seems to want to expand indefinitely, we can and should look for a layer division within this system, separating an inner layer that tends to converge from an outer layer that naturally diverges.

You have probably heard at some point about _Kelvin versioning_, an approach to 

> The true, Martian way to perma-freeze a system is what I call Kelvin versioning.  In Kelvin versioning, releases count down by integer degrees Kelvin.  At absolute zero, the system can no longer be changed.  At 1K, one more modification is possible.

Urbit is not, of course, the only system to adopt an asymptotic approach to its final outcome.  Donald Knuth, famous for many reasons but in this particular instance for the typesetting system TeX, [has specified that TeX versions incrementally approach π.](http://www.texfaq.org/FAQ-TeXfuture) TeX will reach π definitively upon the date of Knuth's death, at which point all remaining bugs are instantly transformed into features and the version becomes π.  The current version of TeX is 3.14159265.  Dr Knuth was born in 1938.

> Kelvin versioned software cuts away until you reach a strong bedrock. Not every piece of software should have a Kelvin version, but infrastructure should.

Kelvin versioning isn't appropriate for many user-oriented applications, but it forms a parsimonious discpline for infrastructural tools.

Since Urbit intends to cool towards a final stable specification, each part of the operating system has a characteristic temperature; at the time of writing, these are:

- Arvo `%240`
- Hoon `%140`
- Zuse `%418` (hot enough to “cook eggs”)
- Lull `%329` (Arvo structures useful for bootstrapping the kernel)
- Nock `%4` (about at liquid helium; not clear what changes would even be desirable now)

Two aspirational runes implement parts of this vision in code:

- `/?` faswut (undocumented) pins a version number.  It is defined but explicitly ignored in `clay.hoon`.  Right now things that mark a version number do so as an arm:  `++  arvo  %240`
- [`!?` zapwut](https://developers.urbit.org/reference/hoon/rune/zap#-zapwut) restricts the Hoon version, requiring that the Kelvin of a particular file be at or below a certain value.  It's present in a few files right now, but not really enforced yet.

- [~sorreg-namtyv Curtis Yarvin, ~ravmel-ropdyl Galen Wolfe-Pauly, “Toward a Frozen Operating System”](https://urbit.org/blog/toward-a-frozen-operating-system)


##  Vanes

Each vane defines a protocol for interacting with other vanes (via Arvo) by defining four types of `move`s: `task`s, `gift`s, `note`s, and `sign`s.  For the most part, you won't need to memorize the subtleties of these to get started.

![](https://media.urbit.org/docs/arvo/cycle.png)

### Interactions

We can interact in one of two ways with a vane at the Dojo prompt:

- Read-only peek (scry) with the [`.^` dotket](https://developers.urbit.org/reference/hoon/rune/dot#-dotket) rune, which only allows vane state to be queried.
- `|pass` a `note` to the vane via Arvo, which allows interactions to take place.

#### Peeks

A peek (or “scry”, deprecated but ubiquitous terminology) is accomplished by passing a type and a `path` to `.^` dotket.  This path includes the vane address as a single letter `term`, a request tag called a `care`, then a beak and address, which depend on the vane.  The return value will be validated against the type.  Very frequently `path`s are built compositely so they won't look like a single argument, but the type system composes them together into a single `path`.

![](https://storage.googleapis.com/media.urbit.org/docs/arvo/scry-diagram-v2.svg)

Most vanes are instrumented to directly several endpoints, except for Gall, which passes almost all peeks through to its agents.

For instance, this peek will tell us which Graph Store keys are available:

```hoon
.^(json %gx /(scot %p our)/graph-store/(scot %da now)/keys/json)
```

It is equivalent to the following:

```hoon
.^(json /gx/(scot %p our)/graph-store/(scot %da now)/keys/json)
```

We can also change the mark of the returned data as long as it's compatible:

```hoon
.^(noun %gx /(scot %p our)/graph-store/(scot %da now)/keys/json)
```

#### `|pass`

The Hood command `|pass` directly injects a `note` for Arvo to process.  Since it cannot receive a `gift` (return `move`) in response, there is only utility for it with a few vanes.

```hoon
|pass [%d %text "hello world"]
|pass [%j %public-keys ~]
```

### 📻 Ames

Urbit knows about two kinds of networking:  Ames over Ames and HTTP over Eyre.  (That is, the network protocol over the implementing vane.)  Ames is the name of both the network protocol and the implementing vane.  Ames is for ship-to-ship communication.

#### Network Protocol

The Ames vane is responsible for sending and receiving messages of arbitrary length. These are broken into MTU-sized fragments—MTU (Maximum Transmission Unit) being the largest packet size which your system can send.

> Ames delivers messages of arbitrary length, broken into MTUshaped fragments. Because Urbit nodes are uniformly persistent, they maintain persistent sessions; message delivery is exactly-once. Every message is a transaction, and acknowledgments are end-to-end; the packet-level acknowledgment that completes a message also reports transaction success.
> 
> Ames messages are typed; the type itself is not sent, just a label (like a MIME type) that the recipient must map to a local source path. Validation failure causes a silent packet drop, because its normal cause is a recipient that has not yet received a new protocol update; we want the sender to back off. Ames also silently drops packets for encryption failure; error reports are just an attack channel.

An Ames message must be processed at the destination using Clay/Ford.

-   Reading: [Curtis Yarvin `~sorreg-namtyv`, Philip Monk `~wicdev-wisryt`, Anton Dyudin, and Raymond Pasco, “Urbit: A Solid-State Interpreter” (“Whitepaper”)](http://media.urbit.org/whitepaper.pdf), sections 9–10

Ames communicates using the [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) (UDP) specification. UDP messages are “transaction oriented, and delivery and duplicate protection are not guaranteed.” To compensate for this, Ames employs a unique system of acks and nacks, covered below.

Each UDP message has a brief header including destination, source, length, and checksum. It’s rather a “minimum viable” packet system.

From [Cloudflare](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/):

> UDP is faster but less reliable than TCP, another common transport protocol. In a TCP communication, the two computers begin by establishing a connection via an automated process called a ‘handshake.’ Only once this handshake has been completed will one computer actually transfer data packets to the other.

Urbit compensates for this lower reliability by sending until receiving an appropriate ack or nack in reply.

> UDP is commonly used in time-sensitive communications where occasionally dropping packets is better than waiting. Voice and video traffic are sent using this protocol because they are both time-sensitive and designed to handle some level of loss. For example VOIP (voice over IP), which is used by many internet-based telephone services, operates over UDP. This is because a staticy phone conversation is preferable to one that is crystal clear but heavily delayed.

-   Reading: [RFC 768](https://tools.ietf.org/html/rfc768) (UDP specification)

#### Acks and Nacks

> Ames receives packets as Arvo events and emits packets as Arvo effects. The runtime is responsible for transferring the bytes in an Ames packet across a physical network to another ship. (Ames Tutorial)

If every message is a transaction (or event), then what is Ames acknowledging (ack) or negative-acknowledging (nack)? “A successful transaction has no result; a failed transaction is a negative ack and can contain an error dump.”

> Ames has an unusual system of acks and nacks (“negative acknowledgments”, but not like TCP’s packets of the same name; Ames nacks mean the packet was received but the message resulted in an error). In brief, each Ames packet of a message should get either an ack or a nack. In the current system, the nack may include an error message (e.g., an error code or a stack trace). ([Phillip Monk, `~wicdev-wisryt`](https://groups.google.com/a/urbit.org/g/dev/c/y_gaSpn9mxM/m/njlRhYZHBwAJ))

Ames will send messages and acks until a replying ack is received. “Ames guarantees that a message will only be delivered once to the destination vane.”

> When a new socket is opened, the client can resend (at-least-once delivery) or fail to resend (at-most-once). The programmer has to understand that the socket is not really a bus, and make sure the POST is actually an idempotent fact rather than an imperative command. (The idempotence problem is often punted to the human layer: “Please click only once to make your purchase.”) (Whitepaper)

Because Ames and Urbit assume several nines of uptime, sessions between ships are treated as persistent.

> The basic argument for including end-to-end acks (and by extension, nacks) is that they’re necessary for everything except those things which we don’t care whether the message was received at all. Thus, for Ames to give the guarantee that “if you give me a payload I will get it to the other side exactly once” isn’t useful in itself, because no application cares about that. They either (1) don’t care whether it gets there or (2) care whether the request itself was “completed”, in an application-defined sense. ([Phillip Monk, `~wicdev-wisryt`](https://groups.google.com/a/urbit.org/g/dev/c/y_gaSpn9mxM/m/njlRhYZHBwAJ))

Keep in mind Postel’s law, also known as the robustness principle: “Be conservative in what you send, and liberal in what you accept.”

#### Vane Operations

Ames arms include:

```hoon
++  call  :: handle request stack
++  take  :: handle response $sign
++  stay  :: extract state before reload
++  load  :: load in old state after reload
++  scry  :: dereference namespace
```

which pretty well covers what Ames needs to do. (There is a collection of `ames-helper` cores as well to handle many specific cases for unpacking and routing messages.)

Ames maintains a duct (queue) of ordered messages. These are passed to and received from the runtime, and represent Arvo events. Each message is encrypted at the source and decrypted at the destination using a symmetric public-key system. A message may be a `%plea` (sent to another ship); in response, Ames can receive zero or more `%boon`s. The ack–nack system is explained above; note that nacks are in response to event crashes.

#### Scries

Most Ames scries aren't particularly useful to us directly unless we want to do direct network negotiation.  Ames is used frequently by Gall but, from the agent's perspective, incidentally.

```hoon
.^((map ship ?(%alien %known)) %ax /=//=/peers)
```

### ⏱️ Behn

Behn is a timer/wake-up call system.  Since it's a simple vane, let's approach it obliquely, by looking at a generator that calls it.

- Open `/base/gen/timers/hoon`.

    ```hoon
    .^((list [date=@da =duct]) %bx (en-beam [our %$ [%da now]] /debug/timers))
    ```

- How would you use this scry at the Dojo prompt?

### 📙 Clay

Clay is the version-controlled, referentially-transparent, globally-addressable filesystem.  All data in Clay are typed and presumably convertible.  For Clay, _referential transparency_ means “a request must always yield the same result for all time.”

As far as the concept of _typed data_ goes, Clay attaches identification tags to any data and has ready to hand a set of conversion routines appropriate to the data type. These ID tags are called “marks,” and they act like MIME types. (You should get used to divorcing the conceptual relationship of data—what we could call it’s _form_ in the Platonic sense—from it’s _representation_ or _instantiation_. For instance, one writes a JSON file a certain way in text, but when parsing it needs to think about it at a higher level of abstraction.)

Whereas a DVCS filesystem like Git has special rules for handling text v. binary blob elements, Clay encourages the use of marks to identify filesystem data type and conversion routines. “It’s best defined as a symbolic mapping from a filesystem to a schema engine.” We’ll deal more with marks and conversions below.

#### Organization

The top-level determiner for Clay is the `beak`:  `(p=ship q=desk r=case)`, for a desk on our current ship.  Most commonly, the `case` is `now`, the timestamp which would refer to the file in its current state.  But a `case` is really `?([%da @da] [%tas @tas] [%ud @ud])`; one of:

1. A date
2. A label or tag
3. A revision number

(Note that since we have to distinguish auras from each other, the value must be tagged with a `term`.)

Any part of the `beak` can be replaced with `=` in a statement:

```hoon
> /===  
[~.~zod ~.base ~.~2022.7.17..23.50.01..3305 ~]  

> /=landscape=  
[~.~zod %landscape ~.~2022.7.17..23.50.05..9d0d ~]  

> /~nec==  
[~.~nec ~.base ~.~2022.7.17..23.50.13..dd5d ~]
```

Clay organizes the world into `desk`s, which are also the most logical unit for app distribution.

We will elide the internal structure of Clay in ASL.  Clay is responsible for building code and has extensive parsing and AST-building tools.

#### Scries

Clay has more cares than any other vane because it needs to store and build Hoon code, as well as handle resource transformation using marks.

-   [%a - Build Hoon code.](https://developers.urbit.org/reference/arvo/clay/scry#a---build-hoon)
-   [%b - Produce dynamic mark core.](https://developers.urbit.org/reference/arvo/clay/scry#b---dyn-mark-core)
-   [%c - Produce dynamic mark conversion gate.](https://developers.urbit.org/reference/arvo/clay/scry#c---dyn-mark-convert)
-   [%d - List desks.](https://developers.urbit.org/reference/arvo/clay/scry#d---list-desks)
-   [%e - Produce static mark core.](https://developers.urbit.org/reference/arvo/clay/scry#e---static-mark-core)
-   [%f - Produce static mark conversion gate.](https://developers.urbit.org/reference/arvo/clay/scry#f---stat-mark-convert)
-   [%p - Return file permissions.](https://developers.urbit.org/reference/arvo/clay/scry#p---file-permissions)
-   [%r - Return file as vase.](https://developers.urbit.org/reference/arvo/clay/scry#r---file-as-vase)
-   [%s - Perform miscellaneous internal scries.](https://developers.urbit.org/reference/arvo/clay/scry#s---misc-scries)
-   [%t - List files.](https://developers.urbit.org/reference/arvo/clay/scry#t---list-files)
-   [%u - Check if resource exists.](https://developers.urbit.org/reference/arvo/clay/scry#u---check-exists)
-   [%v - Retrieve desk state.](https://developers.urbit.org/reference/arvo/clay/scry#v---desk-state) (don't do this at the Dojo prompt as it will print too much information to handle)
-   [%w - Show revision number of a given `case`.](https://developers.urbit.org/reference/arvo/clay/scry#w---revision-number)
-   [%x - Read file.](https://developers.urbit.org/reference/arvo/clay/scry#x---read-file)
-   [%y - Read `arch` (file hash or directory contents).](https://developers.urbit.org/reference/arvo/clay/scry#y---read-arch)
-   [%z - Show content hash.](https://developers.urbit.org/reference/arvo/clay/scry#z---content-hash)

Static `mark` conversion gates only convert from one type directly to another.

```hoon
> =txt-to-mime .^($-(wain mime) %cf /===/txt/mime)

> (txt-to-mime ~['foo'])
[p=/text/plain q=[p=3 q=7.303.014]]
```

Dynamic `mark` conversion gates, or `tube`s, process on `vase`s instead.

```hoon
> =txt-mime-tube .^(tube:clay %cc /===/txt/mime)

> !<  mime  (txt-mime-tube !>(~['foo']))
[p=/text/plain q=[p=3 q=7.303.014]]
```

- Examine the scry call in `/gen/cat/hoon`.
- Examine the scry call in `/gen/ls/hoon`.

#### Marks

A mark is a validated data structure, including rules for transformation between representations.  In this regard, it is like a more rigorous file type.  We frequently use marks in Gall agents to verify classes of operations (such as actions or updates) or to convert incoming data (such as via the JSON mark).

Marks expose several arms for converting between value representations:

- `++grab` cores convert _to_ our `mark` _from_ other `mark`s.
- `++grow` cores convert _from_ our `mark` _to_ another `mark`.
- `++grad` specify functions for revision control like creating diffs, patching files and so on. In our case, rather than writing all those functions, we've just delegated those tasks to the `%noun` `mark`.

Note that marks don't have to perfectly round-trip:  if you converted a `wain` to `json` back to `wain`, you won't necessarily have the same text.

- Examine the mark file `/mar/tape/hoon`.
- Examine the mark file `/mar/xml/hoon`.

- [Curtis Yarvin ~sorreg-namtyv, “Towards a New Clay”](https://urbit.org/blog/toward-a-new-clay/) (very old content but interesting)

### ⌨️ Dill

Dill is the terminal driver.

```hoon
|pass [%d %text "hello world"]
```

Most of the terminal stack actually lives in userspace (inside of Gall).

- [“Developer Call: Urbit’s improved Terminal Stack”](https://www.youtube.com/watch?v=E-6E-l1SxFw)

### 🌬️ Eyre

Eyre is an HTTP server, which receives HTTP messages from Unix and produces HTTP messages in reply.  Your agent can register endpoints which a browser or other tool can interact with.  Eyre can be instrumented to work with threads and generators.

#### Vane Operations

HTTP requests include a method tag.  While other methods exist, we are primarily interested in `POST`, `PUT`, and `GET` requests.  Since we don't want to deal with client-side code yet, we're going to use `curl` to send requests here.

- `POST` is only used with Eyre to obtain a cookie.

    ```sh
    $ curl -i localhost:8080/~/login -X POST -d "password=lidlut-tabwed-pillex-ridrup"
    HTTP/1.1 204 ok  
    Date: Tue, 19 Jul 2022 16:28:05 GMT  
    Connection: keep-alive  
    Server: urbit/vere-1.9  
    set-cookie: urbauth-~nec=0v3.pis4a.sfdhv.f1p6i.lttba.gp93q; Path=/; Max-Age=604800
    ```

    This cookie should be included in subsequent requests.

- `PUT` requests are used to send actions to Eyre:  pokes, subscriptions, acks, unsubscribe requests, and channel deletions.

- `GET` requests are used to connect to a channel and receive any pending events.  (Remember how Urbit prefers a dataflow computing model?)

We only briefly introduce these concepts, as you will work with them in greater detail in Lessons 3 and 4.

- Examine the [“Eyre Guide:  Generators”](https://developers.urbit.org/reference/arvo/eyre/guide#generators) example.

### ⛓️ Gall

Gall manages userspace applications and their state, including subscribers.

While Gall facilitates very complex userspace apps, the vane itself is rather modest.

### 🌈 Iris

Iris is an HTTP client.  It is not currently widely used.

- Examine the [“Iris Guide:  Example”](https://developers.urbit.org/reference/arvo/iris/example) thread.

### 🔑 Jael

Jael stores Azimuth information.  `%jael` is intimately related to Azimuth.  Azimuth represents what we may call the exoteric view of ownership, while Jael is the esoteric view.  Jael’s primary role is ship networking management and cryptography, but it also supports promises.

`%jael` segregates state into two categories: absolute and relative.  Absolute state refers to what is known about the Azimuth PKI, ship ownership, private keys, etc.  Since not every ship is live on the network (such as a fakezod), there is also a notion of relative state, referring to what is known about the current ship only.

#### Organization

`lex` is the durable state of Jael:

```hoon
=|  lex/state
$:  our=ship        ::  our: identity
    now=@da         ::  now: current time
    eny=@uvJ        ::  eny: unique entropy
    ski=sley        ::  ski: namespace resolver
==
```

There are a number of ancillary cores that track the public-key/private-key state.

For the most part, you won't need to directly use Jael when working with Gall agents unless you are carrying out Azimuth operations.

#### Scries

Jael takes no cares, so all information is exposed via the path.  Oddly, rather than a desk name, Jael expects an operation type.

Reveal your web login code:

```hoon
.^(@p %j /=code=/(scot %p our))
```

Query who the ship's sponsor is:

```hoon
.^(@p %j /=sein=/~sampel-palnet)
```

Query the sponsorship chain:

```hoon
.^((list @p) %j /=saxo=/~sampel-palnet)
```

Get current state of subscriptions to public key updates; this won't have much to say if you are on a fakeship:

```hoon
.^([yen=(jug duct ship) ney=(jug ship duct) nel=(set duct)] %j /=subscriptions=/1)
```

- Examine the [`%step` exercise](https://developers.urbit.org/reference/arvo/jael/examples#step) in the Jael docs.

### 🕸️ Khan

Khan allows threads to be triggered from outside of Urbit.

While `%khan` hasn't been documented much yet (we expect some minor API changes, such as the recent addition of inline thread invocation), there are examples of its use in ~midsum-salrux's [Tendiebot price bot](https://github.com/midsum-salrux/tendiebot/blob/master/desk/tendiebot/app/tendiebot.hoon) and [Faux Urbit–Discord bridge](https://github.com/midsum-salrux/faux).

Khan currently takes no cares.


### App Usage

For the most part, you will start designing apps that directly use Gall, of course; Eyre; Behn; and perhaps Clay.  The other vanes are less common to invoke directly.

We do need to spend some attention on some fine-grained distinctions:

1. A desk is a discrete collection of files on Clay.  If you're familiar with Git, you can think of it like a branch.  You can also think of it like a drive.
2. An agent is a particular `/app` entry which can be run.  Once started, it persists indefinitely like a system daemon unless explicitly stopped.
3. “App” is an informal designation which has come to typically refer to distributed desks with end-user agents included.

When you `|install` a desk, any agents listed in its `desk.bill` file are started automatically.  When you need to manipulate agents rather than desks, however, you should use `|rein`, which allows you to start and stop particular agents on a given desk.  `|nuke` removes all state from an agent and stops it, which is helpful when debugging.  (It's also an argument for storing important state in a helper agent rather than the operating vane.)

##  Miscellaneous Types

There are some Arvo and Gall types that are frequently invoked in agents which you should learn:

- `+$vase` is `[type noun]`, a type-value pair (these come from `!>` zapgar).
- `+$cask` is `[mark noun]`, a marked data builder.
- `+$cage` is `(cask vase)`, a marked vase.
- `+$card:agent` (distinct from Arvo's `+$card`) is a Gall-internal proto-`move`.  As you will see next week, Gall distinguishes `move`s as `card`s that talk to `%arvo` vanes from `card`s that talk to other `%agent`s for internal simplicity.
- `+$duct` is `(list wire)`, a causal history.
- `+$bone` is a `duct` handle.
- `+$wire` is an event pretext, and thus a return path.

You will encounter these regularly as you work with Gall agents.

-   Read the [`wire`](https://developers.urbit.org/guides/core/app-school/types#wire) and [`path`](https://developers.urbit.org/guides/core/app-school/types#path) entries in the type reference.

##  Resources

- [App School, “1. Arvo”](https://developers.urbit.org/guides/core/app-school/1-arvo)
- [App School, “9. Vanes”](https://developers.urbit.org/guides/core/app-school/9-vanes)
- [Arvo Overview](https://developers.urbit.org/reference/arvo/overview)
- [Hoon Standard Library, “4o:  Molds”](https://developers.urbit.org/reference/hoon/stdlib/4o)
