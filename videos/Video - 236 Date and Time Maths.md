---
uuid: 236
layout: node
title: "Date and time mathematics"
tags:
 - "%stdlib"
prerequisites:
  - "163"
postrequisites: []
objectives:
  - "Examine `@da` atomic representation of dates and times."
  - "Examine `@dr` atomic representation of date and time deltas."
  - "Examine `+$tarp` and `+$date` broken-out types."
  - "Use `+yo` to produce time values."
  - "Carry out basic time manipulations."
runes: []
irregular: []
key_points: []
assessments: []
comments: ""
content: ""
---

##  Dates in History

The calendrist must reckon with cyclical patterns like the seven-day week on top of variable-length patterns such as the month and the year.  Solar and lunar conventions clash.  In short, time is hard to get right.

Each calendar system has a conventional epoch, or point from which time is calculated forward.
<!-- (gif of _Dinosaurs_ counting down), https://getyarn.io/yarn-clip/5e661fd0-7dba-4a2b-ad28-0ecf9eb74653 ? find better source -->

Computer systems additionally must decide how to represent time granularly:  should a single integer increment represent the passage of a day?  A second?  A nanosecond?

For instance, Microsoft Excel counts dates as floating-point values forwards and backwards from 1 January 1900, with days as whole-number parts and fractions of the day converted into hours, minutes, and seconds.  This means that Excel has variable resolution due to how floating-point values work, but generally can guarantee resolution to milliseconds or better.
<!-- https://www.systematix.co.uk/tips-tricks/microsoft-excel-time-resolution -->

<!-- A sundial reveals _hyperlocal_ time, the direct solar time.  When the sundial reads with no shadow, it is hyperlocally noon, regardless of what the clocks say.  Time zones act as an approximation to allow a relatively local region to treat time as the same without the difficulties that hyperlocal time would introduce. -->

That date, right before 1 January 1900, is Excel's _epoch_, or the point from which all values are reckoned.  Windows computers count from 1 January 1601, while Unix computers count from 1 January 1970.

Positive time is generally straightforward, but negative time requires an offset of one relative to conventional mathematics.  When the Venerable Bede needed to calculate the date of Easter, a moveable feast, he elected to popularize the use of a calendar derived from the birth of Jesus Christ rather than the then-current Diocletian era.  Unfortunately for our purposes as calculators, there was no Year Zero in this scheme:  Year 1 B.C. is immediately followed by A.D. 1.

Urbit represents time internally with respect to Greenwich Mean Time or UTC, and dates with respect to an epoch in the distant past.  This means that we can safely neglect time zones in our internal calculations.


##  `+$date` and  `+$tarp` Representation

Hoon has two native representation styles for time and date values.  The first are broken out into named tuples `+$date` and `+$tarp`, molds which hold separate atoms for year, day, hour, and so forth.  Much as a `tape` breaks out a `cord` into discrete elements which are easier to manipulate, a `+$date` and a `+$tarp` allow us fine-grained expression of time values.

To see the current date and time, you can use `now`; since this is in the atomic format `@da`, we convert it to a `+$date` using `++yore`:

```hoon
> (yore now)
[[a=%.y y=2.022] m=11 t=[d=23 h=1 m=9 s=1 f=~[0xd729]]]
```

A `+$date` consists of a named tuple indicating BC/AD and the current year; a month; and a `+$tarp` representing time within the month.

`++year` converts from a `+$date` back to a `@d` atom:

```hoon
> (year [[%.y 1.997] 7 [1 0 0 0 ~]])
~1997.7.1
```

`++year` automatically handles edge cases like days in a month.

```hoon
> (year [[%.y 2.022] 13 [32 0 0 0 ~]])
~2023.2.1
```

`++yell` converts a `@d` atom to a `+$tarp` with no respect to years and months.

```hoon
> (yell now)
[d=106.751.991.823.264 h=1 m=7 s=19 f=~[0x552d]]
```

Since a `+$tarp` contains days, hours, minutes, seconds, and fractions of a second, we see that a great number of days indeed have passed since the Urbit epoch.


##  `@d` Representation

The other Hoon-native representation of date and time values is the `@d` atom series.

1. `@da` absolute time and date refers to a particular moment in time.
2. `@dr` relative time refers to a span of time.

Absolute time `@da` values are arbitrary-precision integers counting from the Urbit epoch, or zero.  By examining `@da`'s effect on zero, we can see what that epoch is.

```hoon
> `@da`0
~292277024401-.1.1
```

Urbit is thus unable to directly represent dates prior to this time as integers, which is fine for students of modern cosmology but poses difficulties for Vedic chronology.

The rationale for this epoch is that it puts the center of the 64-bit date space at about the B.C./A.D. crossover.

```hoon
> `@da`(dec (bex 128))
~292277024853.11.8..07.00.15..ffff.ffff.ffff.ffff

> `@da`(lsh [0 64] (dec (bex 64)))
~292277024853.11.8..07.00.15

> `@da`0
~292277024401-.1.1

> `@da`(lsh [0 64] (dec (bex 63)))
~226.12.5..15.30.07
```

Similarly, by casting the smallest integer greater than zero to `@da`, we can infer the granularity of time's representation.

```hoon
> `@da`1
~292277024401-.1.1..00.00.00..0000.0000.0000.0001
```

From this result, we see that an increment of `1` in the integer value represents a time interval of $2^{-2^{6}} = 2^{-64} \approx 5.4 \times 10^{-20} \,\textrm{s}$.  The lower 64 bits are $2^{-64}\,\textrm{s}$ precision, while the high 64 bits are essentially TAI64 with a different epoch.  In the `+$tarp` format, the subsecond component is stored as `(list @uxE)`.

`@da` is the only atom which bunts to a value other than zero:  `*@da` resolves to 1 January 2000.

```hoon
> (yore *@da)
[[a=%.y y=2.000] m=1 t=[d=1 h=0 m=0 s=0 f=~]]
```

Since an integer in Hoon can have arbitrary precision, there is not a maximum representable time.

The Urbit date system correctly compensates for the lack of Year Zero:

```hoon
> ~0.1.1
~1-.1.1

> ~1-.1.1
~1-.1.1
```

Finally, `++yule` is used to convert from a `+$tarp` to a `@da`:

```hoon
> (yule (yell now))
0x8000000d312b148891f0000000000000

> `@da`(yule (yell now))
~2022.5.24..16.25.48..c915

> `@da`(yule [d=106.751.991.823.081 h=16 m=26 s=14 f=~[0xf727]])
~2022.5.24..16.26.14..f727
```

Relative time in `@dr` is similar to a `+$tarp`, which only regards days and smaller time units.

```hoon
> `@dr`1
~s0..0000.0000.0000.0001

> `@dr`1.000.000.000.000.000.000.000
~s54..35c9.adc5.dea0

> `@dr`1.000.000.000.000.000.000.000.000
~h15.m3.s30..1bce.cced.a100

> `@dr`1.000.000.000.000.000.000.000.000.000
~d627.h10.m21.s48..9fd0.803c.e800
```

Mathematical operators such as `++add` which sensibly work with time can be used straightforwardly with `@d` atoms.  Tuple values should be converted to `@d` for such operations.

```hoon
> `@da`(add *@da ~d365.h0.m0.s0)
~2000.12.31
```

User-friendly timestamp formatting in text is provided by `++chrono:userlib` in `%zuse`.

```
> (dust:chrono:userlib (yore now))
"Thu, 1 Dec 2022 22:52:51 +0000"
```

These can be parsed back out to `+$date` values as well using `++stud`:

```hoon
> (stud:chrono:userlib (crip (dust:chrono:userlib (yore now))))
[~ [[a=%.y y=2.022] m=12 t=[d=1 h=22 m=54 s=4 f=~]]]

> (stud:chrono:userlib (crip "Thu, 1 Dec 2022 22:54:04 +0000"))
[~ [[a=%.y y=2.022] m=12 t=[d=1 h=22 m=54 s=4 f=~]]]
```

<!-- An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date is written in a standard form such as `2022-11-22T22:23:43+00:00`. -->

JSON dates are commonly stored either as written timestamps of various configurations or as seconds since the Unix epoch.

```hoon
> (du:dejs:format n+'1200')
~1970.1.1..00.20.00

> (di:dejs:format n+'1200000')
~1970.1.1..00.00.01..3333.3333.3333.3333
```

Conversion from Urbit time to a Unix second date is included as `++sect:enjs:format`:

```hoon
> (sect:enjs:format now)
[%n p=~.1669935076]
```

Remember the Y2K problem?  Since memory was at a premium on many early computer systems, the original software authors chose to represent the year as a two-digit entry, assuming that `19` was the prefix.  The rollover to `00` at the Year 2000 was predicted to lead to uncertain chaos, and much effort and dread was focused on what ultimately proved underwhelming.  Similarly, Unix-based systems face a Year 2032 problem when the 32-bit count of seconds since 1 January 1970 rolls over on older systems.

Urbit time can be an arbitrarily large atom, so even if it overflows a 128-bit representation, it can roll over to a new byte and continue to grow into the future.  Maybe Urbit can be more than just a hundred-year computer.
