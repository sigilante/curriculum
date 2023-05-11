---
title: "The Standard Library"
teaching: 45
exercises: 15
nodes:
- "184"
- "233"
objectives:
- "Explore the Hoon standard library."
- "Produce loobean expressions."  
- "Reorder conditional arms."  
- "Switch against a union with or without default."
- "Reel, roll, turn a list."  
- "Curry, cork functions."  
- "Change arity of a gate."
runes:
- "`;:`"
- "`?|`"
- "`?&`"
- "`?!`"
- "`?.`"
- "`?-`"
- "`?+`"
irregular:
- "`&`"
- "`|`"
- "`!`"
- "`:`"
keypoints:
- "The Hoon standard library provides many (but not all) desirable tools.  (It tends to be parser-heavy.)"
- "Good Hoon style weights heavier expressions to the bottom.  Use `?.` wutdot to discretionally control this."
- "Switch statements allow you to make decisions based on possible elements of a type union (e.g. of terms)."
- "Gates can be manipulated to accept different numbers of arguments, or applied across multiple values, using functional programming arms."
readings:
- "https://developers.urbit.org/guides/core/hoon-school/J-stdlib-text" (Text Operations:  Producing Text)
- "https://developers.urbit.org/guides/core/hoon-school/N-logic"
- "https://developers.urbit.org/guides/core/hoon-school/Q-func"
feedback: "https://forms.gle/39y5DT19Ys5m1Hed8"
homework: "https://forms.gle/pNvaatNw15H3ZfjX8"
video: "https://youtu.be/F2O4cslUK_I"
mirror: "https://github.com/sigilante/curriculum/blob/master/hsl-2023.3/hsl6.md"
---

#   The Standard Library

Whenever we run code in the dojo, the subject makes available to us a standard library of operations.  Much of these focus on parsing and building code—after all, that's what Hoon itself must do—but there are many other convenient functions tucked away in the Hoon subject.  Some parts are formally in Arvo, some in `%zuse`, some in `%lull`, and some in Hoon proper (`hoon.hoon`).  (Vane-specific operations are also available, although we don't need any of them quite yet.)  You don't really need to know about where particular parts live yet, although naked generators as we've composed thus far can only see arms of the standard library and don't have access to some Arvo information like `our` or `now`.


##  The Structure of Urbit OS

Navigate to `/sys` in your fakezod's pier in the `%base` desk.  Take a look at the files present here:

```
.  
├── arvo.hoon  
├── hoon.hoon  
├── lull.hoon  
├── vane  
│   ├── ames.hoon  
│   ├── behn.hoon  
│   ├── clay.hoon  
│   ├── dill.hoon  
│   ├── eyre.hoon  
│   ├── gall.hoon  
│   ├── iris.hoon  
│   └── jael.hoon  
└── zuse.hoon
```

Arvo and the vanes provide system services which you won't need until you start working with Gall and building apps.

- `hoon.hoon` provides the language fundamentals for the Hoon parser and builder.  (Some of this functionality is housed in the filesystem handler `clay.hoon` as well.)
- `lull.hoon` contains structures and services necessary to bootstrap Arvo.
- `zuse.hoon` provides a variety of data parsing and representation structures.
- `arvo.hoon` instruments the basic Arvo event loop.
- Vane files provide per-vane service cores and molds.

We are going to venture into the standard library files to start us off today.  Open these with the text editor of your choice.  Let's start with `hoon.hoon`, the core of the standard library.

### `hoon.hoon`

`hoon.hoon` is a bit of a jungle.  It is a core organized into “chapters” with [`+|` lusbar](https://urbit.org/docs/hoon/reference/rune/lus#-lusbar).  [The docs](https://urbit.org/docs/hoon/reference/stdlib#by-section) reflect this structure and give us a good glimpse of what to expect in here.  Some highlights:

-   [1a: basic arithmetic](https://urbit.org/docs/hoon/reference/stdlib#1a-basic-arithmetic)
  -   [`++add`](https://urbit.org/docs/hoon/reference/stdlib/1a/#add "Add") [`++dec`](https://urbit.org/docs/hoon/reference/stdlib/1a/#dec "Decrement") [`++div`](https://urbit.org/docs/hoon/reference/stdlib/1a/#div "Divide") [`++dvr`](https://urbit.org/docs/hoon/reference/stdlib/1a/#dvr "Divide (with remainder)") [`++gte`](https://urbit.org/docs/hoon/reference/stdlib/1a/#gte "Greater than / equal") [`++gth`](https://urbit.org/docs/hoon/reference/stdlib/1a/#gth "Greater than") [`++lte`](https://urbit.org/docs/hoon/reference/stdlib/1a/#lte "Less than / equal (atom)") [`++lth`](https://urbit.org/docs/hoon/reference/stdlib/1a/#lth "Less than (atom)") [`++max`](https://urbit.org/docs/hoon/reference/stdlib/1a/#max "Maximum") [`++min`](https://urbit.org/docs/hoon/reference/stdlib/1a/#min "Minimum (atom)") [`++mod`](https://urbit.org/docs/hoon/reference/stdlib/1a/#mod "Modulus (atom)") [`++mul`](https://urbit.org/docs/hoon/reference/stdlib/1a/#mul "Multiply (atom)") [`++sub`](https://urbit.org/docs/hoon/reference/stdlib/1a/#sub "Subtract")
-   [2a: unit logic](https://urbit.org/docs/hoon/reference/stdlib#2a-unit-logic)
  -   [`++biff`](https://urbit.org/docs/hoon/reference/stdlib/2a/#biff "Unit as argument") [`++bind`](https://urbit.org/docs/hoon/reference/stdlib/2a/#bind "Nonunit function to unit, producing unit") [`++bond`](https://urbit.org/docs/hoon/reference/stdlib/2a/#bond "Replace null") [`++both`](https://urbit.org/docs/hoon/reference/stdlib/2a/#both "Group unit values into pair") [`++clap`](https://urbit.org/docs/hoon/reference/stdlib/2a/#clap "Combine two units with function") [`++clef`](https://urbit.org/docs/hoon/reference/stdlib/2a/#clef "Compose two units with function") [`++drop`](https://urbit.org/docs/hoon/reference/stdlib/2a/#drop "Unit to list") [`++fall`](https://urbit.org/docs/hoon/reference/stdlib/2a/#fall "Give unit a default value") [`++flit`](https://urbit.org/docs/hoon/reference/stdlib/2a/#flit "Make filter") [`++hunt`](https://urbit.org/docs/hoon/reference/stdlib/2a/#hunt "Select between two units by a rule") [`++lift`](https://urbit.org/docs/hoon/reference/stdlib/2a/#lift "Curried bind") [`++mate`](https://urbit.org/docs/hoon/reference/stdlib/2a/#mate "Choose") [`++need`](https://urbit.org/docs/hoon/reference/stdlib/2a/#need "Unwrap unit") [`++some`](https://urbit.org/docs/hoon/reference/stdlib/2a/#some "Wrap value in unit")
-   [2b: list logic](https://urbit.org/docs/hoon/reference/stdlib#2b-list-logic)
  -   [`++bake`](https://urbit.org/docs/hoon/reference/stdlib/2b/#bake "Convert wet gate to dry gate") [`++fand`](https://urbit.org/docs/hoon/reference/stdlib/2b/#fand "All indices in list") [`++find`](https://urbit.org/docs/hoon/reference/stdlib/2b/#find "First index in list") [`++flop`](https://urbit.org/docs/hoon/reference/stdlib/2b/#flop "Reverse list") [`++gulf`](https://urbit.org/docs/hoon/reference/stdlib/2b/#gulf "List from range") [`++homo`](https://urbit.org/docs/hoon/reference/stdlib/2b/#homo "Homogenize list") [`++join`](https://urbit.org/docs/hoon/reference/stdlib/2b/#join "Add separator between list elements") [`++lent`](https://urbit.org/docs/hoon/reference/stdlib/2b/#lent "List length") [`++levy`](https://urbit.org/docs/hoon/reference/stdlib/2b/#levy "Logical AND on list") [`++lien`](https://urbit.org/docs/hoon/reference/stdlib/2b/#lien "Logical OR on list") [`++limo`](https://urbit.org/docs/hoon/reference/stdlib/2b/#limo "Construct list from nullterminated tuple") [`++murn`](https://urbit.org/docs/hoon/reference/stdlib/2b/#murn "Maybe transform") [`++oust`](https://urbit.org/docs/hoon/reference/stdlib/2b/#oust "Remove from list") [`++reap`](https://urbit.org/docs/hoon/reference/stdlib/2b/#reap "Replicate (list)") [`++reel`](https://urbit.org/docs/hoon/reference/stdlib/2b/#reel "Right fold (list)") [`++roll`](https://urbit.org/docs/hoon/reference/stdlib/2b/#roll "Left fold (list)") [`++scag`](https://urbit.org/docs/hoon/reference/stdlib/2b/#scag "Prefix (produce front of list)") [`++skid`](https://urbit.org/docs/hoon/reference/stdlib/2b/#skid "Separate list into two lists from slammed elments") [`++skim`](https://urbit.org/docs/hoon/reference/stdlib/2b/#skim "Produce list of elements from boolean gate") [`++skip`](https://urbit.org/docs/hoon/reference/stdlib/2b/#skip "Produce list of elements failing boolean gate") [`++slag`](https://urbit.org/docs/hoon/reference/stdlib/2b/#slag "Produce all elements from index in list") [`++snag`](https://urbit.org/docs/hoon/reference/stdlib/2b/#snag "Produce element at specific index (list)") [`++snip`](https://urbit.org/docs/hoon/reference/stdlib/2b/#snip "Drop tail off list") [`++snoc`](https://urbit.org/docs/hoon/reference/stdlib/2b/#snoc "Append noun to list") [`++sort`](https://urbit.org/docs/hoon/reference/stdlib/2b/#sort "Quicksort (list)") [`++spin`](https://urbit.org/docs/hoon/reference/stdlib/2b/#spin "Gate to list (with state)") [`++spun`](https://urbit.org/docs/hoon/reference/stdlib/2b/#spun "Gate to list (with state)") [`++swag`](https://urbit.org/docs/hoon/reference/stdlib/2b/#swag "Infix (list)") [`++turn`](https://urbit.org/docs/hoon/reference/stdlib/2b/#turn "Gate to list") [`++weld`](https://urbit.org/docs/hoon/reference/stdlib/2b/#weld "Concatenate two lists") [`++welp`](https://urbit.org/docs/hoon/reference/stdlib/2b/#welp "Perfect concatenate (lists)") [`++zing`](https://urbit.org/docs/hoon/reference/stdlib/2b/#zing "Turn lists into single list by promoting elements from sublists")
-   [2g: unsigned powers](https://urbit.org/docs/hoon/reference/stdlib#2g-unsigned-powers)
  -   [`++pow`](https://urbit.org/docs/hoon/reference/stdlib/2g/#pow "Computes a to the power of b") [`++sqt`](https://urbit.org/docs/hoon/reference/stdlib/2g/#sqt "Compute square root with remainder")
-   [2h: set logic](https://urbit.org/docs/hoon/reference/stdlib#2h-set-logic)
  -   [`++in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#in) [`++all:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#allin "Logical AND (set and wet gate)") [`++any:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#anyin "Logical OR (set and gate)") [`++apt:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#aptin "Check correctness (set)") [`++bif:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#bifin "Bifurcate set") [`++del:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#delin "Delete (set)") [`++dif:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#difin "Difference (set)") [`++dig:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#digin "Address of a in set") [`++gas:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#gasin "Concatenate (set)") [`++has:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#hasin "Key existence check (set)") [`++int:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#intin "Intersection (set)") [`++put:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#putin "Put b in a (set)") [`++rep:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#repin "Accumulate elements (set)") [`++run:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#runin "Apply gate to set") [`++tap:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#tapin "Flatten set into list") [`++uni:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#uniin "Union (sets)") [`++wyt:in`](https://urbit.org/docs/hoon/reference/stdlib/2h/#wytin "Produce number of elements in set")
-   [2i: map logic](https://urbit.org/docs/hoon/reference/stdlib#2i-map-logic)
  -   [`++by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#by "Map operations") [`++all:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#allby "Logical AND (map and wet gate)") [`++any:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#anyby "Logical OR (map and wet gate)") [`++apt:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#aptby "Check correctness (map)") [`++bif:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#bifby "Bifurcate map") [`++del:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#delby "Delete (map)") [`++dif:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#difby "Difference between maps") [`++dig:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#digby "Address of key (map)") [`++gas:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#gasby "Concatenate (map)") [`++get:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#getby "Grab unit value") [`++got:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#gotby "Assert for value (map)") [`++has:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#hasby "Key existence check (map)") [`++int:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#intby "Intersection (map)") [`++jab:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#jabby "Transform value (map)") [`++key:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#keyby "Set of keys") [`++mar:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#marby "Add with validation (map)") [`++put:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#putby "Add keyvalue pair (map)") [`++rep:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#repby "Reduce to product (map)") [`++rib:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#ribby "Transform + product (map)") [`++run:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#runby "Transform values (map)") [`++rut:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#rutby "Transform nodes (map)") [`++tap:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#tapby "Listify pairs") [`++uni:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#uniby "Union, merge (map)") [`++uno:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#unoby "General union (map)") [`++urn:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#urnby "Turn (with key) (map)") [`++wyt:by`](https://urbit.org/docs/hoon/reference/stdlib/2i/#wytby "Produce depth of tree map")
-   [2j: jar and jug logic](https://urbit.org/docs/hoon/reference/stdlib#2j-jar-and-jug-logic)
  -   [`++ja`](https://urbit.org/docs/hoon/reference/stdlib/2j/#ja "Jar engine") [`++add:ja`](https://urbit.org/docs/hoon/reference/stdlib/2j/#addja "Prepend to list") [`++get:ja`](https://urbit.org/docs/hoon/reference/stdlib/2j/#getja "Grab value by key")
  -   [`++ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#ju "Jug operations") [`++del:ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#delju "Delete (jug)") [`++gas:ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#gasju "Concatenate (jug)") [`++get:ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#getju "Retrieve set") [`++has:ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#hasju "Check contents (jug)") [`++put:ju`](https://urbit.org/docs/hoon/reference/stdlib/2j/#putju "Add keyset pair (jar)")
-   [2l: container from container](https://urbit.org/docs/hoon/reference/stdlib#2l-container-from-container)
  -   [`++malt`](https://urbit.org/docs/hoon/reference/stdlib/2l/#malt "Map from list") [`++molt`](https://urbit.org/docs/hoon/reference/stdlib/2l/#molt "Map from pair list") [`++silt`](https://urbit.org/docs/hoon/reference/stdlib/2l/#silt "Produce set from list")
-   [2n: functional hacks](https://urbit.org/docs/hoon/reference/stdlib#2n-functional-hacks)
  -   [`++aftr`](https://urbit.org/docs/hoon/reference/stdlib/2n/#aftr "Pair after") [`++cork`](https://urbit.org/docs/hoon/reference/stdlib/2n/#cork "Compose forward") [`++corl`](https://urbit.org/docs/hoon/reference/stdlib/2n/#corl "Compose backward") [`++curr`](https://urbit.org/docs/hoon/reference/stdlib/2n/#curr "Rightcurry a gate") [`++cury`](https://urbit.org/docs/hoon/reference/stdlib/2n/#cury "Curry left a gate") [`++fore`](https://urbit.org/docs/hoon/reference/stdlib/2n/#fore "Pair before") [`++head`](https://urbit.org/docs/hoon/reference/stdlib/2n/#head "Get head of cell") [`++same`](https://urbit.org/docs/hoon/reference/stdlib/2n/#same "Identity (produces same value)") [`++succ`](https://urbit.org/docs/hoon/reference/stdlib/2n/#succ "Successor") [`++tail`](https://urbit.org/docs/hoon/reference/stdlib/2n/#tail "Get tail of cell") [`++test`](https://urbit.org/docs/hoon/reference/stdlib/2n/#test "Test for equality") [`++lead`](https://urbit.org/docs/hoon/reference/stdlib/2n/#lead "Put head") [`++late`](https://urbit.org/docs/hoon/reference/stdlib/2n/#late "Put tail")
-   [2p: serialization](https://urbit.org/docs/hoon/reference/stdlib#2p-serialization)
  -   [`++cue`](https://urbit.org/docs/hoon/reference/stdlib/2p/#cue "Unpack atom to noun") [`++jam`](https://urbit.org/docs/hoon/reference/stdlib/2p/#jam "Pack noun to atom") [`++mat`](https://urbit.org/docs/hoon/reference/stdlib/2p/#mat "Lengthencode") [`++rub`](https://urbit.org/docs/hoon/reference/stdlib/2p/#rub "Lengthdecode")
-   [2q: molds and mold builders](https://urbit.org/docs/hoon/reference/stdlib#2q-molds-and-mold-builders)
  -   [`+$axis`](https://urbit.org/docs/hoon/reference/stdlib/2q/#axis "Tree address") [`+$bean`](https://urbit.org/docs/hoon/reference/stdlib/2q/#bean "Boolean") [`+$char`](https://urbit.org/docs/hoon/reference/stdlib/2q/#char "Character") [`+$cord`](https://urbit.org/docs/hoon/reference/stdlib/2q/#cord "UTF8 text") [`+$byts`](https://urbit.org/docs/hoon/reference/stdlib/2q/#byts "bytes, LSB first") [`+$date`](https://urbit.org/docs/hoon/reference/stdlib/2q/#date "Parsed date") [`+$flag`](https://urbit.org/docs/hoon/reference/stdlib/2q/#flag "Boolean (flag)") [`+$knot`](https://urbit.org/docs/hoon/reference/stdlib/2q/#knot "Atom type of ASCII characters") [`+$noun`](https://urbit.org/docs/hoon/reference/stdlib/2q/#noun "Any noun") [`+$path`](https://urbit.org/docs/hoon/reference/stdlib/2q/#path "Like unix path") [`+$stud`](https://urbit.org/docs/hoon/reference/stdlib/2q/#stud "Standard name") [`+$tang`](https://urbit.org/docs/hoon/reference/stdlib/2q/#tang "Bottom-first error") [`+$tank`](https://urbit.org/docs/hoon/reference/stdlib/2q/#tank "Formatted print tree") [`+$tape`](https://urbit.org/docs/hoon/reference/stdlib/2q/#tape "List of characters") [`+$tour`](https://urbit.org/docs/hoon/reference/stdlib/2q/#tour "UTF-32 clusters") [`+$tarp`](https://urbit.org/docs/hoon/reference/stdlib/2q/#tarp "Parsed time") [`+$term`](https://urbit.org/docs/hoon/reference/stdlib/2q/#term "Hoon constant") [`+$wain`](https://urbit.org/docs/hoon/reference/stdlib/2q/#wain "List of cords") [`+$wall`](https://urbit.org/docs/hoon/reference/stdlib/2q/#wall "List of list of characters")
-   [3b: floating point](https://urbit.org/docs/hoon/reference/stdlib#3b-floating-point)
  -   [`++rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#rs) [`++add:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#addrs "Add (singleprecision float)") [`++bit:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#bitrs "fn to singleprecision float") [`++div:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#divrs "Divide (singleprecision float)") [`++drg:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#drgrs "@rs to decimal float") [`++equ:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#equrs "Equals (singleprecision float)") [`++exp:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#exprs "Exponent (@rs)") [`++fma:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#fmars "Fused multiplyadd (singleprecision float)") [`++grd:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#grdrs "Decimal float to @rs") [`++gte:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#gters "Greater than / equal (singleprecision float)") [`++gth:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#gthrs "Greater than (singleprecision float)") [`++lte:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#lters "Less than / equal (singleprecision float)") [`++lth:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#lthrs "Less than (singleprecision float)") [`++ma:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#mars "Initialize ff (rs core)") [`++mul:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#mulrs "Multiply (singleprecision float)") [`++san:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#sanrs "Signed integer to @rs") [`++sea:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#sears "Convert from singleprecision float to fn") [`++sig:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#sigrs "Produce sign of @rs") [`++sqt:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#sqtrs "Produce square root of singleprecision float") [`++sub:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#subrs "Subtract from singleprecision float") [`++sun:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#sunrs "Unsigned integer to singleprecision float") [`++toi:rs`](https://urbit.org/docs/hoon/reference/stdlib/3b/#toirs "Round singleprecision float to nearest signed integer")
-   [3c: urbit time](https://urbit.org/docs/hoon/reference/stdlib#3c-urbit-time)
  -   [`++yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yo "Time constants core") [`++cet:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#cetyo "Days in a century") [`++day:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#dayyo "Seconds in day") [`++era:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#erayo "Leapyear period") [`++hor:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#horyo "Seconds in hour") [`++jes:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#jesyo "Maximum 64bit timestamp") [`++mit:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#mityo "Seconds in minute") [`++moh:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#mohyo "Days in month") [`++moy:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#moyyo "Days in months of leapyear") [`++qad:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#qadyo "Seconds in 4 years") [`++yer:yo`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yeryo "Seconds in year")
  -   [`++yall`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yall "Time since beginning of time") [`++yawn`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yawn "Days since beginning of time") [`++year`](https://urbit.org/docs/hoon/reference/stdlib/3c/#year "Date to @d") [`++yell`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yell "Tarp from atomic date") [`++yelp`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yelp "Determine if leapweek") [`++yore`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yore "Date from atomic date") [`++yule`](https://urbit.org/docs/hoon/reference/stdlib/3c/#yule "Daily time to time atom")
-   [4a: exotic bases](https://urbit.org/docs/hoon/reference/stdlib#4a-exotic-bases)
  -   Urbit phonetic base (`@p`):  [`++po`](https://urbit.org/docs/hoon/reference/stdlib/4a/#po "Phonetic base") [`++ind:po`](https://urbit.org/docs/hoon/reference/stdlib/4a/#indpo "Parse suffix") [`++ins:po`](https://urbit.org/docs/hoon/reference/stdlib/4a/#inspo "Parse prefix") [`++tod:po`](https://urbit.org/docs/hoon/reference/stdlib/4a/#todpo "Fetch suffix") [`++tos:po`](https://urbit.org/docs/hoon/reference/stdlib/4a/#tospo "Fetch prefix")
  -   Bitcoin base-58:  [`++fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#fa "base58check") [`++cha:fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#chafa "Decode base58check character") [`++tok:fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#tokfa "Compute base58check checksum") [`++pad:fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#padfa "base58check padding bytes") [`++enc:fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#encfa "Encode base58check") [`++den:fa`](https://urbit.org/docs/hoon/reference/stdlib/4a/#denfa "Decode base58check")
-   [4b: text processing](https://urbit.org/docs/hoon/reference/stdlib#4b-text-processing)
  -   [`++cass`](https://urbit.org/docs/hoon/reference/stdlib/4b/#cass "To lowercase") [`++crip`](https://urbit.org/docs/hoon/reference/stdlib/4b/#crip "Tape to cord") [`++cuss`](https://urbit.org/docs/hoon/reference/stdlib/4b/#cuss "To uppercase") [`++mesc`](https://urbit.org/docs/hoon/reference/stdlib/4b/#mesc "Escape special characters") [`++runt`](https://urbit.org/docs/hoon/reference/stdlib/4b/#runt "Prepend n times") [`++sand`](https://urbit.org/docs/hoon/reference/stdlib/4b/#sand "Softcast by aura") [`++sane`](https://urbit.org/docs/hoon/reference/stdlib/4b/#sane "Check aura validity") [`++teff`](https://urbit.org/docs/hoon/reference/stdlib/4b/#teff "UTF8 length") [`++trim`](https://urbit.org/docs/hoon/reference/stdlib/4b/#trim "Tape split") [`++trip`](https://urbit.org/docs/hoon/reference/stdlib/4b/#trip "Cord to tape") [`++tuba`](https://urbit.org/docs/hoon/reference/stdlib/4b/#tuba "UTF8 to UTF32 tape") [`++tufa`](https://urbit.org/docs/hoon/reference/stdlib/4b/#tufa "UTF32 to UTF8 tape") [`++tuft`](https://urbit.org/docs/hoon/reference/stdlib/4b/#tuft "UTF32 to UTF8 text") [`++taft`](https://urbit.org/docs/hoon/reference/stdlib/4b/#taft "UTF8 to UTF32 cord") [`++wack`](https://urbit.org/docs/hoon/reference/stdlib/4b/#wack "Knot escape") [`++wick`](https://urbit.org/docs/hoon/reference/stdlib/4b/#wick "Knot unescape") [`++woad`](https://urbit.org/docs/hoon/reference/stdlib/4b/#woad "Unescape cord") [`++wood`](https://urbit.org/docs/hoon/reference/stdlib/4b/#wood "Escape cord")
-   [4m: parsing (formatting functions)](https://urbit.org/docs/hoon/reference/stdlib#4m-parsing-formatting-functions)
  -   [`++scot`](https://urbit.org/docs/hoon/reference/stdlib/4m/#scot "Render dime as cord") [`++scow`](https://urbit.org/docs/hoon/reference/stdlib/4m/#scow "Render dime as tape") [`++slat`](https://urbit.org/docs/hoon/reference/stdlib/4m/#slat "Curried slaw") [`++slav`](https://urbit.org/docs/hoon/reference/stdlib/4m/#slav "Demand: parse cord with input aura") [`++slaw`](https://urbit.org/docs/hoon/reference/stdlib/4m/#slaw "Parse cord to input aura") [`++slay`](https://urbit.org/docs/hoon/reference/stdlib/4m/#slay "Parse cord to coin") [`++smyt`](https://urbit.org/docs/hoon/reference/stdlib/4m/#smyt "Render path as tank") [`++spat`](https://urbit.org/docs/hoon/reference/stdlib/4m/#spat "Render path as cord") [`++spud`](https://urbit.org/docs/hoon/reference/stdlib/4m/#spud "Render path as tape") [`++stab`](https://urbit.org/docs/hoon/reference/stdlib/4m/#stab "Parse cord to path") [`++stap`](https://urbit.org/docs/hoon/reference/stdlib/4m/#stap "Path parser")

Let's examine some specific implementations:

How do we convert text into all lower-case?
- [`++cass`](https://urbit.org/docs/hoon/reference/stdlib/4b#cass)

How do we turn a `cord` into a `tape`?
- [`++trip`](https://urbit.org/docs/hoon/reference/stdlib/4b#trip)

How can we make a list of a null-terminated tuple?
- [`++le:nl`](https://urbit.org/docs/hoon/reference/stdlib/2m#lenl)

How can we evaluate Nock expressions?
- [`++mink`](https://urbit.org/docs/hoon/reference/stdlib/4n#mink)

(If you see a `|*` bartar rune in there, it's similar to a `|=` bartis, but what's called a _wet gate_.)

### `zuse.hoon`

When you open `zuse.hoon`, you'll see that it is composed with some data structures from `%lull`, but that by and large it consists of a core including arms organized into “engines”.

Most of these are internal Arvo conventions, such as conversion between Unix-epoch times and Urbit-epoch times.  The main one you are likely to work with is the `++html` core, which contains important tools for working with web-based data, such as [MIME types](https://en.wikipedia.org/wiki/Media_type) and [JSON strings](https://en.wikipedia.org/wiki/JSON).

To convert a `@ux` hexadecimal value to a `cord`:

```hoon
> (en:base16:mimes:html [3 0x12.3456])
'123456'
```

To convert a `cord` to a `@ux` hexadecimal value:

```hoon
> `@ux`q.+>:(de:base16:mimes:html '123456')
0x12.3456
```

There are tools for working with Bitcoin wallet base-58 values, JSON strings, XML strings, and more.

```hoon
> (en-urlt:html "https://hello.me")
"https%3A%2F%2Fhello.me"
```

What seems to be missing from the standard library?


##  Conditional Expressions

Let's wrap up the `?` wut runes, many of which you have already seen:

Conditional decision-making:

- [`?:` wutcol](https://urbit.org/docs/hoon/reference/rune/wut#-wutcol) lets you branch between an expression-if-true and an expression-if-false.
- [`?.` wutdot](https://urbit.org/docs/hoon/reference/rune/wut#-wutdot) inverts the order of `?:`.  Good Hoon style prescribes that the heavier branch of a logical expression should be lower in the file.
- [`?-` wuthep](https://urbit.org/docs/hoon/reference/rune/wut#-wuthep) lets you choose between several possibilities, as with a type union.  Every case must be handled and no case can be unreachable.
- [`?+` wutlus](https://urbit.org/docs/hoon/reference/rune/wut#-wutlus) is similar to `?-` but allows a default value in case no branch is taken.

Assertions:

- [`?>` wutgar](https://urbit.org/docs/hoon/reference/rune/wut#-wutgar) is a positive assertion (`%.y` or crash).
- [`?<` wutgal](https://urbit.org/docs/hoon/reference/rune/wut#-wutgal) is a negative assertion (`%.n` or crash).
- [`?~` wutsig](https://urbit.org/docs/hoon/reference/rune/wut#-wutket) asserts non-null.
- [`?^` wutket](https://urbit.org/docs/hoon/reference/rune/wut#-wutket) asserts cell.
- [`?@` wutpat](https://urbit.org/docs/hoon/reference/rune/wut#-wutpat) asserts atom.

Logical operators:

- [`?&` wutpam](https://urbit.org/docs/hoon/reference/rune/wut#-wutpam), irregularly `&()`, is a logical `AND` over loobean values.
- [`?|` wutbar](https://urbit.org/docs/hoon/reference/rune/wut#-wutbar), irregularly `|()`, is a logical `OR` over loobean values.
- [`?!` wutzap](https://urbit.org/docs/hoon/reference/rune/wut#-wutzap), irregularly `!`, is a logical `NOT`.

Pattern matching:

- [`?=` wuttis](https://urbit.org/docs/hoon/reference/rune/wut#-wuttis) tests for a pattern match in type, someday to be superseded or supplemented by a planned `?#` wuthax rune.


##  Functional Programming

Given a gate, you can manipulate it to accept a different number of values than its sample formally requires, or otherwise modify its behavior.

### Changing Arity

If a gate accepts only two values in its sample, for instance, you can chain together multiple calls automatically using [`;:` miccol](https://urbit.org/docs/hoon/reference/rune/mic#-miccol):

```hoon
> (add 3 (add 4 5))
12
> :(add 3 4 5)
12
> (mul 3 (mul 4 5))
60
> :(mul 3 4 5)
60
```

This is called changing the _arity_ of the gate.  (Does this work on `++mul:rs`?)

### Binding the Sample

If you have a gate which accepts multiple values in the sample, you can fix one of these.  To fix the head of the sample (the first argument), use [`++cury`](https://urbit.org/docs/hoon/reference/stdlib/2n#cury); to bind the tail, use [`++curr`](https://urbit.org/docs/hoon/reference/stdlib/2n#curr).

Consider calculating _a x² + b x + c_, a situation we earlier resolved using a door.  We can resolve the situation differently using currying:

```hoon
> =full |=([x=@ud a=@ud b=@ud c=@ud] (add (add (mul (mul x x) a) (mul x b)) c))
> (full 5 4 3 2)
117
> =one (curr full [4 3 2])  
> (one 5)  
117
```

One can also [`++cork`](https://urbit.org/docs/hoon/reference/stdlib/2n#cork) a gate, or arrange it such that it applies to the result of the next gate.  This pairs well with `;:` miccol.  (There is also [`++corl`](https://urbit.org/docs/hoon/reference/stdlib/2n#corl).)  This example converts a value to `@ux` then decrements it:

```hoon
> ((cork dec @ux) 20)  
0x13
```

### Reeling A Jig

[`++roll`](https://urbit.org/docs/hoon/reference/stdlib/2b#roll) and [`++reel`](https://urbit.org/docs/hoon/reference/stdlib/2b#reel) are used to left-fold and right-fold a list, respectively.  To fold a list is similar to [`++turn`](https://urbit.org/docs/hoon/reference/stdlib/2b#turn), except that instead of yielding a `list` with the values having had each applied, `++roll` and `++reel` produce an accumulated value.

```hoon
> (roll `(list @)`[1 2 3 4 5 ~] add)
q=15
> (reel `(list @)`[1 2 3 4 5 ~] mul)
120
```
