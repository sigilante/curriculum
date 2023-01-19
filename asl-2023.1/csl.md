1. The core stack
  1. The nested core stucture of `hoon.hoon`, `%zuse`, and `%lull`
2. Building and evaluating code
  1. The compiler:  `$hoon`, `+ream`, `+mint`, `$type`, `+nest`, `+play`
  2. Nock
  3. Hints and jetting
  4. Vase-mode Hoon:  `+slap`, `+slop`, `+slot`, `+slam`
3. The Arvo kernel
  1. Arvo's mature structure
  2. Event handling:  wires and ducts, running vanes, vane scrys, builds & kernel upgrades
  3. Arvo/Vere interface:  `+peek` and `+poke` arms, the kelvin stack (`hoon`, `arvo`, `lull`, `zuse`)
  4. The boot sequence:  pills, arvo larval phase, pre-boot validation, vane initialization, userspace initialization (hood)
4. The Vere runtime
  1. Vere:  the urth/mars split, noun IPC, event log and basics of snapshots
  2. The allocator: the loom, noun memory layout, reference counting, structural sharing, roads & metacircularity
  3. paging and snapshots: page faults & memory protection, guard page, incremental snapshots, demand paging
  4. I/O: basics of vanes (other than the "landlocked" vanes: Gall and Jael) and their corresponding I/O drivers
5. Vanes
  1. Behn or Kahn as minimum viable vane example
  2. Ames
    1. Message-level protocol
    2. Packet-level protocol (UDP)
    3. Relation to PKI
    4. Remote scry
  3. Eyre
    1. `+on-poke`/`+on-watch` translation to server-side events
    2. Canned response system
    3. Scrying
    4. Hostnames
    5. `:acme`
  4. Gall
    1. `$agent`
    2. Running agents
    3. Upgrades
  5. Clay
    1. Revision control structure
    2. Basic `+ford` operations
    3. The mark system
    4. Scry cares
    5. Upgrades
  6. Jael
    1. PKI state and transitions
    2. L1 vs. L2 (naive rollup)
    3. Scry cares
    4. HD wallet
    5. rift, life

---

Structure:
- Weekly 90-minute to two-hour working sessions (lecture + discussion + hands-on start)

Preliminary material:
- Hoon School, Genericity and Variance
- Hoon School, Text Parsing III
- The Nested Cores Pattern

Lessons:
- `csl00` The Core Stack
  - Diagram the nested core stucture of `hoon.hoon`, `%zuse`, and `%lull`.
  - Explain how subject search and limb resolution works.
  - Distinguish static and dynamic dispatch.
  - Exercise:  Explain how `+sloe` works.
- `csl01` Building Hoon
  - Explain the compiler stack, including `$hoon`, `+ream`, `+mint`, `$type`, `+nest`, `+play`.
  - Utilize vase-mode Hoon and explain its _raison d'être_:  `+slap`, `+slop`, `+slot`, `+slam`
  - Exercise:  Implement a rune (block comment?).
  - Exercise:  Write your own `+slam`.
- `csl02` Evaluating Nock
  - Explain each Nock rule.
  - Understand hints and jetting.
  - Exercise:  Write your own Nock interpreter in Hoon
  - Exercise:  Write your own jet.
- `csl03` Arvo I:  The Main Sequence
  - Diagram Arvo's mature structure.
  - Diagram event handling:  wires and ducts, running vanes, vane scrys, builds & kernel upgrades.
  - Explain the kelvin stack (`hoon`, `arvo`, `lull`, `zuse`).
  - Exercise:  Produce an annotated move trace.
  - Exercise:  Produce a minimalist Arvo handler.
- `csl04` Arvo II:  The Boot Sequence
  - The boot sequence:  pills, arvo larval phase, pre-boot validation, vane initialization, userspace initialization (hood)
  - Exercise:  Annotate the boot sequence in `hoon.hoon` line-by-line.  TODO
- `csl05` Vere I:  The Runtime
  - Explain the Arvo/Vere interface:  `+peek` and `+poke` arms.
  - Show how Vere works in practice:  the urth/mars split, noun IPC, event log and basics of snapshots.
  - Exercise:  TODO
- `csl06` Vere II:  The Loom
  - Explain the memory allocator:  the loom, noun memory layout, reference counting, structural sharing, roads & metacircularity.
  - Show how paging and snapshots work: page faults & memory protection, guard page, incremental snapshots, demand paging.
  - Exercise:  TODO pack/meld?
- `csl07` Vanes I:  Behn, Dill, Kahn
  - Examine the structure of Behn.
  - Study Dill, including Dojo, Helm, and Hood.
  - Exercise:  Examine the structure of Kahn.
- `csl08` Vanes II:  Ames
  - Study Ames:  message-level protocol, packet-level protocol (UDP), relation to PKI, remote scry
  - Exercise:  TODO
- `csl09` Vanes III:  Eyre
  - Study Eyre:  `+on-poke`/`+on-watch` translation to server-side events, canned response system, scrying, hostnames, `:acme`
  - Exercise:  TODO
- `csl10` Vanes IV:  Clay
  - Study Clay:  revision control structure, basic `+ford` operations, the mark system, scry cares, upgrades, Kiln.
  - Exercise
- `csl11` Vere III:  Vane Drivers
  - Examine I/O:  basics of vanes (other than the "landlocked" vanes: Gall and Jael) and their corresponding I/O drivers
  - Exercise:  TODO
- `csl12` Vanes V:  Gall
  - Study Gall:  `$agent`, running agents, upgrades
  - Exercise:  Implement a minimalist Gall (`%burl`) for agents with a `+poke` gate.
- `csl13` Vanes VI:  Jael, Azimuth
  - Study Jael:  PKI state and transitions, scry cares, rift/life, `%eth-watcher`.
  - Study Azimuth:  L1 vs. L2 (naive rollup), HD wallet.
  - Exercise:  TODO
- `capstone`:  Fix something in the core with `"should"` commented on it.  (More seriously, these will be guided towards core dev needs.)

---



https://arstechnica.com/information-technology/2012/01/microsoft-pimps-it-old-school-with-a-pricey-text-adventure-game/
