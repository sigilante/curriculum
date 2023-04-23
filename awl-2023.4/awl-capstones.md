#   ★ `awlx`. Capstone Projects

This module contains challenge exercises which should be attainable for you given your completion of App Workshop.  As the capstone for AW, these should be completed in teams of two or three.

- Implement a gossip protocol.  (Easy challenge)
- Produce a forward-proxy anonymization service utilizing comets.  (Medium challenge)
- Create a [Forth](https://en.wikipedia.org/wiki/Forth_%28programming_language%29) interpreter.  (Hard challenge)

You may also propose a personal project of commensurate difficulty, but you should get this cleared ahead of time.

##  `%news` Gossip Protocol

A [gossip protocol](https://en.wikipedia.org/wiki/Gossip_protocol) propagates peer-to-peer communications in the absence of a central node.  Currently, Urbit groups like `%groups` rely on a host ship, and if that ship is down then no one can communicate in a particular group.

- Implement a version of `%hut` that synchronizes everyone's awareness of the chat state even if some ships in the `%squad` are down.  You'll need to modify `%hut` to use a library `/lib/news` which implements a gossip protocol.

This should use [solid-state subscriptions](https://github.com/wicrum-wicrun/sss/blob/master/urbit/app/simple.hoon), as these are an apt design pattern for such a protocol.  These have not been documented as of this writing (~2023.4.21), so you may consult ~wicrum-wicrun for insight into design using them.  See also ~rovnys-ricfer's `%poast` agent (I don't have the link at hand.)

How can we test the `%news` protocol?  The simplest scenario starts when we set up three `%squad` member ships; we'll use these for our example since we can utilize them as fake ships under a single fake galaxy ~per for routing purposes:

1. ~ripper
2. ~hopper
3. ~sapper

You'll need four fake ships (including ~per).

The basic operational test is to add the three ships to the same squad, then start a `%hut` chat on ~ripper while ~hopper is live and ~sapper is offline.  Then take ~ripper offline, leave ~hopper live, and boot ~sapper.  The message should propagate forward to ~sapper without ~ripper being available if you have set this up properly.


##  `%leek` Anonymization Protocol

![](https://eqhct8esjgc.exactdn.com/wp-content/uploads/2017/04/leeks-harvested-row.jpg?strip=all&lossy=1&resize=500%2C361)

Leek is a chan-like message anonymizer, which accepts messages targeted to a particular forum, tumbling them Tor-style within an associated graph of comets (called a *bulb*), and emitting the anonymized message.

Using the Leek protocol over Ames, the history of a particular message can only be reconstructed using knowledge of the full bulb.  Comets are regularly retired (and blacklisted) to ensure that the transmission history cannot be recovered.

The elements of Leek include:

* `%bulb` (whitelist service) runs on a ship and accepts requests for a bulb (a mutual comet whitelist) and returns one of the comets from that bulb.  It can also add or remove comets from the whitelist.  You should use `%ahoy` to monitor comet availability.

* `%leek` (gateway agent) wraps a message targeted at a particular group with a random number of jumps, requests a starter comet from `%bulb`, and sends the envelope to `%scape`.

* `%scape` (anonymizing circle) passes the message around random `%bulb` agents in a circle of comets on a mutual whitelist.  This occurs for some Tor-like number of hops to random comets in the associated bulb until emitting the now-anonymized message to a target forum.

* The front-end chat UI should be based on `%hut`.  Since this relies on known ship membership, one way to handle anonymization is to 

The size of a bulb should be considered carefully:  too few comets means fewer comets to “hack”; too many comets means messages are too sparse and can be traced more easily.


##  `%forþ` Forth Interpreter

> Forth is a procedural, stack-oriented programming language and interactive environment.  … Forth typically combines a compiler with an integrated command shell, where the user interacts via subroutines called words. Words can be defined, tested, redefined, and debugged without recompiling or restarting the whole program. All syntactic elements, including variables and basic operators, are defined as words. A stack is used to pass parameters between words, leading to a Reverse Polish Notation style.  ([La Wik](https://en.wikipedia.org/wiki/Forth_%28programming_language%29))

A Forth program works by pushing values onto a stack and then popping them off (replacing the top value of the stack).  It thus has some conceptual commonality with the Nock/Hoon concept of the subject, as everything in Forth is built on the base stack.  Here "stack" is not merely an architectural convention like in "the programming stack", but literally a mathematical [stack](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29), last-in-first-out for value access.

- Implement a Forth interpreter in Hoon, with a minimum viable standard library stack to support calculation.

To calculate the expression $25 \times 10 + 50$ using Forth, one would write:

```forth
25 10 * 50 + CR .
```

where `CR` starts the output on a new line and `.` dot prints the result.  $25$ and $10$ are put on the stack, then popped off by `*` which also pushes the result $250$.  Similarly, $50$ is pushed then $250$ and $50$ are popped by `+` to yield $300$ on the stack.

The language is completely extensible, and changes are introduced by writing a new word.  "A large Forth program is a hierarchy of words" (La Wik).

A new word (subroutine, function) is introduced by a `:` colon.  Here is a new word `FLOOR5` which implements the expression

$$
\texttt{FLOOR5}(x)
=
\begin{cases}
5 & x \leq 6 \\
x-1 & \text{else}
\end{cases}
$$

```forth
: FLOOR5 ( n -- n' )   DUP 6 < IF DROP 5 ELSE 1 - THEN ;
```

A full Forth implementation will have a lot of keywords, but for starters in this exercise let's just complete a Forth interpreter written in Hoon to carry out the following:

1. Parse Forth syntax.  (The Hoon parser does not need to check the existence of words, only their form.)
2. Implement a Forth dictionary.  See the Wikipedia page for details.
3. Build a working Forth interpreter engine.  This should include a flag to print the current user stack at each point.  This will also require establishing a simple Forth standard library stack with basic words included, such as `CREATE`/`DOES`.

    Grammatically, this will need to support built-in syntax like `:` word definition, `--` argument structure, `.` printing, `.(` immediate word, `."` code appending, and arithmetic operators.  While there seems to be little precedent for redefining arithmetic operators as words, just making them words would seem to be the simplest solution.

This exercise is a real challenge, and even completing a subset of these tasks correctly will suffice as a capstone.  But glory to those who dare!

![](https://media2.giphy.com/media/efdPsC5zF28Lu/giphy.gif)

### Resources

- [J. V. Noble, _A Beginner's Guide to Forth_](https://galileo.phys.virginia.edu/classes/551.jvn.fall01/primer.htm)
- [_Starting Forth_](https://www.forth.com/starting-forth/)
- [~tacryt-socryp, `%hick`](https://gist.github.com/tacryt-socryp/b08dc66b7bcc760e914c4db5c9fd7ba7), a Lisp on Hoon
