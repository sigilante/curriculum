---
uuid: 111
layout: node
title: "Work with the file system."
tags:
 - "%sysadmin"
prerequisites:
  - "100"
postrequisites:
  - "113"
objectives:
  - "Identify the `.urb/` directory."
  - "Use the `+ls` generator to show a directory's contents."
  - "`|mount` and `|commit` a desk."
runes: []
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

#   Working with Files

A file system is a way of organizing collections of data, called files, that adhere to certain expected structures.

Originally, a file system was a table containing pointers to the various files located on a physical disk.  Later on, more sophisticated systems allowed for different logical patterns.  One can even consider a version control repository like Git to be a logical file system, and databases share some characteristics with classical file systems.

Many systems face the challenge of synchronizing collections of data for different programs or programs.  Urbit maintains an Urbit-side file system, called Clay, which allows a regular Unix-like folder to be synchronized for development purposes.

When you boot an Urbit ship for the first time, the process creates a directory containing a `.urb/` folder.  This contains the event log and other system files.

Inside of the Urbit ship, the Dojo recognizes the current logical directory as `%` cen.  We can list the contents of the current directory using `+ls`:

```hoon
> +ls %
app/ desk/bill gen/ lib/ mar/ sur/ sys/ ted/
```

If we want to view these files inside Urbit, use `+cat`:

```hoon
> +cat %/gen/hello/hoon
/~tex/base/~2023.1.9..22.49.14..ba56/gen/hello/hoon
::  "Hello world" sample generator
::
::::  /hoon/hello/gen
  ::
::  TODO: reinstate
/?    310
::
::::
  ::
:-  %say
|=  [^ [[txt=@tas ~] ~]]
:-  %noun
(crip (weld "hello, " (trip txt)))
```

It will be convenient for us to have a Unix-side view of the files as well, since file browsers and code editors do not know about Urbit's filesystem now.  To start this process, we run `|mount` and a desk name:

```hoon
> |mount %base
```

A _desk_ represents a particular collection of files within Urbit, and often represents a single app.  The exception is `%base` which contains all system files necessary to run Hoon and Arvo.

If we check the contents of the ship's pier, or folder, in Unix we see the contents of these files available now:

```
$ tree -L 2 -F zod
zod
└── base/
    ├── app/
    ├── desk.bill
    ├── gen/
    ├── lib/
    ├── mar/
    ├── sur/
    ├── sys/
    ├── sys.kelvin
    └── ted/
```

For convenience, I will refer to the Urbit view of the files as _Mars_ and the Unix side as _Earth_.

Each folder contains certain kinds of code:  `/app` contains agents and applications, `/gen` contains generators, or standalone scripts, `/sys` contains system files like Arvo, and so forth.

When we want to write code on Urbit, the simplest way is to compose in a regular text editor or IDE (such as VS Code), save the file in the appropriate directory on Earth, and then synchronize it to Mars using `|commit`.

```sh
$ echo "42" >> tex/base/gen/example.hoon
```

Back on Mars, we can `|commit %base` to synchronize changes:

```hoon
> |commit %base
>=
+ /~tex/base/2/gen/example/hoon

> +cat %/gen/example/hoon
/~tex/base/~2023.1.9..23.02.57..e683/gen/example/hoon
42
```

You will follow this pattern frequently as you begin to develop Urbit code.
