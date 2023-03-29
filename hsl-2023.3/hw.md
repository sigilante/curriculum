#   `%hw1`

Homework #1 for Hoon School Live.  
  
Homework exercises have two purposes for us:  to help validate that you have learned the material that corresponds to a particular lesson, and to stretch you in grasping and applying the relevant concepts.  
  
In particular, you learned about the following runes:  
  
- `%-` cenhep, for applying a function  
- `^-` kethep, for enforcing or converting the type of a value  
- `:-` colhep, for making a cell (pair of nouns)  
- `=/` tisfas, for assigning a name to a value  
- `?:` wutcol, for making a decision

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your actual ship, not your fakeship.)

## Atoms

Atoms are bare values, but they have a type or aura which lets you distinguish, say, a 1 in binary 0b1 from a 1 in hexadecimal 0x1.

- Q1. Find your planet's number by converting your ship’s name to a `@ud` aura.

- Q2. Find your planet's hexadecimal number by converting your ship’s name to a `@ux` aura.

- Q3. What are the types (auras) of each of the following atoms?  Consult https://developers.urbit.org/reference/hoon/auras if you can't tell offhand.  

`@ud`
`@ub`
`@ux`
`@t`
`@da`
`@rs`
`@p`

`1.000`
`0b11.1001`
`0x7fa.45e2`
`'hello Mars'`
`~1992.1.12..15.05.00`
`.2.718281828`
`~sampel-palnet`

##  Cells

Read about the `:` col family of runes in the docs:  
  
[https://urbit.org/docs/hoon/reference/rune/col](https://urbit.org/docs/hoon/reference/rune/col)  
  
These build cells of various sizes (e.g. [1 [2 3]], etc.).

- Q4. Create a duple, or 2-tuple, of 1 and 2, using a single col rune.

- Q5. Create a triple, or 3-tuple, of 'a', 'b', and 'c', using a single col rune.

- Q6. Create a quadruple, or 4-tuple, of ~zod, ~nec, ~bud, and ~wes, using a single col rune.

##  Pinning Values

The =/ tisfas rune is helpful for preserving (“pinning”) values with names for use in subsequent expressions.  For each of these, you should respond with the Hoon expression, not the resulting value.

- Q7. In one expression, pin a value `three` and calculate 3×3 using the ++mul function (gate).

- Q8. In one expression, pin two values `ten` and `hundred` and calculate 10¹⁰⁰ using the ++pow function (gate).

##  Making Decisions

We can cause a computation to choose between two alternatives using the `?:` wutcol rune.

- Q9. Implement the piecewise boxcar function in Hoon.  Since we can't store expressions for future use yet, use 4 for the example input value (but pin it to a face `x`).  (:= is not a rune, it's the mathematical symbols for "defined as".  You can read it as an equals sign.)  
  
That is, your answer will look something like this, i.e. multiple lines (for x²):  
  
```
=/  x  2  
(mul x x)
```

![](https://lh4.googleusercontent.com/WlI6c18pNF3MT06ZXkmHiVur2yU8GFDlaWwmFB2rS6CpOHG_hO7BDnajgICvgnZwZBo5GbNTpMmEQDeKuXcm2WubU8tvo1PU0_TBKCxYYwbnoBCCUkDIq7D0zKSLq44JnIkT7J3WYMIF1StVHZY-WTHSLobaUqWrd3JanplXPkwrtwRDdAkt6e-BhG24Fxazr1HO)

- Q10. Implement the piecewise triangle function in Hoon.  Since we can't store expressions for future use yet, use 2 for the example input value (but pin it to a face `x`).  (:= is not a rune, it's the mathematical symbols for "defined as".  You can read it as an equals sign.)  
  
That is, your answer will look something like this, i.e. multiple lines (for x²):  
  
```
=/  x  2  
(mul x x)
```

![](https://lh3.googleusercontent.com/mTMXcMr2wi4pUSC3ThN7nOVxl_Ou5Oq4UNMiFhjr9cqyt-6mtZFjYwjqYzv8gTtrK7JNe5UfytmO9guGiWBZsxHyqL-x3grQeVzLCdY0at7sHY3u-tLjWpSlADmZylrlxeZAdRtLlwNvzshpd5LRvsLPhmRmB5dJQPC2SspUSh62gQ38qs6mFCWZBI2cngyUoIuf)

##  Hoon Pronunciation

What are the pronounced names of each of the following runes?

- Q11. `%=`

- Q12. `$:`

- Q13. `:*`

- Q14. `~&`

- Q15. `|-`

- Q16. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 1?

---

#   `%hw2`

Homework #2 for Hoon School Live.  
  
You have now learned how to use irregular syntax for Hoon runes, and should think about how to employ it when convenient.  
  
You have learned about the following runes:  
  
- `^+` ketlus, for enforcing a type (like `^-` but with an example)  
- `^*` kettar, for producing an example (a bunt)  
- `!>` zapgar, for ascertaining the type of a value  
- `|=` bartis, for creating a gate  
- `::`, for commenting on code  
  
Not covered in the live lesson but in the notes:  
  
- `$?` bucwut, for producing a type union  
- `$:` buccol, for producing a named tuple  
- `!!` zapzap, for crashing or stubbing out incomplete branches of your Hoon expressions  
- `/+` faslus, for importing a library of code

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

##  Irregular Syntax

Many runes have irregular syntax.  This can make it easier to write aesthetically expressive Hoon code.

- Q1. Convert the irregular form `[1 2 3 4]` to a regular form.

- Q2. Convert the irregular form `(mul 10 5)` to a regular form.

- Q3. Convert the regular form `^-  @ud  ^-  @  'Mars'` to an irregular form.

##  Molds

Molds define Hoon structures.  They have a default value (“bunt”) and are strictly statically typed (i.e. they must match).

- Q4. What is the bunt of `@da`?

- Q5. What is the bunt of `@uc`?

- Q6. What is the bunt of `@da` as a `@ud`?  (I.e., bunt it then convert that value to @ud.)  

- Q7. What is the bunt of `cell`?  (I.e. there is a type in Hoon named `cell`, do it of that.)

- Q8. Produce a type union which can accept a signed or unsigned decimal integer.  (ETA:  actually not a good question since type unions can't distinguish auras, do it for practice but I'll have to take this one out next time around)  

- Q9. Produce a named tuple with three elements `x`, `y`, and `z`, all of type `@rs` (real number, number with a fractional part).

- Q10. What does the infixed `^` ket do?  E.g., `4^5`.  (Infer from its behavior in the Dojo.)

##  Deferring Computation

A gate (made with `|=` bartis) lets you store a computation for future use.  
  
You can store a gate as a standalone reusable file called a generator.

- Q11. Take your code for the boxcar function in the previous homework.  Produce a gate which works for any `@ud` input value `x`.  (Your answer should just be that gate, `|=` onwards.)  

![](https://lh3.googleusercontent.com/GircNC0W49Axuddqbw280FX7CYA53q70TXT1v_qp6OEFutcIcz5Kc1OnwRFbjLIgG9kMfRYuvawL5XWK7a6mb10Itiye6y22UOAX0pPDZOblTLR7IfiwDa6Iwx8PEDkKFVG4jw3fzxbhX89NVT32QTaJMKfkP6SSAmIxM7xgVTOHFBLhQTvtlWHVGfmZPsKJgos_)

- Q12. Take your code for the boxcar function gate in the previous question.  Produce a generator from the gate named `boxcar.hoon`.  Don't forget to add at least one comment to explain its intent.  (Your answer will be very similar to the answer for Q11.)

![](https://lh3.googleusercontent.com/GircNC0W49Axuddqbw280FX7CYA53q70TXT1v_qp6OEFutcIcz5Kc1OnwRFbjLIgG9kMfRYuvawL5XWK7a6mb10Itiye6y22UOAX0pPDZOblTLR7IfiwDa6Iwx8PEDkKFVG4jw3fzxbhX89NVT32QTaJMKfkP6SSAmIxM7xgVTOHFBLhQTvtlWHVGfmZPsKJgos_)

- Q13. Write a generator which accepts the value of a planet as a `@p` and returns the next neighbor, also as a `@p`.  The next neighbor of a planet is calculated by incrementing the numeric value of the planet's address by one.  You will then need to convert it from `@ud` back to `@p`.  (You don't need to filter for planet input or anything, just for `@p`.)  For instance, the next neighbor of ~sampel-palnet is ~radbyr-fonlyr.

- Q14. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 2?

---

#   `%hw3`

Homework #3 for Hoon School Live.

With the introduction of cores, you are now equipped to build Hoon generators that can also function as libraries.

You have learned about the following runes:

- `|-` barhep, for producing a trap (like a loop or repetition label)
- `.+` dotlus, for increasing a value by one
- `.=`, for checking equality/equivalence of two values
- `%=` centis, for "rebooting" the current code with new values
- `|%` barcen, for collecting many functions and values in one core
- `++` luslus (actually a digraph, not a rune, but that's technical), for labeling a gate
- `+$` lusbuc (ditto), for labeling a type
- `=<` tisgar, for
- `=>` tisgal, for
- `~&` sigpam, for output as a debugging or messaging tool

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. You work in a lab.  The lab uses a scale which is inaccurate for values less than 10 grams.  Any weight less than that should simply register as zero in your measurements.  Write a gate in an arm `++corrected-weight` which checks whether the value is less than 10 and returns zero if it is, otherwise returns the normal value.  (Answer with the arm as the only arm in a regular |% core.)

- Q2. The lab needs to know the total quantity of reagent (in grams) you've been able to produce in the past week.  You have the totals for every day.  Write a gate in an arm `++weekly-reagent` which uses a trap to add up the seven values it receives in a 7-element list.  E.g., `~[134 287 12 0 127 194 0]` should sum to 754.  (Answer with the arm as the only arm in a regular |% core.)

- Q3. Produce a type arm named `reptile` using +$ lusbuc which is a type union ($? bucwut) for several reptiles of your choice.  (E.g. if I were doing this for amphibians, I could use %frog, %toad, and %salamander.)  Provide at least four options in the type union.  (The `%word` syntax is a "term", or internal constant value we can use to label things in Hoon:  previewing this a bit!)

- Q4.  Produce a gate (generator) which accepts a list of values and prints out each value in order on a separate line.

  For example, given the `(list @)` `[1 2 3 4 5 ~]`, the generator should  print out
  
  ```
  '1'
  '2'
  '3'
  '4'
  '5'
  ```

  You do not need to store these values in a list; simply output them at each step using `~&` sigpam and return the final value.  Sigpam does *not* return a value, it simply displays a result and then continues to the next line (its second child).

  You can retrieve the n-th element in a list using the `++snag` gate:
  
  ```
  > =/  n  0  (snag n [1 2 3 4 5 ~])
    1
  ```
  
  (Note that `++snag` counts starting at zero, not one.)
  
  You can get the length of a list using `++lent`.
  
  You can check for whether two values are equal using `=(1 2)` syntax (irregular form of `.=` dottis).

- Q5.  Produce a gate (generator) which accepts a list of values and prints out each value in *reverse* order on a separate line.

  For example, given the `(list @ux)` `[0x0 0x1 0x2 ~]`, the generator should  print out

  ```
  0x2
  0x1
  0x0
  ```
  
  Your code from the previous exercise should work with modest changes.

- Q6. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 3?

---

# `%hw4`

Homework #4 for Hoon School Live.  
  
Urbit has several ways to represent and work with text values.  The list is broader than just a text representation format, however, and affords the most common way to work with data in Hoon.

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

##  Text in Hoon

There are four basic representations of text in Urbit:  cords, knots, terms, and tapes.

- Q1. Which text representation do each of the following values fall into?

  - `@t` cord
  - `@ta` knot
  - `@tas` term
  - `(list @t)` tape
  
  - `'nitwit'`
  - `~.blubber`
  - `%oddment`
  - `"tweek"`

- Q2. How would you convert the list `~[114 97 105 110 98 111 119 32 115 104 101 114 98 101 116]` to a `tape`?  (You should actually try this in Dojo to make sure your proposal works; it's similar to clearing a type by passing through the empty aura.)

- Q3. FizzBuzz is a classic computer science challenge question.  For this step, write a gate in an arm `++fizz` which accepts a count and counts upward from one to that value, appending the number each time OR "fizz" (as tape) every third number until the count is reached.  (I.e., given 7, it should yield the list ~[1 2 "fizz" 4 5 "fizz" 7].)  (Answer with the arm as the only arm in a regular |% core.)

- Q4.  For this step, write a gate in an arm ++buzz which accepts a count and counts upward from one to that value, appending the number each time OR "buzz" (as tape) every fifth number until the count is reached.  (I.e., given 7, it should yield the list ~[1 2 3 4 "buzz" 6 7].)  (Answer with the arm as the second arm after ++fizz in a regular |% core.)

- Q5. For this step, write a gate in an arm `++fizzbuzz` which accepts a count and counts upward from one to that value, appending the number each time, "fizz" every third number, and "buzz" every fifth number until the count is reached.  (I.e., given 15, the list should count from 1 to 15 thus: ~[1 2 "fizz" 4 "buzz" "fizz" 7 8 "fizz" "buzz" 11 "fizz" 13 14 "fizz buzz"].)  Make sure that it outputs *both* "fizz" and "buzz" for numbers that are divisible by both three and five.  (Answer with the arm as the third arm after `++fizz` and `++buzz` in a regular |% core.)  

- Q6. In the lesson, there was an exercise to produce a library and a generator which counted the number of words in a given tape.  Compose the library such that it consists of a `|%` barcen core including a `++split-tape` arm and a `++count-elements` arm.  Submit the library as your answer here.

- Q7. In the lesson, there was an exercise to produce a library and a generator which counted the number of words in a given tape.  The generator should import the library using the `/+` faslus rune and return the number of words in a text sample.  Submit the generator as your answer here.

- Q8. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 4?

---

# `%hw5`

Homework #5 for Hoon School Live.  
  
One of the most common kinds of cores in Hoon is the door.  A door is sort of a gate-builder, which uses its arms to produce gates on demand (e.g. for particular types/auras/molds).  
  
You have learned about the following runes:  
  
- `|_` barcab, for producing a door  
- `%~` censig, to "pull an arm" in a door, or use a door to build a new gate and evaluate it  
- `|^` barket, for producing a core with a `$` default arm  
- `|.` bardot, for producing a trap to be evaluated at a later time  
- `|:` barccol, for producing a gate with a custom sample  
- `!: zapcol, to turn on debugging in a library or generator file  
- `$_` buccab, to define a default sample (other than the bunt) in a core

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. Write a gate named ++decrement that implements decrement without using the standard library functions of ++sub or ++dec.  (Hint:  Count up to one less than the input value using recursion).

- Q2. A prime number is a number which is only divisible by itself and one (it has no factors), such as 2, 3, 5, 7, and 11.  Write a gate named ++primes which produces the Euler primes as a list.  The Euler primes are given by k²-k+n (for k = 1 to n-1).  (Note:  Your program will produce a set of primes if given one of "Euler's lucky numbers": 1, 2, 3, 5, 11, 17, or 41.)  See [https://number.subwiki.org/wiki/Lucky_number_of_Euler](https://number.subwiki.org/wiki/Lucky_number_of_Euler) for a table of example values.

- Q3. Consider the gate `|=(a=@ud (add 1 a))`.  What is the compiled battery of this gate?

- Q4. Write an arm named ++factorial which calculates the factorial of a value.  Make its default sample value for the input be 1 using either `$_` or `|:`.  Make sure that 0! results in the value 1.  Answer with the |% core containing the arm.  

- Q5. Write a door (named calc if used in Dojo) that takes a @ud sample.   It should have four arms to handle multiplication, subtraction, addition, and division against this value.  For instance, you should be able to build an addition gate with `~(add calc 3)` and use it with `(~(add calc 3) 5)` to result in 8.  Answer with the door (no containing core necessary, thus no outer arm name); this could be a /lib library file for instance.  

- Q6. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 5?

---

# `%hw6`

Homework #6 for Hoon School Live.  
  
Let's use doors to build some new tools.  
  
You have learned about the following runes:  
  
- `?>` wutgar, branch on a positive assertion  
- `?<` wutgal, branch on a negative assertion  
- `?~` wutsig, branch on a null result  
- `+$` lusbuc, produce a type builder arm

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. Produce a Hoon expression which makes a map which has Shakespeare characters as keys and the corresponding play as the value.  (This does not need to be a jar; you can just include one play for characters that recur in multiple plays.)  You may use ++my or ++put:by or another means to construct the map.  Make sure it has at least four elements.

##  Caesar cipher

The Caesar cipher code is an excellent example of an Urbit generator built with many arms.  You should closely read it, and I recommend even printing or drawing it and putting arrows to track its behavior.

- Q2. Extend the generator to allow for use of characters other than a-z.  It should also permit characters .,;:'" and you may have it rotate those the same way as letters are rotated.

- Q3. Build a gate that can take a Caesar-shifted tape and produce all possible unshifted tapes as a list of tapes.  This should be performed using the original a-z only cipher.

- Q4. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 6?

---

# `%hw7`

Homework #7 for Hoon School Live.  
  
- `;:` miccol, for changing the arity of a gate  
- `?|` wutbar, logical OR  
- `?&` wutpam, logical AND  
- `?!` wutzap, logical NOT  
- `?.` wutdot, inverse ?: wutcol  
- `?-` wuthep, switch  
- `?+` wutlus, switch with default

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. Compose a gate which accepts a tape representing a hexadecimal color value and returns the equivalent @ux hexadecimal value.  E.g., given any of "#ABCDEF", "#abcdef", "ABCDEF", or "abcdef", the gate should return 0xab.cdef.

- Q2. Look up ++sub in hoon.hoon.  Rewrite the arm so that it 1) omits the ~/ and ~_ lines and 2) uses ?. instead of ?:.  (You may also remove the comment lines ::.)

- Q3. What does the @q aura do?  Try it on the values 65.535 and 65.536; compare to @p's behavior on the same values.

- Q4. Write a switch statement using a ? wut rune which branches on a type union of ?(%one %two ...) up to five, and returns the @ud equivalent in a unit.

- Q5. Curry ++gth using ++cury or ++curr such that its input is always evaluated with respect to 10.  (I.e. produce a gate that does this.)

- Q6. Produce a gate which folds a list using ++reel or ++roll with ++add:rs to produce the cumulative sum of a list.  E.g. the sum of ~[.1.0 .0.5 .0.333 .0.25 .0.2 .0.167 .0.143 .0.125 .0.111] should be .2.829.

- Q7. Compose an expression using ;:'s irregular form to calculate the factorial of 5 (=120).

- Q8. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 7?

---

# `%hw8`

Homework #8 for Hoon School Live.  
  
_L'état, c'est moi.__  (Louis XIV)  

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. Take your calculator door from previous homework and compose it into a %say generator that uses =< tisgal and =~ tissig to carry out a sequence of calculations.  (Thus the door should be in the same file, not included as a library.)  

- Q2. Convert your FizzBuzz program to produce a tank (formatted print tree).  Produce a %say generator that yields a ++ram-ed version of this output, bounded by "(" pal and ")" par, and separated by "|" bar.  

- Q3. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 8?

---

# `%hw9`

Homework #9 for Hoon School Live.  
  
It's time to verify our code's behavior and share it with the world!

- Q0. What is your planet or comet?  (Type "our" in the Dojo of your ship to identify if you're not sure—your ship, not your fakeship.)

- Q1. In %hw5 you produced a gate which calculated Euler primes.  Write a test suite for your arm.  It should test at least four different cases, one of which should be a failure to calculate (e.g. is there input it should crash on?).

- Q2. In %hw5 you produced a door which carried out calculator arithmetic functions  Write a test suite for your door.  It should test at least three different cases for each arm.  You should check for failure to compute with subtraction underflow (i.e. 5-7).

- Q3. Collect a generator or library from a previous homework assignment.  Host it on a new desk on a moon of your primary ship.  Use the generator or library name plus a random unpredictable name for the desk (so we don't have to worry about collisions, e.g. calc-12345) and mark it |public.  Let us know which moon you have it running on and we'll sync it and install it.  (You could host on your main ship; the real issue is leaving the source ship running at least until we can check it.)

- Q4. What are your biggest remaining concerns, points of misunderstanding or fuzzy understanding, or other feedback on Lesson 9?
