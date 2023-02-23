---
title: "React Front-End"
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
readings:
  - "https://developers.urbit.org/guides/core/app-school-full-stack/6-react-setup"
  - "https://developers.urbit.org/guides/core/app-school-full-stack/7-app-logic"
  - "https://github.com/urbit/create-landscape-app"
homework:
  - "https://forms.gle/Dt6FdgCLt2Wnodfj8"
mirror: "https://github.com/sigilante/curriculum/blob/master/asl-2023.1/asl4.md"
video: "https://youtu.be/GGZ3ZAUNQGI"
---

#   🦩 `asl4`.  React Front-End.
##  App School Live Lesson 4

When you actually work with Urbit as a developer, you spend a lot of time on the command line.  But a user _doesn't_, and so you need to know how to set up a compatible interface.  By convention, we refer to the part of the system which handles calculations and data as the _back-end_ or _server_, and the part which primarily deals with display the _front-end_ or _client_.  Today, Urbit typically acts as the server unless you are writing a command-line app.

Now that you know how to move data in and out of Urbit, it's time to turn our attention to the place most of those data will originate from and return to:  the front-end interface.

We're going to move fast and light, and if you want to dig deeper into making an Urbit app with a front-end, you should check out the [Full-Stack Walkthrough](https://urbit.org/docs/userspace/full-stack/1-intro) pages.

This lesson will assume that you have a basic familiarity (at least capability to read and understand) HTML and JavaScript.  We _are not_ teaching React and JavaScript to any great extent in App School Live.  You should check these tutorials out if you would like more background:

- [HTML](https://www.w3schools.com/html/html_intro.asp)
- [Javascript](https://javascript.info)
- [React](https://reactjs.org/tutorial/tutorial.html)


##  Front-End Superstructure:  `create-landscape-app`

We will copy the `%delta` app from previous lessons as the basis for our full-stack application.  This one will be called `%echo`.

The front-end itself will be served from the ship by the standard `%docket` agent available on every Urbit ship.  While you can construct HTTP requests directly, most of the time you'll just use the `@urbit/http-api` library functions.

We will build the React front-end using Node.js and the `create-landscape-app` tool.

1. Run `create-landscape-app`:

    ```sh
    $ npx @urbit/create-landscape-app
    ```

2. Name the app `%echo`:

    ```sh
    Need to install the following packages:
      @urbit/create-landscape-app@8.0.0
    Ok to proceed? (y) y
    ✔ What should we call your application? … echo
    ✔ What URL do you use to access Urbit? … localhost:8080
    ```

3. Enter the new `echo/ui` directory and run `npm install @urbit/http-api`.
4. Change the `"name"` in `package.json` to `"echo"` and add a new entry:

    ```json
    "homepage": "/apps/echo/",
    ```

At this point, all we have done is create a blank webapp framework to which we will need to hook up our Urbit ship later.


##  Back-End Communications

Front-end development instruments a browser client session to talk to Urbit.  Since Urbit provides a built-in server vane, we communicate via `GET`/`PUT` HTTP calls.

Most people working with Urbit use React as the framework for their front end, but you can make other arrangements if you're willing to figure out how to make things join up correctly.

We will implement a version of our stack app that runs on one ship and doesn't track communications with other ships.  Although creating such functionality is straightforward, it would take longer than we have in this quick walkthrough.

### Talking to a Ship

Eyre is the HTTP server vane of Arvo.  It will receive and handle `GET` and `PUT` messages.  The web client will produce a unique channel ID and connect that channel to the agent to monitor subscriptions and acks.

This is handled automatically by the Urbit Javascript library in the example we will use.

### The Files

We can copy `%delta` from our previous back-end work and update it to have a small front-end which displays its state and allows the front-end to push and pop values. We can leave the `/sur` file and agent the same, and just add JSON encoding & decoding functions to our mark files, as you saw in the previous lesson.

We will call the two basic actions we are taking _actions_ and _updates_.  Actions take place to an agent (e.g. from another agent or from the user at the Dojo prompt), while updates are communications between the back-end and front-end.

**`/sur/echo.hoon`**

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

The marks are interesting for having `++json` arms.  They should accept a JSON of the forms:

```json
{"push": {"target": "~sampel-palnet", "value": 45}}
{"pop": "~sampel-palnet"}
```

**`/mar/echo/action.hoon`**

```hoon
/-  *echo
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

**`/mar/echo/update.hoon`**

```hoon
/-  *echo
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

**`/app/echo.hoon`**

This is a copy of the latest `%delta` except for name changes.  More sophisticated configurations, including the registration of arbitrary endpoints, are possible.

```hoon
/-  *echo
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
  ?>  ?=(%echo-action mark)
  =/  act  !<(action vase)
  ?-    -.act
      %push
    ?:  =(our.bowl target.act)
      :_  this(values [value.act values])
      [%give %fact ~[/values] %echo-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %echo] %poke mark vase]~
  ::
      %pop
    ?:  =(our.bowl target.act)
      :_  this(values ?~(values ~ t.values))
      [%give %fact ~[/values] %echo-update !>(`update`act)]~
    ?>  =(our.bowl src.bowl)
    :_  this
    [%pass /pokes %agent [target.act %echo] %poke mark vase]~
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
  [%give %fact ~ %echo-update !>(`update`[%init values])]~
++  on-arvo   on-arvo:default
++  on-leave  on-leave:default
++  on-agent  on-agent:default
++  on-fail   on-fail:default
--
```

**`desk.docket-0`**

We also need to an a `desk.docket-0` file to the root of the desk to configure the app tile and source of front-end files:

```hoon
:~  title+'%echo'                                                                                    
    info+'A stack of numbers'
    color+0x2e.4347
    glob-http+['https://bootstrap.urbit.org/glob-0v5.hurm4.ejod5.ngg9h.iub9i.n1j7o.glob' 0v5.hurm4.ejo  d5.ngg9h.iub9i.n1j7o]
    base+'echo'
    version+[0 0 1]
    website+'https://github.com'
    license+'MIT'
==
```

**`desk.bill`**

```sh
$ echo "~[%echo]" > echo/desk/desk.bill
```

Finally, we will also need the docket marks, which are not in `%base` but we can get from `%garden`:

```sh
$ cp ~/zod/garden/mar/docket-0.hoon ~/zod/echo/mar
$ cp ~/zod/garden/lib/docket.hoon ~/zod/echo/lib
$ cp ~/zod/garden/sur/docket.hoon ~/zod/echo/sur
```

Commit these changes to a new `%echo` desk:

```hoon
> |merge %echo our %delta
```

and copy over the `%echo` desk, then

```
> |commit %echo

> |install our %echo
```

The CLI tools still work like they did in `%charlie` and the old `%echo`, but now we're primarily interested in the front end.

```hoon
> :echo &echo-action [%push ~zod 5]

> :echo &echo-action [%push ~zod 10]

> :echo &echo-action [%push ~zod 15]

> :echo &echo-action [%push ~zod 20]

> :echo +dbug
>   [%0 values=~[20 15 10 5]]
```


##  Hooking It Up

We have a front-end and a back-end, and they know how to communicate in JSON, but we don't yet have any communication between them.  Let's hook a web page up using the FE superstructure so we can have them coordinate with each other.

To complete this, we need to modify or create some files:

1. Run `npm install` in `echo/ui`.

2. Next, delete the contents of `src/app.jsx` and add our own code:

    ```javascript
    import React, { useEffect, useState, useReducer } from 'react'
    import Urbit from '@urbit/http-api'
    import { AppTile } from './components/AppTile'
    
    const api = new Urbit( '', '', window.desk )
    api.ship = window.ship
    
    function reducer( state, action ) {
      let newState = [ ...state ]
      switch ( action.type ) {
        case 'init':
          return action.init
        case 'push':
          newState.push(action.val)
          return newState
        case 'pop':
          newState.shift()
          return newState
        default:
          return state
      }
    }
    
    export function App() {
      const [ state, dispatch ] = useReducer( reducer, [] )
      const [ inputValue, setInputValue ] = useState( "" )
    
      useEffect(() => {
        async function init() {
          api.subscribe( { app:"echo", path: '/values', event: handleUpdate } )
        }
        init()
      }, [] )
    
      const handleUpdate = ( upd ) => {
        if ( 'init' in upd ) {
          dispatch({type:'init', init:upd.init})
        }
        else if ( 'push' in upd ) {
          dispatch({type:'push', val:upd.push.value})
        }
        else if ( 'pop' in upd ) {
          dispatch( { type:'pop' } )
        }
      }
    
      const push = () => {
        const val = parseInt( inputValue )
        if ( isNaN( val ) ) return
        api.poke( {
          app: 'echo',
          mark: 'echo-action',
          json: { push: { target:`~${window.ship}`, value:val } }
        } )
        setInputValue( "" )
      }
    
      const pop = () => {
        api.poke( {
          app: 'echo',
          mark: 'echo-action',
          json: { pop: `~${window.ship}` }
        } )
      }
    
      return (
        <main className="flex flex-col items-center justify-center min-h-screen">
          <input style={{width:200}} className='border' type='text' value={inputValue} onChange={(e) => setInputValue(e.target.value)}/>
          <div>
            <button onClick={() => push()} style={{width:100}} className='border p-2 text-black-400'>Push</button>
            <button onClick={() => pop()} style={{width:100}} className='border p-2 text-black-400'>Pop</button>
            <p>Our stack</p>
            {state.map((eachValue, index) => {
              return (<li key={index}>{eachValue}</li>)
            })}
          </div>
        </main>
      )
    }
    
    export default App;
    ```

    This JavaScript code can be most easily read by looking at the `return()` function at the end, then investigating `push()`, `pop()`, and the `state.map()` list builder from the known state.

3. Glob it.  The web page source is itself built using Node.js first, then the Urbit ship can serve it for a web browser to use after it has been uploaded to the ship as a “glob”.
    1. We need to build the React app first:
        ```
        npm run build
        ```
    2. Edit the `dist/index.html` file such that the `script` tags include `type="module"`, to wit:

        ```js
        <script type="module" src="/apps/echo/desk.js"></script>
        <script type="module" src="/session.js"></script>           
        ```

    3. After `|install`ing the desk we can upload the file glob to the `%docket` server app by navigating to `localhost:8080/docket/upload`, selecting our desk, selecting the build directory `echo/ui/dist`, and hitting the `glob!` button.

Take a quick look at the front-end functionality now.  The data passed to and from the Urbit ship are converted by the mark file into JSON.  This makes it straightforward for the front-end and back-end to coordinate, each in their own native idiom.


##  Conclusion

You may notice that we don't spend a lot of time on the front end, proportional to its role in the user's experience.  Urbit serves as a backend database, authentication, and computation server which can talk to a variety of front ends.  Most of these have been either CLI REPLs (like Dojo/`%webterm`) or browser-based webapps, but there's a lot of potential for other configurations that hasn't been explored here yet.

Regardless, most apps today will use an HTML and JavaScript library for rendering the user interface.  Besides React, some Urbit app developers have had good luck working with [Svelte](https://svelte.dev/).


##  Resources

- [`create-landscape-app` tool](https://github.com/urbit/create-landscape-app)
- [App School Full Stack, “6. React Setup”](https://developers.urbit.org/guides/core/app-school-full-stack/6-react-setup)
- [App School Full Stack, “7. App Logic”](https://developers.urbit.org/guides/core/app-school-full-stack/7-app-logic)
