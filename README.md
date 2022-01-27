# curriculum

_A comprehensive and up-to-date developer education platform for Urbit._

This project organizes developer capabilities into a hierarchy of competencies (“objectives”), competency clusters (“lessons”), and ultimately developer education paths.

Given a particular target capability, we can answer the question of exactly what parts of the system you need to learn to be competent at your task.

More or less, we consider the world of Urbit developers to fall into six levels:

1. Tyro
2. Amateur
3. Workaday
4. Master
5. Wizard
6. Client-side

We organize curriculum into series which describe the target transformation:

1. 100	Tyro→Amateur
2. 200	Amateur→Workaday
3. 300	Workaday→Master
4. 400	Master→Wizard
5. 500	Wizard++

Particular paths can be traced through the competency cluster dependencies.  The point isn't to make this overly complicated, it's to make sure that we know what you need to know to accomplish a particular task.

A competency cluster looks like this:

```
#hoon
Cores with Arms

- Consider Hoon structures as cores.
- Identify the special role of the `$` buc arm in many cores.
- Order neighboring cores within the subject for addressibility.

Runes introduced:  `|%`, `++`, `=<`, `=>`
Irregular syntax introduced:
```

with some associated content from urbit.org tutorials and docs.  What we are aiming for is that each objective have a quantitative measurable outcome; that is, we should be able to definitively say that one can “identify the special role of the `$` buc arm in many cores.”  The whole chart looks complicated because some things (like how Jael works, 240 and 290) depend on different prerequisites (in this case, some Azimuth background and how `move`s work).

![](./img/curr.png)

I am currently working on making this more legible, and ultimately will use this to rework Hoon School, Hoon 101, and organize access to recommended study materials and documentation.
