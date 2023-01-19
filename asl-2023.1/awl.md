#   App Workshop Live

> I believe we should teach students design by having them study the great works of the past, just as other disciplines do. They should spend at least a full course reading code and building working models of common applications in order to become familiar with prior art and prior thinking. In their assignments, they should compare and contrast undo/redo handling in Emacs and Vim or the data structures beneath Git and Mercurial, or create programs like Mary Rose Cook’s [Gitlet](http://gitlet.maryrosecook.com/), Matt Brubeck’s [layout engine](https://limpet.net/mbrubeck/2014/08/08/toy-layout-engine-1.html), or Conor Stack’s [little database](https://cstack.github.io/db_tutorial/). (GVW)

App Workshop Live (AWL) should teach developers how to produce more complex practical applications on the Urbit platform, synthesizing all that they've seen in the previous schools and preparing them to work as professional Hoon developers.

- Hoon School and Hoon School Live (HSL) focus on language fundamentals and common design patterns at the object level.
- App School, App School Full-Stack, and App School Live (ASL) demonstrate how to produce apps using Gall and taking advantage of the basic affordances of Urbit.

What is missing to upgrade HSL/ASL graduates and engage senior developers is deep study of existing code exemplars and hands-on demonstration to produce conceptually elegant tools.  This naturally follows from ASL's final lesson covering how to employ third-party libraries to ease development.

This course is architected pairing content overview lessons with guided tutorials.

- `awl0` server actions, Rudder/Schooner, `%feature`
- `awl1` text parsers and CLI agents
- `awl2` filesystem, minimalist Git
- `awl3` database:  data structures
- `awl4` database:  data operators
- `awl5` FE:  forum (`%hut`/Quorum)

Project ideas include Urbit implementations reflecting:

? `%pals` examination?

- `%feature`, a basic Urbit hosting app
- the parser stuff from old HSL
- [Gitlet](http://gitlet.maryrosecook.com/), a minimalist Git
- [Conor Stack's Little Database](https://cstack.github.io/db_tutorial/)
- [Ted Nelson's ZigZag data structure](https://en.wikipedia.org/wiki/ZigZag_%28software%29)
- Basic forum software with threadings (based on `%hut` and Quorum)

---

##  Resources

- [Gregory V. Wilson, _Software Design by Example_](https://third-bit.com/sdxjs/)
- [Gregory V. Wilson, “Thoughts from a Not-So-Influential Educator” (2020 ACM SIGSOFT Influential Educator Award)](https://third-bit.com/2020/07/09/acm-sigsoft-award/)

---

##  Feedback

btw something ive experienced, i rly dunno how to translate this into lesson plan but

walking thru ppl example gall agent, like even before knowing syntax really, and then doing it again after theyve picked up a lot more syntax, ive found good

i havent gone thru lessons in a very long time, but for me as someone who learns most by doing rather than structured lessons i feel like i wasnt sufficiently motivated and learned more slowly until i knew enough to build a gall agent

and there was this whole, "i don't understand anything how does pure language make applications wtf how does io work idgi" thing that made all the first lessons hard in a for what sort of sense


I think Hoon school is a bit cumbersome and much of Hoon seems to go unused in your average gall app. So I think something like "Hoon the good parts" or a Hoon Thesaurus, could 80/20 them to jump right into app school. ime Hoon school took me much longer than app school, and the parts that went slowly seem to have gone unused in development so far (although my memory is not great, being a year out from that now)




---
