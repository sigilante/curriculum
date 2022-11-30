#   Urbit as a Platform

Competitive programming requires developers to move quickly, be ready to employ common code patterns, and troubleshoot without much time for intensive testing.  You have to move quickly.

My objective today is to give you a feel for the components of Urbit as a platform, how they interact with each other, and how they can be used in the hackathon.

- What does it look like to run Urbit?

For the competitive programmer, the Urbit platform offers you many helpful features for free:

- identity & associated state, cryptographically secured
- peer-to-peer end-to-end-encrypted apps
- persistent database
- software distribution without corporate oversight
- interfacing with traditional Web clients

(Show https://developers.urbit.org/ while you talk as well.)

##  Urbit OS (VM)

If you have programmed with a scripting language like Lua inside of a modded game, for instance, (or worked with Unity) you will be familiar with how the game serves as a platform providing correct primitives which speed your development.  Urbit does this for the operating system layer, serving as a platform for personal data management, social media, user apps, and blockchain apps.

https://github.com/urbit/urbit

Computer chips act as a platform in machine language.  However, due to architecture differences, we cannot of course use assembly language portably.  There are two basic solutions to this problem:  

1. Compile a per-chip version of your software for a set of supported architectures.
2. Implement a virtual machine layer that allows the software to be agnostic to the hardware.

Architecturally, you can think of Urbit as a sort of layer-2 operating system.  Once you have a virtual machine layer, as with Java or Ethereum, you can treat it as a virtual chipset with a portable language.

Urbit OS runs on Nock, a minimalist Turing-complete language specification.  Much like assembly language or Java bytecode, you don't need to know any Nock to effectively use the platform.  However, everything running on an Urbit instance or "ship" is ultimately compiled and run as Nock.

We'll circle back around to Urbit OS after taking a look at Urbit ID.


##  Urbit ID

Urbit ID is a separate system for identity, bootstrapped on Ethereum as an ERC-721 token with L1 and L2 components.  Urbit ID is a public key infrastructure, meaning that you hold a wallet and a private key; any message signed with the private key is decrypted using the public key.  Since this is built in, it avoids the pitfalls of using GPG etc.  (Because of the L2 rollup, you'll need access to an Urbit instance to pull the complete current state if you are writing a smart contract app, but these comes out as a JSON object.)

https://github.com/urbit/azimuth

The Urbit address space is divided into several types of points (or addresses):

1. Galaxies are like TLD distributors and routers.
2. Stars are other network infrastructure.
3. Planets serve as individual identities.
4. Comets serve as transient identities (possession is public key).

Address points are mapped to a nonsense mnemonic scheme which allows for easier reference to numeric points and point role.  Galaxies are one syllable, stars are two syllables, planets are four syllables, and comets are sixteen syllables.  This is your `@p`, or spoken point ID.

The Azimuth contracts support ownership interactions (e.g. dapps), attestation claims, reputation censuring, delegated transfers, and so forth.

The Urbit ID on-chain elements have been completely audited for security.


##  Urbit OS (Kernel + Userspace)

To sum up the platform to this point, an Urbit ship is an running instance of Urbit OS which is cryptographically linked to Urbit ID.  But what does Urbit OS look like for a user or developer?

Any operating system has a kernel providing system services, with which user processes interact.

Nock instructions are executed on a runtime executable which runs on your particular hardware.  Currently the runtime is built for x86-64 and ARM64 architectures.

Immediately above Nock is the Hoon language specification, which maps the higher-level Hoon programs to run in Nock.  You will write programs on Urbit in Hoon, but you will be able to use the layers outside of this as well.

Next, the main event processing loop and state machine for the system exists, which we call Arvo.  Arvo is largely invisible to you as an app programmer, except that you will construct events to be evaluated.

System services, such as HTTP server processing, peer-to-peer communication, public key lookup, the file system, and so forth are provided as "vanes" for Arvo events to use.

Finally, end-user apps and middleware are built in what we call "userspace", the part of the system outside of the kernel.

Urbit apps are built with a highly formal structure called "agents" which allows the system and other apps to make certain good assumptions about where data are located, how the agent will respond, etc.  **The userspace app framework**, called Gall, requires a standard application interface and in return gives you access to a rich operating environment, state management, and peer-to-peer software distribution.

At this point, we can summarize how a functioning Urbit ship acts as a personal server:

- Urbit ships have unique attestable cryptographic identity.
- Urbit stores data and program state
- Urbit has a file system which can synchronize with your host OS
- Since Urbit has a built-in database, no external DB is necessary to provision
- Urbit can speak HTTP as both client and server, and supports JSON
- Urbit can serve pages and webapps

Some other points:

- Urbit is a purely functional operating system.  Events are processed then written to disk, so state is a pure function of known enumerable events.
- There is no distinction between primary and secondary memory and the operating system and apps can update themselves while running using hot code reloading.
- All data structures are immutable and persistent, allowing us to have economical shared structures such as libraries without the static/dynamic linking problems of other platforms.
- Code and data are homoiconic, convertible to each other.
- The runtime can optimize slow Nock code using fast C code where appropriate ("jetting").

So what could an Urbit app look like?  Many fruitful approaches are available to you:

1. On-Urbit app development (learn Hoon).
2. Urbit-adjacent app development (front-end UI, e.g. JS).
3. Urbit ID project (dapps, UI).
4. Bridge app from Urbit to Web3 chains and tools (Ceramic, IPFS, Cardano).

The second workshop, to be held next week, will delve into how an app is built on Urbit.  We'll need to look at the Hoon language, since unlike Javascript or Python it is unlikely that you'll be able to interpret it without some exposure first.

The third workshop will consider some of the apps that have been built on Urbit and discuss ideas for the hackathon that should be finishable in the time available.

Urbit development is couched in terms which are unfamiliar to most programmers unless they are versed in something like APL or Lisp.  The Urbit programming language, Hoon, composes statements together in a way that behaves like functional programming but reads a bit more like imperative programming.  While it looks alien, I strongly urge you to seize the nettle and learn some Hoon.  As you put the time into it, I expect that you will find Urbit to be refreshingly different from other platforms, while affording rapid application development and deployment.

If you would like to work with Urbit at a hackathon but don't want to invest time into learning Hoon, you should investigate building Urbit-aware tooling and apps in the other categories, or partnering with a team that has some Hoon experience.

Ahead of that workshop, if you would like to start looking at how Urbit apps can be built, we have a trio of rapid tutorials on developers.urbit.org called "lightning apps".  Go ahead and look at those, or take advantage of other resources in the developer packet that Encode put together for you.

What questions do you have?
