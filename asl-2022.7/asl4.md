---
title: "Passing Data"
teaching: 60
exercises: 0
nodes: []
objectives:
  - "Interact with Urbit using the Javascript library."
  - "Produce an advanced agent with a front-end interface."
  - "Explain the role of a `%glob` and produce one."
runes: []
keypoints:
  - "⛓️Gall agents can talk to a browser client session as a back-end server."
  - "The `create-landscape-app` tool is the easiest way to start an Urbit agent with a front end."
---

#   🦩 `lesson4`.  React Front-End.
##  App School Live Lesson 4

When you actually work with Urbit as a developer, you spend a lot of time on the command line.  But a user _doesn't_, and so you need to know how to set up a compatible interface.  By convention, we refer to the part of the system which handles calculations and data as the _back-end_ or _server_, and the part which primarily deals with display the _front-end_ or _client_.

Now that you know how to move data in and out of Urbit, it's time to turn our attention to the place most of those data will originate from and return to:  the front-end interface.

(We _are not_ teaching React and JavaScript to any great extent in App School Live.  You should [check this tutorial out](https://reactjs.org/tutorial/tutorial.html) if you are interested in knowing more.)


##  A Quick Look

Let's go back to the `%delta` app from previous lessons and set up a front-end for it first.

**`/app/delta.hoon`**

```hoon
/-  *delta
/+  default-agent, dbug
|%
+$  versioned-state
  $%  state-0
  ==
+$  state-0
  $:  [%0 values=(list @)]
  ==
+$  card  card:agent:gall
--
%-  agent:dbug
=|  state-0
=*  state  -
^-  agent:gall
|_  =bowl:gall
+*  this     .
    default  ~(. (default-agent this %|) bowl)
++  on-init   on-init:default
++  on-save   !>(state)
++  on-load
  |=  old=vase
  ^-  (quip card _this)
  `this(state !<(state-0 old))
++  on-poke
  |=  [=mark =vase]
  ^-  (quip card _this)
  ?>  ?=(%delta-action mark)
  =/  act  !<(action vase)
  ?-    -.act
      %push
    ?:  =(our.bowl target.act)
      :_  this(values [value.act values])
      [%give %fact ~[/values] %delta-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %delta] %poke mark vase]~
  ::
      %pop
    ?:  =(our.bowl target.act)
      :_  this(values ?~(values ~ t.values))
      [%give %fact ~[/values] %delta-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %delta] %poke mark vase]~
  ==
::
++  on-peek
  |=  =path
  ^-  (unit (unit cage))
  ?+  path  (on-peek:default path)
    [%x %values ~]  ``noun+!>(values)
  ==
++  on-watch
  |=  =path
  ^-  (quip card _this)
  ?>  ?=([%values ~] path)
  :_  this
  [%give %fact ~ %delta-update !>(`update`[%init values])]~
++  on-arvo   on-arvo:default
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

**`/sur/delta.hoon`**

```hoon
|%
+$  action
  $%  [%push target=@p value=@]
      [%pop target=@p]
  ==
+$  update
  $%  [%init values=(list @)]
      action
  ==
--
```

Front-end development instruments a browser client session to talk to Urbit.  Since Urbit provides a built-in server vane, we communicate via `GET`/`PUT` HTTP calls.

Most people working with Urbit use React as the framework for their front end, but you can make other arrangements if you're willing to figure out how to make things join up correctly.

We're going to move fast and light, and if you want to dig deeper into making an Urbit app with a front-end, you should check out the [Full-Stack Walkthrough](https://urbit.org/docs/userspace/full-stack/1-intro) pages.

We will implement a version of our stack app that runs on one ship and doesn't track communications with other ships.  Although creating such functionality is straightforward, it would take longer than we have in this quick walkthrough.

### Talking to a Ship

Eyre is the HTTP server vane of Arvo.  It will receive and handle `GET` and `PUT` messages.  The web client will produce a unique channel ID and connect that channel to the agent to monitor subscriptions and acks.

This is handled automatically by the Urbit Javascript library in the example we will use.

### Updates to `%delta`

Let's take `%delta` from our back-end work and update it to have a small front-end which displays its state and allows the front-end to push and pop values. We can leave the `/sur` file and agent the same, and just add JSON encoding & decoding functions to our mark files, as you saw in the previous lesson.

**`/mar/delta/action.hoon`**

```hoon
/-  *delta
|_  act=action
++  grow
  |%
  ++  noun  act
  --
++  grab
  |%
  ++  noun  action
  ++  json
    =,  dejs:format
    |=  jon=json
    ^-  action
    %.  jon
    %-  of
    :~  [%push (ot ~[target+(se %p) value+ni])]
        [%pop (se %p)]
    ==
  --
++  grad  %noun
--
```

**`/mar/delta/update.hoon`**

```hoon
/-  *delta
|_  upd=update
++  grow
  |%
  ++  noun  upd
  ++  json
    =,  enjs:format
    ^-  ^json
    ?-    -.upd
      %pop   (frond 'pop' s+(scot %p target.upd))
      %init  (frond 'init' a+(turn values.upd numb))
      %push  %+  frond  'push'
             %-  pairs
             :~  ['target' s+(scot %p target.upd)]
                 ['value' (numb value.upd)]
    ==       ==
  --
++  grab
  |%
  ++  noun  update
  --
++  grad  %noun
--
```

We also need to an a `desk.docket-0` file to the root of the desk to configure the app tile and source of front-end files:

**desk.docket-0**

```hoon
:~
  title+'Delta'
  info+'A stack.'
  color+0xd9.b06d
  version+[0 0 1]
  website+'https://urbit.org'
  license+'MIT'
  base+'delta'
  glob-ames+[~zod 0v0]
==
```

Commit these changes to the `%delta` desk:

```hoon
> |merge %delta our %base

> |mount %delta
```

```sh
$ cd zod/delta
$ echo "~[%delta %delta-follower]" > desk.bill
```

and copy in the other files as appropriate.

```hoon
> |commit %delta
```

The CLI tools still work like they did in `%charlie` and the old `%delta`, but now we're primarily interested in the front end.

The front-end itself will be served from the ship by the standard `%docket` agent available on every Urbit ship.  While you can construct HTTP requests directly, most of the time you'll just use the `@urbit/http-api` library functions.

We will build the React front-end using Node.js.

1. In the working directory for `%delta`, run `npx create-react-app delta-ui`.
2. Enter the new `delta-ui` directory and run `npm i @urbit/http-api`.
3. Change the `"name"` in `package.json` to `"delta"` and add a new entry: `"homepage": "/apps/delta/",`.
4. Add `<script src="/session.js"></script>` to the `<head>` section of `public/index.html` so our React app can discover our ship name.
5. Next, we can delete the contents of `src/App.js` and add our own code:

    ```javascript
    import React, {Component} from 'react';
    import Urbit from '@urbit/http-api';
    
    class App extends Component {
      constructor(props) {
        super(props);
        window.urbit = new Urbit("");
        window.urbit.ship = window.ship;
        this.state = {vals: [], val: ""}
        this.subscribe();
      };
    
      subscribe = () => {
        window.urbit.subscribe({
          app: "delta",
          path: "/values",
          event: this.handleUpdate
        })
      };
    
      pop = () => {
        window.urbit.poke({
          app: "delta",
          mark: "delta-action",
          json: {"pop": "~" + window.ship}
        })
      };
    
      push = () => {
        const val = parseInt(this.state.val);
        if (isNaN(val)) return;
        const target = "~" + window.ship;
        window.urbit.poke({
          app: "delta",
          mark: "delta-action",
          json: {"push": {"target": target, "value": val}}
        })
        this.setState({val: ""})
      };
    
      handleUpdate = (upd) => {
        const {vals} = this.state;
        if ('init' in upd) {
          this.setState({vals: upd.init})
        } else if ('push' in upd) {
          vals.unshift(upd.push.value);
          this.setState({vals: vals})
        } else if ('pop' in upd) {
          vals.shift();
          this.setState({vals: vals})
        }
      };
    
      render() {
        return (
          <>
            <div>
                <input
                  type="text"
                  value={this.state.val}
                  onChange={(e) => this.setState({val: e.target.value})}
                />
                <button onClick={() => this.push()}>Push</button>
            </div>
            <button onClick={() => this.pop()}>Pop</button>
            <ul>
              {this.state.vals.map((val, ind) => <li key={ind}>{val}</li>)}
            </ul>
          </>
        )
      };
    };
    
    export default App;
    ```

The webpage itself is built using Node.js.  We need to build the React app using `npm run build`, then after installing the desk we can upload the file glob to the `%docket` server app by navigating to `localhost:8080/docket/upload`, selecting our desk, selecting the build directory in `delta-ui`, and hitting upload.

- Take a quick look at the front-end functionality now.

    You can see that the data passed to and from the Urbit ship are converted by the mark file into JSON.  This makes it straightforward for the front-end and back-end to coordinate, each in their own native idiom.


##  `create-landscape-app`

(Matilde stuff here)

##  More Thoughts

(Matilde musings here)

##  Conclusion

You may notice that we don't spend a lot of time on the front end, proportional to its role in the user's experience.  Urbit serves as a backend database, authentication, and computation server which can talk to a variety of front ends.  Most of these have been either CLI REPLs (like Dojo/`%webterm`) or browser-based webapps, but there's a lot of potential for other configurations that hasn't been explored here yet.

Regardless, most apps will use an HTML and JavaScript library for rendering the user interface.  Besides React, some Urbit app developers have had good luck working with [Svelte](https://svelte.dev/).

##  Resources

- [App School Full Stack, “6. React Setup”](https://developers.urbit.org/guides/core/app-school-full-stack/6-react-setup)
- [App School Full STack, “7. App Logic”](https://developers.urbit.org/guides/core/app-school-full-stack/7-app-logic)
- [`create-landscape-app` tool](https://github.com/urbit/create-landscape-app)
- [Intro to React](https://reactjs.org/tutorial/tutorial.html)
