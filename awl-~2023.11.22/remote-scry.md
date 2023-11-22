#   `%fine`:  Remote Scry

A scry is a read-only request into the scry namespace.  Historically, only local scries were supported, and these were instrumented synchronously using `.^` dotket.  With the addition of remote scry, a new use case and use pattern emerged:  asynchronous reads over the network.

Why does this matter?  In a classical data request over Ames, each scry request is received into Arvo and registered as an event in the process of returning the data value to the subscriber.  This generates spurious events (since the read-only request is basically a no-op) and prevents parallelizing or otherwise optimizing read-only actions.  With remote scry, Urbit desk and data distribution should be vastly more scalable than pure Ames.

The basic userspace lifecycle looks like this:

1. A publishing ship denotes a particular path to Gall as being bound into the scry namespace along with the data.
2. The publisher's runtime registers this value in its remote scry cache.
3. A subscriber requests (from Gall/Arvo) information at a particular path.
4. If that path exists, the publisher's runtime intercepts the request and dispatches the data back as an Arvo update.

##  Publishing Remote Scry Data

```hoon
+$  note
  $%  [%grow =path =page]  ::  publish
      [%tomb =case =path]  ::  delete one
      [%cull =case =path]  ::  delete up to
  ==
```

- `%grow` registers a `+$page` (a `+$cask`, or `(pair mark data)`) at a particular path.  Here you should think of the `mark` label as similar to a MIME type.  You can often just use either `%atom` or `%noun`.
- `%tomb` tombstones (reversibly removes) the value at the given path.  It's in principle possible to expose the data again at the same case/path later, and the value remains in the runtime cache.
- `%cull` permanently retires the paths up to the revision number.

For instance, `%emissary` publishes data at paths using cards like these:

```hoon
[%pass /emissary/fine %grow /patrons [%emissary-demand %patrons patrons]]
[%pass /emissary/fine %grow /delegates [%emissary-demand %delegates delegates]]
```

To cancel the same data, you would pass a card like this:

```hoon
[%pass /emissary/fine %cull ud+5 /patrons]
```

Right now, a key difficulty in userspace is actually knowing the current `case`, which makes it hard to retire values from the cache using either `%tomb` or `%cull`.  Right now it looks like the best pattern for that is to check if your path exists:

```hoon
.^((list path) %gt /=agent=/$)
```

and then check the latest revision before you decide to `%cull`:

```hoon
.^([%ud @ud] %gw /=agent=/path)
```


##  Retrieving Remote Scry Data

> A ship that wants to read from a remote part of the namespace will have to pass a `%keen` task to its Ames, which then cooperates with Vere to produce the desired data. In some future event when the result is available, Ames gives it back as a `%tune` gift. From the requester's perspective, this is the entire default lifecycle of a remote scry request.

```hoon
+$  task
  $%  [%keen spar]
      [%yawn spar]
      [%wham spar]
==
```

- `%keen` scries for data at the path `[ship /vane/care/case/spur]`.  (A `+$spar` is `[=ship =path]`.  The `+$spur` is the part of the `path` after the `beak`, `ship desk case spur`.)
- `%yawn` cancels an outstanding request from Arvo.
- `%wham` cancels all scry requests from any vane at a path.

When `%emissary` needs a value, it makes a request like this:

```hoon
[%pass /emissary/fine/(scot %da now.bol) %arvo %a %keen ship.que /g/x/0/emissary//patrons]
[%pass /emissary/fine/(scot %da now.bol) %arvo %a %keen ship.que /g/x/0/emissary//patron/(scot %p ship.que)]
```

Note the `//`—this means that the latest revision has been requested.

Most of the time you will simply request a value using `%keen`, but perhaps a `%yawn` will come in handy if you don't want to just throw away a result in `++on-arvo`.

```hoon
+$  gift
  $%  [%tune spar roar=(unit roar)]
  ==
+$  roar  (tale:pki:jael (pair path (unit (page))))
```

The result comes back as `%tune` gift containing a `+$roar`.  If the `roar` is `~` then there is no value at this path at the current time, but there could be later (i.e. the data don't exist yet or the path was tombstoned).  If the data in the `roar` is `~`, then there is no value at this path and never will be (the path was culled).

- `tale` is a signature.
- `path` is the `path` of the requested data.
- `page` represents the data as the `(pair mark data)`.

In `%emissary`, this is processed like this:

```hoon
++  arvo
  |=  [wire=(pole knot) =sign-arvo]
  ^+  that
  ?+    sign-arvo  ~|(%bad-arvo-sign that)
      [%ames %tune *]
    =^  cards  state
      ob-abet:(ob-arvo-tune:(ob-abed:ob queries) +>:sign-arvo)
    (emil cards)
  ==
::
++  ob-arvo-tune
  |=  [[=ship =path] roar=(unit roar:ames)]
  ^+  ob
  ::  if no value then just post a cleared value
  ?~  roar
    =?  queries  (~(has bi queries) ship %patron)
      (~(put bi queries) ship %patron [%unasked-for now.bol ~])
    =?  queries  (~(has bi queries) ship %delegate)
      (~(put bi queries) ship %delegate [%unasked-for now.bol ~])
    ob
  ::  if a value then unpack it and update the appropriate queries
  ?>  =(%emissary-demand p:(need q.dat.u.roar))
  =/  tag  -.q:(need q.dat.u.roar)
  =/  data=?([%patrons p=(set ^ship)] [%delegates p=(set ^ship)])
    ?:  =(%patrons tag)
      =/  pats  q.dat.u.roar
      ?~  pats  [%patrons *(set ^ship)]
      ;;([%patrons p=(set ^ship)] [tag +:q.u.pats])
    ?>  =(%delegates tag)
      =/  dels  q.dat.u.roar
      ?~  dels  [%delegates *(set ^ship)]
      ;;([%delegates p=(set ^ship)] [tag +:q.u.dels])
  =/  ships  ~(tap in `(set ^ship)`p.data)
  =?  queries  &(=(%patrons tag) (~(has bi queries) ship %patron))
    (~(put bi queries) ship %patron [%valid now.bol `p.data])
  =?  queries  &(=(%delegates tag) (~(has bi queries) ship %delegate))
    (~(put bi queries) ship %delegate [%valid now.bol `p.data])
  ob
```

Mostly, you can ignore the `++abed`/`++abet` pattern materials and `ob`.  Just focus on how the `roar` is checked for `~`, then the data are extricated.


##  The Future of Remote Scry

Remote scry came out recently and has primarily been used for distributing desks for OTA updates.  The interface could use a bit of [refinement](https://github.com/urbit/urbit/issues/6849), but the proof of concept is in place for what it was hoped to accomplish.

How should you use remote scry?  If your agent exposes relatively stable data, then publishing the values into the scry namespace may be a good fit for it.  It's not great for transient data (like subscriptions).

The other challenge is that because tracking the revision number can be a bit complicated, you may end up with a clutter of stale scries until you `%cull` them.

Ultimately, Fine is going to be unified into Ames so that the external interface will appear seamless to a calling userspace agent.

- [“Guides:  Remote Scry”](https://docs.urbit.org/userspace/apps/guides/remote-scry)
- [~rovnys-ricfer, “Remote Scry Protocol Proposal”](https://gist.github.com/belisarius222/d9a9c164817d3e8bbda3c45f7d2000b9)
- [Roadmap:  Basic Remote Scry Protocol](https://roadmap.urbit.org/project/remote-scry)
