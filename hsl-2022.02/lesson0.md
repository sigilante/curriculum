---
title: "Development Preliminaries"
teaching: 15
exercises: 15
nodes:
- "100"
- "103"
objectives:
- "Explain what an Urbit ship is.."
- "Distinguish a fakeship from a liveship."
- "Use the `+ls` generator to show a directory's contents."
- "`|mount` and `|commit` a desk."
- "Identify the `.urb/` directory."
- "Pronounce ASCII characters per standard Hoon developer practice."
runes: []
keypoints:
- "Development should typically be done on a disposable ship:  fakeship, comet, or moon."
- "Earth and Mars must synchronize their filesystems."
---

#   Development Preliminaries
##  Hoon School Lesson 0

What is an Urbit ship?  What does it mean to create one?  If we riff off of the Lesson -1 ideas, an Urbit ship has operations, state, and values that conform to the Nock and Arvo specifications.  In particular, identity is required.

There have been several guides put out on how to set up efficiently to develop on Urbit.  The most recent guide targets macOS development and is in preparation by Tlon:

- [“Tlon Dev Guide”](https://github.com/urbit/tlon.io/blob/5b5ab41d506fbc9fe8eda59f73db1254a048c9a2/content/dev/dev-guide.md)

It's a good summary, but more than we need at this point in Hoon School Live.


##  Urbit Ships

Azimuth provides the identity.  Nock and Hoon define the operations.  Arvo provides the state.  But all of these must intersect in a particular instance of reality.  An Urbit ship is that instantiation of identity.

> ### Operating Systems
>
> If you are working on a Linux or macOS system, then you are
> already well-equipped.
>
> For Windows, you need to either set up the [MinGW build](https://github.com/urbit/urbit/releases)
> of Urbit, or install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install).
> Windows has a different way of representing line breaks
> in text files, and this can lead to some incompatibility with
> Clay.  (Your text editor should have an option for Unix-style
> or Windows-style line breaks or newlines; select Unix-style.)
>
> You won't be able to use Port currently for fakeships, although
> a future update promises this feature.
{:callout .challenge}

### Fakeships v. Liveships

An Urbit ship is a particular realization of an _identity_ and an _event log_ or _state_.  Both of these are necessary.

Since live network identities are finite, scarce, and valuable, most prefer to develop on fake identities (fakeships or fakezods).  (This also avoids the possibility of inadvertently receiving an over-the-air update while developing code.)

A fakeship is also different from a comet, which is an unkeyed liveship.

To boot a fakeship, select an appropriate name (almost always ~zod) and boot with `urbit`:

```sh
urbit -F zod
```

If you don't want to download the boot sequence (_pill_) more than once, you can download it one time and use it to boot new fakeships:

```sh
wget https://bootstrap.urbit.org/urbit-v1.8.pill
urbit -F zod -B urbit-v1.8.pill -c zod-2022-02-22
```

This launches the boot sequence, which creates the unique ship for the current system configuration.  The log looks something like this:

```
urbit 1.8  
boot: home is /home/neal/urbit/zod-2022-02-22  
loom: mapped 2048MB  
lite: arvo formula 27e494c5  
lite: core 7b144622  
lite: final state 7b144622  
boot: loading pill urbit-v1.8.pill  
boot: parsing %brass pill  
loom: mapped 2048MB  
boot: protected loom  
live: logical boot  
boot: installed 348 jets  
---------------- playback starting ----------------  
pier: replaying events 1-17  
1-b  
1-c (compiling compiler, wait a few minutes)  
ride: parsing  
ride: compiling  
ride: compiled  
1-d  
1-e  
ride: parsing  
ride: compiling  
ride: compiled  
1-f  
ride: parsing  
ride: compiling  
ride: compiled  
1-g  
lull: ~hidrun-loclun  
zuse: ~tipnut-hacpyl  
vane %ames: ~rigsud-bolmes  
vane %behn: ~sartes-masnyl  
vane %clay: ~dachut-hapdur
vane %dill: ~milwer-fogmeb  
vane %eyre: ~bonler-ranteb  
vane %gall: ~dildus-landef  
vane %iris: ~macryl-midnyl  
vane %jael: ~rabbyl-famdeg  
arvo: metamorphosis  
gall: direct morphogenesis  
%clay-kernel-updated  
clay: rebuilding %base after kernel update  
gall: installing %hood  
drum: link [~zod %dojo]  
kiln: boot  
kiln: installing %base locally  
...
gall: installing %acme  
gall: installing %azimuth  
...
gall: installing %weather  
gall: installing %btc-wallet  
pier: (17): play: done  
---------------- playback complete ----------------  
vere: checking version compatibility  
ames: live on 31337 (localhost only)  
http: web interface live on http://localhost:8080  
http: loopback live on http://localhost:12321  
pier (27): live  
docket: fetching %http glob for %garden desk  
ames: metamorphosis  
```

One way to think of it: Arvo is merely an event log, but to do anything nontrivial it dispatches the events to vanes. Jael must have the identity (either livenet credentials or a fakeship) to boot, and other parts of the system cannot boot until Jael boots.

To quote 

~master-morzod

:

A brass pill is a recipe for a complete bootstrap sequence, starting with a bootstrap Hoon compiler as a Nock formula. It compiles a Hoon compiler from source, then uses it to compile everything else in the kernel.

The main sequence is concerned with getting the entire system in good nick before Arvo runs.

pier: replaying events 1-18

Arvo is going to play the pill’s events to configure itself.

1-b 1-c (compiling compiler, wait a few minutes) ride: parsing ride: compiling ride: compiled 1-d 1-e ride: parsing ride: compiling ride: compiled 1-f ride: parsing ride: compiling ride: compiled 1-g arvo: assembly arvo: assembled

- 1-b: activate the compiler gate  
- 1-c: compile the compiler source  
- 1-d: recompile the compiler (enabling reflection)  
- 1-e: get the type of the kernel core  
- 1-f: compile Arvo source against the kernel core  
- 1-g: create the Arvo kernel with subject of the kernel core

After this, Arvo has been assembled. The lifecycle evaluation of the bootstrap sequence has been completed now.

Later, Arvo refers to itself as metamorphosed. Arvo now sheds its larval form. This means that it has acquired a single home in the kernel and has identity, entropy, and the standard library. At this point, the kernel and userspace have been built.

- [https://groups.google.com/a/urbit.org/g/dev/c/ESrqJb3Ol54/m/bns0S1QkBAAJ?pli=1](https://groups.google.com/a/urbit.org/g/dev/c/ESrqJb3Ol54/m/bns0S1QkBAAJ?pli=1)

Once you have a `dojo>` prompt, the system is ready to go and waiting on input.

Two fakeships can communicate with each other on the same machine, but have no awareness of the broader Urbit network.  We won't need to use this capability in Hoon School Live, but it can be helpful when developing networked apps on Gall later.


##  Filesystem Coordination

In pragmatic terms, an Urbit ship is what results when you successfully boot a new ship.  What you see is an apparently-empty folder.

```sh
$ ls zod
$
```

Contrast this with what the `+ls %` command shows you from inside of your Urbit:

```hoon
> +ls %
app/ desk/bill gen/ lib/ mar/ sur/ sys/ ted/
```

Urbit organizes its internal view of data and files as _desks_, which are associated collections of code and data.  These are not visible to the host operating system unless you explicitly mount them, and changes on one side are not made clear to the other until you “commit” them.  (Think of Dropbox, except that you have to explicitly synchronize to see changes somewhere else.)

Inside of your ship (“Mars”), you can mount a particular desk to the host operating system (“Earth”):

```hoon
> |mount %base
```

Now check what happens outside of your ship:

```sh
$ ls zod
base/
$ ls zod/base
app/  desk.bill gen/ lib/ mar/ sur/ sys/ ted/
```

If we make a change in the folder on Earth, the contents will only update on Mars if we explicitly tell the two systems to coordinate.

On Earth:

```sh
$ cp zod/base/desk.bill zod/base/desk.txt
```

On Mars:

```hoon
> |commit %base
+ /~zod/base/2/desk/txt
```

You can verify the contents of the copied files are the same using the `+cat` command:

```hoon
> +cat %/desk/bill
> +cat %/desk/txt
```

(Dojo does know what a `bill` file is, so it displays the contents slightly formatted.)

From Lesson 2 onwards, we will use this mode to store persistent code as files, editing on Earth and then synchronizing to Mars.

### What Makes a Folder into a Ship?

There appears to be nothing special about the `zod/` folder that `urbit` created.  In fact, there is a hidden folder which contains the system log and state.  (Show a hidden folder or file using `ls -a` at the Earth-side command line.)  You can investigate it (but don't change anything!):

```sh
$ cd zod
$ ls -a
base  .http-ports  .urb/  .vere.lock
$ ls .urb
bhk/ chk/ get/ log/ put/
$ ls .urb/chk/
north.bin  south.bin
```

These files contain all of the information necessary for the Urbit runtime program `urbit` to maintain and operate your ship's log, process new events, and persist the system state.

### Discretion is the Better Part of Valor

You will inevitably lobotimize your fakeship as you learn to develop programs in Hoon.  Such is life.  To save time, you should back up your fakeship now.  You will be able to restore it more quickly if you don't need to reboot it from scratch again.

```sh
$ cp -r zod zod-backup
```

Finally, to close your ship at any time, either type `|exit` or `Ctrl`+`D` to send the stop signal.  When you start your ship again (with `urbit zod` only), it will resume at the exact event from which you left off.


##  Text Editors

There are many fine development environments and text editors to choose from.  While it doesn't do much good, starting out, to just tell you to pick one you like, you can check out the most popular text editors and integrated developer environments (IDEs) as a reasonable proxy of usefulness.  [By popularity in 2021](https://insights.stackoverflow.com/survey/2021#most-popular-technologies-new-collab-tools), the following are the most popular IDEs (stripping out single-platform IDEs):

- [Visual Studio Code](https://code.visualstudio.com/) (if you don't have a strong opinion, use this one or the open-source [VSCodium](https://vscodium.com/))
- [Notepad++](https://notepad-plus-plus.org/)
- [Vim](https://www.vim.org/)/[Neovim](https://neovim.io/) (hard for beginners but very powerful)
- [Sublime Text](https://www.sublimetext.com/)
- [Atom](https://atom.io/) (good GitHub integration)
- [Xcode](https://developer.apple.com/xcode/)
- [Emacs](https://www.gnu.org/software/emacs/) (hard for beginners but very powerful)
- [TextMate](https://macromates.com/)


##  Pronouncing Hoon

Hoon uses _runes_, or two-letter ASCII digraphs, to describe its structure.  (These are analogous to keywords in other programming languages.)  Because there has not really been a standard way of pronouncing, say, `#` (hash, pound, number, sharp, hatch) or `!` (exclamation point, bang, shriek, pling), the authors of Urbit decided to adopt a three-letter mnemonic to uniquely refer to each.

It is highly advisable for you to learn these pronunciations, as the documentation and other developers employ them frequently.  For instance, a rune like `|=` is called a “bartis”, and you will find it designated as such in the docs, in the source code, and among the developers.

```
ace	␣ (1 space)
bar	|
bas	\
buc	$
cab	_
cen	%
col	:
com	,
doq	"
dot	.
fas	/
gal	<
gap	␣␣ (>1 space or line break)
gar	>
hax	#
hep	-
kel	{
ker	}
ket	^
lus	+
mic	;
pal	(
pam	&
par	)
pat	@
sel	[
ser	]
sig	~
soq	'
tar	*
tic	`
tis	=
wut	?
zap	!
```

- [Urbit Docs, “Reading Hoon Aloud”](https://urbit.org/docs/hoon/hoon-school/hoon-syntax#reading-hoon-aloud)
